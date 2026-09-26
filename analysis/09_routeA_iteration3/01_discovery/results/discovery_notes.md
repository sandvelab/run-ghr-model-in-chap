# Discovery notes: route A, iteration 3 (chapkit_ghr_model through chap 2.3.1)

Written by the discovering agent, alongside `discovery_log.tsv`. Narrative only; the row-level
trace is the log.

## What I did

1. Read the discovery-log specification and my node's `claim.md`. The claim names commit
   `a9532c7` of the model and chapkit 2.1.2; the brief itself does not. I pinned to `a9532c7`
   on the strength of the claim, and logged that as a decision.
2. Cloned `https://github.com/chap-models/chapkit_ghr_model` and checked out `a9532c7`
   (the repo's HEAD at that moment). Read the README, Makefile, compose files, Dockerfile,
   `main.py`, and the publish workflow.
   - The README says how to build and run the service (`make build`, `make run`,
     `docker compose -f compose.ghcr.yml up`, port 8000) and documents the config, but
     **says nothing about `chap eval`** or how to point CHAP at the service. It is written
     from the chapkit side of the boundary only.
   - The publish workflow shows images are tagged `sha-<short>` as well as `latest`, which
     is what let me use a published image pinned to the exact commit.
3. On the CHAP side, `chap --help` and `chap eval --help` gave the key fact on their own:
   `--model-name` accepts "chapkit service URL ... http://localhost:8000" together with
   `--run-config.is-chapkit-model`. The chap-core README on GitHub was no help (overview
   only). I cloned chap-core and checked out tag `v2.3.1` so the docs matched the installed
   CLI, then read `docs/chap-cli/eval-reference.md`, `docs/chap-cli/evaluation-workflow.md`
   and `docs/external_models/chapkit.md`. Those three pages together are sufficient:
   - GeoJSON is auto-discovered by the CSV's basename; feature `id`s must match `location`.
     The Lao files already follow this (`chap_LAO_admin1_monthly.{csv,geojson}`, 18
     features with `id` = `shapeISO` = `location`).
   - `chapkit.md` gives the exact pattern: `docker run -p PORT:8000 <image>` then
     `chap eval --model-name http://localhost:PORT ... --run-config.is-chapkit-model --plot`,
     and its example even uses the same public Lao CSV URL.
   - The workflow page names the steps beyond `chap eval`: `chap plot-backtest` and
     `chap export-metrics`.
4. `chap validate` on the Lao CSV passed and picked up the GeoJSON.
5. Pulled `ghcr.io/chap-models/chapkit_ghr_model:sha-a9532c7` (linux/amd64 only; the host
   is arm64, so it runs under emulation). The pull took about 14 minutes (about 5 GB).
6. Ran the container on port 8765. `/api/v1/info` reported `git_revision a9532c7...`,
   version 0.1.2, chapkit 2.1.2, which confirms the image matches the pinned commit.
7. Ran `chap eval` with CHAP's backtest defaults (7 splits, 3 periods, stride 1, one
   training) and the model's default configuration (no YAML). Exit 0 after about 5.5
   minutes: 1 train job (a no-op by design) and 7 predict jobs of about 45 s each.
   Wrote `eval.nc` and, because of `--plot`, `eval.html`.
8. Ran `chap plot-backtest` (default plot type `evaluation_plot`, which is the
   forecast-versus-observed chart: blue forecast bands over orange observations, one panel
   per location and split) to HTML and PNG, and `chap export-metrics` to `metrics.csv`.
9. Wrote `scripts/run_route.sh`, removed the pulled image, and ran the script in a clean
   shell (`env -i HOME=$HOME PATH=/usr/bin:/bin bash scripts/run_route.sh`). Outcome is
   recorded below.

## What the default evaluation output is

`chap eval` on its own writes only the NetCDF (`eval.nc`). The HTML plot needs `--plot`
(default off) or a separate `chap plot-backtest`; both produce the same
"Backtest Forecasts with Observations" chart. Metrics are not written by `chap eval` at all;
they need `chap export-metrics`. So the further steps beyond `chap eval` are
`chap plot-backtest` and `chap export-metrics` (or `--plot` for the plot).

