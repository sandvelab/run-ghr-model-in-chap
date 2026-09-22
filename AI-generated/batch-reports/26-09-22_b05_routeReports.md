# Batch 5 — the two routes, each in full

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 2

Phase C. One report per route: what had to be read, what the process of finding out looked
like, what the working invocation turned out to be, and what the evaluation reported. Every
count comes from `analysis/04_comparison/01_effort/b_normalised/results/effort_by_route.tsv`;
every result from the file CHAP wrote. Nothing here compares the two routes — that is batch 6.

---

# Route A — `chapkit_ghr_model` as a chapkit model service

*(`analysis/02_routeA_chapkit/`)*

A Bayesian spatio-temporal model built on R-INLA, published as a containerised REST service
that CHAP talks to over HTTP.

## (a) What had to be read

**Five sources, all five of which contributed.** Notably, **two of them are files inside the
installed `chap-core` package**. Nothing on the web and nothing in the model's own repository
carries the invocation: route A's README never mentions `chap eval` at all. The service's own
container log was read as a source too, to establish that the spatial term had actually been
fitted.

## (b) The process of finding out

**Four blockers, one of them never resolved** (`results/discovery_log.tsv`):

| Blocker | Outcome |
|---|---|
| The host is arm64; the image is amd64-only, because R-INLA ships x86_64 binaries | **open** — the model runs under emulation throughout, which its README says is correct but slow |
| The published image `ghcr.io/chap-models/chapkit_ghr_model:latest` returns 401 to an anonymous pull | resolved by building the published Dockerfile locally |
| `chap export-metrics evaluation.nc metrics.csv` fails — `--input-files` is variadic and swallows both positionals | resolved with named flags |
| `run_route.sh` under `env -i` failed its own preflight: `docker` is not on a minimal `PATH` | resolved |

The route's first choice was to **pull** the published image rather than build it — the README
offers both, and the published image is the artefact a user would actually get. It was forced
away from that by the 401, and built locally instead. That is a workaround *outside* the
model, and it is logged as a decision with its basis.

**Two commands were logged `ok` and then corrected.** The agent marked them before reading
their output, recorded the failures in later rows, and logged its own decision not to rewrite
the originals. The logs are never edited; how that is counted is the subject of the
`01_effort` fork.

## (c) The working invocation

```
docker build --platform linux/amd64 -t chapkit-ghr-model:latest .
docker run -d --platform linux/amd64 -p 8000:8000 chapkit-ghr-model:latest
chap eval http://localhost:8000 chap_LAO_admin1_monthly.csv evaluation.nc \
     --run-config.is-chapkit-model --plot
chap export-metrics --input-files evaluation.nc --output-file metrics.csv
```

CHAP is pointed at the service's **URL** rather than at a directory, with
`--run-config.is-chapkit-model` to say what it is looking at. All CHAP defaults: 7 splits, 3
prediction periods, 1 retrain, `climatology` future weather. CHAP posted an empty
configuration, so the model ran on its own defaults.

**The geometry has no command-line option.** `chap eval --help` carries nothing for the
GeoJSON; CHAP discovers a `.geojson` sitting beside the CSV with the same stem
(`chap_core.cli_endpoints._common.discover_geojson`). The 18 feature ids matched the CSV's
`location` column exactly, so the model's strict geometry check passed — and the service's log
shows `bym2` in the fitted formula, so the geometry genuinely reached the model rather than
being silently dropped.

## (d) What the evaluation reported

*(`results/eval/metrics.csv`)* 17 of 18 locations — CHAP dropped `LA-VI`, which has no target
values — over 9 periods from 2010-04 to 2010-12, 3 horizons, 1000 samples.

**CRPS 150.25 · MAE 126.07 · RMSE 242.77 · MAPE 150.80 · coverage 10–90 0.821 · coverage
25–75 0.664.**

The figure CHAP draws by default is the backtest grid — observed cases as a line, the forecast
as 10–90 and 25–75 quantile bands — kept as `results/eval/evaluation.html`, with a raster of it
beside it and its 9520 plotted rows in `results/eval/evaluation_plot.tsv`.

---

# Route B — `minimalist_example_uv` as an `MLproject` directory

*(`analysis/03_routeB_mlproject/`)*

A deliberately minimal linear regression, published as a directory with an `MLproject` file
declaring how to train and predict.

## (a) What had to be read

**Four sources, all four of which contributed**: the model's repository page, its full README,
the Lao schema file, and one file inside the installed `chap-core` package.

## (b) The process of finding out

**One blocker, one failed command, and the fault in both is the platform's.**
`chap sanity-check-model --model-url .` dies on a clean chap-core 2.3.1 with
`FileNotFoundError: .../site-packages/example_data/hydromet_5_filtered.csv` — it defaults to a
bundled dataset that the wheel does not ship. Passing `--dataset-path` with the Lao CSV
sidesteps it and the check passes. This is a **packaging defect in chap-core**, not a property
of the MLproject route, and it is worth reporting upstream.

That was the only failure in the entire route. The model ran unmodified everywhere, and it ran
standalone outside CHAP first — `isolated_run.py`, which the model ships, trains and predicts
on its own bundled sample data.

**The README carried a working invocation, and it still worked** despite its own caveat that
it had been verified against earlier chap-core versions.

## (c) The working invocation

From inside the model directory:

```
chap eval --model-name . \
          --dataset-csv <dir>/chap_LAO_admin1_monthly.csv \
          --output-file <out>/eval/eval.nc --plot
chap export-metrics --input-files <out>/eval/eval.nc --output-file <out>/eval/metrics.csv
```

**Nothing is built and no container is involved.** The `MLproject` declares
`uv_env: pyproject.toml`, so CHAP runs train and predict through its command-line runner and
`uv` builds the model's environment on the host. Docker was confirmed to be running and was
never invoked. The resolved environment is kept as `results/chap_run_dir/uv.lock`.

**CHAP executes the model somewhere else than where you point it.** It copies the whole model
directory to a timestamped working directory and runs there, so the per-split
`training_data.csv`, `historic_data_*.csv`, `future_data_*.csv` and `predictions_*.csv` land
in that copy and nowhere near the NetCDF. That tree is kept in full as `results/chap_run_dir/`
— it is the only record of what the model was actually handed.

## (d) What the evaluation reported

*(`results/eval/metrics.csv`)* 17 of 18 locations — `LA-VI` rejected for the same reason — over
7 rolling splits, 3-period horizon, stride 1, one retrain, `climatology` future weather, all
CHAP defaults.

**MAE 171.96 · RMSE 358.93 · CRPS 171.96 · MAPE 383.16 · coverage 10–90 0.000 · coverage
25–75 0.000.**

**The zero coverage is not a defect in the evaluation; it is what the model is.** CRPS equals
MAE to the last digit and both coverages are zero because the model emits a single
deterministic sample: a point prediction has no spread for an interval to cover. The plotted
values show it directly — `q_10` through `q_90` are the same number in every one of the 9520
rows (`results/eval/evaluation_plot.tsv`), which is why the forecast appears in CHAP's default
figure as a mark rather than a band. The `log1p` metrics additionally raise
`invalid value encountered in log1p`, because an ordinary least-squares fit predicts negative
case counts.

---

## State

- Batch 5 **done**. `/validate invariants`: all eight checks pass.
- **The two routes' scores are not compared, here or anywhere.** They are different models
  fitted by different methods; the plan's §2 forbids a cross-route performance claim.
