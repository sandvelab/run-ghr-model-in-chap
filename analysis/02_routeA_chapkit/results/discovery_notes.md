# Discovery notes — route A, chapkit_ghr_model through CHAP

Narrative kept as the route was walked. Counts are in `discovery_log.tsv`.

## Starting position

Given: the model's GitHub URL, `chap` 2.3.1 on PATH, Docker running, three Lao data
files. Nothing about how CHAP expects a model to be presented. No prior knowledge of
any other model or any other integration route was available or sought.

## What the model's README settled in one read

The repository README is unusually complete, and it answered most of the integration
question before any CHAP documentation was opened:

- the model is a **chapkit service**, not a directory of scripts — it runs as a REST
  service on port 8000 and is described as "ready to plug into chap-core";
- there is a `Dockerfile`, a `compose.yml` (build) and a `compose.ghcr.yml` (prebuilt
  image), plus a `Makefile` with `build` / `run` / `run-ghcr`;
- it is **amd64 only** (R-INLA ships x86_64 Linux binaries only). This host is arm64,
  so everything runs under qemu emulation — the README says so explicitly and warns
  that `bym2` fits flood the log with harmless `mbind: Operation not permitted`;
- geometry handling is **strict**: geometry that does not match the data is an error,
  not a silent fallback, and the README warns that BSC's own Laos demo trips over this
  because their GADM polygon names differ from their data's location names.

That last warning was the thing I expected to cost time, so I checked the supplied
GeoJSON against the CSV before running anything.

## The prebuilt image is not pullable

`compose.ghcr.yml` points at `ghcr.io/chap-models/chapkit_ghr_model:latest`, and the
README offers it as the easy path ("once published"). `docker pull` returns
`401 unauthorized` — the package is not anonymously readable. So the route has to build
from the `Dockerfile`. That is a workaround *outside* the model (a different way of
obtaining the same artefact), not a change to it.

**Honest note about the build.** The build finished in 27 seconds with 7 of 8 stage
layers reported `CACHED`; only the final `chmod`/`useradd` layer was rebuilt, because
the `GIT_REVISION` build-arg differs. This host already held a warm BuildKit layer cache
for this image from before I arrived, so **my build time is not a from-scratch
measurement**. A cold build would have to clone GHRmodel from
`gitlab.earth.bsc.es`, compile it from source, and install two CRAN packages, all under
emulation. `results/docker_build.log` is the full log.

## How CHAP wants a chapkit model presented

`chap --help` then `chap eval --help` answered this with no external documentation:

- `chap eval MODEL-NAME DATASET-CSV OUTPUT-FILE`, where MODEL-NAME may be "a local
  directory, a GitHub URL, **or a chapkit service URL**";
- `--run-config.is-chapkit-model` — "Set to True when the model is served via chapkit
  (REST) rather than an MLproject directory";
- `--plot` — "Generate an HTML evaluation plot alongside the NetCDF".

The one thing the `--help` text does *not* say is how geometry reaches the model: there
is no `--geojson` / `--polygons` option on `eval`. Reading the installed
`chap_core/cli_endpoints/_common.py` showed `discover_geojson()`: CHAP looks for a file
with the **same path as the CSV with `.csv` replaced by `.geojson`**. The three supplied
data files share a stem, so this works by itself — but it is a convention discoverable
only from the source or from the `eval` docstring, not from `--help`.

`chap model schema <url>` was the cheap confirmation that CHAP can see the running
service as a model at all, before spending an emulated evaluation on it.

## Geometry matched

The supplied GeoJSON carries a top-level `id` on each feature (`LA-XA`, …), which is
exactly what `Polygons._add_ids` wants, and the 18 ids are exactly the 18 values in the
CSV's `location` column. So the README's Laos name-mismatch warning did not bite: the
warning is about BSC's own GADM polygons, not about CHAP-harmonised data. Nothing had to
be patched.

CHAP itself then dropped one region, `LA-VI`, for having no target values across the
whole training period, leaving 17.

## Contamination notes

- `docker images` on this host lists an unrelated `ghcr.io/chap-models/chapkit_ewars_model`
  image. I saw the name incidentally while checking what was running; I did not inspect
  it, pull it, or use anything about it. The GHR model's own README also mentions "the
  existing chapkit EWARS model" in passing as the precedent for training being a no-op —
  that is public text in the model's own README, not outside knowledge.
- The warm Docker layer cache described above is pre-existing host state from work I know
  nothing about. I report it rather than present the 27-second build as my own result.

## The invocation that worked

```
docker run -d --platform linux/amd64 -p 8000:8000 --name ghr chapkit-ghr-model:latest
chap eval http://localhost:8000 <lao>.csv evaluation.nc --run-config.is-chapkit-model --plot
chap export-metrics --input-files evaluation.nc --output-file metrics.csv
chap plot-backtest evaluation.nc predicted_vs_actual.html --plot-type predicted_vs_actual
```

All with CHAP's defaults (7 splits, 3 periods per split, 1 retrain, `climatology`
future-weather provider) and the model's own config defaults — CHAP posted an empty
config object `{}` to `/api/v1/configs`, so the model ran on `rainfall` +
`mean_temperature`, `bym2`/`rw1`/`iid`, exactly as the README documents. About six
minutes wall clock for the whole backtest under emulation.

## Two things beyond `chap eval`

