# Task history

One line per completed task. Written by `/log-tasks`; expanded entries in
`ai_task_details.md`.

This log is **part of the published record** of how the work came about. Write entries a
reader who was not present can follow, and keep them honest about what did not work.

- T1 (2026-09-21): Defined the project — CHAP's two model-integration routes compared on how
  discoverable and executable each is — set the repository up from `setup-guide.md`, wrote the
  plan and archived it as delivered, and created the four-node tree. Four framing decisions are
  the human's: the research object is route usability rather than predictive performance; each
  route is discovered by an isolated agent; Docker is started by the human; and the
  sealed-holdout rule is deviated from with its voiding condition recorded.
- T2 (2026-09-21): Batch 1 — pinned and archived the three anchors (CHAP 2.1.0 with a
  174-package freeze; both model repositories at named commits; the Lao data with
  `sha256sums.txt`), and wrote `analysis/01_anchors`, which re-verifies the digests,
  characterises the panel, and records four discrepancies without repairing any of them. Two
  anchors turned out to declare no licence, which blocks release but not analysis.
- T3 (2026-09-21): Batch 2 — fixed the discovery-log format and its code in
  `analysis/04_comparison` *before* either route ran, with tests over every statistic and over
  seven kinds of malformed log, plus two integrity statistics that detect a log reconstructed
  at the end. Narrowed the batch's stated aim: confirming the data loads into CHAP was dropped
  because doing it would have contaminated the orchestrator with route knowledge.
- T4 (2026-09-21): Batches 3 and 4 — launched two isolated agents, one per route, on identical
  briefs differing only in repository URL and node path. In progress at the time of writing.
