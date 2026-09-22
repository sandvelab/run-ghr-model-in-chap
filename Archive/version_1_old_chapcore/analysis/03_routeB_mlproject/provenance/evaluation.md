result: results/eval.nc, results/eval.html, results/eval_metrics.csv
        results/validate.log, results/eval_run.log, results/export_metrics.log
                results/chap_run_artifacts/future_data_2010-04-01.csv
        results/chap_run_artifacts/future_data_2010-05-01.csv
        results/chap_run_artifacts/future_data_2010-06-01.csv
        results/chap_run_artifacts/future_data_2010-07-01.csv
        results/chap_run_artifacts/future_data_2010-08-01.csv
        results/chap_run_artifacts/future_data_2010-09-01.csv
        results/chap_run_artifacts/future_data_2010-10-01.csv
        results/chap_run_artifacts/historic_data_2010-04-01.csv
        results/chap_run_artifacts/historic_data_2010-05-01.csv
        results/chap_run_artifacts/historic_data_2010-06-01.csv
        results/chap_run_artifacts/historic_data_2010-07-01.csv
        results/chap_run_artifacts/historic_data_2010-08-01.csv
        results/chap_run_artifacts/historic_data_2010-09-01.csv
        results/chap_run_artifacts/historic_data_2010-10-01.csv
        results/chap_run_artifacts/model_configuration_for_run.yaml
        results/chap_run_artifacts/predictions_2010-04-01.csv
        results/chap_run_artifacts/predictions_2010-05-01.csv
        results/chap_run_artifacts/predictions_2010-06-01.csv
        results/chap_run_artifacts/predictions_2010-07-01.csv
        results/chap_run_artifacts/predictions_2010-08-01.csv
        results/chap_run_artifacts/predictions_2010-09-01.csv
        results/chap_run_artifacts/predictions_2010-10-01.csv
        results/chap_run_artifacts/training_data.csv
        results/chap_run_artifacts/uv.lock
script: scripts/run_route.sh
        sha256:aa3bd580399d93f9ecda65adb3077879041c2551e4a22891fc1725eba06bf100
invocation: bash scripts/run_route.sh
            (which runs, in order: chap validate --dataset-csv data/chap_LAO_admin1_monthly.csv
             --model-name model/minimalist_example_uv ; chap eval --model-name
             model/minimalist_example_uv --dataset-csv data/chap_LAO_admin1_monthly.csv
             --output-file results/eval.nc --plot ; chap export-metrics --input-files
             results/eval.nc --output-file results/eval_metrics.csv)
inputs: ../../Archive/data-lao/chap_LAO_admin1_monthly.csv  sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        ../../Archive/data-lao/chap_LAO_admin1_monthly.geojson  sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
        dhis2-chap/minimalist_example_uv @ 5cd8a1267362d945491353fba1c63a408462fa17,
          fetched as a codeload tarball by the script; the archived copy of the same commit is
          at ../../Archive/model-route-b/repo
environment: the platform's own -- chap-core 2.1.0 (Archive/platform-chap/), plus the model
  environment CHAP builds itself with uv from the model's pyproject.toml. Deliberately NOT
  environment/ (project main): what a route installs, and how, is part of what is measured,
  so pinning it centrally would replace the observation with a copy of it. The uv.lock CHAP
  resolved is kept at results/chap_run_artifacts/uv.lock.
seeds: project 20260921; component none -- no seed was set. The model is an ordinary least
  squares fit with no stochastic component, and CHAP exposes no seed flag on `chap eval`.
  That no seed could be set is itself recorded rather than papered over.
commit: 8c3d6d5
instructions-commit: d2459b1
node: analysis/03_routeB_mlproject
produced: 2026-09-21
alternatives-considered: the backtest could have been configured rather than left at
  CHAP's defaults (7 splits, 3-period horizon, stride 1, retrained once); defaults were kept
  because this project measures what it takes to get an evaluation, and a tuned backtest
  would have been a choice made for the route rather than by it. `chap forecast` was
  available and not used: it produces predictions, not an evaluation. Docker was available
  and deliberately not used -- the MLproject declares `uv_env`, so CHAP builds the model
  environment on the host, and forcing a container would have measured a route nobody takes.
  The four `Column 'X' is present in the dataset but not used by the model` warnings were
  treated as a possible blocker and then checked against the CSV CHAP actually wrote for the
  model (results/chap_run_artifacts/training_data.csv), which showed the columns were in fact
  delivered; taking the warnings at face value would have produced a wrong finding about CHAP.
agency: agent-autonomous (the route was discovered and run by an isolated agent on the §4
  brief); human-pointed (which model repository, which data)
information: agent-retrieved -- the invocation came from `chap --help`, `chap eval --help`
  and the model's own README at the pinned commit, all read during the run
