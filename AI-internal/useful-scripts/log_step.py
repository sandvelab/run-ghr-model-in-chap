#!/usr/bin/env python3
"""Append one contemporaneous row to a route's `discovery_log.tsv`.

    .venv/bin/python AI-internal/useful-scripts/log_step.py <log.tsv> \
        --kind command --ref "chap eval --help" --outcome ok --note "lists the flags"

One implementation for both routes, so neither can drift into its own dialect of the format.
It stamps the row with the current UTC second and the next step number, which is the point:
the timestamp is the moment the step happened, and a log assembled at the end cannot fake
that without lying outright.

It refuses a row the specification does not allow rather than writing it, because a malformed
row is not a smaller measurement — `summarise_discovery.py` rejects the whole log, and finding
that out at the end of a route is finding it out too late.

Format: `AI-internal/skill-references/discovery-log-format.md`.
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

COLUMNS = ["step", "ts_utc", "kind", "ref", "outcome", "note"]
ALLOWED = {
    "resource": {"used", "discarded"},
    "command": {"ok", "failed"},
    "decision": {"used", "discarded"},
    "blocker": {"open", "resolved"},
    "milestone": {"ok"},
}
MILESTONES = (
    "first_doc_opened", "model_obtained", "model_runs_standalone",
    "model_registered_with_chap", "evaluation_started", "evaluation_complete",
    "route_abandoned",
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("log", type=Path)
    ap.add_argument("--kind", required=True, choices=sorted(ALLOWED))
    ap.add_argument("--ref", required=True, help="the URL, path, command line or milestone")
    ap.add_argument("--outcome", required=True)
    ap.add_argument("--note", default="", help="one line; tabs and newlines are refused")
    a = ap.parse_args()

    if a.outcome not in ALLOWED[a.kind]:
        print(
            f"kind {a.kind} may not take outcome {a.outcome!r}; "
            f"allowed: {sorted(ALLOWED[a.kind])}",
            file=sys.stderr,
        )
        return 2
    if a.kind == "milestone" and a.ref not in MILESTONES:
        print(
            f"milestone {a.ref!r} is outside the closed vocabulary: {MILESTONES}",
            file=sys.stderr,
        )
        return 2
    if not a.ref.strip():
        print("ref must not be empty", file=sys.stderr)
        return 2
    for name, value in (("ref", a.ref), ("note", a.note)):
        if "\t" in value or "\n" in value:
            print(f"{name} must be one line with no tab characters", file=sys.stderr)
            return 2

    a.log.parent.mkdir(parents=True, exist_ok=True)
    fresh = not a.log.exists() or a.log.stat().st_size == 0
    step = 1
    if not fresh:
        with a.log.open(newline="", encoding="utf-8") as fh:
            step = sum(1 for _ in csv.reader(fh, delimiter="\t"))  # header counts as step 0

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with a.log.open("a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        if fresh:
            w.writerow(COLUMNS)
        w.writerow([step, ts, a.kind, a.ref, a.outcome, a.note])
    print(f"step {step}  {ts}  {a.kind}  {a.outcome}  {a.ref[:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