`chap eval --plot` already writes the default HTML evaluation plot next to the NetCDF —
that part needs no extra step, only the flag, which is off by default. Two further
commands were needed for what `eval` does not produce:

- `chap export-metrics` for the metrics table. Its `--input-files` is a *variadic*
  parameter, so the obvious positional form `chap export-metrics evaluation.nc
  metrics.csv` fails with "parameter --output-file requires an argument" — both paths
  have to be passed as named flags. The only real friction of the route.
- `chap plot-backtest ... --plot-type predicted_vs_actual` for an explicit
  predicted-versus-observed scatter (the default `evaluation_plot` is the time-series
  view that `--plot` already gives).

## What surprised me

- **Nothing about the CHAP side needed external documentation.** `chap --help` and
  `chap eval --help` name the chapkit service URL as an accepted MODEL-NAME and
  document `--run-config.is-chapkit-model` in one line each. No web search was needed.
- **Except the geometry convention**, which `--help` does not mention at all. Had the
  GeoJSON been named anything other than the CSV's stem, the spatial effect would have
  been silently dropped and the run would still have "succeeded" with a materially
  different model — which is precisely what the model's README says it refuses to do on
  *its* side, but CHAP's side of the handshake is silent about it.
- **The model's own README carried more of the integration than CHAP's CLI did**, and
  its warnings (amd64, strict geometry, the Laos name mismatch) were accurate and
  well-targeted. The one thing it was wrong about in practice is the prebuilt GHCR
  image, which is not anonymously pullable.

## What I would tell the next person

1. Start with the model's README, not with CHAP. It tells you the model is a REST
   service, which is the single fact that determines the whole invocation.
2. Do not budget for the GHCR image; budget for a build.
3. Name the GeoJSON after the CSV, in the same directory. There is no flag.
4. `chap model schema <url>` is a five-second check that the service and CHAP agree,
   before you spend a multi-minute emulated backtest finding out they do not.
5. On arm64, expect emulation. It worked correctly; it was slower, and the container log
   is full of `mbind: Function not implemented` per predict call, which is the README's
   warning with a slightly different errno text than it quotes.

## Evidence that the spatial effect really was fitted

The container log shows the formula each predict call built, which is the proof that
CHAP's auto-discovered GeoJSON reached the model and that `bym2` was not silently
dropped:

```
Combined: 2567 rows; 51 to forecast across 17 locations
Derived covariate terms: rainfall.rsum3.l1, mean_temperature.rmean3.l1
disease_cases ~ 1 + rainfall.rsum3.l1 + mean_temperature.rmean3.l1
  + f(spatial_id, model = 'bym2', graph = g, scale.model = TRUE, hyper = prec1)
  + f(seasonal_id, model = 'rw1', cyclic = TRUE, scale.model = TRUE, hyper = prec1)
  + f(year_id, model = 'iid', constr = TRUE, hyper = prec1)
Wrote 51 rows x 1000 samples to predictions.csv
```

Each predict call also emits ~200 lines of `mbind: Function not implemented` on stderr —
the emulation noise the README warns about, under a slightly different errno text than
it quotes.

## The model was not modified

The clone was read, never edited. `git status` in the clone is clean. Everything that
had to be worked around — the unpullable GHCR image, the variadic `--input-files`, the
GeoJSON naming convention, `docker` missing from a minimal PATH — was worked around
outside the model, in how things were invoked.

## `run_route.sh` verification

Run from `/` under `env -i` with only `HOME` and a minimal `PATH`, with the hand-started
service removed first, so it started from nothing it had not made itself. It failed on
the first attempt — correctly: its preflight refused because `docker` is in
`/usr/local/bin`, which was not on the minimal PATH. With that directory added it ran
clean end to end: clone → build → serve → `chap eval` → `export-metrics` →
`plot-backtest`, outputs in `results/route_run/`.

**What went unverified.** The `docker build` inside `run_route.sh` reported **8 of 8
layers `CACHED`, 0 built fresh** (`results/route_run/docker_build.log`). The host's
BuildKit cache was already warm before the route began, so a genuinely cold build —
cloning GHRmodel from `gitlab.earth.bsc.es` and compiling it from source under x86
emulation, plus two CRAN installs — has **not** been exercised by me at any point. That
is the one part of the script I have not proven. Everything else in it ran.

The earlier hand-run build (`results/docker_build.log`) reported 7 of 8 cached with the
final `chmod`/`useradd` layer fresh, only because a different `GIT_REVISION` build-arg
was in play.

## Reproducibility of the numbers

The two runs of the identical route give slightly different metrics — MAE 126.07 then
128.48, CRPS 150.25 then 149.48. The model's README says plainly that INLA is not
bit-reproducible even at `nthreads=1`, so this is expected, not a fault of the
invocation. Nothing in the route sets a seed, and CHAP does not offer one for a chapkit
service.

## Log integrity

`discovery_log.tsv` was appended to with `log_step.py` at the moment of each step,
never in batches. Three rows are explicit self-corrections, kept rather than rewritten:
step 12 records a `docker pull` as `ok` that in fact failed (step 13 corrects it), and
step 28 records `chap export-metrics` as `ok` that in fact failed (steps 30 and 32
correct it). In both cases the row was written before the command's output was read. A
log that could be edited afterwards would have hidden this; leaving it visible is the
point.
