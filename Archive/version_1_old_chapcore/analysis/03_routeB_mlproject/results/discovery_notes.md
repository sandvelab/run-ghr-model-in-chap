# Discovery notes — Route B: `minimalist_example_uv` (MLproject/uv) through CHAP

Task: run <https://github.com/dhis2-chap/minimalist_example_uv> at commit
`5cd8a1267362d945491353fba1c63a408462fa17` through CHAP (chap-core 2.1.0) and get an
evaluation on the Lao admin-1 monthly dataset.

**Outcome: success.** The evaluation ran, first attempt, no patching of the model.
`results/eval.nc`, `results/eval.html`, `results/eval_metrics.csv`.

---

## The honest headline: this route was easy

I want to say this plainly because the interesting part of this exercise is *how much
finding out* a route costs, and for this one the answer is "almost none". The model's
own README contains a literal, copy-pasteable `chap eval` invocation, and that
invocation worked unchanged against the Lao data on the first try. There was no dead
end, no abandoned path, no workaround. Total elapsed time from opening the README to a
written `.nc` was about twenty minutes, most of it dependency installation.

If you are comparing routes: the thing that made this cheap is that the model ships an
`MLproject` file, and `chap eval --model-name <dir>` consumes an `MLproject` directory
directly. There is no separate "register the model" step for a local directory — CHAP
reads `MLproject` at eval time and that *is* the registration. I logged
`model_registered_with_chap` at the point where CHAP printed `Loading model template
from model/minimalist_example_uv`, but I want to be candid that this milestone does not
correspond to a distinct action I took; it is something CHAP does implicitly inside
`chap eval`. Someone comparing milestone counts across routes should not read it as
work.

## Order I actually did things in

1. `chap --help`, then `chap eval --help`. I started with the installed CLI rather than
   the web docs, on the assumption that a 2.1.0 binary is more authoritative about its
   own flags than any page. That was the right call — the CLI help gives the full
   signature and every backtest parameter.
2. Downloaded the repo tarball from `codeload.github.com` at the pinned commit. The task
   forbids git commands, so `git clone && git checkout` was not available; a tarball URL
   of the form `https://codeload.github.com/<org>/<repo>/tar.gz/<sha>` gives a pinned
   checkout without git. Worth knowing.
3. Read `README.md` and `MLproject`. These two files were the entire documentation I
   needed.
4. Ran `uv run python isolated_run.py` in a scratch copy to confirm the model works at
   all before involving CHAP. It did (`output/model.pkl`, `output/predictions.csv`).
   This step is optional but it cleanly separates "the model is broken" from "the
   integration is broken", and cost 50 seconds.
5. `chap validate` against model + data.
6. `chap eval`. Worked.
7. `chap export-metrics` to get numbers out of the NetCDF.

## The one thing that genuinely confused me

`chap validate` (and `chap eval`) emit four warnings:

```
Column 'mean_relative_humidity' is present in the dataset but not used by the model
Column 'mean_temperature' is present in the dataset but not used by the model
Column 'population' is present in the dataset but not used by the model
Column 'rainfall' is present in the dataset but not used by the model
```

I read this as a probable blocker and logged it as such (step 12): `train.py` indexes
`df[["rainfall", "mean_temperature"]]`, so if CHAP really were withholding those columns
the model would die with a `KeyError`. I was wrong, and it is worth saying why so the
next person does not waste time on it.

The warning is about *declaration*, not *delivery*. This `MLproject` declares no
covariates at all (no `required_fields`, no user options — it is deliberately
minimalist), so CHAP's static check concludes that nothing in the dataset is used. But
CHAP writes the **whole** dataset to the train/predict CSVs regardless. I confirmed this
by reading what CHAP actually handed the model:

```
runs/minimalist_example_uv/<timestamp>/training_data.csv
  ,time_period,disease_cases,population,location_name,rainfall,mean_temperature,mean_relative_humidity,parent,location
```

All covariates present. The warnings are noise for an undeclared-covariate MLproject.
**They cannot be used to check whether a model will get the data it needs.** That is the
single most misleading thing I hit.

A second, softer one, repeated once per split:

```
Dataset has polygons, but command python predict.py {model} {historic_data} {future_data} {out_file}
does not ask for polygons. Will not insert polygons into command.
```

Also harmless — this model does not use geography. But note that CHAP *did* load and
rewrite the GeoJSON (`polygons.geojson` in the run directory) even though nothing
consumed it.

## Undocumented things I had to work out

- **The GeoJSON has no CLI flag.** `chap eval` takes only `--dataset-csv`. CHAP picks up
  the polygons by looking for a `.geojson` with the *same basename next to the CSV*. I
  only discovered this because the log line `Loading polygons from
  data/chap_LAO_admin1_monthly.geojson` appeared without my asking for it. If you copy
  the CSV somewhere and rename it, you silently lose the polygons. This is not in the
  model README, and it is why `scripts/run_route.sh` copies both files together, keeping
  the stem.
- **CHAP writes into the current working directory.** It creates `runs/<model
  name>/<timestamp>/` relative to cwd, copies the whole model directory in there, and
  runs the model from that copy. Good news: the pristine `model/` copy is left
  untouched (I diffed it — identical to the tarball). But it does mean cwd matters.
