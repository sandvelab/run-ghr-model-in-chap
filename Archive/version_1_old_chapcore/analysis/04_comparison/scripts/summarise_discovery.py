#!/usr/bin/env python3
"""Turn the routes' raw discovery logs into the effort statistics the comparison rests on.

Usage:
    summarise_discovery.py --route A=<path/to/discovery_log.tsv> \
                           --route B=<path/to/discovery_log.tsv> \
                           --out results/effort_by_route.tsv

Every count in the per-route reports and in the comparative report is read back from the
file this writes. Nothing counts rows by hand, and nothing carries a number out of a
terminal (plan §3).

The output is long, not wide -- one row per (route, statistic) -- so that adding a statistic
or a route later does not change the shape of a file other scripts already read.

A log that does not meet `AI-internal/skill-references/discovery-log-format.md` stops this
script. It is not repaired here: an invalid log is a finding about how the route was run, and
belongs in the record as one.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import discovery_log as dl  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--route", action="append", required=True, metavar="NAME=PATH",
                    help="route label and the path to its discovery_log.tsv; repeatable")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--normalise", action="store_true",
                    help="count information sources by the two rules in discovery_log.py "
                         "rather than taking each log's own coding at face value")
    ap.add_argument("--not-a-source", action="append", default=[], metavar="SUBSTRING",
                    help="with --normalise: a resource whose ref contains this is a given "
                         "input or an artefact of the run, not documentation that had to be "
                         "found; repeatable, and declared in run.sh so it is visible")
    args = ap.parse_args(argv)

    rows_out = []
    for spec in args.route:
        if "=" not in spec:
            ap.error(f"--route expects NAME=PATH, got {spec!r}")
        name, _, path = spec.partition("=")
        log = Path(path)
        if not log.exists():
            ap.error(f"route {name}: no log at {log}")
        rows = dl.load(log)
        for statistic, value in dl.summarise(rows, normalise=args.normalise,
                                            not_a_source=tuple(args.not_a_source)):
            rows_out.append((name, statistic, value))
        print(f"route {name}: {len(rows)} log rows from {log}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerow(["route", "statistic", "value"])
        writer.writerows(rows_out)
    print(f"wrote {args.out} ({len(rows_out)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
