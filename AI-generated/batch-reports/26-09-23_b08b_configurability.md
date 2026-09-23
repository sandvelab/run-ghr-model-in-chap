# Batch 8b — configuring route A's model: can it be done, and what changes when it is

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 2

Outside the original plan, at the human's request. Four questions: can a model option be set
through CHAP at all, how hard is it, what do several configurations produce on the Lao data,
and what the answer says about the boundary between CHAP and a chapkit service.

Every number here is read from a file under `analysis/06_configurability/results/`.

---

## 1. Can it be done? No — not through CHAP

Route A's model declares **eighteen** options: the spatial, seasonal and interannual random
effects, the likelihood family, penalised-complexity priors, per-covariate lags and rolling
windows, the offset and its scale, posterior sample count, threads. `chap eval` has a
`--model-configuration-yaml` flag, and `chap model schema <url> --example` writes a
ready-to-edit file with every default filled in. Everything on the surface says this is easy.

It does not work. The two ends require incompatible shapes, and **neither reports it**:

| End | Requires | Evidence |
|---|---|---|
| **chap-core** | values **nested** under `user_option_values` | `ModelConfiguration` is `extra="forbid"` with exactly two fields. A flat mapping raises `ValidationError` before any request is made — both shapes were validated directly against the class. |
| **the model's service** | a **flat** mapping | Handed the nested payload it returns **HTTP 201**, fills every option from its own defaults, keeps the operator's values in an inert `user_option_values` block, and fits with the defaults. |

So **the one shape CHAP will send is the one the model discards.**

### The failure mode is the worst available one

A discarded configuration produces a run that **completes successfully**, writes a valid
NetCDF, exports real metrics and draws a real plot. There is no error, no warning, and no
field anywhere in the output that differs from a correctly configured run. Confirmed three
ways:

1. **The stored configuration, read back over HTTP**: every option at its default, with the
   operator's values parked in a nested block beside them.
2. **The model formula actually fitted**: `f(seasonal_id, model = 'rw1')` and
   `f(year_id, model = 'iid')` — the defaults — when `rw2` and `none` had been asked for.
3. **The same values POSTed flat** are stored and honoured correctly.

### Where the fault sits

Awkwardly for a straightforward bug report: **the model advertises a schema it does not
consume.** Its own `/api/v1/configs/$schema` declares `user_option_values` as a nested object
with `additionalProperties: false`. chap-core reads that schema and sends exactly what it
describes. The service then ignores its own advertised shape and honours a flat one instead.

The defect is reportable against the model. That CHAP cannot tell an operator their
configuration had no effect is a separate and smaller weakness — but it is the reason the
first one goes unnoticed.

## 2. How hard was it? Not discoverable from documentation

Getting from "the flag exists" to "the flag does nothing" required:

- reading chap-core's installed source to find `ModelConfiguration` and `_chapkit_config_payload`;
- validating both candidate shapes directly against the chap-core class, off-line, to establish
  that flat is refused before any network call;
- reading the service's stored configuration back over HTTP and comparing it to what was sent;
- running the model twice and diffing the fitted formulas.

**None of this is in any documentation**, because nothing anywhere reports the failure. A user
following the documented path gets a plausible answer and no reason to doubt it.

Getting a *configured* run then required interposing
`scripts/lib/config_proxy.py` — a reverse proxy that rewrites the body of `POST /api/v1/configs`,
lifting `user_option_values` into `data` and forwarding everything else untouched. **Neither
the model nor the platform is modified.** Without it there is no configured run to report.

## 3. What changes when configuration does reach the model

Five runs, one option changed at a time from the published defaults. The control sets those
defaults explicitly, so it travels the identical path through the proxy and controls for the
proxy as well as for the data. All CHAP defaults otherwise — 7 splits, 3 periods, 1 retrain.
*(`results/variants_table.tsv`)*

| Variant | Changed | MAE | vs control | RMSE | CRPS | MAPE | Coverage 10–90 |
|---|---|---|---|---|---|---|---|
| `v0_published_defaults` | — | 126.42 | — | 238.43 | 149.16 | 148.70 | 0.821 |
| `v1_no_spatial` | `re_spatial: none` | 166.51 | +31.7% | 350.25 | 111.24 | 78.85 | 0.819 |
| `v2_seasonal_rw2` | `re_seasonal: rw2` | 124.03 | −1.9% | 234.04 | 144.68 | 145.57 | 0.821 |
| `v3_interannual_rw1` | `re_interannual: rw1` | 134.47 | +6.4% | 267.79 | 163.08 | 171.49 | 0.830 |
| `v4_poisson` | `family: poisson` | 105.47 | −16.6% | 202.76 | 100.61 | 160.26 | **0.238** |

**All five are confirmed to have reached the model.** The service stored each value flat with
no nested remainder; and for the three variants re-run to capture it, the fitted formula agrees
— `v1_no_spatial` drops the spatial term entirely where the others fit `bym2`
*(`results/variants_formulas.tsv`)*. The formula evidence is kept in its own column, from a
two-split re-run whose scores are deliberately reported nowhere, so it can never be mistaken
for a seven-split result.

