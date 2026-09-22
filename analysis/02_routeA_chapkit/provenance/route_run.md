# Provenance — the route reproduced by its own script

result: results/run_route_verify.log
        sha256:6567e4ff817ee9a5f2e8bf11b6f2d157cd489f3741a4335224689fc5fce29268
        results/route_run/docker_build.log
                sha256:ef5c04528821b7339afd3c7bd7b63acacf488fd7c2ea0661d8d6cfece2692099
        results/route_run/chap_eval.log
                sha256:37bb4440db1e6f446f377d8c77ef0108f5f8526e7f6a2bee95a70851e57e9771
        results/route_run/chap_export_metrics.log
                sha256:2510b7bca2f4b171400aee5fbb96081ffe71199752fefd8d031e3243cdd80664
        results/route_run/chap_plot_backtest.log
                sha256:f3d77a9912e9e285745497023bb6b24c687dccd0e8c70001555a540abb0e1faa
        results/route_run/model_schema.yaml
                sha256:c114df1054d320c528f57e52e996c258e6914dec1f76725cf8fb2c72ac97f510
        results/route_run/evaluation.nc
                sha256:7a8aa94ec30ea8441af8973d4d52c6cabbdf66317c9e201083bd46eab396f274
        results/route_run/evaluation.html
                sha256:a73711c83df83ed6617ac5786e344a75279f6a116e9a5784d3c904926178aa55
        results/route_run/metrics.csv
                sha256:9523d760afc81e4b262f6c0c705ac11ed26b6a36d0dd07239aa423a04fdfec7a
        results/route_run/predicted_vs_actual.html
                sha256:92cce03e617b583953d9acb29019a02eda0d57828af1a08a0b0888fcb746e696
        results/route_run/chap_LAO_admin1_monthly.csv
                sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        results/route_run/chap_LAO_admin1_monthly.geojson
                sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
script: scripts/run_route.sh
        sha256:22315b88ec966ba043f1b66cd853c76164cc66fb6c1ed31a4e9194cb2126e1f2
invocation: env -i HOME="$HOME" PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin \
      bash analysis/02_routeA_chapkit/scripts/run_route.sh
  — run from `/`, with no environment and no working directory inherited
inputs: ../../Archive/data-lao/chap_LAO_admin1_monthly.csv  sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        ../../Archive/data-lao/chap_LAO_admin1_monthly.geojson  sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
        the model, cloned from its public remote by the script itself
environment: none of this project's — the route supplies its own, which is part of what is
  being measured. CHAP is the pinned platform anchor (`chap-core` 2.3.1, `chapkit` 2.1.0,
  `servicekit` 2.0.2); the model runs in a container it builds from its own Dockerfile.
seeds: project 20260921; no component seed reaches this route. The model fits with R-INLA,
  which its own README states is not bit-reproducible, and CHAP offers no seed for a chapkit
  service. Recorded as an absence rather than left unstated.
commit: d37fdcd
instructions-commit: d2459b1
node: analysis/02_routeA_chapkit
produced: 2026-09-22
alternatives-considered: writing the recipe out of the discovery log at the end without
  running it. Refused by the plan's §2b — a recipe that has not been run is not a recipe — and
  the refusal earned its keep: the first attempt under `env -i` failed at preflight because
  `docker` lives in `/usr/local/bin`, which a minimal PATH does not carry. A script assembled
  from the log would have shipped with that defect invisible.
  The script builds the Dockerfile rather than pulling the published image, because the
  published image is not anonymously pullable; and it stages the CSV and the GeoJSON side by
  side in its own output directory, because `chap eval` has no option for the geometry and
  discovers a sibling file with the same stem instead.
  **What this run does not verify**: the container build, which came back 8 of 8 layers cached
  from the host's warm BuildKit cache (`results/route_run/docker_build.log`). Everything after
  the build — serve, evaluate, export metrics, plot — ran for real.
  The two CSV/GeoJSON copies under `results/route_run/` are the staged inputs the script
  created, kept because they are what CHAP actually read.
contamination: the discovering agent was a fresh agent given the plan's §4 brief and nothing
  else. It was told explicitly which three paths in this repository it could read and that
  `CLAUDE.md`'s instruction to read `readme-at-start.md` was overridden, because that file
  names both models and would have told it the answer. It reports one incidental exposure of
  its own: `docker images` listed an unrelated chapkit model image belonging to the human's
  other work, which it did not inspect or use. The **orchestrating** agent is separately and
  fully contaminated — it holds a previous iteration's findings for both routes — and its
  contribution here was the brief and the storage of what came back, not the route.
agency: `agent-autonomous`
information: `agent-retrieved`

---

## Appended 2026-09-22 — re-run by `analysis/run.sh`, and the digests that changed

Every file listed in the section above was rewritten when the whole tree was run end to end
(6m56s for both routes). Those digests described the discovering agent's verification run and
are right about it; these describe the run that is on disk now.

        results/route_run/chap_LAO_admin1_monthly.csv
        sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        results/route_run/chap_LAO_admin1_monthly.geojson
        sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
        results/route_run/chap_eval.log
        sha256:331fd0eca40647c56d869b085b2f453066b211d9995bcf60305f990b7285aff2
        results/route_run/chap_export_metrics.log
        sha256:07b946e29389657bd6931385a8de54e45c463b7a7a84fc413e5c4555dd0af34a
        results/route_run/chap_plot_backtest.log
        sha256:3e446efb32f8e1d62b6a3bc9306a705cffeb1443ace9337b02b1c29f5b04ea1e
        results/route_run/docker_build.log
        sha256:407dc1bd9fae78f5528ca4f0f5cbe11c79d10258016d3410b1bf654e635680b7
        results/route_run/evaluation.html
        sha256:85a690a952479fb4639e8abf1e004cc3d079c1dcc0dfe12094653e0d8acfcf97
        results/route_run/evaluation.nc
        sha256:f8e555681a7153603ea26a049eefb88e4ab93df9b6e49708b645273093a4c20b
        results/route_run/metrics.csv
        sha256:38c97ef155c824b3593da4a6429c06cf52ec6119e1f0b91252314020555c16b0
        results/route_run/model_schema.yaml
        sha256:c114df1054d320c528f57e52e996c258e6914dec1f76725cf8fb2c72ac97f510
        results/route_run/predicted_vs_actual.html
        sha256:8b6368b3816017d48f9de6540cdbd474ac3673c7f72f839051623a30582181c6
        results/run_route_verify.log
        sha256:6567e4ff817ee9a5f2e8bf11b6f2d157cd489f3741a4335224689fc5fce29268
script: scripts/run_route.sh
        sha256:22315b88ec966ba043f1b66cd853c76164cc66fb6c1ed31a4e9194cb2126e1f2
invocation: bash analysis/run.sh — which calls this node's run.sh, which calls the route
environment: as above
commit: fa3d04d
instructions-commit: d2459b1
node: analysis/02_routeA_chapkit
produced: 2026-09-22
alternatives-considered: having the route write to a fresh directory per run so that nothing
  is ever overwritten. Rejected: `analysis/run.sh` has to reproduce the analysis, and a tree
  that accumulates a directory per reproduction stops being reproducible and starts being an
  archive. The hand run in `results/eval/` is the one the reports quote and is never touched
  by a re-run; how far the numbers move between runs is the repeatability node's subject.
  The container build in this re-run was again fully cached (8 of 8 layers), so the cold-build
  path remains unexercised.
agency: agent-autonomous
information: agent-retrieved
