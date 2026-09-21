result: results/completion.tsv, results/score_spread.tsv
script: scripts/collect_runs.py
        sha256:37924c556752457aaf2adb6590f90a8579db00ae620681d9e798134ec43a2638
invocation: "$PYTHON" scripts/collect_runs.py  (called by run.sh)
inputs: results/run_ledger.tsv  sha256:80429ae7f19c73ed6fd005e278186b60176f5a97644db7b1bdf92e4090f567e9
        every file under results/history/, listed in provenance/repeat_runs.md
environment: environment/ (project main; stdlib-only Python 3.13.0)
seeds: project 20260921; component none -- the computation is deterministic
commit: ea3a485
instructions-commit: d2459b1
node: analysis/05_repeatability
produced: 2026-09-21
alternatives-considered: the spread could have been reported as a standard deviation or a
  coefficient of variation rather than as a range and a percentage of the mean; the range was
  chosen because with two and three runs a standard deviation would give a spurious air of
  distributional knowledge. Reporting the spread as a percentage is undefined where the mean
  is zero, which happens for route B's two coverage metrics, and that is printed as
  "undefined (mean is 0)" rather than as a zero, which would read as stability. A judgment on
  whether a given spread is acceptable is deliberately not computed: under the plan as amended
  the spread is a property to report, not a threshold to pass.
agency: agent-autonomous
information: agent-retrieved