### Reading the table against the noise

Route A's measured run-to-run spread, from four re-runs of the control, is **2.2% on MAE and
3.4% on RMSE** (`analysis/05_repeatability/results/score_spread.tsv`). R-INLA is not
bit-reproducible and nothing in the route can seed it. **Movement smaller than that is not
distinguishable from running the same configuration twice.**

1. **`v2_seasonal_rw2` moved −1.9% MAE and −1.8% RMSE — inside the noise floor.** On this
   evidence it did nothing measurable. A reader who saw only the ranking would call it the
   second-best configuration; it is indistinguishable from the control.
2. **`v3_interannual_rw1` moved +6.4% MAE and +12.3% RMSE — outside it**, so that is a real
   degradation. Treating each year as independent beats carrying a trend forward, here.
3. **`v1_no_spatial` moves the metrics in opposite directions.** MAE +31.7% and RMSE +46.9%
   (much worse) against CRPS −25.4% and MAPE −47% (much better). **Which metric you consult
   changes the sign of the answer.** Dropping the spatial term makes the point predictions worse
   and the distributional and relative scores better.
4. **`v4_poisson` is the trap.** It has the best MAE, RMSE and CRPS of all five — and its
   coverage collapses from 0.82 to **0.24**. Forcing mean-equals-variance onto overdispersed
   counts narrows the predictive intervals until they stop covering. Anyone selecting on point
   accuracy would have chosen the configuration whose uncertainty is worthless.

### What this table does not say

**No configuration is chosen and none is recommended.** The plan's §3 stops this project if a
batch begins choosing between model configurations on the basis of Lao scores, because nothing
here is held out to catch selection. Reporting a spread is not selecting on it, and the noise
floor is printed beside the table precisely so a reader can see which differences are real
without any of them being picked. A genuine selection is a different study and needs a sealed
holdout first.

## 4. CHAP against chapkit: where the boundary is, and why it is the route's cost

Route A works only if chap-core and the model's chapkit service agree on the payload of **eight
distinct endpoints**, exercised 198 times in a single evaluation
*(`results/chapkit_contract_surface.tsv`)*:

| Endpoint | Calls | What has to agree |
|---|---|---|
| `GET /api/v1/jobs/{id}` | 166 | asynchronous job status, polled until a job finishes |
| `GET /api/v1/info` | 9 | service identity and version fields; chap-core **validates** this payload |
| `POST /api/v1/ml/$predict` | 7 | the prediction request, per forecast window |
| `GET /api/v1/artifacts/{id}` | 7 | the trained artefact handed between train and predict |
| `GET /api/v1/configs/$schema` | 6 | the schema the service advertises for its configuration |
| `POST /api/v1/configs` | 1 | **the configuration payload — where the two ends disagree** |
| `GET /api/v1/configs` | 1 | as above, read back |
| `POST /api/v1/ml/$train` | 1 | the training request and the dataset encoding |

**This is the structural difference between the two routes, stated concretely.** An `MLproject`
model has no such surface at all: CHAP invokes `train` and `predict` as commands and passes data
as files. There is no schema for two independently versioned packages to disagree about, because
there is only one package.

Three properties of the boundary are worth separating:

- **It is versioned on both sides and independently.** chap-core and chapkit are separate
  releases on separate schedules. A pairing that works is a fact about that pairing, not about
  the mechanism, which is why this project pins the resolved `chapkit` and `servicekit`
  versions alongside `chap-core` rather than `chap-core` alone.
- **Agreement is checked in some places and not others.** `/api/v1/info` is validated by
  chap-core, so a mismatch there fails loudly. `/api/v1/configs` is not, so a mismatch there
  fails silently. The same boundary therefore has two completely different failure modes, and
  the quiet one is the dangerous one.
- **The schema is advertised, which makes disagreement look impossible.** Both ends have a
  machine-readable contract available to them at `/api/v1/configs/$schema`, and they still
  disagree, because the service does not validate itself against what it publishes. A published
  schema is a promise, not a guarantee.

**None of this makes chapkit the wrong mechanism.** Serving a model over REST buys things an
`MLproject` cannot — language independence, a deployed model that many clients can share, a
process boundary around a fragile statistical runtime. The honest statement is that it buys
them at the cost of a compatibility surface, and that this project has now seen that surface
fail quietly at one of its eight endpoints.

## State

- Batch 8b **done**. `/validate invariants`: all eight checks pass.
- One defect of the batch's own, recorded rather than quietly fixed: the first sweep's formula
  capture wrote empty files, because macOS `grep` caps interval repetition at 255 and the
  pattern said `{0,400}`. Every variant was reported as unconfigured until it was noticed, and
  the containers had been removed by then, so the evidence went with them. The scripts now keep
  the raw container log, and the collector states which evidence each verdict rests on rather
  than asserting one.
- `analysis/run.sh` now costs about 40 minutes, because the sweep is in the tree rather than
  beside it.
