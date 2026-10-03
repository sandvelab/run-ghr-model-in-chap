# Claim

What does it take, working only from public material, to find out how to run the stated model through the stated route and to actually run it, until CHAP has written an evaluation on the Lao admin-1 monthly data? Logged as it happens.

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_

**The route completes and the model runs as published, but only after a workaround for the
image download.** CHAP wrote an evaluation twice: by hand during discovery (`results/eval.nc`,
`results/metrics.csv`) and again from the route's own script in a clean shell
(`results/clean_run/`, exit 0) *(`provenance/evaluation.md`, `provenance/route_run.md`)*.

**The working invocation** *(`results/discovery_notes.md`, `scripts/run_route.sh`)*:

```
curl -fsSL https://raw.githubusercontent.com/winterop-com/chaps/main/install.sh | sh -s -- --dir <bin>
chaps run https://github.com/chap-models/chapkit_ghr_model --port 5060
chap eval --model-name http://localhost:5060 --dataset-csv chap_LAO_admin1_monthly.csv \
     --output-file eval.nc --run-config.is-chapkit-model
chap plot-backtest --input-file eval.nc --output-file evaluation_plot.html
chap export-metrics --input-files eval.nc --output-file metrics.csv
```

chaps recognises the repository URL as its marketplace model `chapkit_ghr_model` and serves
its pinned image `sha-dfb2e3f` (0.1.3, chapkit 2.2.0). The loaded image's id is the published
config digest *(`results/image_id.txt`)*. chaps replaces the two `docker` commands of
iteration 3; the evaluation is still the `chap` CLI's.

**chaps' own documentation stops before the evaluation.** Its agent page (`docs/ai.md`)
covers serving the model and a backtest on sample data the model generates itself, not an
evaluation on one's own dataset. The `chap eval` step came from `chap eval --help` and the
same chap-core pages iteration 3 used. The agent also read one installed chap-core source file
(`cli_endpoints/_common.py`) to confirm the GeoJSON is picked up beside the CSV *(log rows 5,
9, 18, 20–21)*.

**The image download failed through chaps on this link** *(log rows 24–32,
`results/chaps_run_attempt1.log`)*. ghcr.io kept cutting the 1.42 GB layer. chaps pulls the
image twice (a uid probe, then Compose), Docker discards a partial layer when a pull fails, and
after 93 minutes `chaps run` stopped with "fix that, then … tries again". The agent fetched the
same image with resumable, digest-checked `curl` (`scripts/fetch_image_oci.sh`) and loaded it;
`chaps run` then started the model in 2 s. The model was not changed. A second, smaller defect:
when its uid probe failed, chaps carried on and planned to chown the model's data volume to a
guessed `1000:1000` (`results/chaps_run_attempt1.log`, line 125). That run then failed on the
download anyway; in the run that worked, the probe found the image locally and no guess was made.

**Things that do not hold** (from the notes; none blocking):
- CHAP warns that `rainfall` and `mean_temperature` are unused; the model's log shows both used.
- `chaps doctor` passed a host with 14.4 GB free disk although chaps' docs ask for ~25 GB.
- `LA-VI` is dropped with only a log warning (17 of 18 locations evaluated).

**What the evaluation reported** *(`results/metrics.csv`, `results/clean_run/metrics.csv`)*.
CHAP's defaults (7 splits, 3 periods). Manual run: CRPS 149.2, MAE 124.1, RMSE 238.9,
coverage 10–90 0.815. Script run: CRPS 149.8, MAE 127.7, RMSE 244.3, coverage 10–90 0.815.
Iteration 3 (0.1.2, without chaps) reported CRPS 151.4 and 151.0: the same model behaviour,
as the code diff between the pins suggests (`Archive/model-route-a-chaps/diff-stat-since-it3-pin.txt`).

**What it cost the agent** *(`results/agent_usage.tsv`)*: 178,763 tokens and 103 tool calls
in all; 143,158 tokens when the first evaluation was written (iteration 3: 139,417). Of 6.5 h
wall-clock, about 3.0 h was the image download and about 2.8 h the host asleep.

**Untested branch**: the clean-shell run found the image already in Docker, so the download
step did not run inside it.
