#!/usr/bin/env python3
"""Iteration 2's route A against iteration 3's, one row per quantity, every value read from a file.

Agent effort comes from `results/effort_normalised.tsv` (the main path of the effort fork, as in
batch 6), human estimates from each iteration's `summary.tsv`, agent usage from
`agent_usage.tsv`, scores from the metrics CHAP wrote. Where iteration 2 has no value, the cell
is `NA` and the reason is in `note`; nothing is estimated to fill it.

Standard library only.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
NODE = HERE.parents[2]
REPO = HERE.parents[5]
A2 = REPO / "analysis/02_routeA_chapkit/results"
A3 = REPO / "analysis/09_routeA_iteration3/01_discovery/results"


def tsv(p: Path) -> list[dict[str, str]]:
    with p.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def metrics(p: Path) -> dict[str, float]:
    with p.open(encoding="utf-8", newline="") as fh:
        r = next(csv.DictReader(fh))
    return {k: float(r[k]) for k in ("crps", "mae", "rmse", "coverage_10_90")}


def main() -> int:
    rows: list[dict[str, str]] = []

    def add(group, quantity, it2, it3, note=""):
        rows.append({"group": group, "quantity": quantity, "iteration2": str(it2),
                     "iteration3": str(it3), "note": note})

    eff = {r["statistic"]: r for r in tsv(NODE / "results/effort_normalised.tsv")}
    for s in ("reached_evaluation", "n_resources", "n_resources_discarded", "n_commands",
              "n_commands_failed", "n_decisions", "n_blockers_hit", "n_blockers_unresolved",
              "n_dead_ends", "elapsed_minutes_to_evaluation"):
        add("agent effort (normalised window)", s, eff[s]["it2-route-a"], eff[s]["it3-route-a"],
            "iteration 2's build hit a warm layer cache; iteration 3 started fully cold"
            if s == "elapsed_minutes_to_evaluation" else "")

    use = {r["field"]: r["value"] for r in tsv(A3 / "agent_usage.tsv")}
    add("agent usage", "model", "Claude Opus (version not recorded)", use["agent_model"])
    add("agent usage", "tokens", "NA", use["harness_tokens"], "no earlier batch recorded tokens")
    add("agent usage", "tool_uses", "NA", use["harness_tool_uses"], "not recorded in iteration 2")
    add("agent usage", "agent_wall_clock_min", "NA",
        round(int(use["harness_duration_ms"]) / 60000, 1),
        "iteration 3 includes the agent's own ~12 min clean-shell verification")

    for label, p2, p3 in (("discovery run", A2 / "eval/metrics.csv", A3 / "manual_run/metrics.csv"),
                          ("script run", A2 / "route_run/metrics.csv", A3 / "route_run/metrics.csv")):
        m2, m3 = metrics(p2), metrics(p3)
        for k in m2:
            add(f"scores, {label}", k, round(m2[k], 3), round(m3[k], 3),
                "same model family and data; R-INLA is not bit-reproducible, so read as a spread")

    h2 = {r["persona"]: r for r in tsv(REPO / "analysis/08_humanCost/results/summary.tsv")
          if r["route"] == "route-a"}
    h3 = {r["persona"]: r for r in tsv(REPO / "analysis/09_routeA_iteration3/02_humanCost/results/summary.tsv")}
    for persona in ("engineer", "statistician"):
        for q in ("total_low", "total_exp", "total_high", "human_min_exp", "machine_min_exp",
                  "learn_min_exp", "diagnose_min_exp", "unguided_share", "n_prereqs_lacked",
                  "n_prereqs_partial", "cold_build_excluded", "arm64_host_only_min_exp"):
            note = ""
            if q.startswith("total") and h2[persona]["cold_build_excluded"] == "yes":
                note = "iteration 2 excludes an unmeasured cold image build; iteration 3 needs none, and its image pull is included"
            add(f"human estimate, {persona}", q, h2[persona][q], h3[persona][q], note)
        ratio = float(h3[persona]["total_exp"]) / float(h2[persona]["total_exp"])
        add(f"human estimate, {persona}", "total_exp_ratio_it3_over_it2", "1", round(ratio, 2))

    waits = {r["wait_key"]: int(r["seconds"]) for r in
             tsv(REPO / "analysis/09_routeA_iteration3/02_humanCost/results/machine_waits.tsv")}
    add("human estimate, sensitivity", "extra_min_if_first_pull_as_slow_as_discovery", "-",
        round((waits["pull_discovery_upper_bound"] - waits["pull"]) / 60, 1),
        "added to both personas' totals if the pull ran at the discovery run's upper bound")

    out = NODE / "results/comparison.tsv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out.relative_to(REPO)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
