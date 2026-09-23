#!/usr/bin/env python3
"""Collect what each configuration variant fitted and what it scored, into two files.

  variants_table.tsv   one row per variant: the option changed, whether the configuration
                       demonstrably reached the model, and the metrics CHAP wrote
  variants_formulas.tsv the model formula each variant actually fitted, which is the evidence
                       that the configuration took effect rather than being silently dropped

The second file is the important one. A configured run of this model is indistinguishable
from an unconfigured one by its output alone -- both write a valid NetCDF and real metrics --
so the only way to know a setting was applied is to read what the model fitted.

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

METRICS = ["mae", "rmse", "crps", "mape", "coverage_10_90", "coverage_25_75"]

# What each formula fragment tells you the model used.
PROBES = {
    "spatial": re.compile(r"f\(spatial_id, model = '([a-z0-9]+)'"),
    "seasonal": re.compile(r"f\(seasonal_id, model = '([a-z0-9]+)'"),
    "interannual": re.compile(r"f\(year_id, model = '([a-z0-9]+)'"),
}


def read_metrics(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return rows[0] if rows else {}


def parse_simple_yaml(path: Path) -> dict[str, str]:
    """The variant configs are two levels deep and written by this node; a full parser is
    more dependency than the pinned environment carries."""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if not line.startswith("  ") or ":" not in line:
            continue
        k, _, v = line.strip().partition(":")
        out[k.strip()] = v.strip()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variants-dir", type=Path, required=True)
    ap.add_argument("--formula-check-dir", type=Path, default=None,
                    help="a short-backtest re-run kept only for the fitted formula; its "
                         "scores are NOT used, because its backtest differs")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    variants = sorted(p for p in a.variants_dir.iterdir() if p.is_dir())
    baseline_key = None
    rows, formula_rows = [], []

    for v in variants:
        asked = parse_simple_yaml(v / "config.yaml")
        formula = (v / "fitted_formula.txt").read_text().strip() if (v / "fitted_formula.txt").exists() else ""

        # Corroboration from the short-backtest re-run, where one exists. Kept in its own
        # column and never merged with the row's own formula: it is a different run, and a
        # reader must be able to see which evidence came from which.
        fc_formula = ""
        if a.formula_check_dir:
            fc = a.formula_check_dir / v.name / "fitted_formula.txt"
            if fc.exists():
                fc_formula = fc.read_text().strip()
        fc_terms = ""
        if fc_formula:
            fc_terms = " ".join(
                f"{k}={(m.group(1) if (m := rx.search(fc_formula)) else 'ABSENT')}"
                for k, rx in PROBES.items()
            )
        got = {k: (m.group(1) if (m := rx.search(formula)) else "") for k, rx in PROBES.items()}
        metrics = read_metrics(v / "metrics.csv")

        stored = {}
        sc = v / "stored_config.json"
        if sc.exists():
            try:
                cfgs = json.loads(sc.read_text())
                stored = (cfgs[0] if isinstance(cfgs, list) and cfgs else {}).get("data", {})
            except ValueError:
                stored = {}

        # Did the configuration reach the model? Two independent lines of evidence, in order
        # of how directly they answer it.
        #
        # 1. The formula the model fitted. This is what the model DID, and is decisive.
        # 2. The configuration the service stored, read back from it. This shows the value
        #    arrived flat and was not parked in an ignored nested block -- which is the exact
        #    failure this node exists to characterise -- but it is what the service RECORDED,
        #    one step short of what it fitted.
        #
        # Which one was available is reported, because a reader should not have to guess
        # whether a "yes" rests on the model's behaviour or on its bookkeeping.
        checks = []
        for term, asked_key in (("spatial", "re_spatial"), ("seasonal", "re_seasonal"),
                                ("interannual", "re_interannual")):
            want = asked.get(asked_key)
            if want is None:
                continue
            have = got[term]
            checks.append((want == "none" and have == "") or want == have)

        if formula and checks:
            applied = "yes" if all(checks) else "no"
            evidence = "fitted formula"
        elif stored:
            asked_flat = {k: str(val) for k, val in asked.items()}
            stored_flat = {k: str(stored.get(k)) for k in asked_flat}
            nested_left = bool(stored.get("user_option_values"))
            applied = ("yes" if asked_flat == stored_flat and not nested_left else "no")
            evidence = "stored config read back from the service"
        else:
            applied, evidence = "not established", "none"

        rows.append({
            "variant": v.name,
            "re_spatial": asked.get("re_spatial", ""),
            "re_seasonal": asked.get("re_seasonal", ""),
            "re_interannual": asked.get("re_interannual", ""),
            "family": asked.get("family", ""),
            "configuration_applied": applied,
            "applied_evidence": evidence,
            "formula_check_terms": fc_terms,
            "completed": "yes" if metrics else "no",
            **{m: (f"{float(metrics[m]):.4f}" if metrics.get(m) not in (None, "") else "")
               for m in METRICS},
            "stored_family": str(stored.get("family", "")),
        })
        formula_rows.append({
            "variant": v.name,
            "fitted_formula": formula.replace("\n", " | "),
            "formula_from_short_backtest": fc_formula.replace("\n", " | "),
        })
        if v.name.endswith("published_defaults"):
            baseline_key = v.name

    # Movement against the control, so a reader does not have to subtract in their head.
    base = next((r for r in rows if r["variant"] == baseline_key), None)
    for r in rows:
        for m in METRICS:
            key = f"{m}_pct_vs_control"
            if base and base.get(m) and r.get(m):
                b, x = float(base[m]), float(r[m])
                r[key] = f"{(x - b) / b * 100:+.1f}" if b else ""
            else:
                r[key] = ""

    fields = (["variant", "re_spatial", "re_seasonal", "re_interannual", "family",
               "configuration_applied", "applied_evidence", "formula_check_terms",
               "completed", "stored_family"]
              + METRICS + [f"{m}_pct_vs_control" for m in METRICS])
    with (a.out / "variants_table.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n",
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    with (a.out / "variants_formulas.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["variant", "fitted_formula",
                                          "formula_from_short_backtest"],
                           delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(formula_rows)

    for r in rows:
        print(f"{r['variant']:24s} applied={r['configuration_applied']:16s} "
              f"({r['applied_evidence']})  mae={r['mae'] or '-'}"
              + (f"  |  formula: {r['formula_check_terms']}" if r['formula_check_terms'] else ""))
    print(f"wrote variants_table.tsv and variants_formulas.tsv to {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
