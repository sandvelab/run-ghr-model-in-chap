# Provenance — the discovery record

result: results/discovery_log.tsv
        sha256:5e1a21e95001cd77e2c37abfafeba6e1eabc5906a6f18d4d3df990bef4c35c77
        results/discovery_notes.md
        sha256:96da4dab27eea91e906fe9788f0608d2fe88202180352d7b6c89a22dad5297f7
        results/model_commit.txt
        sha256:6028787857532a70ef25a1986fbb31f9c4b5b63c31aae025ce58c9fcb6843b76
script: none of this project's — the log is written step by step by the discovering agent
  through `AI-internal/useful-scripts/log_step.py`, the same implementation route A used
        sha256:951d9f5c54e4e51b6b1172612f5074dc1070f5209cb987c84a64903298362fbe
invocation: one invocation of log_step.py per row, at the moment of the step; the narrative
  written alongside by the same agent
inputs: the public internet and the platform installed on this machine; the brief in the
  plan's §4, identical to route A's but for the model URL and the node path
environment: none of this project's — the route supplies its own, which is part of what is
  being measured. CHAP is the pinned platform anchor (`chap-core` 2.3.1).
seeds: project 20260921; no component seed reaches this route. The model fits ordinary least
  squares and emits one deterministic sample, so there is nothing to seed; recorded as an
  absence rather than left unstated.
commit: fa3d04d
instructions-commit: d2459b1
node: analysis/03_routeB_mlproject
produced: 2026-09-22
alternatives-considered: 33 rows across 18 distinct timestamps, at most 3 sharing one, and the
  file grew by append only — checked against the version committed while the agent was still
  running, which added 14 lines and removed none. Nothing in it was rewritten, and the same
  refusal to rewrite applies here as on route A. One row (step 33) corrects an earlier row's
  factual claim rather than its outcome; the normalised reading deliberately leaves such a
  correction alone, because correcting a fact is not a failure.
contamination: the discovering agent was a fresh agent given the plan's §4 brief and nothing
  else, with the same closed list of three readable paths and the same explicit override of
  `CLAUDE.md`'s instruction to read `readme-at-start.md`. It reports no incidental exposure of
  its own. The **orchestrating** agent is separately and fully contaminated — it holds a
  previous iteration's findings for both routes — and its contribution here was the brief and
  the storage of what came back, not the route.
agency: `human-set` (that each route is discovered by a separate isolated agent on an
  identical brief); `agent-autonomous` (every judgment call inside the route)
information: `agent-retrieved` — every resource in the log was found by the agent itself;
  `human-pointed` only for the model repository URL and the three data files
