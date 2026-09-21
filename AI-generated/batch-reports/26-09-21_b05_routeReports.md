# Batch 5 — The two route reports

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 3

Each route was discovered and run by an agent that knew nothing of the other, on briefs
identical except for the repository URL and the node path. Every count below is read from
`analysis/04_comparison/01_effort/b_normalised/results/effort_by_route.tsv`; every score is
read from the CSV CHAP wrote. The narrative sections draw on each route's own
`results/discovery_notes.md`, written as the work happened.

---

# Route A — `chapkit_ghr_model`, a chapkit model service

Node: `analysis/02_routeA_chapkit`. Model pinned at `60b16a2`, GPL-3.0.

## a) What resources were used

Nine information sources, of which eight contributed. In the order they mattered:

| Source | What it gave |
|---|---|
| `chap eval --help` | That `MODEL-NAME` accepts a "chapkit service URL", and that `--run-config.is-chapkit-model` exists |
| **`chap_core/cli_endpoints/evaluate.py`, the installed package's docstring** | The only place the whole recipe appears — *and* the only statement anywhere that the GeoJSON is auto-discovered as the sibling `<stem>.geojson` |
| The model's `README.md` at the pinned commit | The chapkit service on port 8000, `make run`, amd64-only because of R-INLA, the configuration fields, and a warning about geometry name matching |
| The model's `Makefile` and `Dockerfile` | `--platform linux/amd64`, the port, and the GHCR image reference |
| The model's `main.py` | That the service's own config defaults are `rainfall` + `mean_temperature` — which the Lao data has |
| `chap_core/models/utils.py`, `external_chapkit_model.py`, `chapkit_service_manager.py`, `geometry.py` | The **root cause** of the failure, and that URL mode is the only viable path |
| `chap --help` | The command list |
| `chap model schema` / `sanity-check-model --help` | Consulted and discarded — introspection helpers, not on the eval path |

The single most load-bearing source is **not documentation at all**: it is a docstring inside
the installed Python package. Nothing on the web, and nothing in the model's own repository,
carries the working invocation. The model's README never mentions `chap eval`; it stops at
"ready to plug into chap-core" and documents `make run`.

## b) How the finding-out went

Seventeen commands, two of which failed; three blockers, one never resolved; **five dead
ends**; 52.5 minutes to a written evaluation.

The shape of it was: read the CLI help, clone at the pinned commit, read the model's README
and Dockerfile, then try to obtain the service. The first attempt was to pull the prebuilt
image the README and a repository badge advertise — `docker pull
ghcr.io/chap-models/chapkit_ghr_model:latest` — which returns `unauthorized`, and an
anonymous GHCR token request returns 403. The package is not public. That forced a local
build: 22 minutes and 4.98 GB, under qemu emulation, because R-INLA ships x86-64 Linux
binaries only and the host is an Apple M3.

Then the real obstacle. With the service healthy and `GET /api/v1/info` visibly returning
`200 OK`, CHAP said:

> `ValueError: URL http://localhost:8000 was provided but could not be reached as a chapkit service. Ensure the server is running and exposes /api/v1/info, or use --run-config.is-chapkit-model to skip auto-detection.`

Both halves of that sentence are wrong, and the remedy it offers does not work. Finding out
why took reading the platform's own source: `_is_chapkit_url()` validates the response with
`MLServiceInfo` imported from the chapkit package pinned *inside chap-core's own virtual
environment* — **chapkit 1.1.0**, which declares `extra="forbid"`. The model is built on
**chapkit 2.0.0**, whose `/api/v1/info` carries three additional fields. Every probe
therefore fails validation, and the exception is swallowed and re-reported as
unreachability. `--run-config.is-chapkit-model` only skips the probe; the same
`ValidationError` then surfaces from `CHAPKitRestAPIWrapper.info()`.

There is an irony worth recording: the pinned commit is the one that *added* `git_revision`
to the payload, and `git_revision` is one of the three fields that make the validation fail.

