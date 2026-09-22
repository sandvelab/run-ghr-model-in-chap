#!/usr/bin/env python3
"""Read, validate and summarise a route's `discovery_log.tsv`.

This is the project's measuring instrument. Both routes' logs are read by this one module,
so the two can never be measured by subtly different code — which is the whole reason the
summarising lives in the comparison node and not in either route's.

The format it enforces is specified in `AI-internal/skill-references/discovery-log-format.md`
and is not restated here; where the two disagree the specification is right and this file is
a bug.

## What counts as what

Two of the statistics are definitions rather than counts, and they are stated here because a
reader has to be able to argue with them:

- **A dead end** is an attempt that did not work and had to be abandoned or corrected: a
  `command` row with outcome `failed`, plus each *distinct* `blocker` that was hit. A blocker
  logged `open` and later `resolved` is one dead end, not two — the route still had to go
  round it.
- **Elapsed minutes** are wall-clock between the first and last row, and between the first
  row and `evaluation_complete`. They are reported because they are cheap, and they are not
  the primary measure: two agents running concurrently on one machine contend for it, and
  an agent's own thinking time is not in the log.

Standard library only.
"""
from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

COLUMNS = ["step", "ts_utc", "kind", "ref", "outcome", "note"]

KINDS = ("resource", "command", "decision", "blocker", "milestone")

# Which outcomes each kind may take. A row outside this table is a malformed row, not a
# finding about the route.
ALLOWED_OUTCOMES = {
    "resource": {"used", "discarded"},
    "command": {"ok", "failed"},
    "decision": {"used", "discarded"},
    "blocker": {"open", "resolved"},
    "milestone": {"ok"},
}

# Closed vocabulary: these are the fixed points the two routes are aligned on.
MILESTONES = (
    "first_doc_opened",
    "model_obtained",
    "model_runs_standalone",
    "model_registered_with_chap",
    "evaluation_started",
    "evaluation_complete",
    "route_abandoned",
)

TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def parse_ts(value: str) -> datetime:
    return datetime.strptime(value, TS_FORMAT).replace(tzinfo=timezone.utc)


def read_log(path: str | Path) -> list[dict[str, str]]:
    """Read a log file into rows, without judging it. Validation is a separate step."""
    with Path(path).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if reader.fieldnames != COLUMNS:
            raise ValueError(
                f"{path}: header is {reader.fieldnames}, specification requires {COLUMNS}"
            )
        return [{c: (r.get(c) or "").strip() for c in COLUMNS} for r in reader]


def validate(rows: list[dict[str, str]]) -> list[str]:
    """Every way a log can fail the specification. Empty list means it conforms."""
    errors: list[str] = []
    if not rows:
        return ["log is empty"]

    for i, r in enumerate(rows, start=1):
        where = f"row {i} (step {r['step'] or '?'})"
        try:
            step = int(r["step"])
        except ValueError:
            errors.append(f"{where}: step is not an integer: {r['step']!r}")
            step = None
        if step is not None and step != i:
            errors.append(f"{where}: step must be {i}, strictly increasing by 1")

        try:
            parse_ts(r["ts_utc"])
        except ValueError:
            errors.append(f"{where}: ts_utc is not YYYY-MM-DDTHH:MM:SSZ: {r['ts_utc']!r}")

        if r["kind"] not in KINDS:
            errors.append(f"{where}: kind {r['kind']!r} is not one of {KINDS}")
        elif r["outcome"] not in ALLOWED_OUTCOMES[r["kind"]]:
            errors.append(
                f"{where}: kind {r['kind']} may not take outcome {r['outcome']!r}; "
                f"allowed: {sorted(ALLOWED_OUTCOMES[r['kind']])}"
            )

        if r["kind"] == "milestone" and r["ref"] not in MILESTONES:
            errors.append(f"{where}: milestone {r['ref']!r} is outside the closed vocabulary")

        if not r["ref"]:
            errors.append(f"{where}: ref is empty")
        if "\t" in r["note"] or "\n" in r["note"]:
            errors.append(f"{where}: note contains a tab or newline")

    stamps = []
    for r in rows:
        try:
            stamps.append(parse_ts(r["ts_utc"]))
        except ValueError:
            stamps.append(None)
    for i in range(1, len(stamps)):
        if stamps[i] and stamps[i - 1] and stamps[i] < stamps[i - 1]:
            errors.append(f"row {i + 1}: ts_utc goes backwards")

    return errors


def _milestone_index(rows: list[dict[str, str]], name: str) -> int | None:
    for i, r in enumerate(rows):
        if r["kind"] == "milestone" and r["ref"] == name:
            return i
    return None


def summarise(rows: list[dict[str, str]]) -> dict[str, str | int | float]:
    """The statistics §2 of the plan defines as the primary measure of a route."""
    kinds = Counter(r["kind"] for r in rows)
    stamps = [parse_ts(r["ts_utc"]) for r in rows]
    per_stamp = Counter(r["ts_utc"] for r in rows)

    def count(kind: str, outcome: str, upto: int | None = None) -> int:
        window = rows if upto is None else rows[: upto + 1]
        return sum(1 for r in window if r["kind"] == kind and r["outcome"] == outcome)

    blockers_hit = {r["ref"] for r in rows if r["kind"] == "blocker"}
    blockers_resolved = {
        r["ref"] for r in rows if r["kind"] == "blocker" and r["outcome"] == "resolved"
    }
    failed_commands = count("command", "failed")

    done = _milestone_index(rows, "evaluation_complete")
    reached = done is not None

    elapsed_total = (stamps[-1] - stamps[0]).total_seconds() / 60
    elapsed_to_done = (
        (stamps[done] - stamps[0]).total_seconds() / 60 if reached else ""
    )

    out: dict[str, str | int | float] = {
        "reached_evaluation": "yes" if reached else "no",
        "n_steps": len(rows),
        "n_resources": kinds["resource"],
        "n_resources_used": count("resource", "used"),
        "n_resources_discarded": count("resource", "discarded"),
        "n_commands": kinds["command"],
        "n_commands_failed": failed_commands,
        "n_decisions": kinds["decision"],
        "n_decisions_taken": count("decision", "used"),
        "n_decisions_discarded": count("decision", "discarded"),
        "n_blockers_hit": len(blockers_hit),
        "n_blockers_unresolved": len(blockers_hit - blockers_resolved),
        "n_dead_ends": failed_commands + len(blockers_hit),
        "n_resources_before_evaluation": count("resource", "used", done)
        + count("resource", "discarded", done) if reached else "",
        "n_commands_before_evaluation": count("command", "ok", done)
        + count("command", "failed", done) if reached else "",
        "elapsed_minutes_total": round(elapsed_total, 1),
        "elapsed_minutes_to_evaluation": round(elapsed_to_done, 1) if reached else "",
        "milestones_reached": "+".join(
            m for m in MILESTONES if _milestone_index(rows, m) is not None
        ),
        # Integrity. A log written in one sitting at the end shows up as a handful of
        # distinct timestamps carrying many rows each; plan §3 requires that such a log be
        # reported as inadmissible rather than quietly used.
        "n_distinct_timestamps": len(per_stamp),
        "max_rows_sharing_one_timestamp": max(per_stamp.values()),
    }
    return out


STATISTICS = list(summarise([{
    "step": "1", "ts_utc": "2026-01-01T00:00:00Z", "kind": "milestone",
    "ref": "first_doc_opened", "outcome": "ok", "note": "",
}]).keys())
