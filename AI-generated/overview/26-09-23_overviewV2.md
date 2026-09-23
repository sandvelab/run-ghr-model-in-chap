# Running a model through CHAP: chapkit or MLproject — overview

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 2

**Version 2.** The single entry point to this project: what was asked, what was done, what came
out, and where to look for the detail behind any of it. Supersedes [[26-09-22_overviewV1]],
which is kept unchanged as the record of what was known before batch 8b.

> **What is new in version 2.** A batch outside the original plan asked whether route A's model
> can be **configured** through CHAP, and ran several published-alternative configurations on the
> same data. The answer changed the assessment of route A materially, and has its own section
> below. Still to come: the claim collection and the three validation passes.

Every number below is read from a file in the analysis tree, and each section names the file.

---

## The question

CHAP evaluates climate–health prediction models. A model can be integrated with it in two quite
different ways, and this project asks **how hard each one is to actually get running**:

- **Route A — a chapkit model service.** The model is a containerised REST service that CHAP
  talks to over HTTP. Represented here by `chap-models/chapkit_ghr_model`, a Bayesian
  spatio-temporal model built on R-INLA.
- **Route B — an `MLproject` model.** The model is a directory with an `MLproject` file
  declaring how to train and predict. Represented here by `dhis2-chap/minimalist_example_uv`,
  a deliberately minimal linear regression.

Each was taken down its route by a **separate agent that knew nothing of the other**, working
from identical instructions and public material only, until it produced a CHAP evaluation on the
same public Lao data. Each agent logged every documentation source it opened, every command it
ran and every dead end it hit, at the moment it happened.

The object of study is the **route**, not the prediction. The two models are not competitors and
their scores are never compared against each other.

## The short answer

**Both routes run. Route A is consistently the more expensive, and — the finding of version 2 —
it cannot be configured through CHAP at all.**

1. **Both produce a CHAP evaluation, repeatably.** Re-run from clean, route A completed 4 times
   out of 4 and route B 2 out of 2. Neither has failed once.
2. **Both models ran as published.** Nothing was interposed and neither was modified.
3. **Route A costs more on every effort statistic that orders** — 5 sources to 4, 11 commands to
   9, 3 dead ends to 2, 13.0 minutes to a written evaluation against 4.8.
4. **The one difference of kind is the prerequisite.** Route A needs a container runtime, an
   image build and a container registry. Route B needs none of the three.
5. **Route A's model exposes eighteen configuration options and none of them can be set through
   CHAP.** The values are accepted, stored and silently ignored. A configured run is
   indistinguishable from an unconfigured one by its output.

## What was actually run

| | Pinned to |
|---|---|
| Platform | CHAP, `chap-core` **2.3.1**, resolving `chapkit` **2.1.0** and `servicekit` **2.0.2** |
| Route A model | `chap-models/chapkit_ghr_model` @ `60b16a2`, GPL-3.0 |
| Route B model | `dhis2-chap/minimalist_example_uv` @ `5cd8a12`, **no licence declared** |
| Data | `dhis2/climate-health-data`, `lao/` @ `af362d5`, **no licence declared** |

The data is an **18-unit, 156-month admin-1 panel for Laos, 1998-01 to 2010-12, 2808 rows**.
Target `disease_cases` (dengue, OpenDengue). 233 rows have no target value, and one unit
(`LA-VI`) has none at all, so both evaluations cover 17 of 18 units.
*(`analysis/01_anchors/results/lao_characterisation.tsv`)*

---

## Can route A's model be configured? — the new section

*(`analysis/06_configurability/`)*

The model declares **eighteen options** — spatial, seasonal and interannual random effects,
likelihood family, priors, lags, rolling windows, offsets, sample counts. `chap eval` has a
`--model-configuration-yaml` flag and `chap model schema <url> --example` writes you a filled-in
file. On the surface this is as easy as it could be.

### It does not work, and nothing tells you

Established by direct test, not by inference:

| | |
|---|---|
| **CHAP will only send nested.** | `--model-configuration-yaml` validates against chap-core's `ModelConfiguration`, which is `extra="forbid"` with exactly two fields. Values must be nested under `user_option_values`; a flat mapping is **rejected before any request is made**. |
| **The model only honours flat.** | Handed the nested payload the service returns **HTTP 201**, fills every option from its own defaults, keeps your values in an inert `user_option_values` block, and fits with the defaults. |

**So the one shape CHAP will send is the one the model discards.** The run completes, writes a
valid NetCDF and real metrics, and looks configured. Three independent confirmations: the stored
configuration read back from the service, the model formula actually fitted (`rw1`/`iid` — the
defaults — when `rw2`/`none` had been asked for), and the fact that the same values POSTed flat
are stored and honoured correctly.

