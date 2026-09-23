# Running a model through CHAP: chapkit or MLproject

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 2

**Version 3 — executive.** Supersedes [[26-09-23_overviewV2]] and [[26-09-22_overviewV1]], which
are kept unchanged. Detail lives in the appendix at the foot; every number here is read from a
named file.

> Version 3 sharpens one thing earlier versions got wrong. `MLproject` models **are**
> configurable — `user_options` is a first-class field of the template and is how a
> ConfiguredModel is made from a ModelTemplate. The surface `MLproject` lacks is the *negotiated
> REST payload*, not configuration itself.

---

## Bottom line

**Both routes run. Route A costs about twice as much to get running, and it is the only one
where a documented feature is silently broken.**

| | Route A — chapkit | Route B — MLproject |
|---|---|---|
| Reached a CHAP evaluation | yes | yes |
| Runs again from clean | 4 of 4 | 2 of 2 |
| Sources read / commands run / dead ends | 5 / 11 / **3** | 4 / 9 / **2** |
| Minutes to a written evaluation | 13.0 | 4.8 |
| Container runtime · image build · registry | **yes · yes · yes** | no · no · no |
| Model exposes configurable options | **18** | 0 |
| Can those options be set through `chap eval`? | **no — accepted and silently ignored** | n/a (declares none) |

## How you run each — in full

**Route A.** Needs git, curl, a running Docker daemon. About 6 min plus the image build.

```bash
uv tool install chap-core==2.3.1
mkdir -p chap-routeA && cd chap-routeA
git clone --depth 1 https://github.com/dhis2/climate-health-data
mkdir -p run && cp climate-health-data/lao/chap_LAO_admin1_monthly.{csv,geojson} run/

# The published GHCR image is NOT anonymously pullable (401), so build the Dockerfile.
# --platform linux/amd64 is mandatory: R-INLA ships x86_64 binaries only.
git clone --depth 1 https://github.com/chap-models/chapkit_ghr_model model
docker build --platform linux/amd64 \
    --build-arg GIT_REVISION="$(git -C model rev-parse HEAD)" \
    -t chapkit-ghr-model:latest model
docker run -d --platform linux/amd64 -p 8000:8000 --name ghr chapkit-ghr-model:latest
until curl -fsS http://localhost:8000/health >/dev/null 2>&1; do sleep 3; done

cd run
chap eval http://localhost:8000 chap_LAO_admin1_monthly.csv evaluation.nc \
    --run-config.is-chapkit-model --plot
chap export-metrics --input-files evaluation.nc --output-file metrics.csv
docker rm -f ghr
```

**Route B.** Needs git and curl. Everything else installs itself. About 50 seconds.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv tool install chap-core==2.3.1
mkdir -p chap-routeB && cd chap-routeB
git clone --depth 1 https://github.com/dhis2/climate-health-data
mkdir -p run && cp climate-health-data/lao/chap_LAO_admin1_monthly.{csv,geojson} run/

git clone https://github.com/dhis2-chap/minimalist_example_uv
cd minimalist_example_uv
chap eval --model-name . \
    --dataset-csv ../run/chap_LAO_admin1_monthly.csv \
    --output-file ../run/eval.nc --plot