Headline aggregate metrics (manual run): CRPS 151.4, MAE 128.6, RMSE 251.7,
coverage 10-90 0.815, coverage 25-75 0.664.

## What was confusing, and what did not hold

- **CHAP's warning that the covariates were unused was false.** `chap eval` logged
  `Column 'mean_temperature' is present in the dataset but not used by the model` and the
  same for `rainfall`. The model's service log shows the fitted formula uses
  `rainfall.rsum3.l1` and `mean_temperature.rmean3.l1`. CHAP appears to judge "used" from
  something (probably the service's declared required covariates, which list only
  `population`) that does not reflect the model's default `additional_continuous_covariates`.
  A user trusting the warning would think the model ignores climate.
- **`--run-config.log-file` wrote nothing.** I passed it on the manual run and no file
  appeared; output went to stdout only. The script tees stdout instead.
- **One province is silently dropped.** CHAP rejected `LA-VI` ("missing target values for
  the whole training period") and evaluated 17 of 18 provinces. It is a warning in the log,
  not in the outputs.
- **The metrics CSV names the model by URL.** `model_name` is `http://localhost:8765`, not
  `chapkit-ghr-model`, so comparing evaluations by that column depends on the port used.
- **Schema `row_count` (2575) differs from the CSV's 2808 rows.** The difference is exactly
  the 233 rows with empty `disease_cases`, so the schema counts non-missing targets. Not a
  problem for the run, but misleading on first read.
- **Geometry did reach the model.** `/api/v1/info` says `requires_geo: false`, and the
  README says missing geometry silently drops the spatial term; the service log confirms the
  formula included `f(spatial_id, model = 'bym2', graph = g, ...)`, so the auto-discovered
  GeoJSON was passed through.
- The README's warning about GADM name mismatches in BSC's Laos demo did not arise: these
  files key on ISO codes, and the ids match.
- The README's warning about `mbind: Operation not permitted` under emulation held: the
  service log is full of it, harmlessly.
- The model was not modified, and nothing had to be patched around.

## Clean-shell run of run_route.sh

Run as `env -i HOME=$HOME PATH=/usr/bin:/bin bash scripts/run_route.sh` from `/tmp`, after
`docker rmi` of the pulled image, so the run started with no model image, no data copy and
no inherited environment. The script adds `~/.local/bin` (where `chap` lives) and Docker's
bin directories to `PATH` itself. Full console output: `results/run_route_clean_shell.out`.

**Outcome: exit 0, clean**, about 12 minutes end to end (pull about 5.5 min this time, eval
about 5.5 min). It fetched the Lao CSV and GeoJSON from the public
`dhis2/climate-health-data` repository (checksums match the local copies, recorded in
`route_run/input_sha256.txt`), validated them, pulled `sha-a9532c7`, ran the service,
ran `chap eval --plot`, `chap plot-backtest` (HTML and PNG) and `chap export-metrics`, and
saved the service log. No container was left behind.

The metrics are close to the manual run's but not identical (CRPS 151.03 against 151.36,
MAE 125.6 against 128.6, coverage 10-90 0.83 against 0.82). The model draws posterior
samples with no seed CHAP can set, and INLA itself is not bit-reproducible (the model
README says so). The route reproduces; its numbers reproduce only to about two
significant figures.

## Where the outputs are

- `results/manual_run/`: the discovery run. `eval.nc` (the evaluation), `eval.html` (from
  `--plot`), `evaluation_plot.html` and `.png` (default `plot-backtest`), `metrics.csv`
  (`export-metrics`), `chap_eval.stdout`, `service.log`, `service_info.json`, `input/`.
- `results/route_run/`: the same set, produced by `scripts/run_route.sh` in the clean shell,
  plus `image_id.txt` (image digest) and `input_sha256.txt`.
