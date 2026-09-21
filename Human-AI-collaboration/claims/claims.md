# Claim collection

Everything the analysis supports, each statement bound to the result grounding it. The
manuscript is written from this file; nothing enters the manuscript that is not here.

Format — one block per claim, appended by `/claims add`:

```
## C1
The statement, in one or two sentences.
grounds: analysis/02_measure/a_jaccard/results/summary.tsv
node: analysis/02_measure/a_jaccard
scope: holds for the strict filtering convention only
alternatives: the base-pair measure gives a weaker effect (see C9)
by: agent-autonomous
```

`by:` is the agency field — `human-set`, `agent-on-human-assessment` or `agent-autonomous`.
Claims about **stability** are claims like any other and belong here too: what the
perturbation set showed, and which choices the conclusion turned out to be sensitive to.

No claims yet — the tree has not produced a result.

## C1
Route B, the MLproject/uv mechanism, cost less than route A, the chapkit service mechanism, on every effort statistic that orders: 9 versus 5 information sources, 17 versus 8 commands, 13 versus 6 commands before completion, and 52.5 versus 29.7 minutes to a written evaluation.
grounds: analysis/04_comparison/results/comparison_table.tsv
node: analysis/04_comparison
scope: one model and one agent run per route, CHAP 2.1.0, Lao admin-1 monthly data, 2026-09-21, both agents running concurrently on one 8-CPU host
alternatives: taking each log exactly as its agent coded it instead of normalising (analysis/04_comparison/01_effort/a_asLogged/results/effort_by_route.tsv); it moves route A from 9 sources to 10 and route B from 5 to 4 and changes nothing else
by: agent-autonomous

## C2
Route A hit 5 dead ends and 3 blockers, one of which was never resolved; route B hit none of either.
grounds: analysis/04_comparison/results/comparison_table.tsv
node: analysis/04_comparison
scope: as above
alternatives: the as-logged reading, which gives the same counts: the normalisation touches only resource statistics, which the instrument's tests assert
by: agent-autonomous

## C3
Route A did not complete as published: chap-core 2.1.0 pins chapkit 1.1.0, whose MLServiceInfo forbids extra fields, while the model is built on chapkit 2.0.0, whose /api/v1/info carries three more; the route reached an evaluation only through an interposed proxy that strips those three keys from that one response.
grounds: analysis/02_routeA_chapkit/results/discovery_log.tsv
node: analysis/02_routeA_chapkit
scope: chap-core 2.1.0 against chapkit_ghr_model at 60b16a2; a chap-core shipping chapkit 2.x would likely not show it
alternatives: upgrading chapkit inside chap-core's own environment, which would probably also have worked and was rejected because it changes the platform under test
by: agent-autonomous

## C4
CHAP's 'column X is present in the dataset but not used by the model' warning reports what was declared to CHAP, not what CHAP delivered to the model, and was wrong on both routes.
grounds: analysis/03_routeB_mlproject/results/chap_run_artifacts/training_data.csv · analysis/02_routeA_chapkit/results/service.log
node: analysis/04_comparison
scope: CHAP 2.1.0; established independently on both routes
alternatives: trusting the warning, which route B's agent initially did and which would have produced a wrong conclusion about the platform
by: agent-autonomous

## C5
CHAP discovers a dataset's polygons by looking for a GeoJSON with the same basename beside the CSV; there is no command-line flag for geometry, and the rule is stated only in the docstring of the installed chap_core/cli_endpoints/evaluate.py.
grounds: analysis/02_routeA_chapkit/results/discovery_log.tsv · analysis/03_routeB_mlproject/results/discovery_log.tsv
node: analysis/04_comparison
scope: CHAP 2.1.0; found independently by both agents
alternatives: none -- both logs record it and route A's records where it is documented
by: agent-autonomous

## C6
Both CHAP evaluations cover 17 of the 18 Lao admin-1 units: CHAP silently drops LA-VI, which has no target values over the whole training period, announcing it in a warning inside a long log.
grounds: analysis/01_anchors/results/lao_characterisation.tsv · analysis/03_routeB_mlproject/results/eval.nc
node: analysis/04_comparison
scope: the Lao data at commit af362d5 with chap eval's default backtest
alternatives: none
by: agent-autonomous

## C7
Route A's evaluation is not reproducible to better than about 2-4 per cent: two identical invocations gave MAE 130.00 and 133.28, because R-INLA is not bit-reproducible even single-threaded.
grounds: analysis/02_routeA_chapkit/results/eval_metrics.csv · analysis/02_routeA_chapkit/results/eval_metrics_firstrun.csv
node: analysis/02_routeA_chapkit
scope: chapkit_ghr_model at 60b16a2 on this host; the model's own README states the non-determinism
alternatives: quoting a single run, which would overstate precision
by: agent-autonomous

## C8
Neither the model repository dhis2-chap/minimalist_example_uv nor the data repository dhis2/climate-health-data declares a licence, so redistribution of the archived copies is not established.
grounds: analysis/01_anchors/results/anchor_discrepancies.tsv
node: analysis/01_anchors
scope: as of the pinned commits, 2026-09-21
alternatives: none -- this is a question for the human, not a finding to be resolved in the tree
by: agent-autonomous
