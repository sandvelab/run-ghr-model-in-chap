#!/usr/bin/env python3
"""Write each sensitivity's inputs as the main inputs with exactly one named change.

The main figure keeps every batch-10 rate (the runner refuses to run otherwise). A sensitivity
is never substituted for it; it is reported beside it. Each one is written out in full under
results/sensitivity/<name>/inputs/ so what was costed can be read rather than reconstructed.

- `docker_lighter` -- chaps asks the persona to have Docker installed and running, not to
  build images, run containers or map ports by hand, which is what batch 10's `docker-basics`
  row prices (45/90/240 learning minutes). Here it is priced at 15/30/60, the authored guess
  of this batch (plan §4b), with the same description narrowed to match. Every other row is
  unchanged.
- `run_doc_not_ai_page` -- the agent read chaps' page for AI agents (`docs/ai.md`, step 6). A
  human following the README would more plausibly read `docs/run.md`, the page on `chaps run`.
  Step 6 reads that document instead; nothing else changes.

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

LIGHTER = {"learn_low": "15", "learn_exp": "30", "learn_high": "60",
           "description": "Install Docker Desktop and keep it running, without building images "
                          "or running containers by hand (batch 14 sensitivity)"}


def rw(path: Path, edit) -> int:
    with path.open(encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        fields, rows = rd.fieldnames, list(rd)
    n = sum(1 for r in rows if edit(r))
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return n


def docker_lighter(r: dict) -> bool:
    if r["prereq"] != "docker-basics":
        return False
    r.update(LIGHTER)
    return True


def run_doc(r: dict) -> bool:
    if not (r["route"] == "route-a-chaps" and r["seq"] == "6" and r["doc_key"] == "chaps_ai"):
        return False
    r["doc_key"] = "chaps_run_doc"
    r["label"] = "read chaps' docs/run.md, the page on chaps run"
    r["note"] = "sensitivity: the page a human following the README would read, in place of ai.md"
    return True


SENS = {"docker_lighter": ("prerequisites.tsv", docker_lighter),
        "run_doc_not_ai_page": ("steps.tsv", run_doc)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--results", required=True, help="main results dir (doc sizes, waits)")
    ap.add_argument("--name", required=True, choices=sorted(SENS))
    a = ap.parse_args()
    main_in, main_res = Path(a.inputs), Path(a.results)
    out = main_res / "sensitivity" / a.name
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(main_in, out / "inputs")
    for f in ("doc_sizes.tsv", "machine_waits.tsv"):
        shutil.copy2(main_res / f, out / f)
    fname, edit = SENS[a.name]
    if rw(out / "inputs" / fname, edit) != 1:
        raise SystemExit(f"{a.name}: expected exactly one row changed in {fname}")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
