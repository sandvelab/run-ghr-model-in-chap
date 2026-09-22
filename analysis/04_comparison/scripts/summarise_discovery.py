#!/usr/bin/env python3
"""Compute both routes' effort statistics from their discovery logs, into one file.

    summarise_discovery.py --log route-a=<path> --log route-b=<path> --out <file.tsv>

Every count in the reports comes from this file. Nothing is counted by hand and nothing is
carried out of terminal output (plan §3, AGENTS.md §1).

A log that does not conform to the specification is a hard failure, not a warning: the
statistics are defined over the columns, so a log in another shape is not a smaller
measurement but no measurement. The one thing this cannot check is whether the log was
written as the work happened; `n_distinct_timestamps` and `max_rows_sharing_one_timestamp`
are written into the output so a reader can judge that for themselves.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import discovery_log as dl  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--log", action="append", required=True, metavar="ROUTE=PATH",
        help="a route's label and the path to its discovery_log.tsv; repeatable",
    )
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    logs = []
    for spec in a.log:
        if "=" not in spec:
            ap.error(f"--log wants ROUTE=PATH, got {spec!r}")
        route, path = spec.split("=", 1)
        logs.append((route, Path(path)))

    summaries = {}
    failed = False
    for route, path in logs:
        if not path.exists():
            print(f"{route}: no log at {path}", file=sys.stderr)
            failed = True
            continue
        rows = dl.read_log(path)
        errors = dl.validate(rows)
        if errors:
            print(f"{route}: {path} does not conform to the specification:", file=sys.stderr)
            for e in errors:
                print(f"    {e}", file=sys.stderr)
            failed = True
            continue
        summaries[route] = dl.summarise(rows)
        print(f"{route}: {len(rows)} rows, conforms")
    if failed:
        return 1

    routes = [r for r, _ in logs]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["statistic", *routes])
        for stat in dl.STATISTICS:
            w.writerow([stat, *(summaries[r][stat] for r in routes)])
    print(f"wrote {a.out} ({len(dl.STATISTICS)} statistics x {len(routes)} routes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
