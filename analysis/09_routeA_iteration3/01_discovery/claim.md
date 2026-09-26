# Claim

What does it take, on chap-core 2.3.1 with chapkit 2.1.2, to find out how to run chapkit_ghr_model at a9532c7 through CHAP and to actually run it, working only from public material, until CHAP has written an evaluation on the Lao admin-1 monthly data? Logged as it happens.

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_

**The route completes, the model runs as published, and nothing had to be worked around.**
CHAP wrote an evaluation twice: by hand during discovery (`results/manual_run/`) and again
from the route's own script in a clean shell, starting with no model image
(`results/route_run/`, exit 0). No command failed, no blocker was hit, and there were no dead
ends (`../03_versusIteration2/results/effort_normalised.tsv`).

**The working invocation** *(`results/discovery_notes.md`)*:

```
docker pull --platform linux/amd64 ghcr.io/chap-models/chapkit_ghr_model:sha-a9532c7
docker run -d --platform linux/amd64 -p 8765:8000 ghcr.io/chap-models/chapkit_ghr_model:sha-a9532c7
chap eval --model-name http://localhost:8765 --dataset-csv chap_LAO_admin1_monthly.csv \
     --output-file eval.nc --run-config.is-chapkit-model --plot
chap plot-backtest --input-file eval.nc --output-file evaluation_plot.html
chap export-metrics --input-files eval.nc --output-file metrics.csv
```

**The published image is used, pinned by commit.** It pulls anonymously, and the image
publishing workflow tags each image `sha-<commit>`. The service reports `git_revision a9532c7`,
version 0.1.2 and chapkit 2.1.2 (`results/manual_run/service_info.json`). No build ran.

**The route was reached through CHAP's own documentation.** Twelve resources were read and
eleven used. Among them are three chap-core pages at tag `v2.3.1`: `docs/chap-cli/eval-reference.md`,
`docs/chap-cli/evaluation-workflow.md` and `docs/external_models/chapkit.md`. Between them
they carry the service-URL form of `chap eval`, the convention that the GeoJSON sits beside
the CSV with the same stem, and the follow-on `plot-backtest` and `export-metrics` steps. No
installed library source was read. The model's README still never mentions `chap eval`.

**Things that do not hold** (all from the notes, and none of them blocking):
- CHAP warns that `rainfall` and `mean_temperature` are unused, but the service log shows both
  in the fitted formula, beside the `bym2` spatial term.
- `--run-config.log-file` writes nothing.
- `LA-VI` is dropped with only a log warning.
- `metrics.csv` names the model by its URL, not its id.

**What the evaluation reported.** 17 of 18 locations and CHAP's defaults (7 splits, 3
periods, stride 1). Manual run: CRPS 151.4, MAE 128.6, RMSE 251.7, coverage 10–90 0.815.
Script run: CRPS 151.0, MAE 125.6, coverage 10–90 0.818. R-INLA is not bit-reproducible, so
these read as a spread.

**Untested branches**:
- The script's `uv` install of chap-core, for a host where `chap` is absent, did not run.
- The script fetches the data from a branch of `dhis2/climate-health-data`, not from the
  pinned commit. It was byte-identical on the day.
