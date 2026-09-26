# Provenance — the route reproduced by its own script in a clean shell (iteration 3)

result: results/route_run/eval.nc
          sha256:da415614bbf8bc3553672eec8660eb2eae8ae202f3888e54c287b25c80bd51f6
        results/route_run/eval.html
          sha256:4f54bb70d0d11e7c9aef593d727c22f793357ebc5ca0d4f37fe18924ffa6d521
        results/route_run/evaluation_plot.html
          sha256:d5031775a977a3d41029307d44ca80201ebbd7dd171cf503a335d4805ea1309a
        results/route_run/evaluation_plot.png
          sha256:c22fdc0c92da012e3b6524d815ddaa3ceaa30b265670ac8c564a066a48358d78
        results/route_run/evaluation_plot.tsv
          sha256:786bb7d748dbe828265f1b12fc7e905ab7dc94248eec1b201db2c49269d5d95d
        results/route_run/metrics.csv
          sha256:95752408c3451106362f9ee32957a1c3395a1e4dbcfdcb50999fdc63f64304ce
        results/route_run/chap_eval.log
          sha256:15342be3ac5a763b7b03a181d5960012fb720fee4d79f77e1a7bdfd6540cd1cb
        results/route_run/service.log
          sha256:bad78b6330d802d07c9de5bcc026e11ebcd178f6d21544f1ba1a22f23986fe03
        results/route_run/service_info.json
          sha256:8ba11500eb58cb6cdf3ef16e9b270fe9db004ca92e0d5597b0ad63c5249cfd8b
        results/route_run/image_id.txt
          sha256:272cc3303b20140437b4045f5de42a106428eff1368239275ac011cd817c80ba
        results/route_run/input_sha256.txt
          sha256:35e460630ac52beb64bfede56d8d77e02385bad19c06643558713534154c8f0a
        results/run_route_clean_shell.out
          sha256:8058ef9b60c8c769d4fbffb988706440d449ee3849380b495fa454265ba21dce
        results/route_run/input/chap_LAO_admin1_monthly.csv
          sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        results/route_run/input/chap_LAO_admin1_monthly.geojson
          sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
script: scripts/run_route.sh
          sha256:8feb76a67074405466c131b47bde8c805cade9d6d68e240e517eeedbda0af282
        scripts/evaluation_plot.py
          sha256:6545e9db0388c292a653393527473b45bec3b191742170a57935099f1806df82
invocation: docker rmi ghcr.io/chap-models/chapkit_ghr_model:sha-a9532c7 ; cd /tmp && env -i HOME=$HOME PATH=/usr/bin:/bin bash <node>/scripts/run_route.sh  (exit 0, about 12 min), run by the discovering agent; then scripts/evaluation_plot.py by the orchestrator
inputs: the Lao CSV and GeoJSON fetched by the script from https://raw.githubusercontent.com/dhis2/climate-health-data/refs/heads/main/lao/ — a branch, not the pinned commit; input_sha256.txt shows them byte-identical to Archive/data-lao/ on the day. A later run may fetch different data, and DATA_DIR pins it to the archive
environment: as discovery.md
seeds: none can be set; the script run's metrics differ from the manual run's in the third significant figure
commit: b524390
instructions-commit: d2459b1
node: analysis/09_routeA_iteration3/01_discovery
produced: 2026-09-26
alternatives-considered: the script's fallback that installs chap-core with uv when chap is absent was not exercised — chap is in ~/.local/bin, which the script adds to PATH itself. Recorded as an untested branch, not as verified
agency: agent-autonomous
information: agent-retrieved
