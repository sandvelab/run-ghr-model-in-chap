#!/usr/bin/env python3
"""Tests for the measuring instrument.

Run: environment/env/bin/python analysis/04_comparison/scripts/test_discovery_log.py

The instrument is what the project's primary measure is defined over, so a defect in it is a
defect in every number the reports carry. These tests exist because the plan's §3 requires
contemporaneous logging and a rule with no detector is a rule that will be honoured until it
is not.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import discovery_log as dl


HEADER = "\t".join(dl.COLUMNS)


def log(*rows: str) -> list[dict[str, str]]:
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, newline="") as fh:
        fh.write(HEADER + "\n")
        for r in rows:
            fh.write(r + "\n")
        path = fh.name
    return dl.read_log(path)


def row(step, ts, kind, ref, outcome, note=""):
    return "\t".join([str(step), ts, kind, ref, outcome, note])


T = "2026-09-22T1{}:00:00Z"


class Format(unittest.TestCase):
    def test_a_conforming_log_validates(self):
        rows = log(
            row(1, T.format(0), "milestone", "first_doc_opened", "ok"),
            row(2, T.format(1), "resource", "https://example.org/readme", "used"),
            row(3, T.format(2), "command", "chap eval --help", "ok"),
        )
        self.assertEqual(dl.validate(rows), [])

    def test_wrong_header_is_refused_at_read(self):
        with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False) as fh:
            fh.write("step\tts\tkind\n1\tx\ty\n")
            path = fh.name
        with self.assertRaises(ValueError):
            dl.read_log(path)

    def test_steps_must_increase_by_one(self):
        rows = log(
            row(1, T.format(0), "milestone", "first_doc_opened", "ok"),
            row(3, T.format(1), "command", "ls", "ok"),
        )
        self.assertTrue(any("strictly increasing" in e for e in dl.validate(rows)))

    def test_timestamps_must_not_go_backwards(self):
        rows = log(
            row(1, T.format(2), "milestone", "first_doc_opened", "ok"),
            row(2, T.format(0), "command", "ls", "ok"),
        )
        self.assertTrue(any("backwards" in e for e in dl.validate(rows)))

    def test_outcome_must_be_legal_for_its_kind(self):
        rows = log(row(1, T.format(0), "command", "ls", "used"))
        self.assertTrue(any("may not take outcome" in e for e in dl.validate(rows)))

    def test_milestone_vocabulary_is_closed(self):
        rows = log(row(1, T.format(0), "milestone", "nearly_there", "ok"))
        self.assertTrue(any("closed vocabulary" in e for e in dl.validate(rows)))

    def test_empty_log_is_an_error_not_a_zero(self):
        self.assertEqual(dl.validate([]), ["log is empty"])


class Statistics(unittest.TestCase):
    def rows(self):
        return log(
            row(1, T.format(0), "milestone", "first_doc_opened", "ok"),
            row(2, T.format(0), "resource", "https://a.example/readme", "used"),
            row(3, T.format(1), "resource", "https://b.example/docs", "discarded"),
            row(4, T.format(1), "command", "git clone https://a.example/m", "ok"),
            row(5, T.format(1), "milestone", "model_obtained", "ok"),
            row(6, T.format(2), "command", "chap eval --wrong-flag", "failed"),
            row(7, T.format(2), "blocker", "docker daemon not running", "open"),
            row(8, T.format(3), "blocker", "docker daemon not running", "resolved"),
            row(9, T.format(3), "blocker", "registry needs credentials", "open"),
            row(10, T.format(4), "decision", "build locally instead of pulling", "used"),
            row(11, T.format(4), "milestone", "evaluation_started", "ok"),
            row(12, T.format(5), "milestone", "evaluation_complete", "ok"),
            row(13, T.format(6), "command", "chap export-metrics", "ok"),
        )

    def test_counts(self):
        s = dl.summarise(self.rows())
        self.assertEqual(s["reached_evaluation"], "yes")
        self.assertEqual(s["n_resources"], 2)
        self.assertEqual(s["n_resources_used"], 1)
        self.assertEqual(s["n_resources_discarded"], 1)
        self.assertEqual(s["n_commands"], 3)
        self.assertEqual(s["n_commands_failed"], 1)
        self.assertEqual(s["n_decisions_taken"], 1)

    def test_a_blocker_hit_and_resolved_is_one_blocker(self):
        s = dl.summarise(self.rows())
        self.assertEqual(s["n_blockers_hit"], 2)
        self.assertEqual(s["n_blockers_unresolved"], 1)

    def test_dead_ends_are_failed_commands_plus_distinct_blockers(self):
        s = dl.summarise(self.rows())
        self.assertEqual(s["n_dead_ends"], 1 + 2)

    def test_before_evaluation_windows_exclude_later_rows(self):
        s = dl.summarise(self.rows())
        # the export-metrics command at step 13 is after evaluation_complete
        self.assertEqual(s["n_commands"], 3)
        self.assertEqual(s["n_commands_before_evaluation"], 2)

    def test_elapsed_is_measured_to_the_milestone_not_to_the_end(self):
        s = dl.summarise(self.rows())
        self.assertEqual(s["elapsed_minutes_total"], 360.0)
        self.assertEqual(s["elapsed_minutes_to_evaluation"], 300.0)

    def test_an_abandoned_route_reports_no_evaluation_and_blank_windows(self):
        rows = log(
            row(1, T.format(0), "milestone", "first_doc_opened", "ok"),
            row(2, T.format(1), "command", "chap eval", "failed"),
            row(3, T.format(2), "milestone", "route_abandoned", "ok", "no way in"),
        )
        s = dl.summarise(rows)
        self.assertEqual(s["reached_evaluation"], "no")
        self.assertEqual(s["elapsed_minutes_to_evaluation"], "")
        self.assertEqual(s["n_commands_before_evaluation"], "")
        self.assertEqual(s["n_dead_ends"], 1)


class Integrity(unittest.TestCase):
    """Plan §3: a log reconstructed at the end has a visible signature."""

    def test_a_contemporaneous_log_spreads_over_many_timestamps(self):
        rows = log(*[
            row(i, f"2026-09-22T1{i % 10}:0{i % 6}:00Z", "command", f"cmd{i}", "ok")
            for i in range(1, 7)
        ])
        s = dl.summarise(rows)
        self.assertEqual(s["n_distinct_timestamps"], 6)
        self.assertEqual(s["max_rows_sharing_one_timestamp"], 1)

    def test_a_log_written_in_one_sitting_is_visible_in_the_statistics(self):
        rows = log(*[
            row(i, T.format(0), "command", f"cmd{i}", "ok") for i in range(1, 7)
        ])
        s = dl.summarise(rows)
        self.assertEqual(s["n_distinct_timestamps"], 1)
        self.assertEqual(s["max_rows_sharing_one_timestamp"], 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
