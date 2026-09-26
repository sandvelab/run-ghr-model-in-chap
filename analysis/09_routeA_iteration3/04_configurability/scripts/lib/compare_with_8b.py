#!/usr/bin/env python3
"""Batch 8b's configured variants (through its proxy, on chapkit 2.1.0 and model 60b16a2) beside
this node's (direct, on chapkit 2.1.2 and model a9532c7), one row per variant, plus the evidence
of the configuration's route in each batch.

Scores are set side by side only to show that each setting did something in both batches.
Nothing is selected on them (plan §3). Standard library only.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

NODE = Path(__file__).resolve().parents[2]
REPO = NODE.parents[2]
OLD = REPO / "analysis/06_configurability/results/variants_table.tsv"
NEW = NODE / "results/variants_table.tsv"
METRICS = ("mae", "rmse", "crps", "coverage_10_90")


def tsv(p: Path) -> list[dict[str, str]]:
    with p.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main() -> int:
    old = {r["variant"]: r for r in tsv(OLD)}
    new = {r["variant"]: r for r in tsv(NEW)}
    rows = []
    for v in sorted(new):
        o, n = old.get(v, {}), new[v]
        row = {"variant": v,
               "it2_path": "through config_proxy.py", "it3_path": "direct, nothing interposed",
               "it2_applied": o.get("configuration_applied", "NA"),
               "it2_evidence": o.get("applied_evidence", "NA"),
               "it3_applied": n["configuration_applied"], "it3_evidence": n["applied_evidence"],
               "it3_stored_family": n["stored_family"]}
        for m in METRICS:
            row[f"it2_{m}"] = o.get(m, "NA")
            row[f"it3_{m}"] = n[m]
            row[f"it2_{m}_pct_vs_control"] = o.get(f"{m}_pct_vs_control", "NA")
            row[f"it3_{m}_pct_vs_control"] = n[f"{m}_pct_vs_control"]
        rows.append(row)
    with (NODE / "results/configurability_then_and_now.tsv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    # The shape questions, from this node's own files.
    schema = json.loads((NODE / "results/config_schema.json").read_text())
    nested_left = []
    for v in sorted(new):
        stored = json.loads((NODE / f"results/variants/{v}/stored_config.json").read_text())
        nested_left.append("user_option_values" in (stored[0].get("data", {}) if stored else {}))
    flat_log = (NODE / "results/flat_shape/chap_eval.log").read_text()
    flat_posts = (NODE / "results/flat_shape/service.log").read_text().count("POST /api/v1/configs")
    facts = [
        ("variants_run_direct", str(len(new))),
        ("variants_applied", str(sum(r["configuration_applied"] == "yes" for r in new.values()))),
        ("variants_with_nested_remainder_in_stored_config", str(sum(nested_left))),
        ("service_schema_declares_user_option_values", str("user_option_values" in schema.get("properties", {})).lower()),
        ("service_schema_option_count", str(len(schema.get("properties", {})))),
        ("flat_yaml_exit_code", (NODE / "results/flat_shape/chap_eval_exit_code.txt").read_text().strip()),
        ("flat_yaml_refused_with_extra_forbidden", str("extra_forbidden" in flat_log).lower()),
        ("flat_yaml_config_posts_reaching_service", str(flat_posts)),
    ]
    with (NODE / "results/configurability_facts.tsv").open("w", encoding="utf-8", newline="") as fh:
        fh.write("fact\tvalue\n")
        for k, v in facts:
            fh.write(f"{k}\t{v}\n")
    for k, v in facts:
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
