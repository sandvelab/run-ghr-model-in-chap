# Running a model through CHAP: chapkit or MLproject — overview

**Version 1.** The single entry point to this project: what was asked, what was done, what
came out, and where to look for the detail behind any of it.

> **This version will be modified.** It covers the work through batch 7 (2026-09-21): both
> routes discovered, run, re-run from clean, and compared. Still to come, and each will
> change something here — clean-room and outsider validation (batch 8), the closing
> reproducibility report, and the human's decision on two undeclared licences. The comparative
> and per-route batch reports it draws on were written under an earlier framing in which
> run-to-run variability was treated as a caveat; that framing was withdrawn on the human's
> instruction and this document is written under the current one, in which variability is
> accepted and reported rather than held against a route.

Every number below is read from a file in the analysis tree, and each section names the file.

---

## The question

CHAP evaluates climate–health prediction models. A model can be integrated with it in two
quite different ways, and this project asks **how hard each one is to actually get running**:

- **Route A — a chapkit model service.** The model is a containerised REST service that CHAP
  talks to over HTTP. Represented here by `chap-models/chapkit_ghr_model`, a Bayesian
  spatio-temporal model built on R-INLA.
- **Route B — an `MLproject` model.** The model is a directory with an `MLproject` file
  declaring how to train and predict. Represented here by
  `dhis2-chap/minimalist_example_uv`, a deliberately minimal linear regression.

Each was taken down its route by a **separate agent that knew nothing of the other**, working
from identical instructions and public material only, until it produced a CHAP evaluation on
the same public Lao data. Each agent logged every documentation source it opened, every
command it ran and every dead end it hit, at the moment it happened.

The object of study is the **route**, not the prediction. The two models are not competitors
and their scores are never compared against each other.

## The short answer

**Both routes run. They are not, however, equally easy — and the difference is not variability.**

1. **Both produce a CHAP evaluation, repeatably.** Each route's own script was re-run end to
   end from clean and both completed: route A in 1534 s including its container build, route
   B in 92 s. Neither failed.
2. **Route B ran as published.** One README, the exact command in it, correct, worked first
   try. Zero failed commands, zero blockers, zero dead ends.
3. **Route A did not run as published.** CHAP and the model disagree about a payload schema,
   and CHAP reports that disagreement as though the service were unreachable. Route A reaches
   an evaluation only through a small proxy interposed between the two. It is a version
   incompatibility, not a tolerance and not noise.
4. **The scores wobble on route A and not on route B, and this does not matter.** Route A's
   metrics move by 1.5–7 % between identical runs because R-INLA is not bit-reproducible;
   route B's are identical to the last digit. Both are working routes.

## What was actually run

| | Pinned to |
|---|---|
| Platform | CHAP, `chap-core` **2.1.0**, installed as a `uv` tool; a 174-package freeze is archived |
| Route A model | `chap-models/chapkit_ghr_model` @ `60b16a2`, GPL-3.0 |
| Route B model | `dhis2-chap/minimalist_example_uv` @ `5cd8a12`, **no licence declared** |
| Data | `dhis2/climate-health-data`, `lao/` @ `af362d5`, **no licence declared** |

The data is an 18-unit, 156-month admin-1 panel for Laos, 1998-01 to 2010-12, 2808 rows.
Target `disease_cases` (dengue, OpenDengue); covariates rainfall, mean temperature, mean
relative humidity. 233 rows have no target value. *(`analysis/01_anchors/results/`)*

Three inconsistencies in the published data were **recorded and deliberately not repaired** —
the schema's row count is of target-present rows rather than rows, the schema names a boundary
file that was renamed upstream, and the target has gaps. How each route copes with them is part
of what was being observed.

## Does each route run?

*(`analysis/05_repeatability/results/completion.tsv`, `run_ledger.tsv`)*