**Where the fault sits is awkward.** The model's own `/api/v1/configs/$schema` *advertises* the
nested shape, so chap-core sends exactly what it is told. The service ignores the schema it
publishes. It is reportable against the model — but a platform that cannot tell you your
configuration had no effect is its own weakness.

### What it took to get a configured run

`analysis/06_configurability/scripts/lib/config_proxy.py` — a reverse proxy that rewrites the
body of `POST /api/v1/configs`, lifting `user_option_values` into `data` and forwarding
everything else untouched. **Neither the model nor CHAP is modified.**

Reaching that took reading chap-core's installed source, reading the service's stored
configuration back over HTTP, and comparing two fitted formulas. It is not something a user
would discover from documentation, because nothing anywhere reports the failure.

### Four configurations, run on the same data

One option changed at a time from the model's published defaults. The control sets those
defaults explicitly, so it travels the identical path through the proxy and controls for the
proxy as well as for the data. All CHAP defaults otherwise: 7 splits, 3 periods, 1 retrain.
*(`analysis/06_configurability/results/variants_table.tsv`)*

| Variant | Changed | MAE | RMSE | CRPS | Coverage 10–90 |
|---|---|---|---|---|---|
| `v0_published_defaults` | — (control) | 126.42 | 238.43 | 149.16 | 0.821 |
| `v1_no_spatial` | `re_spatial: none` | 166.51 | 350.25 | 111.24 | 0.819 |
| `v2_seasonal_rw2` | `re_seasonal: rw2` | 124.03 | 234.04 | 144.68 | 0.821 |
| `v3_interannual_rw1` | `re_interannual: rw1` | 134.47 | 267.79 | 163.08 | 0.830 |
| `v4_poisson` | `family: poisson` | 105.47 | 202.76 | 100.61 | **0.238** |

All five completed, and all five are confirmed to have reached the model.

### Reading that table — three things it says, and one it does not

**The measured noise floor is 2.2% on MAE and 3.4% on RMSE**, from four re-runs of the control
configuration (`analysis/05_repeatability/results/score_spread.tsv`). R-INLA is not
bit-reproducible and nothing in the route can seed it. Movement smaller than that is not
distinguishable from running the same configuration twice.

1. **`v2_seasonal_rw2` moved −1.9% MAE and −1.8% RMSE — inside the noise floor.** On this
   evidence it did nothing measurable. Reading it as an improvement would be reading noise.
2. **`v3_interannual_rw1` moved +6.4% MAE and +12.3% RMSE — outside the noise floor**, so that is
   a real degradation.
3. **`v1_no_spatial` splits the metrics in opposite directions**: MAE +31.7% and RMSE +46.9%
   (much worse) while CRPS −25.4% and MAPE −47% (much better). Which metric you look at changes
   the sign of the answer. That is worth more than any individual number here.
4. **`v4_poisson` is the trap.** Point accuracy improves substantially — MAE −16.6%, RMSE −15.0%
   — while **coverage collapses from 0.82 to 0.24**. The intervals become far too narrow, which
   is the textbook signature of forcing mean-equals-variance onto overdispersed counts. Anyone
   selecting on MAE alone would have chosen the configuration whose uncertainty is worthless.

**What this table does not say is which configuration is better.** No configuration is chosen and
none is recommended. The plan's §3 stops this project if a batch begins choosing between model
configurations on the basis of Lao scores, because nothing here is held out to catch selection.
Reporting the spread is not selecting on it. A genuine selection is a different study and needs a
sealed holdout first.

---

## Run it yourself

Each route's verified artefact is its `run_route.sh`, run end to end in a clean shell under
`env -i`. The blocks below are the essential path through those scripts; the scripts are the
tested thing and handle waiting, checking and cleanup.

### Route A — chapkit service

*(full script: `analysis/02_routeA_chapkit/scripts/run_route.sh`)*