Two other paths were tried and abandoned: chapkit *directory* mode, which runs `uv run
fastapi dev` on the host and so needs R and INLA there; and `chap model schema` as an entry
point, which has no `--run-config` override and therefore cannot reach this model at all.

## c) How to actually run it

**The route does not complete as published.** What made it complete is `scripts/info_shim.py`
— a standard-library reverse proxy that forwards everything verbatim and strips exactly the
three chapkit-2.0-only keys from the body of `GET /api/v1/info`. Neither the model nor the
platform was modified; upgrading chapkit inside chap-core's environment would have worked and
was rejected, because it changes the platform under test and the incompatibility is the
finding.

```bash
docker build --platform linux/amd64 \
  --build-arg GIT_REVISION=60b16a2e929405ce95fae2043a63d7e27292ca0f \
  -t chapkit-ghr-model:60b16a2 <model checkout>
docker run -d --platform linux/amd64 -p 8000:8000 \
  --name chapkit-ghr-model-route-a chapkit-ghr-model:60b16a2
python3 scripts/info_shim.py 8010 http://localhost:8000 &      # the interposition

chap eval --model-name http://localhost:8010 --run-config.is-chapkit-model \
  --dataset-csv <copy of the Lao CSV, with its .geojson beside it under the same stem> \
  --output-file results/eval_lao_ghrmodel.nc \
  --backtest-params.n-splits 7 --backtest-params.n-periods 3 --backtest-params.stride 1 --plot
chap export-metrics --input-files results/eval_lao_ghrmodel.nc --output-file results/eval_metrics.csv
```

No `--model-configuration-yaml`: an empty configuration makes the service apply its own
published schema defaults, which is the model exactly as published. The whole sequence,
including the build, is `analysis/02_routeA_chapkit/scripts/run_route.sh`, which was verified
by running it end to end — the files in `results/` are that run's.

Timings on this host: build ~22 min; cold start to `/health` ~40 s; one INLA fit with 1000
draws ~70–110 s; the full 7-split evaluation ~11 min, which was faster than the README's
emulation warnings suggested.

## d) What came out

From `results/eval_metrics.csv`, with `results/eval_metrics_firstrun.csv` beside it — the
**same invocation run an hour earlier**:

| | run 1 | run 2 |
|---|---|---|
| MAE | 130.00 | 133.28 |
| CRPS | 159.99 | 162.42 |
| RMSE | 262.17 | 273.65 |
| coverage 10–90 | 0.824 | 0.836 |

The 2–4 % spread is R-INLA's own non-determinism, which the model's README states plainly, so
nothing here should be quoted to more than two significant figures. Both runs are kept for
that reason. The fitted model really did use the geometry — `service.log` records
`f(spatial_id, model='bym2', graph=g, …)` — and the default backtest puts all seven splits
inside 2010, over 17 of the 18 admin units, `LA-VI` having been dropped by CHAP for having no
target values at all.

CHAP also warns that `rainfall` and `mean_temperature` are "not used by the model". They are.
`warn_unused_covariates()` compares against the empty configuration CHAP sent and cannot see
the service-side defaults; the warning is correct only for `mean_relative_humidity`.

---

# Route B — `minimalist_example_uv`, an MLproject model run with `uv`

Node: `analysis/03_routeB_mlproject`. Model pinned at `5cd8a12`. **No licence is declared
upstream**, which blocks redistribution of the archived copy.

## a) What resources were used

Five information sources, of which four contributed:

| Source | What it gave |
|---|---|
| `chap eval --help` | The full signature and every backtest parameter |
| The model's `README.md` at the pinned commit | **A literal, copy-pasteable `chap eval` line**, and a statement that it was verified against chap-core 1.4.0 and 2.1.0 |
| The model's `MLproject` | `uv_env: pyproject.toml` plus train and predict entry points — this *is* the registration |
| `chap --help` | The command list |
| `chap.dhis2.org/.../evaluation-workflow/` | Consulted and discarded — it confirms `export-metrics` and lists plot types, but added nothing the CLI help had not given |

