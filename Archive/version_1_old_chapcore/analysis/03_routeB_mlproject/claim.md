# Claim

What does it take to find out how to run the MLproject/uv model minimalist_example_uv through CHAP, and what does running it on the Lao data yield?

## Children

kind: sub-analyses
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

Yielded by `results/discovery_log.tsv` (24 rows), `results/discovery_notes.md`, and the
evaluation CHAP wrote to `results/eval.nc` and `results/eval_metrics.csv`.

1. **The route reached an evaluation, on the first attempt, with no failed command.** The
   effort statistics computed from the log by `../04_comparison` are: 4 resources consulted
   (3 used, 1 discarded), 8 commands run and **0 failed**, 0 blockers, **0 dead ends**, 58.2
   minutes in total and 29.7 to `evaluation_complete`. Every milestone in the closed
   vocabulary except `route_abandoned` was reached.

2. **The working invocation is two commands**, and both came from `chap --help`, `chap eval
   --help` and the model's own README, which carries a literal copy-pasteable `chap eval`
   line and states it was verified against chap-core 2.1.0:

   ```
   chap eval --model-name model/minimalist_example_uv \
             --dataset-csv data/chap_LAO_admin1_monthly.csv \
             --output-file results/eval.nc --plot
   chap export-metrics --input-files results/eval.nc --output-file results/eval_metrics.csv
   ```

   There is **no registration step**: CHAP reads the model's `MLproject` file directly from a
   local directory, and `uv_env: pyproject.toml` is what tells it to build the environment
   with `uv` on the host. **Docker was running and was not needed.**

3. **Four things the documentation does not say, all found by running it.** The GeoJSON has
   no command-line flag — CHAP finds it by looking for a file with the same basename beside
   the CSV, so renaming the CSV silently loses the polygons. `chap eval` prints no metrics at
   all; `chap export-metrics` is a separate step the model's README never mentions. One admin
   unit, `LA-VI`, was **silently dropped** for missing targets across the whole training
   period, so the evaluation covers 17 of 18 units — a warning buried in a long log. And each
   invocation leaves a ~197 MB virtualenv at a doubled path, `runs/<model>/<ts>/runs/<model>/<ts>/.venv`,
   because CHAP computes it relative to the directory it is already inside.

4. **CHAP's own validation cannot be used to check that a model will receive its data.**
   `chap validate` warned that `rainfall`, `mean_temperature`, `mean_relative_humidity` and
   `population` were "present in the dataset but not used by the model". The warning is about
   *declaration*: this MLproject declares no covariates. CHAP delivers the whole dataset
   anyway, which the CSV it wrote for the model
   (`results/chap_run_artifacts/training_data.csv`) shows directly. Taking the warning at face
   value would have produced a wrong conclusion about the platform.

5. **The scores, and why they are not to be compared.** From `results/eval_metrics.csv`:
   MAE 172.77, RMSE 357.52, CRPS 172.77, MAPE 423.60, coverage 10–90 and 25–75 both 0.0, over
   336 samples. CRPS equals MAE exactly and coverage is zero because the model emits a single
   deterministic sample — the CRPS of a point mass *is* the absolute error, and there is no
   interval to cover. The model also predicts negative case counts (26 of 459 forecast cells,
   minimum −35.4), which is what makes the `*_log1p` metrics NaN. Observed cases average about
   153, so an MAE of 172.8 is essentially no skill. This is a demonstration model behaving as
   its README says it will, and the plan's §2 rules out comparing it across routes.

6. **The re-runnable deliverable is `scripts/run_route.sh`**, which re-fetches the model at
   the pinned commit, re-copies the data, validates, evaluates and exports metrics; the agent
   ran it end to end and it reproduced `eval_metrics.csv` byte-identically. It hard-codes the
   absolute path of `Archive/data-lao`, so it is re-runnable on this machine rather than
   portable. That is recorded rather than repaired: it is the artefact the route produced.
