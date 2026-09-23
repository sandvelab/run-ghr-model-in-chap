#!/usr/bin/env python3
"""Measure the grounded half of the human-cost model.

Two things in that model are measured rather than authored, and they are measured here so
that nothing downstream has to take them on trust:

**Document lengths.** Every `read_doc` step in `steps.tsv` names a document the discovering
agent actually opened. Its length in words is a property of the document, not of the reader,
and it is counted from `Archive/` (for the models and the data schema), from the installed
`chap-core` (for the library source the agents read), and from the CLI itself (for `--help`
output, which is captured to `results/help_text/` so the count can be checked).

**Machine wait times.** How long the machine takes is the same for every reader. Route A's
evaluation span is taken from the discovery log's own timestamps, which separate
`evaluation_started` from `evaluation_complete`. Route B's log collapses the two onto one
timestamp -- its agent wrote both rows when the command returned -- so route B's span is taken
from file modification times in the repeatability node's clean re-run instead. Which method
produced which number is written into the output, because the two are not equally strong.

One span is deliberately **not** measured: route A's image build from cold. Every build this
repository logged ran against a warm layer cache, so nothing here grounds it. It is carried
through as an explicitly separated unknown rather than filled in with a guess.

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORD = re.compile(r"\S+")


def count_words(text: str) -> int:
    return len(WORD.findall(text))


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def find_chapcore(repo_root: Path) -> Path | None:
    """Locate the installed chap-core package that the agents read."""
    candidates = sorted(
        Path(os.path.expanduser("~/.local/share/uv/tools/chap-core/lib")).glob(
            "python*/site-packages/chap_core"
        )
    )
    return candidates[0] if candidates else None


def capture_help(command: str, out_dir: Path) -> str | None:
    """Run a `--help` invocation and keep its output as an intermediate (AGENTS.md rule 5)."""
    parts = command.split()
    try:
        proc = subprocess.run(parts, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    text = proc.stdout or proc.stderr
    if not text.strip():
        return None
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "_", command.lower()).strip("_")
    (out_dir / f"{slug}.txt").write_text(text, encoding="utf-8")
    return text


def measure_documents(repo_root: Path, manifest: list[dict[str, str]], out_dir: Path):
    chapcore = find_chapcore(repo_root)
    rows: list[dict[str, object]] = []
    missing: list[str] = []
    for entry in manifest:
        key, kind, ref = entry["doc_key"], entry["kind"], entry["path"]
        text = None
        source = ref
        if kind == "file":
            p = repo_root / ref
            if p.is_file():
                text = p.read_text(encoding="utf-8", errors="replace")
                source = str(p.relative_to(repo_root))
        elif kind == "command":
            if chapcore is not None:
                p = chapcore.parent / ref
                if p.is_file():
                    text = p.read_text(encoding="utf-8", errors="replace")
                    source = ref + " (installed chap-core)"
        elif kind == "help":
            text = capture_help(ref, out_dir / "help_text")
            source = ref + " (captured to results/help_text/)"
        if text is None:
            missing.append(f"{key}: {ref}")
            continue
        rows.append({"doc_key": key, "words": count_words(text), "source": source})

    merged: dict[str, dict[str, object]] = {}
    for r in rows:
        k = str(r["doc_key"])
        if k in merged:
            merged[k]["words"] = int(merged[k]["words"]) + int(r["words"])
            merged[k]["source"] = f"{merged[k]['source']} + {r['source']}"
        else:
            merged[k] = dict(r)
    return [merged[k] for k in sorted(merged)], missing


def parse_ts(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def measure_waits(repo_root: Path) -> list[dict[str, object]]:
    """Route A from the discovery log's timestamps; route B from the clean re-run's mtimes."""
    out: list[dict[str, object]] = []

    log_a = repo_root / "analysis/02_routeA_chapkit/results/discovery_log.tsv"
    rows = read_tsv(log_a)
    started = next(r for r in rows if r["ref"] == "evaluation_started")
    done = next(r for r in rows if r["ref"] == "evaluation_complete")
    span_a = (parse_ts(done["ts_utc"]) - parse_ts(started["ts_utc"])).total_seconds()
    if not 60 <= span_a <= 3600:
        raise SystemExit(f"route A evaluation span implausible: {span_a} s")
    out.append(
        {
            "wait_key": "route-a",
            "seconds": round(span_a),
            "method": "discovery-log timestamps, evaluation_started to evaluation_complete",
            "source": "analysis/02_routeA_chapkit/results/discovery_log.tsv",
        }
    )

    rerun_b = repo_root / "analysis/05_repeatability/results/rerun_routeB"
    start_f = rerun_b / "chap_run_dir/model_configuration_for_run.yaml"
    end_f = rerun_b / "eval/eval.nc"
    if start_f.is_file() and end_f.is_file():
        span_b = end_f.stat().st_mtime - start_f.stat().st_mtime
        if not 1 <= span_b <= 3600:
            raise SystemExit(f"route B evaluation span implausible: {span_b} s")
        out.append(
            {
                "wait_key": "route-b",
                "seconds": round(span_b),
                "method": (
                    "file mtimes in the clean re-run, CHAP's written run configuration to the "
                    "written evaluation; the discovery log collapses both milestones onto one "
                    "timestamp, so it cannot supply this"
                ),
                "source": "analysis/05_repeatability/results/rerun_routeB/",
            }
        )
    else:
        raise SystemExit(
            "route B wait not measurable: the repeatability re-run outputs are absent. "
            "mtimes are a filesystem property and do not survive a fresh clone -- re-run "
            "analysis/05_repeatability before this node."
        )
    return out


def write_tsv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out-docs", required=True)
    ap.add_argument("--out-waits", required=True)
    a = ap.parse_args()

    repo_root = Path(a.repo_root).resolve()
    out_dir = Path(a.out_docs).resolve().parent

    docs, missing = measure_documents(repo_root, read_tsv(Path(a.manifest)), out_dir)
    if missing:
        raise SystemExit(
            "documents named by the model could not be measured:\n  "
            + "\n  ".join(missing)
            + "\nThe model must not run on a partial reading table."
        )
    write_tsv(Path(a.out_docs), docs, ["doc_key", "words", "source"])
    write_tsv(Path(a.out_waits), measure_waits(repo_root), ["wait_key", "seconds", "method", "source"])
    print(f"measured {len(docs)} documents and 2 machine waits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
