# Provenance — the discovery record

result: results/discovery_log.tsv
        sha256:c04c44c96cce3d2c3b1c95b00367793285e25ec85e6fbb466bbde9b853a3c5df
        results/discovery_notes.md
        sha256:59fc8df4b747d3631ef42f0ee2d39b57372b38ea2b943a96703bbf00cd7d04b8
script: none of this project's — the log is written step by step by the discovering agent
  through `AI-internal/useful-scripts/log_step.py`, which stamps each row with the current UTC
  second and refuses a row the format does not allow
        sha256:951d9f5c54e4e51b6b1172612f5074dc1070f5209cb987c84a64903298362fbe
invocation: one invocation of log_step.py per row, at the moment of the step; the narrative
  written alongside by the same agent
inputs: the public internet and the platform installed on this machine; the brief in the
  plan's §4
environment: none of this project's — the route supplies its own, which is part of what is
  being measured. CHAP is the pinned platform anchor (`chap-core` 2.3.1, `chapkit` 2.1.0,
  `servicekit` 2.0.2); the model runs in a container it builds from its own Dockerfile.
seeds: project 20260921; no component seed reaches this route. The model fits with R-INLA,
  which its own README states is not bit-reproducible, and CHAP offers no seed for a chapkit
  service. Recorded as an absence rather than left unstated.
commit: d37fdcd
instructions-commit: d2459b1
node: analysis/02_routeA_chapkit
produced: 2026-09-22
alternatives-considered: correcting the two rows (12 and 28) that were marked `ok` for
  commands whose output turned out to show a failure. Rejected, and the discovering agent
  logged the rejection itself at step 42: both rows were written before the command's output
  was read, which is what logging at the moment of the step costs, and later rows (13, 30, 32)
  carry the correction. Editing the log would make the instrument unfalsifiable — the one
  thing a contemporaneous log has over a reconstructed one is that it shows what was believed
  when. The consequence is that the as-logged `n_commands_failed` reads 0 where the route in
  fact had two commands fail, and that discrepancy is carried into the comparison node as a
  reading of the log rather than repaired here.
  It was also considered to have the agent write the log itself in whatever shape it liked;
  rejected because the statistics are defined over fixed columns and two shapes are not one
  measurement.
contamination: the discovering agent was a fresh agent given the plan's §4 brief and nothing
  else. It was told explicitly which three paths in this repository it could read and that
  `CLAUDE.md`'s instruction to read `readme-at-start.md` was overridden, because that file
  names both models and would have told it the answer. It reports one incidental exposure of
  its own: `docker images` listed an unrelated chapkit model image belonging to the human's
  other work, which it did not inspect or use. The **orchestrating** agent is separately and
  fully contaminated — it holds a previous iteration's findings for both routes — and its
  contribution here was the brief and the storage of what came back, not the route.
agency: `human-set` (that each route is discovered by a separate isolated agent on an
  identical brief); `agent-autonomous` (every judgment call inside the route, each logged as a
  `decision` row with its basis)
information: `agent-retrieved` — every resource in the log was found by the discovering agent
  itself; `human-pointed` only for the model repository URL and the three data files
