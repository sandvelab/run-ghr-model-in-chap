# Discovery notes — running chapkit_ghr_model through CHAP (route A)

Written as I went. Timestamps of the individual steps are in `discovery_log.tsv`.

## What I was starting from

`chap` 2.1.0 on the host (a uv tool install), Docker Desktop 27.4.0, an Apple M3
(arm64) host, and the model repo pinned at `60b16a2e929405ce95fae2043a63d7e27292ca0f`.

## How I found the invocation

`chap --help` lists `eval` as "Evaluate a model using backtesting and export results to
NetCDF format". `chap eval --help` was already enough to see the shape of the answer:

- `MODEL-NAME` takes "Model path (local directory), GitHub URL, **or chapkit service URL**".
- there is a `--run-config.is-chapkit-model` flag, "Set to True when the model is served
  via chapkit (REST) rather than an MLproject directory".

The exact recipe is in the docstring of `chap_core/cli_endpoints/evaluate.py` (installed
at `~/.local/share/uv/tools/chap-core/lib/python3.13/site-packages/chap_core/`):

```
chap eval --model-name http://localhost:8000 --run-config.is-chapkit-model \
    --dataset-csv ./data/vietnam.csv --output-file ./results/eval.nc
```

That same docstring is where I learned that **the GeoJSON is not a CLI argument**: it is
auto-discovered from "files with the same name as the CSV but with .geojson extension"
(`discover_geojson()`). That is worth knowing — nothing in `chap eval --help` mentions
geometry at all, and this model's spatial random effect needs it.

## The things that were not in any documentation

1. **The published image is not pullable.** The README says
   `docker compose -f compose.ghcr.yml up` runs the prebuilt image from GHCR "(once
   published)". The badge in the README points at the package page, but
   `docker pull ghcr.io/chap-models/chapkit_ghr_model:latest` returns `unauthorized`, and
   an anonymous GHCR token request for that repository returns 403. So the package is not
   public. I had to build the image locally from the pinned checkout. That is the single
   biggest cost of this route: the base image `ghcr.io/dhis2-chap/chapkit-r-inla` alone is
   ~1.4 GB compressed, and the build then installs two CRAN packages and compiles GHRmodel
   from BSC's GitLab.
2. **arm64.** The README is honest about this ("amd64 only", R-INLA ships x86_64 Linux
   binaries only), but it is easy to miss how much it costs: everything below runs under
   qemu emulation on this host.
3. **`chap eval` has no way to pass geometry explicitly** — see above.

(Sections below were filled in as the run progressed.)

## The real blocker: chap-core 2.1.0 cannot talk to a chapkit 2.0.0 service

This is the finding of the exercise, and it is a platform/model version mismatch, not
anything wrong with the model.

`chap model schema http://localhost:8000 --example` failed with

```
ValueError: URL http://localhost:8000 was provided but could not be reached as a
chapkit service. Ensure the server is running and exposes /api/v1/info, or use
--run-config.is-chapkit-model to skip auto-detection.
```

even though `GET /api/v1/info` was returning `200 OK` two log lines earlier. The error
message is actively misleading: the service *was* reachable and *did* expose
`/api/v1/info`.

`chap_core/models/utils.py::_is_chapkit_url()` probes the URL and then does
`MLServiceInfo.model_validate(response.json())`, swallowing every exception. That
`MLServiceInfo` is imported from `chapkit.api.service_builder` — i.e. from the chapkit
package pinned inside chap-core's own virtualenv, which is **chapkit 1.1.0**
(servicekit 1.0.1). The model image is built on **chapkit 2.0.0** (servicekit 2.0.2),
whose `/api/v1/info` carries three extra fields. chapkit 1.1.0's `MLServiceInfo` is
declared `extra="forbid"`, so:

```
3 validation errors for MLServiceInfo
git_revision        Extra inputs are not permitted
chapkit_version     Extra inputs are not permitted
servicekit_version  Extra inputs are not permitted
```

