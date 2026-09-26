# Provenance — batch reports

One section per file. Append; never overwrite an existing section. Sections exist only for
reports whose producing session wrote them; the earlier reports have none, and none has been
reconstructed (`AI-internal/ai_task_details.md`, T9).

## 26-09-26_b12_routeA.md

- **What it is**: the route A report for iteration 3 — resources, process, invocation,
  evaluation — and its human cost for batch 10's two personas.
- **Generated from**: `analysis/09_routeA_iteration3/` at commit `5225531` —
  `01_discovery/results/{discovery_log.tsv,discovery_notes.md,agent_usage.tsv,manual_run/,route_run/}`,
  `02_humanCost/results/{summary.tsv,walkthrough_*_route-a-it3.tsv,prereq_exposure.tsv,machine_waits.tsv,doc_sizes.tsv}`,
  `03_versusIteration2/results/effort_normalised.tsv`. Hand-written by the orchestrating agent
  (Claude Opus 5.5) from those files; every number was read from them.
- **Produced**: 2026-09-26. **Agency**: `agent-autonomous`, at the human's request.

## 26-09-26_b12_whatChanged.md

- **What it is**: the brief report the human asked for on what differs between iteration 2's
  and iteration 3's route A — success, agent time and tokens, estimated human time.
- **Generated from**: `analysis/09_routeA_iteration3/03_versusIteration2/results/comparison.tsv`
  at commit `5225531`, and `02_humanCost/results/machine_waits.tsv` for the pull bound.
- **Produced**: 2026-09-26. **Agency**: `agent-autonomous`, at the human's request.