chap export-metrics --input-files ../run/eval.nc --output-file ../run/metrics.csv
```

Three traps, both routes: the **GeoJSON is never named on a command line** (CHAP matches the
CSV's stem in the same directory); **`chap eval` writes a file, not an answer** (`--plot` is off
by default, metrics need `export-metrics`); and **`--input-files` is variadic**, so positional
arguments to `export-metrics` fail silently-ish.

## Configuration: how easy is it to find out about?

This is where the two mechanisms genuinely differ, and the difference is not what the effort
counts suggest.

**MLproject — one file, one writer, one reader.** A template declares `user_options` in its
`MLproject` file, which sits in the model repository and can be read without running anything.
The operator passes `--model-configuration-yaml`; chap-core writes the whole configuration to
`model_configuration_for_run.yaml` in the run directory, beside the data; the model's own
train/predict script reads it. Nothing is negotiated, because there is no second party. The
file appears in every run directory — route B's run wrote one containing `prediction_length: 3`
even though that model declares no options at all — so an operator can always see exactly what
the model was handed.

**chapkit — two conventions that do not meet.** A chapkit model advertises a JSON schema at
`/api/v1/configs/$schema`, which you can only read by building and starting the container.
chap-core reads it and POSTs a configuration **nested** under `user_option_values`. The service
stores a **flat** mapping. Handed the nested one it returns **HTTP 201**, fills every option
from its defaults, keeps your values in an inert block, and fits with the defaults. The one
shape CHAP will send is the one the model discards, and **nothing reports it**: the run
completes, writes a valid NetCDF, exports real metrics and draws a real plot.

**GHRmodel specifically — the model is not the problem.** `chapkit_ghr_model` is the
best-documented artefact in this study. Its README carries a full table of all **18** options
with the R-INLA latent models explained, the nested-parameter encoding spelled out, and
citations; the repository ships `example_data/config.yml` whose own comment says it is *"in the
flat layout chapkit's ShellModelRunner writes"*. So the model documents its configuration
thoroughly and implements chapkit's **file** convention correctly. What is undiscoverable is
that chap-core's **REST** bridge does not deliver it. Neither document is wrong; they describe
different transports, and only one of them is what `chap eval` uses.

**Finding this out took**: reading chap-core's installed source, validating both candidate
shapes off-line against `ModelConfiguration`, reading the stored configuration back over HTTP,
and diffing two fitted formulas. None of it is in any documentation, because nothing anywhere
reports the failure.

**The structural point.** Route A depends on **8 distinct chapkit endpoints, called 198 times
in one evaluation**. Agreement is validated at `/api/v1/info` — a mismatch there fails loudly —
and not at `/api/v1/configs`, where it fails silently. The same boundary therefore has two
failure modes, and the quiet one is the dangerous one. An `MLproject` model has no negotiated
payload at all.

## What came out

**Each route's evaluation**, 17 of 18 units (CHAP drops `LA-VI`, which has no target), CHAP
defaults throughout. **Reported per route and never compared** — two different models, different
methods; the plan's §2 forbids a cross-route performance claim.

| | Route A | Route B |
|---|---|---|
| MAE · RMSE · CRPS | 126.07 · 242.77 · 150.25 | 171.96 · 358.93 · 171.96 |
| Coverage 10–90 | 0.82 | **0.00** |
| Spread across re-runs | 0.45–3.4 % | 0 % (bit-identical) |

Route B's zero coverage is the model, not the route: it emits a single deterministic sample, so
`q_10` through `q_90` are the same number in all 9520 plotted rows — which is why its CRPS
equals its MAE exactly, and why its forecast renders as a mark where route A's is a band.

![Route A: CHAP's default backtest plot, observed against forecast bands](../../analysis/02_routeA_chapkit/results/eval/evaluation_plot.png)

**Configuration changes the answer far more than noise does.** Five runs through an interposed
proxy, one option changed at a time from the published defaults, against a measured noise floor
of 2.2 % MAE / 3.4 % RMSE:

| Variant | MAE (vs control) | Coverage 10–90 |
|---|---|---|
| published defaults | 126.42 | 0.821 |
| `re_spatial: none` | 166.51 (+31.7 %) | 0.819 |
| `re_seasonal: rw2` | 124.03 (−1.9 %, **inside noise**) | 0.821 |
| `re_interannual: rw1` | 134.47 (+6.4 %) | 0.830 |
| `family: poisson` | 105.47 (**−16.6 %**) | **0.238** |

Two readings matter more than the ranking. Dropping the spatial term moves MAE and CRPS in
**opposite directions**, so which metric you consult flips the sign of the answer. And
`poisson` has the best MAE, RMSE and CRPS of all five while its coverage collapses to 0.24 —
selecting on point accuracy would pick the model whose uncertainty is worthless.

**No configuration is chosen or recommended.** The plan's §3 stops this project if a batch
selects between configurations on Lao scores, with nothing held out to catch it.

## Open for the human

1. **Two anchors declare no licence** — `minimalist_example_uv` and `dhis2/climate-health-data`.
   Blocks release, not analysis.
2. **`origin` points at the starting-point template repository**, branch ahead of it, nothing
   pushed.
3. **`.claude/settings.json` still holds `<PARENT_DIR>` and `<HOME>` placeholders.**
4. **Three defects look worth reporting upstream** — the silently discarded model configuration
   (most serious), `chap sanity-check-model` crashing on a clean install, and `export-metrics`
   failing on positional arguments.

---

## Appendix — where the detail is

| For | Go to |
|---|---|
| Configuration, the variant sweep, and the CHAP/chapkit boundary in full | `AI-generated/batch-reports/26-09-23_b08b_configurability.md` |
| Each route in full — resources, process, invocation, results | `AI-generated/batch-reports/26-09-22_b05_routeReports.md` |
| The route-by-route comparison | `AI-generated/batch-reports/26-09-22_b06_comparativeReport.md` |
| How the two discovering agents were kept independent | `AI-generated/batch-reports/26-09-22_b03b04_routesDiscovered.md` |
| The anchors and the Lao dataset | `AI-generated/batch-reports/26-09-22_b01_anchors.md` |
| What each agent did, minute by minute, in its own words | `analysis/0{2,3}_route*/results/discovery_notes.md` |
| The raw effort logs and both readings of them | `analysis/04_comparison/01_effort/` |
| Variant results, fitted formulas, contract surface | `analysis/06_configurability/results/` |
| Repeatability across every run | `analysis/05_repeatability/results/` |
| The aim, non-negotiables, ledger, every judgment call with its agency | `Human-input/Plans for AI generation/26-09-21_chapModelIntegrationRoutes.md` (§4b) |
| To re-run a route yourself | `analysis/0{2,3}_route*/scripts/run_route.sh` |
| To reproduce everything | `analysis/run.sh` — about 40 minutes |
