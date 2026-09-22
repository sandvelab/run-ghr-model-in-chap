#!/usr/bin/env python3
"""Assemble the route-by-route comparison table from files the tree produced.

Three blocks, and the third is fenced off deliberately:

1. **Effort** — read from the main path of the `01_effort` fork. Only the main path is read,
   because `analysis/run.sh` follows the main path at every fork, so a table naming a
   non-main alternative's output would name a file a full reproduction never regenerates.
2. **Prerequisites beyond CHAP** — derived from each route's own log: whether it had to invoke
   a container runtime, whether it had to build an image, whether it hit a registry.
3. **What each route's evaluation reported** — read from the metrics file CHAP wrote for each
   route, and **reported per route, never compared across routes**. The two routes may land on
   different models, different splits and different metric sets; the project's question is the
   route, not the prediction (plan §2).

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import discovery_log as dl  # noqa: E402

# The effort statistics worth putting in front of a reader, in the order they answer
# "how hard was it": what you had to read, what you had to run, what went wrong, how long.
HEADLINE = [
    ("reached_evaluation", "Reached a CHAP evaluation"),
    ("n_resources", "Information sources consulted"),
    ("n_resources_used", "...that contributed"),
    ("n_commands", "Commands run"),
    ("n_commands_failed", "...that failed"),
    ("n_blockers_hit", "Blockers hit"),
    ("n_blockers_unresolved", "...left unresolved"),
    ("n_dead_ends", "Dead ends"),
    ("n_decisions", "Judgment calls logged"),
    ("elapsed_minutes_to_evaluation", "Minutes to a written evaluation"),
    ("n_distinct_timestamps", "Distinct log timestamps (integrity)"),
    ("max_rows_sharing_one_timestamp", "Most rows on one timestamp (integrity)"),
]

# Metrics reported per route. A metric absent from a route's file is left blank rather than
# imputed: the routes are not required to land on the same metric set.
METRICS = [
    ("mae", "MAE"), ("rmse", "RMSE"), ("crps", "CRPS"), ("mape", "MAPE"),
    ("coverage_10_90", "Coverage 10-90"), ("coverage_25_75", "Coverage 25-75"),
]


def prerequisites(log_path: Path) -> dict[str, str]:
    """What a route needed beyond CHAP, read off its own log rather than asserted."""
    rows = dl.read_log(log_path)
    cmds = [r["ref"] for r in rows if r["kind"] == "command"]
    blob = " ".join(cmds).lower()
    notes = " ".join(f"{r['ref']} {r['note']}" for r in rows).lower()
    # A route *needs* a container runtime when it runs the model in one. Checking that a
    # daemon is up (`docker info`, `docker images`) is due diligence, not a dependency, and
    # counting it as one would report a route as needing Docker because it looked.
    USES_CONTAINER = ("docker run", "docker build", "docker compose", "docker start",
                      "docker-compose")
    return {
        "Needs a container runtime": (
            "yes" if any(c in blob for c in USES_CONTAINER) else "no"
        ),
        "Needs a container image build": "yes" if "docker build" in blob else "no",
        "Hits a container registry": "yes" if "docker pull" in blob else "no",
        "Ran the model outside CHAP first": (
            "yes" if any(r["kind"] == "milestone" and r["ref"] == "model_runs_standalone"
                         for r in rows) else "no"
        ),
        "Needed the platform's installed source": (
            "yes" if "site-packages" in notes or "chap_core/" in notes
            or "installed chap_core" in notes else "no"
        ),
    }


def read_metrics(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return rows[0] if rows else {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--effort", type=Path, required=True,
                    help="the main path's effort_by_route.tsv")
    ap.add_argument("--route", action="append", required=True,
                    metavar="LABEL=NAME:LOG:METRICS",
                    help="a route's column label, display name, log and metrics file")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    routes = []
    for spec in a.route:
        label, rest = spec.split("=", 1)
        name, log, metrics = rest.split(":", 2)
        routes.append((label, name, Path(log), Path(metrics)))

    with a.effort.open(newline="", encoding="utf-8") as fh:
        effort = {r[0]: dict(zip(next(iter([None])) or [], [])) for r in []}  # placeholder
    with a.effort.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader)
        effort = {row[0]: dict(zip(header[1:], row[1:])) for row in reader}

    missing = [lab for lab, *_ in routes if lab not in next(iter(effort.values()), {})]
    if missing:
        print(f"effort file has no column for: {missing}", file=sys.stderr)
        return 1

    out_rows = []
    for stat, label in HEADLINE:
        out_rows.append(["effort", label, *(effort[stat][lab] for lab, *_ in routes)])

    prereq = {lab: prerequisites(log) for lab, _, log, _ in routes}
    for key in next(iter(prereq.values())):
        out_rows.append(["prerequisite", key, *(prereq[lab][key] for lab, *_ in routes)])

    mets = {lab: read_metrics(m) for lab, _, _, m in routes}
    for key, label in METRICS:
        vals = []
        for lab, *_ in routes:
            v = mets[lab].get(key, "")
            vals.append(f"{float(v):.2f}" if v not in ("", None) else "")
        out_rows.append(["result (per route, NOT compared)", label, *vals])

    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["block", "measure", *(name for _, name, _, _ in routes)])
        w.writerows(out_rows)
    print(f"wrote {a.out} ({len(out_rows)} rows x {len(routes)} routes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
