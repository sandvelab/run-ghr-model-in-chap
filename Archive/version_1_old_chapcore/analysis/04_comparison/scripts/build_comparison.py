#!/usr/bin/env python3
"""Put the two routes' effort statistics side by side, as a file the reports read from.

Reads the effort statistics produced by the **main path** of the alternatives node below
this one, and writes `results/comparison_table.tsv`. It reads only the main path on purpose:
`analysis/run.sh` follows the main path at every fork, so a comparison built from a
non-main alternative's output would name a file that a full reproduction never regenerates.
How much the conclusion depends on that choice is the stability node's question, not this
one's.

Nothing here decides which route is easier. It writes the numbers, the direction of each
difference, and the ratio where one is meaningful; the reading of them belongs in the
claim and the reports, where it can be argued with.
"""
from __future__ import annotations

import csv
from pathlib import Path

NODE = Path(__file__).resolve().parent.parent
EFFORT = NODE / "01_effort" / "b_normalised" / "results" / "effort_by_route.tsv"
OUT = NODE / "results" / "comparison_table.tsv"

# For each statistic, whether a smaller number means a cheaper route. Statistics that do not
# order at all -- the reading label, the milestone list -- are carried through with no
# direction, because dropping them would remove the context the numbers are read in.
LOWER_IS_CHEAPER = {
    "n_resources_consulted": True,
    "n_resources_used": True,
    "n_resources_discarded": True,
    "n_commands_run": True,
    "n_commands_failed": True,
    "n_decisions_logged": True,
    "n_blockers_hit": True,
    "n_blockers_unresolved": True,
    "n_dead_ends": True,
    "n_resources_before_evaluation_complete": True,
    "n_commands_before_evaluation_complete": True,
    "elapsed_minutes_total": True,
    "elapsed_minutes_to_evaluation_complete": True,
    "n_log_rows": True,
}


def main():
    rows = list(csv.DictReader(open(EFFORT, newline=""), delimiter="\t"))
    routes = []
    for row in rows:
        if row["route"] not in routes:
            routes.append(row["route"])
    if len(routes) != 2:
        raise SystemExit(f"expected two routes in {EFFORT}, found {routes}")
    a, b = routes
    values = {(r["route"], r["statistic"]): r["value"] for r in rows}
    statistics = [r["statistic"] for r in rows if r["route"] == a]

    out = []
    for statistic in statistics:
        va, vb = values[(a, statistic)], values[(b, statistic)]
        direction, ratio = "", ""
        if statistic in LOWER_IS_CHEAPER and va != "" and vb != "":
            fa, fb = float(va), float(vb)
            if fa == fb:
                direction = "equal"
            else:
                direction = f"{a} lower" if fa < fb else f"{b} lower"
            if min(fa, fb) > 0:
                ratio = f"{max(fa, fb) / min(fa, fb):.2f}"
            elif max(fa, fb) > 0:
                ratio = "undefined (one route is zero)"
        out.append((statistic, va, vb, direction, ratio))

    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["statistic", f"route_{a}", f"route_{b}",
                    "cheaper_route", "ratio_larger_over_smaller"])
        w.writerows(out)
    print(f"wrote {OUT.relative_to(NODE)} ({len(out)} statistics, routes {a} and {b})")


if __name__ == "__main__":
    main()