The model's own README was accurate and sufficient. That is the whole story of this route's
discovery cost.

## b) How the finding-out went

Eight commands, **none of which failed**; no blockers; **no dead ends**; 29.7 minutes to a
written evaluation, most of it dependency installation.

CLI help first, on the reasoning that the installed 2.1.0 binary is more authoritative about
its own flags than any web page — which proved right for both routes. Then the model at the
pinned commit, then its README and `MLproject`, then a 50-second standalone run of the model
outside CHAP to separate "the model is broken" from "the integration is broken", then
`chap validate`, then `chap eval`. It worked on the first attempt.

One thing genuinely misled: `chap validate` and `chap eval` both warn that `rainfall`,
`mean_temperature`, `mean_relative_humidity` and `population` are "present in the dataset but
not used by the model". Since `train.py` indexes `df[["rainfall","mean_temperature"]]` and
would fail loudly without them, this looked like a blocker and was logged as one. It is not.
**The warning is about declaration, not delivery**: this MLproject declares no covariates, so
CHAP's static check concludes nothing is used — but CHAP writes the entire dataset into the
train and predict CSVs regardless. That was settled not by reasoning but by reading the file
CHAP actually handed the model, kept at `results/chap_run_artifacts/training_data.csv`. The
warnings cannot be used to check whether a model will receive the data it needs.

## c) How to actually run it

Two commands, and **no registration step** — CHAP reads a local directory's `MLproject`
directly at eval time, and `uv_env: pyproject.toml` is what tells it to build the model's
environment with `uv` on the host:

```bash
chap eval --model-name model/minimalist_example_uv \
  --dataset-csv <copy of the Lao CSV, with its .geojson beside it under the same stem> \
  --output-file results/eval.nc --plot
chap export-metrics --input-files results/eval.nc --output-file results/eval_metrics.csv
```

Docker was running and **was not needed**: a container matters only for a `docker_env` model.
The whole sequence is `analysis/03_routeB_mlproject/scripts/run_route.sh`, verified end to
end; it reproduced `eval_metrics.csv` byte-identically, the pipeline having no seed to set.

Four things not in the documentation, all found by running it:

1. **The GeoJSON has no CLI flag.** CHAP finds polygons by looking for a `.geojson` with the
   same basename beside the CSV. Rename the CSV and you silently lose the geometry.
2. **`chap eval` prints no metrics at all** — it writes a NetCDF and stops. `chap
   export-metrics` is a separate step the model's README never mentions.
3. **One admin unit was silently dropped.** `Rejected regions: ['LA-VI'] due to missing target
   values for the whole training period`, so the evaluation covers 17 of 18 units — a WARNING
   in a long log.
4. **Each invocation leaves ~197 MB of virtualenv at a doubled path**,
   `runs/<model>/<ts>/runs/<model>/<ts>/.venv`, because CHAP computes it relative to the run
   directory it is already inside. Four invocations left 401 MB.

## d) What came out

From `results/eval_metrics.csv`: MAE 172.77, RMSE 357.52, CRPS 172.77, MAPE 423.60, coverage
10–90 and 25–75 both 0.0, over 336 samples.

Three things must be read with those numbers. **CRPS equals MAE exactly**, and coverage is
zero, because the model emits a single deterministic sample — the CRPS of a point mass is the
absolute error, and there is no interval to cover; comparing this against a probabilistic
model on CRPS or coverage compares different kinds of object. **The model predicts negative
case counts** (26 of 459 forecast cells, minimum −35.4), which is what makes the `*_log1p`
metrics NaN. And observed cases average about 153 while forecasts span −35 to 92, so an MAE of
172.8 means essentially no skill — which is the intended behaviour of a demonstration model
whose own README says it is "not meant to accurately capture any interesting relations", not
a finding about CHAP.

---

## What this batch did not settle

Whether either route's cost is typical of its mechanism, or particular to this model, this
platform version and this machine. One run per route cannot separate those. Phase D runs a
replicate of each.
