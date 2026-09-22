#!/usr/bin/env python3
"""Gather every run of each route that this repository holds, and report the spread.

A route is re-run whenever `analysis/run.sh` is run, and each re-run overwrites the metrics
file of the run before it. The overwritten versions are not lost — they are in the commits
that recorded them — so the evidence for "does it run again" is assembled from the working
tree **and** from git history, and every value still comes from a file that was executed.

Three outputs:

  run_ledger.tsv    one row per run found: route, where it came from, commit, when
  completion.tsv    did each route reach a written evaluation, and how many times
  score_spread.tsv  per metric and route, the min, the max and the spread as a percentage

The spread is reported, not corrected for. Plan §2: a route whose numbers move between
identical invocations is still a working route, and the question a route has to answer is
whether it runs again from clean.

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import io
import subprocess
from pathlib import Path

METRICS = ["mae", "rmse", "crps", "mape", "coverage_10_90", "coverage_25_75"]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          check=True).stdout


def read_metrics_text(text: str) -> dict[str, str]:
    rows = list(csv.DictReader(io.StringIO(text)))
    return rows[0] if rows else {}


def runs_for(path: Path) -> list[tuple[str, str, str, str, dict[str, str]]]:
    """Every version of one metrics file: the working tree, then each commit that changed it.

    A run is counted whether or not its numbers differ from the run before. Collapsing
    identical results would report a route that reproduces exactly as having run once, which
    is the opposite of what repeatability means: identical numbers are the strongest possible
    evidence that a route re-ran, not evidence that it did not.
    """
    found: list[tuple[str, str, str, str, dict[str, str]]] = []
    texts: list[str] = []

    if path.exists():
        text = path.read_text()
        texts.append(text)
        found.append(("working tree", "-", "-", "", read_metrics_text(text)))

    log = git("log", "--format=%h\t%ad", "--date=format:%Y-%m-%dT%H:%M:%SZ", "--", str(path))
    for line in log.splitlines():
        if not line.strip():
            continue
        commit, when = line.split("\t")
        try:
            text = git("show", f"{commit}:{path}")
        except subprocess.CalledProcessError:
            continue
        found.append(("git history", commit, when, "", read_metrics_text(text)))
        texts.append(text)

    # `git log -- <path>` lists only the commits that changed the file, so a version equal to
    # the working tree's is the same run recorded twice rather than a second run.
    out = []
    seen: set[str] = set()
    for (source, commit, when, _, metrics), text in zip(found, texts):
        if source == "git history" and text in seen:
            continue
        seen.add(text)
        out.append((source, commit, when, "identical to another run" if
                    texts.count(text) > 1 and source == "working tree" else "", metrics))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--metrics", action="append", required=True,
                    metavar="ROUTE:LABEL:PATH",
                    help="a route, what that file is, and its path; repeatable")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    a.out.mkdir(parents=True, exist_ok=True)
    ledger, by_route = [], {}
    for spec in a.metrics:
        route, label, path = spec.split(":", 2)
        for source, commit, when, note, metrics in runs_for(Path(path)):
            if not metrics:
                continue
            ledger.append([route, label, source, commit, when, path, note])
            by_route.setdefault(route, []).append(metrics)

    with (a.out / "run_ledger.tsv").open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["route", "which_run", "recovered_from", "commit", "committed_at",
                    "path", "note"])
        w.writerows(ledger)

    with (a.out / "completion.tsv").open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["route", "n_runs_found", "n_distinct_results",
                    "all_wrote_an_evaluation", "bit_reproducible"])
        for route, runs in sorted(by_route.items()):
            complete = all(r.get("mae") not in (None, "") for r in runs)
            distinct = len({tuple(sorted(r.items())) for r in runs})
            w.writerow([route, len(runs), distinct, "yes" if complete else "no",
                        "yes" if distinct == 1 and len(runs) > 1 else
                        "no" if len(runs) > 1 else "not established (one run)"])

    with (a.out / "score_spread.tsv").open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["route", "metric", "n_runs", "min", "max", "spread_pct_of_mean"])
        for route, runs in sorted(by_route.items()):
            for m in METRICS:
                vals = [float(r[m]) for r in runs if r.get(m) not in (None, "")]
                if not vals:
                    continue
                lo, hi = min(vals), max(vals)
                mean = sum(vals) / len(vals)
                spread = (hi - lo) / mean * 100 if mean else 0.0
                w.writerow([route, m, len(vals), f"{lo:.4f}", f"{hi:.4f}", f"{spread:.2f}"])

    for route, runs in sorted(by_route.items()):
        print(f"{route}: {len(runs)} distinct run(s)")
    print(f"wrote run_ledger.tsv, completion.tsv, score_spread.tsv to {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
