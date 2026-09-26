# Provenance — the evaluation, as run by hand down the route (iteration 3)

result: results/manual_run/eval.nc
          sha256:56fe37eb421c8faa641e1d6e192f508e98308f025840aee389c4f84569469f9e
        results/manual_run/eval.html
          sha256:79920796e84510c0a77ce1c4af0fea4bbc588075c27ab7236c381d3e0339299a
        results/manual_run/evaluation_plot.html
          sha256:62e75d9e3ac7886ef9b4d1db237b8ff9e1b7b46fb5a6b6a4100a17daa850e87d
        results/manual_run/evaluation_plot.png
          sha256:c2e8e16089fba0e8c53c196b264fb86d273e33754f4fd47f190f035d02a78457
        results/manual_run/evaluation_plot.tsv
          sha256:f05d34d56e26e995c1b3846800a3b501019afcbd7dd1f0f917dc3e66218a6f8c
        results/manual_run/metrics.csv
          sha256:de225017f9b842b1d3525f5e6b85aec3034acaf3132a3037c4c689ba72dddd99
        results/manual_run/chap_eval.stdout
          sha256:bf121879fa582392b31524ee52305787ad320e3719369297dee2f91114260c0e
        results/manual_run/service.log
          sha256:c4dfb0e1303636d5bbb53216fd8feb0e0aa25b04f465cbabe7aa5d6e22bf5131
        results/manual_run/service_info.json
          sha256:8ba11500eb58cb6cdf3ef16e9b270fe9db004ca92e0d5597b0ad63c5249cfd8b
        results/manual_run/input/chap_LAO_admin1_monthly.csv
          sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        results/manual_run/input/chap_LAO_admin1_monthly.geojson
          sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
script: scripts/evaluation_plot.py
          sha256:6545e9db0388c292a653393527473b45bec3b191742170a57935099f1806df82
invocation: docker pull --platform linux/amd64 ghcr.io/chap-models/chapkit_ghr_model:sha-a9532c7 ; docker run -d --platform linux/amd64 -p 8765:8000 --name ghr-route-a <image> ; chap eval --model-name http://localhost:8765 --dataset-csv results/manual_run/input/chap_LAO_admin1_monthly.csv --output-file results/manual_run/eval.nc --run-config.is-chapkit-model --plot ; chap plot-backtest --input-file eval.nc --output-file evaluation_plot.html (and .png) ; chap export-metrics --input-files eval.nc --output-file metrics.csv ; then environment/env/bin/python scripts/evaluation_plot.py for evaluation_plot.tsv (run by the orchestrator, after the agent)
inputs: results/manual_run/input/chap_LAO_admin1_monthly.{csv,geojson}, copies of Archive/data-lao/ (checksums identical, route_run/input_sha256.txt)
environment: as discovery.md; the image reports git_revision a9532c7, version 0.1.2, chapkit 2.1.2 (service_info.json)
seeds: none can be set; see discovery.md
commit: b524390
instructions-commit: d2459b1
node: analysis/09_routeA_iteration3/01_discovery
produced: 2026-09-26
alternatives-considered: building the Dockerfile locally (make build), kept by the agent as a fallback and not needed — the published image now pulls anonymously; running the model from its directory without Docker, rejected by the agent because it needs R, INLA and GHRmodel on the host. --run-config.log-file was passed and wrote nothing; stdout was kept instead
agency: agent-autonomous (the discovering agent); agent-autonomous (the orchestrator's plot-value extraction)
information: agent-retrieved
