# Provenance — the evaluation, as run by hand down the route

result: results/eval/metrics.csv
        sha256:0ca96e54c693d0f033c199bf5cfbbdaf25c9d747981d903fa9fd88facb229673
        results/eval/evaluation.nc
        sha256:d8deeb37db657377c2c82f95d35acc9abe0016116cfdf6f59d7d71c139cfab1d
        results/eval/evaluation.html
        sha256:d516e847cbc552cb19d76a4929810c3df1f1ebc5573a9e23b72c92f2cd542b50
        results/eval/predicted_vs_actual.html
        sha256:790b4e97f22ab1815ec89636db2a14d8bdd34683006adec694db2baf8eb9a248
        results/eval/chap_eval.log
        sha256:365806e72c4561ec75d867f7db8cfea8c294baaebb09fcfb1c3181236ae2870e
        results/docker_build.log
        sha256:7c8c5f7c4fdd44968333d3973617678c0d2fbfdd65fce0b1ed8926fed53c7dc3
        results/ghcr_pull_attempt.log
        sha256:851b213525bdb682ac45196f14d526394adef1c62b24108d9abf987e525a4b5d
script: none of this project's — CHAP and the published model, both run as they come
invocation: docker build --platform linux/amd64 -t chapkit-ghr-model:latest . ;
  docker run -d --platform linux/amd64 -p 8000:8000 chapkit-ghr-model:latest ;
  chap eval http://localhost:8000 chap_LAO_admin1_monthly.csv evaluation.nc
      --run-config.is-chapkit-model --plot ;
  chap export-metrics --input-files evaluation.nc --output-file metrics.csv ;
  chap plot-backtest evaluation.nc predicted_vs_actual.html --plot-type predicted_vs_actual
inputs: ../../Archive/data-lao/chap_LAO_admin1_monthly.csv  sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        ../../Archive/data-lao/chap_LAO_admin1_monthly.geojson  sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
        the model at chap-models/chapkit_ghr_model, cloned fresh by the route and built from
        its own Dockerfile; the pinned copy is ../../Archive/model-route-a/
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
alternatives-considered: pulling the published GHCR image rather than building the Dockerfile.
  This was the route's first choice — the README offers both, and the published image is the
  artefact a user would actually get — and it was forced away from it: the image returns 401
  to an anonymous pull (`results/ghcr_pull_attempt.log`). Building locally is a workaround
  *outside* the model and is logged as such. Running the amd64 image natively was not
  available on an arm64 host, so it runs under emulation, which the model's own README says is
  correct but slow; that blocker is logged `open` and never resolved. All CHAP defaults were
  taken — 7 splits, 3 prediction periods, 1 retrain, `climatology` future weather — rather than
  tuned, because the route is the object of study and a tuned split scheme would be this
  project selecting on the data.
  **The build-time figure is not a cold build.** The host's BuildKit layer cache was already
  warm before the route started (7 of 8 layers cached here, 8 of 8 in the verification run),
  so the clone-and-compile path through R-INLA was never exercised. Recorded rather than
  worked around; deleting a cache belonging to the human's other work was not the agent's to do.
contamination: the discovering agent was a fresh agent given the plan's §4 brief and nothing
  else. It was told explicitly which three paths in this repository it could read and that
  `CLAUDE.md`'s instruction to read `readme-at-start.md` was overridden, because that file
  names both models and would have told it the answer. It reports one incidental exposure of
  its own: `docker images` listed an unrelated chapkit model image belonging to the human's
  other work, which it did not inspect or use. The **orchestrating** agent is separately and
  fully contaminated — it holds a previous iteration's findings for both routes — and its
  contribution here was the brief and the storage of what came back, not the route.
agency: `agent-autonomous` (every choice in the route); `human-set` (the data, the model and
  the platform)
information: `agent-retrieved`

---

## Appended 2026-09-22 — the two figures rendered to raster

result: results/eval/evaluation_plot.png
        sha256:930493efe23a66d8309fb117cca033a62b0386f8079cf4608cd644245adb7190
        results/eval/predicted_vs_actual.png
        sha256:111c21d6d2f458604d09067b00e3118c48dca6f5fbd466c4fecf2dabaf02d66a
script: none — a rendering of the two HTML files CHAP wrote, not a new plot
        results/eval/evaluation.html  sha256:d516e847cbc552cb19d76a4929810c3df1f1ebc5573a9e23b72c92f2cd542b50
        results/eval/predicted_vs_actual.html  sha256:790b4e97f22ab1815ec89636db2a14d8bdd34683006adec694db2baf8eb9a248
invocation: the two HTML files served over http://127.0.0.1:8731 from the repository root and
  opened in Chrome at a 1400x1000 window; a viewport screenshot of each, converted to PNG with
  `sips -s format png`, and the predicted-versus-actual one cropped to its content with
  `sips -c 410 1010`
inputs: the two HTML files above, as CHAP wrote them
environment: none of this project's — Chrome and macOS `sips`
seeds: none
commit: 0edf636
node: analysis/02_routeA_chapkit
produced: 2026-09-22
alternatives-considered: re-plotting the evaluation from `evaluation.nc` with a plotting
  library of this project's own. Rejected: the figure the project is asked to show is **CHAP's
  default output**, and a re-plot would be this project's picture of CHAP's numbers rather than
  CHAP's own. It would also have meant adding a plotting library to the pinned analysis
  environment, which currently declares no dependencies, for a figure that CHAP already draws.
  The cost of rendering instead is that these PNGs are a **viewport** capture: CHAP's backtest
  grid is 17 locations by 7 splits and the raster shows the first two locations across the
  first three splits. The HTML beside it is the complete figure and is what the overview links
  to; the raster is what it embeds. Rule 7's obligation is met by the values behind the plot
  being stored in full as `evaluation.nc` and `metrics.csv`, which are CHAP's own outputs.
agency: agent-autonomous
information: agent-retrieved

---

## Appended 2026-09-22 — the plotted values, and one figure withdrawn

result: results/eval/evaluation_plot.tsv
        sha256:cc4b81266e56b2678bf24dbe980d56afebf67e47e881fcb33690b7e73fd8d43e
script: scripts/evaluation_plot.py
        sha256:0b21c0ae88084bd4b8442f778309fe44495f12d9aa79901e404812b2aa0f7b48
        ../../AI-internal/useful-scripts/vega_values.py
        sha256:f5bb18ac091d6848b2f3d16821e71f0b81058a32468f493731c05d46a3ff910c
invocation: ../../environment/env/bin/python scripts/evaluation_plot.py
inputs: results/eval/evaluation.html  sha256:d516e847cbc552cb19d76a4929810c3df1f1ebc5573a9e23b72c92f2cd542b50
environment: environment/ (project main)
seeds: none
commit: fa3d04d
instructions-commit: d2459b1
node: analysis/02_routeA_chapkit
produced: 2026-09-22
alternatives-considered: reading the plotted values out of `evaluation.nc` instead. Rejected
  because the obligation is to store the values *behind the figure*, and the NetCDF is what
  CHAP computed rather than what it drew — the two could diverge and nothing would show it.
  Reading the figure's own inline Vega-Lite specification means the table and the picture
  cannot disagree. 9520 rows, one per location x period x horizon x split.
  **`results/eval/predicted_vs_actual.png` was withdrawn** and no longer exists. It was a
  raster of `chap plot-backtest`'s scatter, which is a second figure from a second command;
  keeping it would have obliged a second plotted-values file and a second plotting script for
  a figure the project does not use. The HTML it was rendered from is kept, because *that*
  command having to exist at all is one of this route's findings.
agency: agent-autonomous
information: agent-retrieved
