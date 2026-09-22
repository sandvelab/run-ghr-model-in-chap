result: results/eval_lao_ghrmodel.nc, results/eval_lao_ghrmodel.html, results/eval_metrics.csv
        results/eval_lao_ghrmodel_firstrun.nc, results/eval_metrics_firstrun.csv
        results/chap_eval.log, results/service.log, results/docker_build.log
        results/service_info.json, results/model_schema_example.yaml
script: scripts/run_route.sh
        sha256:2b3aaaf124ceb82e5427d1d122c30dfbe1adcdde0026e8a60889c233d18852da
        scripts/info_shim.py
        sha256:3404a5dc1e655a7fa116b41e15a0e5e82f416606575765efe9779f837f80a7be
        scripts/log.sh
        sha256:606d0af69404d1246c88ef0fa4ff75906c57ee6c1bddd62161eb07ff6c211fce
invocation: bash scripts/run_route.sh
            (which runs, in order: docker build --platform linux/amd64 --build-arg
             GIT_REVISION=60b16a2e929405ce95fae2043a63d7e27292ca0f -t chapkit-ghr-model:60b16a2 ;
             docker run -d --platform linux/amd64 -p 8000:8000 ; python3 scripts/info_shim.py
             8010 http://localhost:8000 ; chap eval --model-name http://localhost:8010
             --run-config.is-chapkit-model --dataset-csv <copy of the Lao csv>
             --output-file results/eval_lao_ghrmodel.nc --backtest-params.n-splits 7
             --backtest-params.n-periods 3 --backtest-params.stride 1 --plot ;
             chap export-metrics --input-files results/eval_lao_ghrmodel.nc
             --output-file results/eval_metrics.csv)
inputs: ../../Archive/data-lao/chap_LAO_admin1_monthly.csv  sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        ../../Archive/data-lao/chap_LAO_admin1_monthly.geojson  sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
        chap-models/chapkit_ghr_model @ 60b16a2e929405ce95fae2043a63d7e27292ca0f, cloned by the
          script; the archived copy of the same commit is at ../../Archive/model-route-a/repo
environment: the platform's own -- chap-core 2.1.0 (Archive/platform-chap/) -- plus the model's
  own Docker image, built locally from the pinned commit for linux/amd64 (4.98 GB, ~22 min on
  this arm64 host under emulation). Deliberately NOT environment/ (project main): what a route
  installs, and how, is part of what is measured. The build log is results/docker_build.log.
seeds: project 20260921; component none. No seed was set and none could be: the model fits with
  R-INLA, which the model's own README states is not bit-reproducible even at nthreads=1. Two
  identical invocations were therefore both kept (see alternatives-considered).
commit: 1c032d2
instructions-commit: d2459b1
node: analysis/02_routeA_chapkit
produced: 2026-09-21

intervention: **the route did not complete as published.** chap-core 2.1.0 pins chapkit 1.1.0
  and validates a chapkit service's /api/v1/info with that version's MLServiceInfo, which
  declares extra="forbid". The model image is built on chapkit 2.0.0, whose /api/v1/info adds
  git_revision, chapkit_version and servicekit_version, so every probe fails validation and
  chap-core reports "URL ... could not be reached as a chapkit service" while the endpoint is
  visibly returning 200. --run-config.is-chapkit-model only skips the probe; the same
  ValidationError then surfaces from the wrapper. scripts/info_shim.py is a stdlib reverse
  proxy that strips exactly those three keys from that one response body and passes everything
  else through untouched. Neither the model nor the platform was modified. This interposition
  is a finding about the route, not a detail of running it, and every statement about route A
  reaching an evaluation is conditional on it.
alternatives-considered: upgrading chapkit inside chap-core's own virtual environment to 2.0.0
  would have removed the need for the shim and was rejected -- it changes the platform under
  test, and the incompatibility is itself the finding. Pulling the prebuilt image the README
  advertises (ghcr.io/chap-models/chapkit_ghr_model:latest) was the first choice and failed
  with 403 on an anonymous token, so the image was built locally, which also guarantees it
  matches the pinned commit. chapkit *directory* mode was rejected because it runs
  `uv run fastapi dev` on the host and the host has no R/INLA. `chap model schema` and
  `chap sanity-check-model` were tried as entry points and abandoned: the former has no
  --run-config override and so cannot reach this model without the shim. No
  --model-configuration-yaml was passed, so the service applies its own published schema
  defaults (rainfall + mean_temperature, bym2/rw1/iid, 1000 draws) -- the model as published
  rather than a configuration chosen here. The backtest was set explicitly to 7 splits x 3
  periods x stride 1, which are chap eval's own defaults.
agency: agent-autonomous (the route was discovered and run by an isolated agent on the §4
  brief); human-pointed (which model repository, which data)
information: agent-retrieved -- the working recipe came from `chap eval --help`, the model's
  README, Makefile and Dockerfile, and the docstring of the installed
  chap_core/cli_endpoints/evaluate.py, which is the only place the sibling-GeoJSON rule is
  stated; the root cause came from reading chap_core/models/utils.py and
  external_chapkit_model.py in the installed platform