```bash
# Needs: git, curl, a running Docker daemon.
uv tool install chap-core==2.3.1          # if you do not already have `chap`
mkdir -p chap-routeA && cd chap-routeA

# 1. The data. The GeoJSON is never named on a command line: CHAP finds it by
#    matching the CSV's stem in the same directory, so these two must sit together.
git clone --depth 1 https://github.com/dhis2/climate-health-data
mkdir -p run
cp climate-health-data/lao/chap_LAO_admin1_monthly.csv     run/
cp climate-health-data/lao/chap_LAO_admin1_monthly.geojson run/

# 2. The model. The published GHCR image is NOT anonymously pullable (401), so
#    build the Dockerfile. --platform linux/amd64 is mandatory: R-INLA ships
#    x86_64 binaries only, so an arm64 host runs this under emulation.
git clone --depth 1 https://github.com/chap-models/chapkit_ghr_model model
docker build --platform linux/amd64 \
    --build-arg GIT_REVISION="$(git -C model rev-parse HEAD)" \
    -t chapkit-ghr-model:latest model
docker run -d --platform linux/amd64 -p 8000:8000 --name ghr chapkit-ghr-model:latest
until curl -fsS http://localhost:8000/health >/dev/null 2>&1; do sleep 3; done

# 3. The evaluation. CHAP takes the service URL where a model name would go.
cd run
chap eval http://localhost:8000 chap_LAO_admin1_monthly.csv evaluation.nc \
    --run-config.is-chapkit-model --plot

# `chap eval` writes a file, not an answer. --input-files is variadic, so both
# paths must be named flags; positional arguments fail.
chap export-metrics --input-files evaluation.nc --output-file metrics.csv
docker rm -f ghr
```

Roughly **6 minutes** for the evaluation on an arm64 host under emulation, plus the image build.

> **Do not expect `--model-configuration-yaml` to work here.** It is accepted and has no effect.
> See the configurability section above.

### Route B — `MLproject` directory

*(full script: `analysis/03_routeB_mlproject/scripts/run_route.sh`)*

```bash
# Needs: git, curl. Everything else installs itself. No container, ever.
curl -LsSf https://astral.sh/uv/install.sh | sh     # if you do not already have uv
export PATH="$HOME/.local/bin:$PATH"
uv tool install chap-core==2.3.1
mkdir -p chap-routeB && cd chap-routeB

git clone --depth 1 https://github.com/dhis2/climate-health-data
mkdir -p run
cp climate-health-data/lao/chap_LAO_admin1_monthly.csv     run/
cp climate-health-data/lao/chap_LAO_admin1_monthly.geojson run/

# Nothing is built: the MLproject declares `uv_env: pyproject.toml`, so CHAP
# runs train/predict through uv on the host.
git clone https://github.com/dhis2-chap/minimalist_example_uv
cd minimalist_example_uv
chap eval --model-name . \
    --dataset-csv ../run/chap_LAO_admin1_monthly.csv \
    --output-file ../run/eval.nc --plot
chap export-metrics --input-files ../run/eval.nc --output-file ../run/metrics.csv
```

About **50 seconds** end to end.

> **Do not run `chap sanity-check-model --model-url .` without `--dataset-path`.** On a clean
> chap-core 2.3.1 it dies with `FileNotFoundError: …/example_data/hydromet_5_filtered.csv` — it
> defaults to a bundled dataset the wheel does not ship.

---

## What the evaluations look like

`chap eval --plot` draws a **backtest grid**: observed cases as a line, the forecast as 10–90 and
25–75 quantile bands, one panel per admin unit per split. The plot is **off by default**. The
rasters below show the first two units across the first three splits; the linked HTML is the
complete figure.

### Route A — `chapkit_ghr_model`

![Route A: backtest forecasts against observations](../../analysis/02_routeA_chapkit/results/eval/evaluation_plot.png)

- **Full figure**: [`evaluation.html`](../../analysis/02_routeA_chapkit/results/eval/evaluation.html)
- [`metrics.csv`](../../analysis/02_routeA_chapkit/results/eval/metrics.csv) · `evaluation.nc` · `evaluation_plot.tsv` (9520 plotted rows)

### Route B — `minimalist_example_uv`

![Route B: backtest forecasts against observations](../../analysis/03_routeB_mlproject/results/eval/evaluation_plot.png)

- **Full figure**: [`eval.html`](../../analysis/03_routeB_mlproject/results/eval/eval.html)
- [`metrics.csv`](../../analysis/03_routeB_mlproject/results/eval/metrics.csv) · `eval.nc` · `evaluation_plot.tsv` (9520 plotted rows)

**The visible difference between the two figures is a property of the models, not of the
routes.** Route A's forecast is a band; route B's is a bare mark, because that model emits a
single deterministic sample — `q_10` through `q_90` are the same number in all 9520 rows. That is
also why its CRPS equals its MAE to the last digit and both its coverage figures are zero.

### What each route's evaluation reported

| Metric | Route A | Route B |
|---|---|---|
| MAE | 126.07 | 171.96 |
| RMSE | 242.77 | 358.93 |
| CRPS | 150.25 | 171.96 |
| Coverage 10–90 | 0.82 | 0.00 |

**These two columns are reported per route and are not compared.** They are two different models
fitted by different methods; the plan's §2 forbids a cross-route performance claim.

---

## Does each route run again, from clean?

*(`analysis/05_repeatability/results/`)*

