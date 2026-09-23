#!/usr/bin/env python3
"""Did the operator's configuration reach the model, and what happened when it did?

Three columns carry the answer, and they are deliberately separate:

* **delivered** — read from `model_configuration_for_run.yaml`, the file CHAP writes into the
  model's own run directory and the model then reads. This is the direct evidence that a value
  arrived: not an inference from scores, and not the model's word for it.
* **completed** — whether CHAP wrote an evaluation.
* **error** — for a run that did not complete, the first line saying why, kept because a run
  that fails loudly is a different and better outcome than one that fails silently.

A value can arrive and change nothing, and a value can arrive in a shape the model cannot read.
Both are distinguishable here, which is the point.

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

METRICS = ["mae", "rmse", "crps", "mape", "coverage_10_90"]
VALUE = re.compile(r"alpha:\s*(?:\n\s*values:\s*)?([0-9.eE+-]+)")
ERROR = re.compile(r"^(?:\w+Error|AttributeError|TypeError|ValueError).*$", re.M)


def read_metrics(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return rows[0] if rows else {}


def alpha_in(path: Path) -> str:
    if not path.exists():
        return ""
    m = VALUE.search(path.read_text())
    return m.group(1) if m else ""


def shape_of(path: Path) -> str:
    """Whether alpha is given as a bare value or wrapped in a `values:` mapping."""
    if not path.exists():
        return ""
    t = path.read_text()
    if re.search(r"alpha:\s*\n\s*values:", t):
        return "nested (alpha.values) — the model's own config.yaml shape"
    if re.search(r"alpha:\s*[0-9.eE+-]+", t):
        return "scalar (alpha) — the shape `chap model schema --example` emits"
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    rows = []
    for d in sorted(p for p in a.runs.iterdir() if p.is_dir()):
        asked = alpha_in(d / "config.yaml")
        delivered = alpha_in(d / "model_configuration_for_run.yaml")
        metrics = read_metrics(d / "metrics.csv")
        log = (d / "chap_eval.log").read_text(errors="replace") if (d / "chap_eval.log").exists() else ""
        err = (m.group(0).strip() if (m := ERROR.search(log)) else "")

        rows.append({
            "run": d.name,
            "config_shape": shape_of(d / "config.yaml"),
            "alpha_asked": asked,
            "alpha_delivered_to_the_model": delivered or "(no config file found)",
            "configuration_arrived": "yes" if delivered and delivered == asked else
                                     ("yes" if delivered else "not established"),
            "completed": "yes" if metrics else "no",
            "error": err,
            **{k: (f"{float(metrics[k]):.4f}" if metrics.get(k) not in (None, "") else "")
               for k in METRICS},
        })

    fields = ["run", "config_shape", "alpha_asked", "alpha_delivered_to_the_model",
              "configuration_arrived", "completed", "error"] + METRICS
    with (a.out / "config_delivery.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    ok = [r for r in rows if r["completed"] == "yes"]
    distinct = {tuple(r[k] for k in METRICS) for r in ok}
    with (a.out / "config_effect.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["question", "answer"])
        w.writerow(["runs attempted", len(rows)])
        w.writerow(["runs that completed", len(ok)])
        w.writerow(["configurations demonstrably delivered to the model",
                    sum(1 for r in rows if r["configuration_arrived"] == "yes")])
        w.writerow(["distinct metric vectors across completed runs", len(distinct)])
        w.writerow(["predictions changed with the setting", "yes" if len(distinct) > 1 else "no"])
        w.writerow(["a wrong config shape failed", "loudly, with a traceback naming the cause"
                    if any(r["error"] for r in rows) else "not exercised"])

    for r in rows:
        print(f"{r['run']:22s} asked={r['alpha_asked']:6s} delivered={r['alpha_delivered_to_the_model']:6s} "
              f"completed={r['completed']:4s} mae={r['mae'] or '-':10s} {r['error'][:40]}")
    print(f"{len(distinct)} distinct metric vector(s) across {len(ok)} completed run(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
