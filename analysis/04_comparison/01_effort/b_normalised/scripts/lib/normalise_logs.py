#!/usr/bin/env python3
"""Count effort after applying two rules to both routes' logs alike.

Two agents given the identical format still code the same act differently, and that
difference reads as a difference between the routes when it is a difference between the
writers. The alternative beside this one (`a_asLogged`) takes each log at face value and is
the only purely observational reading; this one argues that two specific codings are
artefacts and states the rules that remove them.

**The logs themselves are never edited** (AGENTS.md §1). The rules are applied in memory,
here, where they can be read and disagreed with, and the raw logs stay exactly as their agents
wrote them.

## Rule 1 — failure attribution

An agent that ran a command, marked it `ok` before reading its output, and then recorded the
failure in a later row has logged a failed command as something else. So: a row whose `ref` or
`note` names an earlier step as a correction *and* says that step failed reclassifies that
earlier `command` row to `failed`.

A correcting row that is itself a `blocker` **whose `ref` is the correction** is then not
counted as a blocker as well — it is the same event as the command failure, and counting both
would charge the route twice for one mistake. A blocker whose `ref` names a real external
condition stays a blocker even when its note also carries a correction.

A correction that does not say the earlier step failed changes nothing: correcting a factual
claim is not a failure.

## Rule 2 — the discovery window

Every statistic is counted over the rows up to and including the **first**
`evaluation_complete`. After that the route demonstrably works, and what follows — verifying a
script, re-running from clean, reading a plot format — is not the cost of finding out how to
run the model. Both logs continue past that milestone, and unequally.

Standard library only.
"""
from __future__ import annotations

import argparse
import copy
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "lib"))
import discovery_log as dl  # noqa: E402

CORRECTION = re.compile(r"correction to step (\d+)", re.I)
SAYS_FAILED = re.compile(r"\bfail(ed|s)?\b", re.I)


def apply_rules(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    """Return the normalised rows and a human-readable list of what each rule changed."""
    rows = copy.deepcopy(rows)
    changes: list[str] = []

    # --- Rule 1 -------------------------------------------------------------------
    drop_as_blocker: set[int] = set()
    for i, r in enumerate(rows):
        text = f"{r['ref']} {r['note']}"
        m = CORRECTION.search(text)
        if not m or not SAYS_FAILED.search(text):
            continue
        target = int(m.group(1))
        if not 1 <= target <= len(rows):
            continue
        t = rows[target - 1]
        if t["kind"] == "command" and t["outcome"] != "failed":
            t["outcome"] = "failed"
            changes.append(
                f"rule 1: step {target} ({t['ref'][:60]}) reclassified ok -> failed, "
                f"on the correction carried by step {r['step']}"
            )
        if r["kind"] == "blocker" and CORRECTION.match(r["ref"].strip()):
            drop_as_blocker.add(i)
            changes.append(
                f"rule 1: step {r['step']} not counted as a blocker -- its ref is the "
                f"correction to step {target}, not an external condition"
            )
    for i in sorted(drop_as_blocker, reverse=True):
        rows[i]["kind"] = "decision"       # kept in the record, out of the blocker count
        rows[i]["outcome"] = "used"

    # --- Rule 2 -------------------------------------------------------------------
    done = next(
        (i for i, r in enumerate(rows)
         if r["kind"] == "milestone" and r["ref"] == "evaluation_complete"),
        None,
    )
    if done is not None and done + 1 < len(rows):
        changes.append(
            f"rule 2: {len(rows) - done - 1} row(s) after the first evaluation_complete "
            f"(step {rows[done]['step']}) are outside the discovery window"
        )
        rows = rows[: done + 1]

    for n, r in enumerate(rows, start=1):     # keep the log self-consistent for the summariser
        r["step"] = str(n)
    return rows, changes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--log", action="append", required=True, metavar="ROUTE=PATH")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--changes", type=Path, required=True,
                    help="what the rules changed, per route, so the reading can be audited")
    a = ap.parse_args()

    summaries, audit = {}, []
    routes = []
    for spec in a.log:
        route, path = spec.split("=", 1)
        routes.append(route)
        raw = dl.read_log(Path(path))
        errors = dl.validate(raw)
        if errors:
            print(f"{route}: log does not conform: {errors}", file=sys.stderr)
            return 1
        rows, changes = apply_rules(raw)
        summaries[route] = dl.summarise(rows)
        audit.append((route, len(raw), len(rows), changes))
        print(f"{route}: {len(raw)} rows -> {len(rows)} in window, {len(changes)} change(s)")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["statistic", *routes])
        for stat in dl.STATISTICS:
            w.writerow([stat, *(summaries[r][stat] for r in routes)])

    with a.changes.open("w", encoding="utf-8") as fh:
        fh.write("# What the two rules changed\n\n")
        fh.write("Applied to both logs alike. The logs themselves are not edited.\n")
        for route, n_raw, n_win, changes in audit:
            fh.write(f"\n## {route}\n\n{n_raw} rows logged, {n_win} inside the discovery window.\n\n")
            fh.write("\n".join(f"- {c}" for c in changes) + "\n" if changes
                     else "- neither rule changed anything in this log\n")
    print(f"wrote {a.out} and {a.changes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