| | Route A | Route B |
|---|---|---|
| Runs found, all completing | **4 of 4** | **2 of 2** |
| Bit-reproducible | no | **yes** |
| Widest spread across runs | 3.4 % (RMSE) | 0.00 % |

Route A's scores move 0.45–3.4% between identical invocations, because R-INLA is not
bit-reproducible and nothing in the route sets a seed. Route B's do not move at all. **This is a
property of the two models' inference methods, not of the two integration mechanisms**, and it is
reported rather than corrected for.

## How hard was each to get running?

*(`analysis/04_comparison/results/comparison_table.tsv`)*

| | Route A | Route B |
|---|---|---|
| Information sources consulted | 5 | 4 |
| Commands run / that failed | 11 / 1 | 9 / 1 |
| Blockers hit / left unresolved | 2 / **1** | 1 / 0 |
| **Dead ends** | **3** | **2** |
| Minutes to a written evaluation | 13.0 | 4.8 |
| Needs a container runtime / build / registry | yes / yes / yes | **no / no / no** |

**Route A's largest single cost belongs to its model rather than to its route.** The image is
amd64-only because R-INLA ships x86_64 binaries, so on an arm64 host it runs under emulation
throughout — the one blocker hit and never resolved.

**What *is* attributable to the mechanism** is the surface area: serving a model over HTTP means
an image has to be built, shipped and run, and it means two independently versioned components
must agree on a payload schema. Version 2 shows that surface failing in a second place — the
configuration payload — where an `MLproject` model has no equivalent.

### One measurement problem, handled in the open

Taken at face value, route A has zero failed commands and route B has one, which is backwards:
route A's agent marked two commands `ok` before reading their output. Rather than edit a log,
that became an **alternatives node** (`analysis/04_comparison/01_effort/`). `a_asLogged` takes
each log at face value; `b_normalised` is the main path and applies two rules to both logs alike.
Both readings order the routes identically. Everything the rules touched is written to
`what_the_rules_changed.md`; the logs are never edited.

## What is true of CHAP regardless of route

Three things turned up **independently in both logs**, written by agents that never communicated:

1. **The GeoJSON has no command-line flag.** CHAP matches the CSV's stem in the same directory.
   Both agents established it by reading installed source. Rename or move the CSV alone and the
   geometry is silently lost.
2. **`chap eval` writes a file, not an answer.** Metrics need `chap export-metrics`; the default
   figure needs `--plot`. Neither README mentions either.
3. **One admin unit is silently dropped** — announced in a warning inside a long log.

Plus two defects found since: `chap sanity-check-model` crashes on a clean install, and a model
configuration can be accepted and silently discarded.

## What this cannot tell you

- **Each route is one model, one agent, one machine.**
- **The build-time figures are not cold-build figures.** The host's Docker layer cache was warm
  throughout, so the expensive path was never exercised. A cold measurement needs
  `docker builder prune -a` first.
- **The variant table does not license a choice of configuration**, for the reasons in that
  section. It shows that configuration matters and that metrics disagree about how.
- **One branch of each recipe went unverified** — route A's cold build, route B's `uv`
  self-install.

## Where to look next

| If you want | Go to |
|---|---|
| What the project is, its anchors, current status | `readme-at-start.md` |
| The aim, non-negotiables, ledger, every judgment call with who made it | `Human-input/Plans for AI generation/26-09-21_chapModelIntegrationRoutes.md` (§4b) |
| How the two agents were kept independent | `AI-generated/batch-reports/26-09-22_b03b04_routesDiscovered.md` |
| Each route in full | `AI-generated/batch-reports/26-09-22_b05_routeReports.md` |
| The route-by-route comparison | `AI-generated/batch-reports/26-09-22_b06_comparativeReport.md` |
| The configurability finding and the variant sweep | `analysis/06_configurability/claim.md` |
| What each agent did, minute by minute, in its own words | `analysis/0{2,3}_route*/results/discovery_notes.md` |
| To re-run a route yourself | `analysis/0{2,3}_route*/scripts/run_route.sh` |
| To reproduce everything | `analysis/run.sh` — about 40 minutes with the variant sweep |

## Open for the human

1. **Two anchors declare no licence** — `minimalist_example_uv` and `dhis2/climate-health-data`.
   Redistribution of the archived copies is not established. Blocks release, not analysis.
2. **`origin` points at the starting-point template repository**,
   `sandvelab/agentic-model-development-start`, with this branch ahead of it. Nothing pushed.
3. **`.claude/settings.json` still holds `<PARENT_DIR>` and `<HOME>` placeholders.**
4. **Three findings look worth reporting upstream**: the silently discarded model configuration
   (the most serious), `chap sanity-check-model`'s missing bundled dataset, and `export-metrics`
   failing on positional arguments.