| | Route A | Route B |
|---|---|---|
| Re-run from clean, completed | **yes** | **yes** |
| Seconds | 1534 (incl. container build) | 92 |
| Needs a container runtime | **yes** — R-INLA is amd64-only; 4.98 GB image, ~22 min first build | no — `uv_env` builds on the host |
| Runs as published | **no** | yes |

### What "does not run as published" means, concretely

This was reproduced first-hand rather than taken on the discovering agent's word
*(`analysis/05_repeatability/results/as_published_probe.log`, re-runnable in ten seconds via
`scripts/probe_as_published.sh`)*:

- The model service answers `GET /api/v1/info` with **HTTP 200**.
- It declares **chapkit 2.0.0 / servicekit 2.0.2**. chap-core 2.1.0's own environment holds
  **chapkit 1.1.0 / servicekit 1.0.1**.
- chapkit 1.1.0's `MLServiceInfo` is declared `extra="forbid"`, and 2.0.0 sends three fields
  it does not know: `git_revision`, `chapkit_version`, `servicekit_version`.
- Pointed straight at the service, CHAP exits 1 with
  `URL http://localhost:8000 ... could not be reached as a chapkit service`.
- With `--run-config.is-chapkit-model`, the escape hatch that error message recommends, CHAP
  exits 1 again — three `extra_forbidden` validation errors.

So the failure is a schema disagreement between two independently versioned packages, and the
error message points at the wrong thing. Route A's `run_route.sh` gets past it with
`info_shim.py`: a standard-library reverse proxy that forwards everything untouched except
those three keys. **Neither the model nor the platform was modified** — upgrading chapkit
inside chap-core would probably also work, and was rejected because it changes the platform
being studied.

There is an irony in the record: the commit this model is pinned at is the one that *added*
`git_revision` to the payload.

## How much did the variability turn out to be?

*(`analysis/05_repeatability/results/score_spread.tsv`)*

| Metric | Route A, 3 runs | Route B, 2 runs |
|---|---|---|
| MAE | 126.85 – 133.28 (**4.9 %** of mean) | identical |
| RMSE | 255.20 – 273.65 (**7.0 %**) | identical |
| MAPE | 156.56 – 168.12 (**7.2 %**) | identical |
| CRPS | 159.99 – 162.42 (**1.5 %**) | identical |
| coverage 10–90 | 0.824 – 0.836 (**1.4 %**) | — |

Route A fits with R-INLA, which its own README states is not bit-reproducible even
single-threaded. Route B fits ordinary least squares, which has nothing to vary. **This is a
property of the two models' inference methods, not of the two integration mechanisms**, and it
is reported rather than corrected for: a route whose numbers move a few per cent is a working
route. The practical consequence is only that route A's scores should not be quoted to more
than two significant figures.

## How hard was each to get running?

*(`analysis/04_comparison/results/comparison_table.tsv`)*

| | Route A | Route B |
|---|---|---|
| Information sources consulted | 9 | 5 |
| …that contributed | 8 | 4 |
| Commands run | 17 | 8 |
| Commands that failed | 2 | **0** |
| Blockers hit / left unresolved | 3 / 1 | **0 / 0** |
| **Dead ends** | **5** | **0** |
| Minutes to a written evaluation | 52.5 | 29.7 |

The ratios cluster around two, but the ratios understate it. **The difference is one of kind.**

- **Route B's answer was in the model's own README** — a literal, copy-pasteable `chap eval`
  line, stated to have been verified against chap-core 2.1.0, and accurate.
- **Route A's answer was in a docstring inside the installed Python package.** Nothing on the
  web and nothing in the model's repository carries the invocation; route A's README never
  mentions `chap eval` at all. Diagnosing *why* it failed meant reading the platform's source.

Route B's agent was following instructions. Route A's agent was debugging an integration. The
first cost is one documentation can remove; the second is one only a compatible release can.

Route A's five dead ends: the prebuilt image its README advertises is not publicly pullable
(403), forcing a local build; chapkit *directory* mode needs R and INLA on the host; `chap
model schema` has no `--run-config` override; plus the two failed commands above.

### One measurement problem, handled in the open

