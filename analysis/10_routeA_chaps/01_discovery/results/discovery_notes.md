# Discovery notes — route A through chaps, chapkit_ghr_model on Lao admin-1 monthly

Written as the work went, by the discovering agent (batch 14, attempt 2).

## Starting point (08:41Z)

- Read the log specification and my node directory. The node held an orchestrator note
  (`docker_state_before_run.txt`): chaps not installed, the model image is ~2.1 GB
  compressed and ghcr.io gives ~0.5 MB/s, so a ~70-minute pull was to be expected.
- chaps README → it points AI agents at `docs/ai.md`. That page is well made for an
  agent: numbered options, one "It worked when" line each, explicit advice for an agent
  that runs commands itself (`-C`, poll `chaps status` by exit code, long timeouts).
- What ai.md does *not* say: how to evaluate a model **on your own data**. Its only
  evaluation advice without DHIS2 is `chaps models test --all --backtest`, which uses
  sample data the model generates itself. The Lao CSV is nowhere in the chaps path
  except as the DHIS2 demo (weekly dengue 2019–2024, a different dataset from ours).
- So the route became: chaps serves the model (`chaps run <github url>`, ai.md options
  7/11), and the installed `chap eval` (2.3.1) evaluates it by URL with
  `--run-config.is-chapkit-model`. That flag is in `chap eval --help`, and the chap-core
  doc `docs/external_models/chapkit.md` shows exactly this pattern — its example even
  uses the public `chap_LAO_admin1_monthly.csv`, which I checked is byte-identical to the
  CSV and GeoJSON given to me.
- Considered and not taken: a full `chaps init` + `chaps up` deployment of chap-core and
  evaluating through its API. More moving parts, ai.md asks for ~25 GB free disk and the
  host had 14.4 GB, and nothing in chaps' docs shows how to post a dataset of one's own
  for a backtest.

## Install and doctor

- `install.sh --dir` put chaps 0.99.4 into a scratch directory without trouble.
- `chaps doctor`: 10 ok, 1 warn (arm64 host; amd64 images run under Rosetta). It did not
  flag the 14.4 GB free disk even though ai.md asks for ~25 GB.
- `chaps models list`: chapkit_ghr_model is a marketplace model ("GHRmodel",
  experimental, 0.1.3). `chaps run <github url>` says so and enables the marketplace pin
  (`sha-dfb2e3f`).

## What the default evaluation output is