The suggested escape hatch in the error message does **not** work. `--run-config.
is-chapkit-model` only skips the *probe*; `ExternalChapkitModelTemplate.name` then calls
`CHAPKitRestAPIWrapper.info()`, which validates with the same strict class and raises the
`ValidationError` directly. I confirmed that by calling the wrapper from Python.

Ironically the offending `git_revision` field is exactly what the model's most recent
commit (the pinned one, "fix/git-revision-build-arg") is about — the pin lands on the
commit that made the service report its build revision, and that is one of the three
fields chap-core's pinned chapkit refuses.

### What I did about it

I did **not** patch the model, and I did **not** upgrade chapkit inside chap-core's
virtualenv — that would have changed the platform under test, and the incompatibility is
itself the result worth recording.

Instead I wrote `scripts/info_shim.py`: a transparent stdlib reverse proxy that forwards
every request verbatim to the container and does exactly one thing — drops
`git_revision`, `chapkit_version` and `servicekit_version` from the JSON body of
`GET /api/v1/info`. CHAP then points at the shim instead of the container.

Everything else in the chapkit API validated unchanged under chapkit 1.1.0's models:
`/api/v1/configs`, `/api/v1/configs/$schema`, `/api/v1/jobs/{id}`, `/api/v1/artifacts/{id}`,
`/api/v1/ml/$train`, `/api/v1/ml/$predict`. The OpenAPI path set of the 2.0.0 service is a
superset of what chap-core's client calls. So the drift really is only that one payload.

**If you are attempting this next:** either use a chap-core new enough to ship chapkit
2.x, or keep a shim like this one. Do not waste time on `--run-config.is-chapkit-model`;
it does not rescue you.

## Other things worth knowing

- `chap validate <csv>` is a cheap first check and does auto-discover the sibling GeoJSON,
  so it is a good way to confirm the geometry will be picked up before spending an hour.