The two agents, given the *same* log format, coded some identical acts differently — one
logged `chap eval --help` as a documentation source, the other as a command. Rather than edit
the logs or hand-correct rows, that became an **alternatives node** in the tree
(`analysis/04_comparison/01_effort/`): one reading takes each log at face value, the other
applies two rules to both logs alike. It moves route A from 10 sources to 9 and route B from 4
to 5 — towards each other — and reverses nothing. Both readings stay runnable.

## What is true of CHAP regardless of route

Four things turned up **independently in both logs**, written by agents that never
communicated, which is what makes them findings about the platform rather than about a route:

1. **The "column X is present in the dataset but not used by the model" warning is unreliable.**
   It reports what was *declared* to CHAP, not what CHAP *delivered*. It was wrong on both
   routes. Route B's agent nearly abandoned a working setup because of it, and settled it only
   by reading the CSV CHAP actually wrote for the model.
2. **The GeoJSON has no command-line flag.** CHAP finds polygons by matching the CSV's basename
   in the same directory. Rename or move the CSV alone and you silently lose the geometry —
   documented only in an installed source docstring.
3. **`chap eval` writes a file, not an answer.** Metrics require a separate `chap
   export-metrics` step, which neither model's README mentions.
4. **One admin unit is silently dropped.** `LA-VI` has no target values at all, so both
   evaluations cover **17 of 18** units — announced in a warning inside a long log.

## What this cannot tell you

- **Each route is one model, one agent, one machine.** Route A's largest costs — an
  amd64-only image, a 4.98 GB build, a GHCR package that is not public — belong to *this
  model*, not to the chapkit mechanism. A chapkit model without a compiled statistical backend
  would not pay them.
- **What *is* attributable to the mechanism** is the version-compatibility surface: serving a
  model over REST means two independently versioned packages must agree on a payload schema.
  An `MLproject` model has no such surface. That is a structural difference, and it is the one
  that bit here.
- **Route A's specific difficulty is dated.** A chap-core shipping chapkit 2.x would remove
  most of it at a stroke. What would outlive that version pair is the *diagnosis* cost: a
  schema mismatch presenting as "could not be reached".
- **The elapsed-minute figures are contaminated.** Both discovery agents ran concurrently on
  one 8-CPU machine. Counts are the primary measure for this reason.

## Where to look next

| If you want | Go to |
|---|---|
| What the project is, its anchors, current status | `readme-at-start.md` |
| The aim, non-negotiables, batch ledger, and every judgment call with who made it | `Human-input/Plans for AI generation/26-09-21_chapModelIntegrationRoutes.md` (§4b is the decision log) |
| Each route in full — resources, process, invocation, results | `AI-generated/batch-reports/26-09-21_b05_routeReports.md` |
| The route-by-route comparison in detail | `AI-generated/batch-reports/26-09-21_b06_comparativeReport.md` |
| To click down from any claim to the raw file behind it | `AI-generated/hierarchical-report/index.html` |
| What each agent actually did, minute by minute, in its own words | `analysis/0{2,3}_route*/results/discovery_notes.md` and `discovery_log.tsv` |
| To re-run a route yourself | `analysis/0{2,3}_route*/scripts/run_route.sh` |
| The statements this project will stand behind, each bound to its file | `Human-AI-collaboration/claims/` |

## Open for the human

1. **Two anchors declare no licence** — `minimalist_example_uv` and
   `dhis2/climate-health-data`. Redistribution of the archived copies is not established.
   This blocks release, not analysis.
2. **`.claude/settings.json` still holds `<PARENT_DIR>` and `<HOME>` placeholders.** Attempts
   to substitute them were refused by the session's permission classifier. Until they are real
   paths, a parent directory's `CLAUDE.md` can reach this project's instructions, which the
   set-up guide exists to prevent.
3. **Whether route A's incompatibility is worth reporting upstream.** It is reproducible in ten
   seconds, the error message is misleading, and the documented workaround does not work.