- `chap eval` alone writes only the NetCDF; `--plot` (default off) adds an HTML plot.
- chap-core's `docs/chap-cli/evaluation-workflow.md` defines the workflow as three
  steps: `eval` → `plot-backtest` (default plot type `evaluation_plot`, "forecasts vs
  observations and uncertainty bands") → `export-metrics` (all aggregate metrics, CSV).
  I took those three, with defaults throughout, as CHAP's default evaluation output.
- The GeoJSON is picked up automatically when it sits beside the CSV with the same stem;
  its feature `id`s are the CSV `location` codes, so the model's strict geometry check
  (README: mismatched geometry is an error) should pass.

## Image pull and model start

_(continued below as it happens)_
- `chaps run https://github.com/chap-models/chapkit_ghr_model --port 5060 --timeout 7000`
  started at 08:42Z. chaps first pulls the image to ask it what uid `app` has. All layers
  but one arrived within ~8 minutes; the 1.42 GB layer `7c4627a62657` kept being cut by
  ghcr.io (Docker's "Retrying in N seconds", 5 times) and the pull died with
  `unexpected EOF` around 09:30Z.
- **chaps carried on after that failure** with a warning ("runs as `app`, which has no
  known uid:gid ... chown /work/data to 1000:1000 instead") and started `docker compose`,
  which pulled the image a second time. Because the first pull never extracted its
  finished layers, compose re-downloaded several of them too. The second pull also died
  on the same layer with `unexpected EOF` (at 10:15Z it even showed the layer at
  983.3MB/983.3MB of its resumed remainder before the EOF). chaps then stopped with
  `error: chapkit-ghr-model did not start (unexpected EOF); fix that, then chaps run ...
  tries again` (docker compose status 18). 93 minutes, nothing running.
- Docker here uses the overlay2 store, which discards a partly downloaded layer when a
  pull fails, so simply rerunning `chaps run` (what the error suggests) starts the
  1.42 GB layer from zero again with the same odds. This is a network/infrastructure
  blocker, not something in the model or in chaps' logic — but chaps' advice ("fix that")
  gives nothing to act on, and its uid probe doubles the download on a slow link.
- Workaround taken (not a change to the model): `scripts/fetch_image_oci.sh` downloads
  the same manifest and blobs from ghcr.io with `curl -C -` (resumes across cut-offs),
  checks every blob against its sha256 digest, assembles an OCI image layout and
  `docker load`s it under the original tag `ghcr.io/chap-models/chapkit_ghr_model:sha-dfb2e3f`.
  The loaded image is byte-for-byte the published one. Then `chaps run` again, which
  should find the image locally.
- The resumable fetch took 10:16Z–11:44Z. The 1.42 GB layer was cut off four times
  (`curl: (92) HTTP/2 stream 1 was not closed cleanly: PROTOCOL_ERROR`), and once a
  278 MB layer too; each time curl resumed. That confirms the blocker was ghcr.io / the
  link cutting long streams, not chaps.
- First `docker load` failed: a bare OCI layout is not enough for the overlay2 loader
  (`open /var/lib/docker/tmp/.../blobs/json: no such file`). Adding a docker-archive
  `manifest.json` beside the OCI index (what `docker save` writes) fixed it. Loaded image
  id `cf686a4edb71` = the config digest in the published manifest.
- Second `chaps run` (11:46Z): docker checks the tag against the registry ("Image is up
  to date"), chaps starts the init container and the service, `running chapkit_ghr_model
  on http://localhost:5060 (answered in 2s)`. `/health` healthy; `/api/v1/info` reports
  GHRmodel (chapkit) 0.1.3, git dfb2e3f, chapkit 2.2.0. The service logs that it skipped
  registration (no orchestrator URL) — expected, `chaps run` has no chap-core.

## The evaluation (11:47Z–11:54Z)

- `chap eval --model-name http://localhost:5060 --dataset-csv <Lao csv> --output-file
  results/eval.nc --run-config.is-chapkit-model`, all backtest parameters at their
  defaults (7 splits, 3 periods, stride 1, 1 retrain, climatology future weather).
  1 train job (a no-op by design) + 7 predict jobs at ~55–75 s each under emulation;
  6.8 minutes. rc=0, `eval.nc` 3.7 MB.
- Two things in chap's log that look alarming and turned out not to matter / to be
  data facts:
  - `Rejected regions: ['LA-VI'] due to missing target values for the whole training
    period` — Vientiane prefecture has no disease_cases at all in this CSV; chap drops it,
    so the evaluation covers 17 of 18 provinces.
  - `Column 'rainfall' / 'mean_temperature' / 'mean_relative_humidity' is present in the
    dataset but not used by the model`. **This does not hold**: the model's own job log
    shows the training data arriving with all nine columns, and every predict job fitting
    `disease_cases ~ 1 + rainfall.rsum3.l1 + mean_temperature.rmean3.l1 + f(spatial_id,
    model='bym2', graph=g, ...) + f(seasonal_id, 'rw1', cyclic) + f(year_id, 'iid')` —
    i.e. the model's default configuration, covariates and spatial effect included
    (geometry was passed as geo.json and matched). chap's warning seems to be computed
    from the service's `required_covariates` (only `population`) and ignores
    `allow_free_additional_continuous_covariates` plus the model's own covariate config.
- The evaluation window is 2010-04..2010-12 (forecasts for 9 periods × horizons 1–3,
  1000 samples), with 72 months of history for plotting.

## Beyond `chap eval`: the default output

- `chap eval` alone wrote only `eval.nc`. Two further steps, both with defaults:
  `chap plot-backtest --input-file eval.nc --output-file evaluation_plot.html` (default
  plot type `evaluation_plot`: forecasts vs observations with uncertainty bands) and
  `chap export-metrics --input-files eval.nc --output-file metrics.csv`.
- metrics.csv (aggregate): crps 149.2, mae 124.1, rmse 238.9, mape 150.8,
  coverage_10_90 0.815, coverage_25_75 0.664, ratio_above_truth 0.357,
  outbreak sensitivity 0.452 / specificity 0.82.
- Kept in results/: eval.nc, evaluation_plot.html, metrics.csv, the logs of each command
  (chap_eval.log, plot_backtest.log, export_metrics.log), the model service's container
  log (model_service.log), both `chaps run` logs and the image fetch log.

## run_route.sh in a clean shell

- Script: `scripts/run_route.sh [OUT_DIR] [WORK_DIR]`, with `scripts/fetch_image_oci.sh`
  beside it. It needs only bash, curl, tar, shasum and a running Docker; it installs
  chaps (install.sh `--dir`), uv and `chap-core==2.3.1` (from PyPI, via `uv tool
  install`) into WORK, downloads the Lao CSV + GeoJSON from
  dhis2/climate-health-data and checks their sha256 against the given files, prefetches
  the pinned image with the resumable fetcher (skipped if already present), runs
  `chaps run <github url> --port 5060`, then `chap eval` / `plot-backtest` /
  `export-metrics` with defaults, and `chaps stop` on exit.
- Run as `env -i HOME=<empty dir> PATH=/usr/bin:/bin bash scripts/run_route.sh
  results/clean_run <scratch>/cleanwork`. An **empty HOME** (stricter than the brief's
  example) so that neither this laptop's chap/uv installs nor chaps' state under
  `~/.local/share/chaps` could leak in; Docker Desktop still works because
  `/var/run/docker.sock` is a system symlink. The script adds the usual Docker
  locations (`/usr/local/bin` etc.) to PATH itself.
- **Outcome: rc=0.** results/clean_run/ holds eval.nc, evaluation_plot.html,
  metrics.csv and the full run log (run_route.log). The run took 23 minutes of
  execution (14:45–15:08Z): ~12 min was uv downloading 177 wheels for chap-core on this
  slow link, ~8 min the evaluation.
- What the clean run did **not** exercise: the image download. The 4.85 GB image was
  already in the Docker store, so the prefetch printed "already present" and chaps only
  checked the tag against the registry. A truly empty machine would add the ~1.5 h fetch
  on this link; the fetcher itself was exercised during discovery (download + the fixed
  load step), but not inside the clean-shell run.
- Wall-clock caveat: I launched the clean run at 11:55Z, but the laptop went to sleep
  (pmset: Sleep/DarkWake cycles, FullWake 14:37Z) and the script only started at ~14:45Z
  (chaps binary mtime). That gap is sleep, not route effort; the two blocker rows for it
  were written after the fact, when I found it.
- Metrics differ slightly between the discovery run and the clean run (crps 149.2 vs
  149.8, mae 124.1 vs 127.7, rmse 238.9 vs 244; coverage identical). Expected: the model
  draws 1000 posterior samples with no seed exposed, and its README says INLA is not
  bit-reproducible. Not a route problem.
- Small things: the uv installer skipped its own checksum check under the bare PATH
  ("requires the 'sha256sum' command"; macOS has shasum). The leftover chaps volume
  (`*_ck_chapkit_ghr_model_data`) is kept by `chaps stop` by design.

## Summary of what did and did not hold

- Held: chaps' agent page is accurate for what it covers; `chaps run <github url>`
  correctly maps the repository to the marketplace pin and serves the model;
  chap 2.3.1's `chap eval --run-config.is-chapkit-model` against that URL works with no
  glue; the GeoJSON is auto-discovered and matches; the model runs as published with
  its defaults (no change to the model).
- Did not hold / was missing: chaps' docs give no path to evaluating a model on one's
  own dataset (only model-generated sample data via `models test --backtest`), so the
  evaluation step came from chap-core's docs, not chaps'. chaps' download path is fragile
  on a slow link (uid-probe pull + compose pull, no resume across failures, advice "fix
  that" with nothing to act on). chap's "column not used by the model" warning for
  rainfall/mean_temperature is false for this model.
- One logging slip: the `model_obtained` milestone was written at the end (step 48), not at 11:46Z when the image was loaded (step 31). The note on that row says so.
