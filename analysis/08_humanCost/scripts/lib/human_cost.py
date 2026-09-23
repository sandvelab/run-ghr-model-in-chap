#!/usr/bin/env python3
"""Carry two personas through each route's logged act sequence and cost it in human minutes.

**This computes a model, not a measurement.** No human has been timed on either route. What
is measured is the *structure* of the encounter -- which documents were opened, which commands
were run, where the route stopped and had to be diagnosed -- and that structure is a property
of the route, not of the agent that met it. What is authored is the pace: how long each kind
of act takes each persona, what each persona already knows, and what changes when they do not
know it. Measured and authored inputs live in separate files for exactly this reason.

## How a step is costed

Every step has an act class. `milestone` and `instrument` rows cost nothing -- the second are
rows that exist only because the agent was logging for this study, and charging a human for
them would be charging them for the instrument. `wait` rows cost the machine's measured time
and are identical for both personas. `read_doc` rows cost the document's measured length
divided by the persona's reading rate. Everything else takes its base time from `act_costs`.

## How knowledge enters

Each step names the prerequisites it is gated on. A persona `hold`s, `partial`ly holds, or
`lack`s each one. Whichever prerequisite the persona holds least well sets that step's
multiplier -- the worst gate, not the product of all of them, because a step is not made four
times harder by four familiar things and one unfamiliar one. The first time a persona meets a
prerequisite they do not fully hold, they pay to acquire it, once per route.

## How a persona's path diverges from the agent's

The logs record what an agent did with the knowledge an agent had. Where a persona lacks
something the agent silently held, the path changes shape, and every such change is a row in
`divergences.tsv` rather than a liberty taken here. The sharpest is the sibling-GeoJSON
convention: route A's agent found it by reading installed library source, and a persona who
would not open library source does not find it that way -- they meet it as a failure, later,
with nothing to tell them what went wrong.

## What is deliberately left out of the totals

Route A's image build from cold. Every build this repository logged ran against a warm layer
cache, so nothing here grounds it; it is carried in its own column, never added in.

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

POINTS = ("low", "exp", "high")
FREE_ACTS = {"milestone", "instrument"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def split_prereqs(cell: str) -> list[str]:
    cell = (cell or "").strip()
    if not cell or cell == "-":
        return []
    return [p.strip() for p in cell.split(";") if p.strip()]


class Model:
    def __init__(self, inputs: Path, results: Path):
        self.prereqs = {r["prereq"]: r for r in read_tsv(inputs / "prerequisites.tsv")}
        self.modifiers = {r["state"]: r for r in read_tsv(inputs / "modifiers.tsv")}
        self.acts = {
            (r["persona"], r["act"]): r for r in read_tsv(inputs / "act_costs.tsv")
        }
        self.rates = {r["persona"]: r for r in read_tsv(inputs / "reading_rates.tsv")}
        self.steps = read_tsv(inputs / "steps.tsv")
        self.divergences = read_tsv(inputs / "divergences.tsv")
        self.docs = {r["doc_key"]: int(r["words"]) for r in read_tsv(results / "doc_sizes.tsv")}
        self.waits = {
            r["wait_key"]: int(r["seconds"]) for r in read_tsv(results / "machine_waits.tsv")
        }
        self.knowledge: dict[tuple[str, str], str] = {}
        for r in read_tsv(inputs / "personas.tsv"):
            self.knowledge[(r["persona"], r["prereq"])] = r["state"]
        self.personas = sorted({p for p, _ in self.knowledge})
        self.routes = sorted({s["route"] for s in self.steps})
        self._check()

    def _check(self) -> None:
        """Refuse to run on an incomplete table rather than silently costing a gap as zero."""
        named = set(self.prereqs)
        for s in self.steps + self.divergences:
            for p in split_prereqs(s.get("prereqs", "")):
                if p not in named:
                    raise SystemExit(f"step names an unknown prerequisite: {p}")
        for persona in self.personas:
            for p in named:
                if (persona, p) not in self.knowledge:
                    raise SystemExit(f"persona {persona} has no state for prerequisite {p}")
        for s in self.steps:
            if s["act"] == "read_doc" and s["doc_key"] not in self.docs:
                raise SystemExit(f"read_doc step names an unmeasured document: {s['doc_key']}")

    def state(self, persona: str, prereq: str) -> str:
        return self.knowledge[(persona, prereq)]

    def gate(self, persona: str, prereqs: list[str]) -> tuple[str, float, float]:
        """The least-held prerequisite sets the step's multipliers."""
        order = {"hold": 0, "partial": 1, "lack": 2}
        worst, worst_rank = "hold", 0
        for p in prereqs:
            st = self.state(persona, p)
            if order[st] > worst_rank:
                worst, worst_rank = st, order[st]
        m = self.modifiers[worst]
        return worst, float(m["act_multiplier"]), float(m["diagnose_multiplier"])

    def base(self, persona: str, step: dict) -> dict[str, float]:
        act = step["act"]
        if act in FREE_ACTS:
            return {p: 0.0 for p in POINTS}
        if act == "wait":
            secs = self.waits[step["route"]]
            return {p: secs / 60.0 for p in POINTS}
        if act == "wait_unknown":
            return {p: 0.0 for p in POINTS}
        if act == "read_doc":
            rate = self.rates[persona]
            wpm = float(rate["wpm_exp"])
            minutes = self.docs[step["doc_key"]] / wpm
            return {
                "low": minutes * float(rate["spread_low"]),
                "exp": minutes,
                "high": minutes * float(rate["spread_high"]),
            }
        if "base_low" in step and step.get("base_low") not in (None, "", "-"):
            return {p: float(step[f"base_{p}"]) for p in POINTS}
        row = self.acts[(persona, act)]
        return {p: float(row[f"base_{p}"]) for p in POINTS}

    def path(self, persona: str, route: str) -> list[dict]:
        """The persona's step sequence, after the divergence rules that apply to them."""
        steps = [dict(s) for s in self.steps if s["route"] == route]
        dropped: set[str] = set()
        added: dict[str, list[dict]] = {}
        applied: list[str] = []
        for d in self.divergences:
            if d["route"] != route:
                continue
            if self.state(persona, d["condition_prereq"]) != d["condition_state"]:
                continue
            applied.append(d["rule"])
            if d["action"] == "drop_step":
                dropped.add(d["anchor_seq"])
            elif d["action"] == "add_after":
                added.setdefault(d["anchor_seq"], []).append(
                    {
                        "route": route,
                        "seq": f"{d['anchor_seq']}+",
                        "log_step": "-",
                        "source": f"divergence {d['rule']}",
                        "act": d["act"],
                        "label": d["label"],
                        "doc_key": "-",
                        "prereqs": d["prereqs"],
                        "note": d["note"],
                        "base_low": d["base_low"],
                        "base_exp": d["base_exp"],
                        "base_high": d["base_high"],
                        "condition": "",
                    }
                )
        out: list[dict] = []
        for s in steps:
            if s["seq"] in dropped:
                s = dict(s, act="dropped", note=next(
                    d["note"] for d in self.divergences
                    if d["route"] == route and d["action"] == "drop_step"
                    and d["anchor_seq"] == s["seq"]
                ))
                s["_dropped"] = "yes"
            out.append(s)
            out.extend(added.get(s["seq"], []))
        for s in out:
            s["_rules"] = ",".join(sorted(set(applied))) if applied else "-"
        return out

    def walk(self, persona: str, route: str) -> tuple[list[dict], dict]:
        rows: list[dict] = []
        learned: set[str] = set()
        cum = {p: 0.0 for p in POINTS}
        totals = {
            "human": {p: 0.0 for p in POINTS},
            "machine": {p: 0.0 for p in POINTS},
            "learn": {p: 0.0 for p in POINTS},
            "diagnose": {p: 0.0 for p in POINTS},
        }
        exposure: list[dict] = []
        build_unknown = "no"
        conditional: dict[str, float] = {}

        for step in self.path(persona, route):
            act = step["act"]
            if step.get("_dropped") == "yes" or act == "dropped":
                rows.append(
                    {
                        "seq": step["seq"], "log_step": step["log_step"], "act": "dropped",
                        "label": step["label"], "gate": "-", "learn_exp": 0.0,
                        "min_low": 0.0, "min_exp": 0.0, "min_high": 0.0,
                        "cum_exp": round(cum["exp"], 1), "note": step["note"],
                    }
                )
                continue
            if act == "wait_unknown":
                build_unknown = "yes"
                rows.append(
                    {
                        "seq": step["seq"], "log_step": step["log_step"], "act": act,
                        "label": step["label"], "gate": "-", "learn_exp": 0.0,
                        "min_low": 0.0, "min_exp": 0.0, "min_high": 0.0,
                        "cum_exp": round(cum["exp"], 1), "note": step["note"],
                    }
                )
                continue

            prereqs = split_prereqs(step.get("prereqs", ""))
            gate, act_mult, diag_mult = self.gate(persona, prereqs)
            mult = diag_mult if act == "diagnose" else act_mult
            base = self.base(persona, step)

            learn = {p: 0.0 for p in POINTS}
            for p in prereqs:
                if p in learned:
                    continue
                st = self.state(persona, p)
                frac = float(self.modifiers[st]["learn_fraction"])
                if frac <= 0:
                    learned.add(p)
                    continue
                pr = self.prereqs[p]
                for point in POINTS:
                    learn[point] += float(pr[f"learn_{point}"]) * frac
                learned.add(p)
                exposure.append(
                    {
                        "persona": persona, "route": route, "prereq": p, "state": st,
                        "first_seq": step["seq"],
                        "learn_min_exp": round(float(pr["learn_exp"]) * frac, 1),
                        "description": pr["description"],
                    }
                )

            minutes = {}
            for point in POINTS:
                if act == "wait":
                    minutes[point] = base[point]
                else:
                    minutes[point] = base[point] * mult + learn[point]
            for point in POINTS:
                cum[point] += minutes[point]
                if act == "wait":
                    totals["machine"][point] += minutes[point]
                else:
                    totals["human"][point] += minutes[point]
                totals["learn"][point] += learn[point]
                if act == "diagnose":
                    totals["diagnose"][point] += base[point] * mult
            cond = (step.get("condition") or "").strip()
            if cond:
                conditional[cond] = conditional.get(cond, 0.0) + minutes["exp"]

            rows.append(
                {
                    "seq": step["seq"], "log_step": step["log_step"], "act": act,
                    "label": step["label"], "gate": gate,
                    "learn_exp": round(learn["exp"], 1),
                    "min_low": round(minutes["low"], 1),
                    "min_exp": round(minutes["exp"], 1),
                    "min_high": round(minutes["high"], 1),
                    "cum_exp": round(cum["exp"], 1),
                    "note": step["note"],
                }
            )

        human_exp = totals["human"]["exp"]
        unguided = totals["learn"]["exp"] + totals["diagnose"]["exp"]
        lacked = sum(1 for e in exposure if e["state"] == "lack")
        partial = sum(1 for e in exposure if e["state"] == "partial")
        summary = {
            "persona": persona, "route": route,
            "total_low": round(cum["low"], 1),
            "total_exp": round(cum["exp"], 1),
            "total_high": round(cum["high"], 1),
            "human_min_exp": round(human_exp, 1),
            "machine_min_exp": round(totals["machine"]["exp"], 1),
            "learn_min_exp": round(totals["learn"]["exp"], 1),
            "diagnose_min_exp": round(totals["diagnose"]["exp"], 1),
            "unguided_share": round(unguided / human_exp, 3) if human_exp else 0.0,
            "n_prereqs_lacked": lacked,
            "n_prereqs_partial": partial,
            "cold_build_excluded": build_unknown,
            "n_steps": sum(1 for r in rows if r["act"] not in FREE_ACTS | {"dropped"}),
            "arm64_host_only_min_exp": round(conditional.get("arm64-host", 0.0), 1),
        }
        return rows, summary, exposure


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--results", required=True)
    a = ap.parse_args()
    inputs, results = Path(a.inputs), Path(a.results)
    m = Model(inputs, results)

    summaries, exposures = [], []
    walk_fields = ["seq", "log_step", "act", "label", "gate", "learn_exp",
                   "min_low", "min_exp", "min_high", "cum_exp", "note"]
    for persona in m.personas:
        for route in m.routes:
            rows, summary, exposure = m.walk(persona, route)
            write_tsv(results / f"walkthrough_{persona}_{route}.tsv", rows, walk_fields)
            summaries.append(summary)
            exposures.extend(exposure)

    write_tsv(results / "summary.tsv", summaries, list(summaries[0]))
    write_tsv(
        results / "prereq_exposure.tsv", exposures,
        ["persona", "route", "prereq", "state", "first_seq", "learn_min_exp", "description"],
    )
    print(f"wrote {len(summaries)} walkthroughs and a summary")
    for s in summaries:
        print(
            f"  {s['persona']:<13} {s['route']}  "
            f"{s['total_low']:>7.1f} / {s['total_exp']:>7.1f} / {s['total_high']:>7.1f} min  "
            f"unguided {s['unguided_share']:.0%}  lacked {s['n_prereqs_lacked']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
