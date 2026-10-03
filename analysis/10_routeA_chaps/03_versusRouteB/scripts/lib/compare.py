#!/usr/bin/env python3
"""Route A through chaps against route B (MLproject) and against route A without chaps.

Nothing is re-estimated by hand. Route B is re-costed by batch 10's own model on batch 10's own
inputs, filtered to route B; the recomputation must reproduce batch 10's published summary to
the decimal, or this stops. Two route B sensitivities then each change one thing:

- `route-b-noD2` -- divergence D2 removed (the plan's §4b row). The statistician still reads
  library source at step 19, as the agent did; only the 20/50/150-minute GeoJSON trap goes.
- `route-b-docs` -- D2 removed *and* step 19 reads chap-core's `eval-reference.md` (gated on
  `cli-help-reading`) instead of library source. Batch 12 found the sibling-GeoJSON convention
  documented there at v2.3.1, which is what makes D2 an overstatement on today's platform.

The batch 12 and batch 14 figures are read from their own `summary.tsv` files.

Standard library only.
"""
from __future__ import annotations

import csv
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
NODE = HERE.parents[2]
REPO = HERE.parents[5]
B10 = REPO / "analysis/08_humanCost"
B12 = REPO / "analysis/09_routeA_iteration3/02_humanCost"
B14 = REPO / "analysis/10_routeA_chaps/02_humanCost"
MODEL = B10 / "scripts/lib/human_cost.py"
OUT = NODE / "results"


def read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        return list(rd.fieldnames or []), list(rd)


def write(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n",
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def route_b_variant(name: str, edit_steps, keep_divergence) -> Path:
    d = OUT / "routeB" / name
    if d.exists():
        shutil.rmtree(d)
    (d / "inputs").mkdir(parents=True)
    for f in ("act_costs", "personas", "prerequisites", "modifiers", "reading_rates"):
        shutil.copy2(B10 / "scripts/inputs" / f"{f}.tsv", d / "inputs" / f"{f}.tsv")
    fields, steps = read(B10 / "scripts/inputs/steps.tsv")
    steps = [edit_steps(dict(s)) for s in steps if s["route"] == "route-b"]
    write(d / "inputs/steps.tsv", fields, steps)
    fields, div = read(B10 / "scripts/inputs/divergences.tsv")
    write(d / "inputs/divergences.tsv", fields,
          [r for r in div if r["route"] == "route-b" and keep_divergence(r)])
    fields, docs = read(B10 / "results/doc_sizes.tsv")
    docs += [r for r in read(B12 / "results/doc_sizes.tsv")[1] if r["doc_key"] == "doc_eval_ref"]
    write(d / "doc_sizes.tsv", fields, docs)
    shutil.copy2(B10 / "results/machine_waits.tsv", d / "machine_waits.tsv")
    subprocess.run([sys.executable, str(MODEL), "--inputs", str(d / "inputs"), "--results", str(d)],
                   check=True, stdout=subprocess.DEVNULL)
    return d / "summary.tsv"


def docs_not_source(s: dict) -> dict:
    if s["seq"] == "19":
        if s["doc_key"] != "chapcore_common":
            raise SystemExit("route B step 19 is not the library-source read")
        s.update(doc_key="doc_eval_ref", prereqs="cli-help-reading",
                 label="read chap-core's docs/chap-cli/eval-reference.md",
                 note="sensitivity: the documented convention in place of library source")
    return s


def main() -> int:
    same = route_b_variant("as_batch10", lambda s: s, lambda r: True)
    _, b10 = read(B10 / "results/summary.tsv")
    _, again = read(same)
    keys = ("total_low", "total_exp", "total_high", "unguided_share", "n_prereqs_lacked")
    for r in again:
        ref = next(x for x in b10 if x["persona"] == r["persona"] and x["route"] == "route-b")
        if any(r[k] != ref[k] for k in keys):
            raise SystemExit(f"route B recomputation differs from batch 10 for {r['persona']}")
    nod2 = route_b_variant("noD2", lambda s: s, lambda r: r["rule"] != "D2")
    docs = route_b_variant("docs", docs_not_source, lambda r: r["rule"] != "D2")

    sources = [
        ("route B, MLproject (batch 10)", "main", B10 / "results/summary.tsv", "route-b"),
        ("route B without the D2 GeoJSON trap", "sensitivity", nod2, "route-b"),
        ("route B, convention from the docs, not source", "sensitivity", docs, "route-b"),
        ("route A without chaps (batch 12)", "main", B12 / "results/summary.tsv", "route-a-it3"),
        ("route A through chaps (batch 14)", "main", B14 / "results/summary.tsv", "route-a-chaps"),
        ("route A through chaps, Docker priced lighter", "sensitivity",
         B14 / "results/sensitivity/docker_lighter/summary.tsv", "route-a-chaps"),
        ("route A through chaps, docs/run.md in place of the agent page", "sensitivity",
         B14 / "results/sensitivity/run_doc_not_ai_page/summary.tsv", "route-a-chaps"),
        ("route A through chaps on this batch's link, to the point it fails", "slow link",
         B14 / "results/summary.tsv", "route-a-chaps-slowlink"),
    ]
    rows = []
    for label, kind, path, route in sources:
        for r in read(path)[1]:
            if r["route"] != route:
                continue
            rows.append({"persona": r["persona"], "row": label, "kind": kind, "route": route,
                         **{k: r[k] for k in ("total_low", "total_exp", "total_high",
                                              "human_min_exp", "machine_min_exp",
                                              "learn_min_exp", "diagnose_min_exp",
                                              "unguided_share", "n_prereqs_lacked",
                                              "n_prereqs_partial", "n_steps")},
                         "source": str(path.relative_to(REPO))})
    rows.sort(key=lambda r: r["persona"])
    write(OUT / "comparison.tsv", list(rows[0]), rows)

    # Ratios against route B for the two main route A rows, per persona.
    ratios = []
    for persona in sorted({r["persona"] for r in rows}):
        b = next(r for r in rows if r["persona"] == persona and r["row"].startswith("route B, ML"))
        for r in rows:
            if r["persona"] == persona and r["kind"] == "main" and r["route"] != "route-b":
                ratios.append({"persona": persona, "row": r["row"],
                               "total_exp": r["total_exp"], "route_b_total_exp": b["total_exp"],
                               "ratio_to_route_b": round(float(r["total_exp"])
                                                         / float(b["total_exp"]), 2),
                               "difference_min": round(float(r["total_exp"])
                                                       - float(b["total_exp"]), 1)})
    write(OUT / "ratios_to_route_b.tsv", list(ratios[0]), ratios)
    for r in rows:
        print(f"{r['persona']:<13} {r['total_exp']:>7} ({r['total_low']}-{r['total_high']})  "
              f"unguided {r['unguided_share']}  lacked {r['n_prereqs_lacked']}  {r['row']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
