result: results/discovery_log.tsv, results/discovery_notes.md
script: none, and deliberately none. The log is written directly by the isolated discovering
        agent, row by row, as each step happens (scripts/log.sh is the one-line appender it
        used): it is the primary observation of this project, not a derivation from some
        other file.
        scripts/log.sh
        sha256:606d0af69404d1246c88ef0fa4ff75906c57ee6c1bddd62161eb07ff6c211fce
        sha256:a26966f22189a4c4b2ca9512939c077fc8a232dc1dede54fef3dcae96e9771fd  (results/discovery_log.tsv)
        sha256:dc96feef559fdd3537db201ba947381f816a2571108740f2d21d80b42b30e687  (results/discovery_notes.md)
invocation: appended to with `date -u +%Y-%m-%dT%H:%M:%SZ` at each step, per the brief in the
            plan's §4 and the format in AI-internal/skill-references/discovery-log-format.md
inputs: none -- this is an observation, not a transformation
environment: not applicable; the log is a record of a process, not an output of one
seeds: project 20260921; component none
commit: 1c032d2
instructions-commit: d2459b1
node: analysis/02_routeA_chapkit
produced: 2026-09-21
validation: the log passes the comparison node's validator: 46 rows, 28 distinct timestamps,
  at most 3 rows sharing one timestamp, spanning 66.2 minutes. Consistent with contemporaneous
  logging rather than with a log reconstructed at the end.
known-coding-differences: two rows are coded in a way route B's log does not match, and both
  inflate route A's resource count if taken at face value. Step 11 logs the three
  brief-supplied Lao data files as a consulted `resource`; route B logged the same act as a
  `decision`. Step 45 logs the agent's own `results/discovery_notes.md` as a `resource`, which
  is a self-reference and not an information source at all. Conversely route B logged
  `chap --help` and `chap eval --help` as `command` rows while route A logged the latter as a
  `resource`. These are honest differences in coding, not errors of fact, and the logs are
  **not edited** to remove them (AGENTS.md §1). They are handled downstream by the
  alternatives node under analysis/04_comparison, which computes the effort statistics both
  as logged and under a normalisation applied identically to both routes.
alternatives-considered: the agent could have been asked to log only at milestones, which
  would have been far less intrusive on the work being measured; rejected because the
  dead-end count -- the statistic that most distinguishes an easy route from a hard one -- is
  not recoverable from milestones.
agency: agent-autonomous
information: agent-retrieved