- The GeoJSON's features already carry a feature-level `id` (`LA-XA` etc.) matching the
  CSV's `location`, and `properties.shapeISO` carries the same value, so the model's
  strict geometry matching (`build_graph()` in `scripts/lib.R`) found a match on the first
  try. The README's warning about BSC's Laos demo (GADM names like `Louangnamtha` vs the
  data's `LouangNamtha`) does **not** bite on this CHAP-harmonised dataset — different
  boundary source (OCHA COD-AB via HDX, keyed on ISO codes rather than names).
- CHAP drops `LA-VI` ("Rejected regions: ['LA-VI'] due to missing target values for the
  whole training period"), so the fit is over 17 of the 18 admin units. `LA-VI`'s
  `disease_cases` sum over the whole series is 0.
- `chap eval` emits `Column 'rainfall' is present in the dataset but not used by the
  model` for `rainfall`, `mean_temperature` **and** `mean_relative_humidity`. The first two
  are wrong: the model's own config defaults *do* use them, and the fitted formula proves
  it. The warning comes from `warn_unused_covariates()`, which compares against the
  configuration CHAP sent (empty, so the service's own defaults applied) and has no way to
  see the service-side defaults. Ignore it for the first two; it is correct for
  `mean_relative_humidity`, which this model does not use.
- An empty model configuration is the right thing to send: `get_model()` drops an empty
  `additional_continuous_covariates` specifically so the chapkit service's schema defaults
  apply. Those defaults (`rainfall` + `mean_temperature`) happen to match this dataset, so
  no `--model-configuration-yaml` was needed.
- The fitted formula, from the container log:
  `disease_cases ~ 1 + rainfall.rsum3.l1 + mean_temperature.rmean3.l1 + f(spatial_id, model='bym2', graph=g, scale.model=TRUE, hyper=prec1) + f(seasonal_id, model='rw1', cyclic=TRUE, scale.model=TRUE, hyper=prec1) + f(year_id, model='iid', constr=TRUE, hyper=prec1)`
- The emulation noise the README predicts is real: every predict job's stderr is hundreds
  of `mbind: Function not implemented` lines. Harmless, but it makes the container log
  unreadable and it is the bulk of `results/service.log`.

## The invocation that worked

```bash
docker run -d --platform linux/amd64 -p 8000:8000 \
  --name chapkit-ghr-model-route-a chapkit-ghr-model:60b16a2
python3 scripts/info_shim.py 8010 http://localhost:8000 &

chap eval \
  --model-name http://localhost:8010 \
  --run-config.is-chapkit-model \
  --dataset-csv /tmp/chapdata/chap_LAO_admin1_monthly.csv \
  --output-file results/eval_lao_ghrmodel.nc \
  --backtest-params.n-splits 7 --backtest-params.n-periods 3 \
  --backtest-params.stride 1 --plot

chap export-metrics --input-files results/eval_lao_ghrmodel.nc \
  --output-file results/eval_metrics.csv
```

`scripts/run_route.sh` does all of the above from a clean start, including the build.
I ran it end to end to verify it, so the files currently in `results/` are that run's,
not the hand-driven one's.

No model code was modified. There is no `results/model_modifications.diff`, because
nothing needed patching in the model. The one adaptation is `scripts/info_shim.py`,
which sits *outside* both the model and the platform.

## The results, and run-to-run stability

Two identical invocations, back to back:

| | run 1 (hand-driven) | run 2 (`run_route.sh`) |
|---|---|---|
| MAE | 130.00 | 133.28 |
| CRPS | 159.99 | 162.42 |
| RMSE | 262.17 | 273.65 |
| coverage 10-90 | 0.824 | 0.836 |

Both are kept (`eval_metrics.csv` / `eval_metrics_firstrun.csv`, and the two `.nc`
files). The spread is ~2-4%, which is the INLA non-determinism the model README already
warns about ("INLA is not bit-reproducible even at nthreads=1"). Do not quote any of
these to more than two significant figures, and do not treat a difference of this size
between configurations as meaningful.

Note the evaluation is a very short one: the 7 splits all fall in 2010, with test periods
2010-04 to 2010-12. That is `chap eval`'s default backtest, not a choice I made, and it
means the numbers describe one year of one country, not general skill. The evaluated grid
is 17 locations x 9 test periods x 3 horizons x 1000 samples.

## Timings on this host (Apple M3, everything amd64-emulated)

- `docker build`: ~22 minutes, 4.98 GB image.
- service cold start to `/health`: ~40 s.
- one predict job (one INLA fit over ~2650 rows, 1000 posterior draws): ~70-110 s.
- full 7-split `chap eval`: ~11 minutes.

That last number was the pleasant surprise. Given the README's warnings about emulation I
had expected hours and had planned to reduce the number of splits; it was not necessary.

## What I would tell the next person

1. Read `chap eval --help` and then the docstring of `chap_core/cli_endpoints/evaluate.py`
   in the installed package. Between them they contain the whole recipe. The model's own
   README never mentions `chap eval` at all — it stops at "ready to plug into chap-core"
   and documents `make run`.
2. Check the chapkit version on both sides *first*
   (`curl .../api/v1/info | grep chapkit_version` versus `python -c "import
   importlib.metadata as m; print(m.version('chapkit'))"` inside chap-core's venv). If
   they differ across a major version, expect exactly the failure above, and do not trust
   the "could not be reached" error message.
3. Run a 1-split smoke evaluation before the real one. Mine took 87 s and would have
   surfaced any data or geometry problem immediately.
4. Do not bother trying to pull the GHCR image.

## Things I got wrong or nearly got wrong

- I assumed the prebuilt GHCR image would be pullable because the README and a badge
  advertise it, and I only found out otherwise after deciding against building. Building
  should have been the default assumption for a research model.
- I initially read `--run-config.is-chapkit-model` as the fix for the auto-detection
  failure, because that is what the error message says. It is not; I only found that out
  by reading `ExternalChapkitModelTemplate` rather than trusting the message.
- I considered upgrading chapkit inside chap-core's virtualenv and rejected it. That would
  probably also have worked and is what a real deployment should do, but it would have
  meant reporting on a platform other than the one installed here.
