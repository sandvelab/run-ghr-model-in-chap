result: results/discovery_log.tsv, results/discovery_notes.md
script: none, and deliberately none. The log is written directly by the isolated
        discovering agent, row by row, as each step happens: it is the primary observation
        of this project, not a derivation from some other file. Its digests, and the digests
        of the statistics computed from it, are below.
        sha256:1a7c67c99c43c0908d5e4dbb7e7d58bdaf4b0cc94d197d0282a0565b0543eb10  (results/discovery_log.tsv)
        sha256:1f70ffe680ae5b76ca30f0b6fb19dfc36ba6301818214253cfdd4d710a47f934  (results/discovery_notes.md)
invocation: appended to with `date -u +%Y-%m-%dT%H:%M:%SZ` at each step, per the brief in the
            plan's §4 and the format in AI-internal/skill-references/discovery-log-format.md
inputs: none -- this is an observation, not a transformation
environment: not applicable; the log is a record of a process, not an output of one
seeds: project 20260921; component none
commit: 8c3d6d5
instructions-commit: d2459b1
node: analysis/03_routeB_mlproject
produced: 2026-09-21
computed-from-this: the effort statistics land in the comparison node, written by
  its `summarise_discovery.py` over `discovery_log.py`; they are that node's result and carry
  that node's record, because one implementation must measure both routes.
validation: the log passes the comparison node's validator: 24 rows, 11 distinct
  timestamps, at most 5 rows sharing one timestamp, spanning 58.2 minutes. The clumping at
  12:05:57 covers the evaluation launch and completion, which happened inside a single ~57
  second command, so it is consistent with contemporaneous logging rather than with a log
  reconstructed at the end.
alternatives-considered: the agent could have been asked to log only at milestones, which
  would have been cheaper and far less intrusive on the work being measured; rejected because
  the dead-end count -- the statistic that most distinguishes an easy route from a hard one --
  is not recoverable from milestones. The agent records in its own notes that it logged the
  chap.dhis2.org evaluation-workflow page as a resource before having actually read it, and
  corrected this by reading it afterwards (step 23); the correction is left in the log rather
  than tidied out of it.
agency: agent-autonomous
information: agent-retrieved
