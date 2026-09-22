"""Validate and summarise a discovery log.

The specification this implements is `AI-internal/skill-references/discovery-log-format.md`.
Read it before changing anything here: the columns and vocabularies are the instrument the
project's comparison is defined over, and loosening a check here silently widens what counts
as a valid measurement.

Kept as a module so that the summarising script and its test share one implementation.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

COLUMNS = ["step", "ts_utc", "kind", "ref", "outcome", "note"]

KIND_OUTCOMES = {
    "resource": {"used", "discarded"},
    "command": {"ok", "failed"},
    "decision": {"used", "discarded"},
    "blocker": {"open", "resolved"},
    "milestone": {"ok"},
}

MILESTONES = [
    "first_doc_opened",
    "model_obtained",
    "model_runs_standalone",
    "model_registered_with_chap",
    "evaluation_started",
    "evaluation_complete",
    "route_abandoned",
]


class LogError(ValueError):
    """A log that does not meet the specification. Never repaired silently."""


def _parse_ts(value: str, step: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise LogError(f"step {step}: ts_utc {value!r} is not YYYY-MM-DDTHH:MM:SSZ") from exc


def load(path: str | Path) -> list[dict]:
    """Read a log and raise LogError on the first thing that is not to specification."""
    path = Path(path)
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if reader.fieldnames != COLUMNS:
            raise LogError(f"{path}: header is {reader.fieldnames}, expected {COLUMNS}")
        rows = list(reader)
    if not rows:
        raise LogError(f"{path}: no rows")

    previous_ts = None
    for index, row in enumerate(rows, start=1):
        step = row["step"]
        if step != str(index):
            raise LogError(f"{path}: step column is {step!r} at row {index}; "
                           "steps start at 1 and increase by 1")
        ts = _parse_ts(row["ts_utc"], step)
        if previous_ts is not None and ts < previous_ts:
            raise LogError(f"step {step}: ts_utc goes backwards")
        previous_ts = ts
        row["_ts"] = ts

        kind = row["kind"]
        if kind not in KIND_OUTCOMES:
            raise LogError(f"step {step}: kind {kind!r} not one of {sorted(KIND_OUTCOMES)}")
        if row["outcome"] not in KIND_OUTCOMES[kind]:
            raise LogError(f"step {step}: outcome {row['outcome']!r} is not allowed for "
                           f"kind {kind!r} (allowed: {sorted(KIND_OUTCOMES[kind])})")
        if kind == "milestone" and row["ref"] not in MILESTONES:
            raise LogError(f"step {step}: milestone {row['ref']!r} is not in the closed "
                           f"vocabulary {MILESTONES}")
        if not row["ref"].strip():
            raise LogError(f"step {step}: ref is empty")
    return rows


HELP_MARKERS = ("--help", " -h")


def _is_help(ref: str) -> bool:
    """A CLI help invocation is a command that is also a piece of documentation.

    The two routes' agents coded these differently -- one logged `chap eval --help` as a
    `resource`, the other as a `command` -- and neither is wrong. The normalisation counts
    such a row as both, by a rule applied identically to both logs rather than by a
    per-row correction, so that nothing depends on which rows a reader thought to adjust.
    """
    return any(marker in ref for marker in HELP_MARKERS)


def _information_sources(rows, normalise, not_a_source):
    """The distinct information sources a route consulted, and which of them contributed.

    As logged (`normalise=False`) this is simply the `resource` rows, which is what the
    agents were asked for. Normalised, two rules apply, in both logs alike:

      R1  a `command` row that is a CLI help invocation is also an information source, and
          counts as used, because running it is how the agent read that documentation;
      R2  a `resource` row naming something the run itself produced, or one of the inputs
          the brief handed the agent, is not an information source -- it is evidence or a
          given, not documentation that had to be found.

    `not_a_source` holds the substrings R2 matches on, declared in the node's run.sh so
    that what was excluded is visible beside the number rather than buried here.
    """
    sources: dict[str, bool] = {}
    for row in rows:
        ref = row["ref"]
        if row["kind"] == "resource":
            if normalise and any(pattern in ref for pattern in not_a_source):
                continue
            sources[ref] = sources.get(ref, False) or row["outcome"] == "used"
        elif normalise and row["kind"] == "command" and _is_help(ref):
            sources[ref] = True
    return sources


def _first_index(rows, ref):
    for i, row in enumerate(rows):
        if row["kind"] == "milestone" and row["ref"] == ref:
            return i
    return None


def summarise(rows: list[dict], normalise: bool = False,
              not_a_source: tuple[str, ...] = ()) -> list[tuple[str, object]]:
    """Statistics defined in the format specification. Order is part of the output.

    `normalise` selects between the two readings of the logs that the alternatives node
    under this one keeps side by side. The reading used is emitted as the first row, so a
    file of these statistics always says which one it is.
    """
    commands = [r for r in rows if r["kind"] == "command"]
    decisions = [r for r in rows if r["kind"] == "decision"]
    blockers = [r for r in rows if r["kind"] == "blocker"]

    sources = _information_sources(rows, normalise, not_a_source)
    used_resources = {ref for ref, used in sources.items() if used}
    failed_commands = [r for r in commands if r["outcome"] == "failed"]
    opened = [r for r in blockers if r["outcome"] == "open"]
    resolved = {r["ref"] for r in blockers if r["outcome"] == "resolved"}

    done = _first_index(rows, "evaluation_complete")
    prefix = rows if done is None else rows[: done + 1]

    span = (rows[-1]["_ts"] - rows[0]["_ts"]).total_seconds() / 60.0
    to_done = ("" if done is None
               else round((rows[done]["_ts"] - rows[0]["_ts"]).total_seconds() / 60.0, 1))

    timestamps = [r["ts_utc"] for r in rows]
    per_timestamp = {t: timestamps.count(t) for t in set(timestamps)}

    before = _information_sources(prefix, normalise, not_a_source)

    return [
        ("reading", "normalised" if normalise else "as-logged"),
        ("n_log_rows", len(rows)),
        ("reached_evaluation_complete", int(done is not None)),
        ("reached_route_abandoned", int(_first_index(rows, "route_abandoned") is not None)),
        ("n_resources_consulted", len(sources)),
        ("n_resources_used", len(used_resources)),
        ("n_resources_discarded", len(sources) - len(used_resources)),
        ("n_commands_run", len(commands)),
        ("n_commands_failed", len(failed_commands)),
        ("n_decisions_logged", len(decisions)),
        ("n_blockers_hit", len(opened)),
        ("n_blockers_unresolved", len([r for r in opened if r["ref"] not in resolved])),
        ("n_dead_ends", len(failed_commands) + len(opened)),
        ("n_resources_before_evaluation_complete", len(before)),
        ("n_commands_before_evaluation_complete",
         len([r for r in prefix if r["kind"] == "command"])),
        ("elapsed_minutes_total", round(span, 1)),
        ("elapsed_minutes_to_evaluation_complete", to_done),
        ("n_distinct_timestamps", len(per_timestamp)),
        ("max_rows_sharing_one_timestamp", max(per_timestamp.values())),
        ("milestones_reached", ";".join(
            r["ref"] for r in rows if r["kind"] == "milestone")),
    ]
