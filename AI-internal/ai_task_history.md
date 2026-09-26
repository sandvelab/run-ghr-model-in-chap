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
- T4 (2026-09-21): Batches 3 and 4 — two isolated agents, one per route, on identical briefs.
  Both reached a CHAP evaluation on the Lao data. Route B ran as published on the first attempt;
  route A completed only through an interposed proxy, because chap-core 2.1.0's pinned chapkit
  1.1.0 rejects the chapkit 2.0.0 service's `/api/v1/info`. Both logs validated against the
  instrument before anything was computed from them.
- T5 (2026-09-21): Batch 5 — found that the two agents coded some acts differently, and made the
  coding question an alternatives node (`a_asLogged` / `b_normalised`, the latter the main path)
  rather than editing the logs or hand-correcting rows. The normalisation moves the two routes
  towards each other and reverses nothing.
- T6 (2026-09-21): Batches 5 and 6 — wrote the two per-route reports (resources, process,
  invocation, results) and the comparative report. Route B cheaper on every ordered statistic;
  5 dead ends to 0. Four findings recur in both independent logs and are therefore about CHAP
  rather than either route.
- T7 (2026-09-21): Batch 8 (part) — built the claim collection: eight claims, each bound to its
  grounding file with a scope qualifier and the alternative reading. `claims.py audit` reports
  that every claim resolves; all invariants hold.
- T8 (2026-09-23): Batch 10, outside the plan — node `analysis/08_humanCost`, estimating what
  each route costs a *human* rather than an agent, for two personas the human named. Report at
  `AI-generated/batch-reports/26-09-23_b10_humanCost.md`. Also recorded, late, that batches 3
  and 4 ran on Claude Opus: no file here had named the model behind the discovering agents.
- T9 (2026-09-23): Published batch 10 and corrected the repository's record of its own remote.
  `origin` is `sandvelab/run-ghr-model-in-chap` — public, this project's own repository, and
  already pushed — against three statements here saying the remote was unset, or the
  starting-point template, or unpushed. Ledger row 11; §4b entry superseding the earlier
  decision rather than editing it. Release scan run on each push and made a standing
  obligation. Also wrote the missing `AI-generated/batch-reports/README.md` and corrected two
  stale folder READMEs.
- T10 (2026-09-26): Batch 12, outside the plan — iteration 3, route A only, after the chapkit
  upgrade. Re-pinned the model to `a9532c7`, archived the refreshed platform (chapkit 2.1.2, 25
  packages changed), made Docker fully cold, and ran a fresh discovering agent on the stored
  verbatim brief: evaluation reached with 0 failures, 0 blockers, 0 dead ends; 139,417 tokens.
  Re-costed with batch 10's unchanged model: 110 / 436 min against 119 / 649. Node
  `analysis/09_routeA_iteration3`; reports `26-09-26_b12_routeA.md`, `26-09-26_b12_whatChanged.md`.
  Found that batch 10's 'undocumented' GeoJSON convention is in chap-core's v2.3.1 docs.
