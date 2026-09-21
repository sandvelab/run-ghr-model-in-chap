#!/usr/bin/env python3
"""Tests for the discovery-log instrument.

Run by this node's run.sh before anything is summarised, because every number in the
comparative report is produced by the code these tests exercise. A silently wrong count here
would be indistinguishable from a real difference between the two routes.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import discovery_log as dl  # noqa: E402

HEADER = "\t".join(dl.COLUMNS)

GOOD = [
    "1\t2026-09-21T09:00:00Z\tmilestone\tfirst_doc_opened\tok\tstart",
    "2\t2026-09-21T09:00:30Z\tresource\thttps://a/readme\tused\tnames the entry point",
    "3\t2026-09-21T09:05:00Z\tresource\thttps://b/docs\tdiscarded\twrong major version",
    "4\t2026-09-21T09:06:00Z\tcommand\tgit clone https://a\tok\t",
    "5\t2026-09-21T09:06:10Z\tmilestone\tmodel_obtained\tok\t",
    "6\t2026-09-21T09:08:00Z\tblocker\tdocker daemon\topen\tnot running",
    "7\t2026-09-21T09:12:00Z\tblocker\tdocker daemon\tresolved\tstarted by the human",
    "8\t2026-09-21T09:20:00Z\tcommand\tchap evaluate --bad-flag\tfailed\tunknown option",
    "9\t2026-09-21T09:25:00Z\tdecision\tuse the compose file\tused\tthe README's path",
    "10\t2026-09-21T09:30:00Z\tcommand\tchap evaluate --ok\tok\t",
    "11\t2026-09-21T09:30:00Z\tmilestone\tevaluation_complete\tok\twrote results.csv",
    "12\t2026-09-21T09:40:00Z\tresource\thttps://c/after\tdiscarded\tread after the fact",
]


def write(lines):
    fh = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8")
    fh.write("\n".join([HEADER] + lines) + "\n")
    fh.close()
    return fh.name


def expect_error(lines, fragment):
    try:
        dl.load(write(lines))
    except dl.LogError as exc:
        assert fragment in str(exc), f"expected {fragment!r} in {exc}"
        return
    raise AssertionError(f"expected a LogError mentioning {fragment!r}")


def main():
    rows = dl.load(write(GOOD))
    got = dict(dl.summarise(rows))

    # Counts are over distinct resources, so the three resource rows are three resources,
    # one of which contributed. The row logged after evaluation_complete is excluded from
    # the "before" counts: what a route cost is what it cost to get there.
    assert got["n_log_rows"] == 12
    assert got["reached_evaluation_complete"] == 1
    assert got["reached_route_abandoned"] == 0
    assert got["n_resources_consulted"] == 3
    assert got["n_resources_used"] == 1
    assert got["n_resources_discarded"] == 2
    assert got["n_resources_before_evaluation_complete"] == 2
    assert got["n_commands_run"] == 3
    assert got["n_commands_failed"] == 1
    assert got["n_commands_before_evaluation_complete"] == 3
    assert got["n_decisions_logged"] == 1
    assert got["n_blockers_hit"] == 1
    assert got["n_blockers_unresolved"] == 0
    assert got["n_dead_ends"] == 2
    assert got["elapsed_minutes_total"] == 40.0
    assert got["elapsed_minutes_to_evaluation_complete"] == 30.0
    assert got["milestones_reached"] == (
        "first_doc_opened;model_obtained;evaluation_complete")

    # The integrity statistics: steps 10 and 11 share a timestamp, nothing else does.
    assert got["n_distinct_timestamps"] == 11
    assert got["max_rows_sharing_one_timestamp"] == 2

    # A log written in one sitting at the end is the failure these two statistics exist to
    # expose: one timestamp carrying every row.
    same = [line.split("\t") for line in GOOD]
    for parts in same:
        parts[1] = "2026-09-21T09:00:00Z"
    flat = dl.summarise(dl.load(write(["\t".join(p) for p in same])))
    flat = dict(flat)
    assert flat["n_distinct_timestamps"] == 1
    assert flat["max_rows_sharing_one_timestamp"] == 12
    assert flat["elapsed_minutes_total"] == 0.0

    # An unfinished route reports its span and leaves the to-completion field empty rather
    # than substituting a number that would read as a completion time.
    unfinished = GOOD[:8]
    part = dict(dl.summarise(dl.load(write(unfinished))))
    assert part["reached_evaluation_complete"] == 0
    assert part["elapsed_minutes_to_evaluation_complete"] == ""
    assert part["n_commands_before_evaluation_complete"] == 2

    expect_error(["1\t2026-09-21T09:00:00Z\tresource\thttps://a\tok\tx"],
                 "outcome 'ok' is not allowed")
    expect_error(["1\t2026-09-21T09:00:00Z\tmilestone\tgot_it_working\tok\tx"],
                 "not in the closed")
    expect_error(["1\t2026-09-21T09:00:00Z\treading\thttps://a\tused\tx"],
                 "kind 'reading'")
    expect_error(["2\t2026-09-21T09:00:00Z\tcommand\tls\tok\tx"],
                 "steps start at 1")
    expect_error(["1\t2026-09-21T09:05:00Z\tcommand\tls\tok\tx",
                  "2\t2026-09-21T09:00:00Z\tcommand\tls\tok\tx"],
                 "goes backwards")
    expect_error(["1\t21/09/2026 09:00\tcommand\tls\tok\tx"], "is not YYYY")
    expect_error(["1\t2026-09-21T09:00:00Z\tcommand\t\tok\tx"], "ref is empty")

    print("discovery-log instrument: all checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