- **Each eval leaves ~197 MB of virtualenv behind, at a surprising path.** CHAP builds
  the model's uv environment at `runs/<model>/<timestamp>/.venv` computed *relative to
  the run directory it is already inside*, so you end up with
  `runs/minimalist_example_uv/<ts>/runs/minimalist_example_uv/<ts>/.venv` — the path
  doubled. Four invocations (two `validate`, two `eval`) produced 401 MB. I deleted the
  nested venv trees after copying the run's CSVs to `results/chap_run_artifacts/`; that
  is the only thing I removed, and the CHAP-written data files are all preserved. If you
  run this repeatedly, watch the disk.
- **`chap eval` does not print any metrics.** It writes a NetCDF and stops. To get
  numbers you need the separate `chap export-metrics` step, which the model README never
  mentions.
- **Docker was not needed.** It was offered and running, but this `MLproject` declares
  `uv_env: pyproject.toml`, so CHAP builds the environment with `uv` on the host.
  Docker would only be relevant for a `docker_env` model.
- **One region was silently dropped.** `Rejected regions: ['LA-VI'] due to missing
  target values for the whole training period`. The evaluation therefore covers 17 of
  the 18 admin units. This is a WARNING in a long log, easy to miss, and it means the
  evaluation is not quite on the dataset you think you gave it.

## Where I guessed

- **Backtest parameters.** I left all of them at CHAP's defaults (7 splits, 3-period
  horizon, stride 1, retrained once). The brief asks for "an evaluation", not a
  particular one, and defaults are the most reproducible choice. This gives a test window
  of 2010-04 … 2010-12 only — nine months at the very end of a thirteen-year dataset.
  If you want an evaluation that exercises more of the record, raise `--backtest-params.n-splits`.
- **`chap validate` before `chap eval`.** Not required; I did it as a cheap check.

## About the numbers (read them with suspicion)

From `results/eval_metrics.csv`:

| metric | value |
|---|---|
| MAE | 172.77 |
| RMSE | 357.52 |
| CRPS | 172.77 |
| CRPS (log1p) | 1.668 |
| MAPE | 423.60 |
| coverage 10–90 | 0.0 |
| coverage 25–75 | 0.0 |
| sample_count | 336 |
| ratio_above_truth | 0.461 |

Things to be aware of before quoting these:

- **CRPS equals MAE exactly.** That is not a coincidence and not a bug: the model emits a
  single deterministic sample (`sample_0` only, `sample` dimension of length 1 in the
  `.nc`), and CRPS of a point mass is the absolute error. For the same reason both
  coverage figures are 0.0 — there is no predictive interval to cover anything. Any
  comparison of this model against a probabilistic one on CRPS or coverage is comparing
  different kinds of object.
- **The model predicts negative case counts.** 26 of 459 forecasts are below zero (min
  −35.4). This is what triggers the `RuntimeWarning: invalid value encountered in log1p`
  during `export-metrics`, so the `*_log1p` metrics are computed over some NaNs. Expected
  for an unconstrained linear regression on counts, but it means `crps_log1p` and the
  log1p Winkler scores are not fully trustworthy.
- **Scale mismatch.** Observed cases average 153 and peak at 1943; forecasts span −35 to
  92. The model is a global (pooled across all 17 provinces) linear regression on
  rainfall and temperature with no location term, no population offset and no
  autoregression — the README says outright it is "not meant to accurately capture any
  interesting relations". MAE 172.8 against a mean of 153.1 should be read as "this
  model has essentially no skill here", which is the intended behaviour of a
  demonstration model, not a finding about CHAP.
- **17 locations × 9 test periods × 3 horizons × 1 sample = 459 forecast cells**; the 336
  `sample_count` reflects non-missing observed values.

## Reproducibility

`scripts/run_route.sh` runs the whole thing from scratch. I ran it end to end after
writing it and it reproduced `eval_metrics.csv` byte-identically — the pipeline is
deterministic (OLS has no seed).

Raw CHAP output kept in `results/`: `eval.nc`, `eval.html` (2.8 MB interactive plot),
`eval_metrics.csv`, plus `validate.log`, `eval_run.log`, `export_metrics.log`.
`results/chap_run_artifacts/` holds what CHAP actually handed the model and got back for
the final run — `training_data.csv`, seven `historic_data_*.csv`, seven
`future_data_*.csv`, seven `predictions_*.csv`, `model_configuration_for_run.yaml`
(empty config) and the resolved `uv.lock`. That is the evidence for the
"covariates really were delivered" claim above.

## What I would tell the next person

1. Read the model's own README first. For a dhis2-chap example repo it is likely to
   contain the exact command, and it is likelier to be right than anything else.
2. Keep the CSV and GeoJSON together with the same basename.
3. Ignore "column X not used by the model" warnings unless the run actually fails.
4. Budget a separate step for metrics — `chap eval` gives you a file, not an answer.
5. Read the WARNING lines in the eval log. The dropped region was in there.

## Things I got wrong, collected

- Predicted that the undeclared-covariate warnings would break the run. They did not.
- I logged step 17 (the evaluation-workflow docs page) as a `resource` at a point when I
  had only seen it *linked* from the model README, not read it. That was sloppy: the log
  spec says a `resource` is something you read. I corrected it by actually reading the
  page afterwards (step 23) so the row is true. It confirmed `chap export-metrics` and
  lists five plot types, but taught me nothing I had not already got from `chap --help`,
  so it stays `discarded`.
- No model modification was necessary, so there is **no** `results/model_modifications.diff`.
