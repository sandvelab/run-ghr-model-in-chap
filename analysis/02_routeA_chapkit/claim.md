# Claim

What does it take to find out how to run the published model chapkit_ghr_model through CHAP, and to actually run it, working only from public material? The route is taken until CHAP has written an evaluation of the model's predictions on the Lao admin-1 monthly data, and what it took is logged as it happens.

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(Each belongs in the claim collection under `Human-AI-collaboration/claims/` with a pointer
to the result grounding it.)_

**The route completes, and the model runs as published.** CHAP wrote an evaluation of
`chapkit_ghr_model` on the Lao admin-1 monthly data twice — once by hand down the route
(`results/eval/`) and once reproduced by the route's own script in a clean shell
(`results/route_run/`). Nothing was interposed between CHAP and the model, and the model's
own code was not touched: the clone's `git status` was clean at the end.

**The working invocation** *(`results/discovery_notes.md`, §"The invocation that worked")*.
The model is a chapkit REST service, so CHAP is pointed at its URL rather than at a
directory, with the flag that tells CHAP what it is looking at:

```
docker build --platform linux/amd64 -t chapkit-ghr-model:latest .
docker run -d --platform linux/amd64 -p 8000:8000 chapkit-ghr-model:latest
chap eval http://localhost:8000 chap_LAO_admin1_monthly.csv evaluation.nc \
     --run-config.is-chapkit-model --plot
chap export-metrics --input-files evaluation.nc --output-file metrics.csv
chap plot-backtest evaluation.nc predicted_vs_actual.html --plot-type predicted_vs_actual
```

All CHAP defaults were taken: 7 splits, 3 prediction periods, 1 retrain, `climatology` future
weather. CHAP posted an empty configuration, so the model ran on its own defaults.

**`chap eval` alone does not give you an answer, and it takes two further commands to get
one.** The evaluation writes a NetCDF file; the default plot appears only if `--plot` is
passed, which is off by default; the metrics table needs `chap export-metrics`; and a
predicted-versus-observed figure needs `chap plot-backtest --plot-type predicted_vs_actual`.
None of the three is mentioned in the model's documentation.

**The geometry has no command-line option and is found by filename.** `chap eval --help`
carries nothing for the GeoJSON; CHAP discovers a `.geojson` sitting beside the CSV with the
same stem (`chap_core.cli_endpoints._common.discover_geojson`, read in the installed source).
The route's script therefore stages the two files side by side deliberately rather than by
luck. The 18 feature ids matched the CSV's `location` column exactly, so the model's strict
geometry check passed, and its container log shows `bym2` in the fitted formula — the
geometry genuinely reached the model rather than being silently dropped.

**Four blockers, one of them never resolved** (`results/discovery_log.tsv`):

| Blocker | Outcome |
|---|---|
| Host is arm64; the model is amd64-only because R-INLA ships x86_64 binaries | **open** — runs under emulation throughout, correct but slow |
| `ghcr.io/chap-models/chapkit_ghr_model:latest` returns 401 to an anonymous pull | resolved by building the published Dockerfile locally |
| `chap export-metrics evaluation.nc metrics.csv` fails: `--input-files` is variadic and swallows both positionals | resolved with named flags |
| `run_route.sh` under `env -i` failed preflight — `docker` is not on a minimal `PATH` | resolved |

**The route was reached through the platform's own source, not through its documentation.**
Six resources were opened and all six contributed; two of them are files inside the installed
`chap-core` package. Nothing on the web and nothing in the model's repository carries the
invocation — the model's README never mentions `chap eval`.

**What the evaluation reported** *(`results/eval/metrics.csv`,
`results/route_run/metrics.csv`)*. 17 of 18 locations — CHAP dropped `LA-VI`, which has no
target values — over 9 periods from 2010-04 to 2010-12, 3 horizons, 1000 samples. Across the
two runs: CRPS 149.5–150.2, MAE 126.1–128.5, RMSE 242.8–245.0, MAPE 150.8–155.0, coverage
10–90 0.810–0.821. **These are not compared against any other route** (plan §2). The two runs
differ because the model fits with R-INLA, which its own README states is not
bit-reproducible; nothing in the route sets a seed and CHAP offers none for a chapkit service.

**The recipe was verified, and verifying it found a defect.** `scripts/run_route.sh` ran end
to end from `/` under `env -i` with only `HOME` and a minimal `PATH`. The first attempt failed
correctly at its own preflight check, because `docker` lives in `/usr/local/bin`; a recipe
written out of the log at the end would have shipped with that fault invisible.

**One part of the route is unverified, and it is the expensive part.** The host's BuildKit
layer cache was already warm when the route began — 7 of 8 layers cached on the first build,
8 of 8 on the verification build (`results/docker_build.log`,
`results/route_run/docker_build.log`). A genuinely cold build, which clones GHRmodel from a
third-party GitLab and compiles it under emulation alongside two CRAN installs, was never
exercised. The build-time figures therefore understate a build from nothing, and this is
recorded rather than worked around.
