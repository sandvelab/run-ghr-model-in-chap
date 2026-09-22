# Claim

What does it take to find out how to run the chapkit-based model chapkit_ghr_model through CHAP, and what does running it on the Lao data yield?

## Children

kind: sub-analyses
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

Yielded by `results/discovery_log.tsv` (46 rows), `results/discovery_notes.md`, and the two
evaluations CHAP wrote to `results/eval_lao_ghrmodel.nc` / `eval_metrics.csv` and
`results/eval_lao_ghrmodel_firstrun.nc` / `eval_metrics_firstrun.csv`.

1. **The route reached an evaluation, but not as published.** As logged: 10 resources
   consulted (9 used), 17 commands run of which 2 failed, 3 blockers hit and 1 left
   unresolved, **5 dead ends**, 66.2 minutes in total and 52.5 to `evaluation_complete`. Every
   milestone except `model_runs_standalone` and `route_abandoned` was reached. These are the
   as-logged numbers; `../04_comparison` also computes them under a normalisation applied
   identically to both routes, because the two logs code some acts differently.

2. **The platform and the model do not fit together at the version each is published at, and
   the route completes only through an interposition.** chap-core 2.1.0 pins chapkit 1.1.0 and
   validates a chapkit service's `/api/v1/info` with that version's `MLServiceInfo`, declared
   `extra="forbid"`. The model is built on chapkit 2.0.0, whose `/api/v1/info` adds
   `git_revision`, `chapkit_version` and `servicekit_version`. Every probe therefore fails
   validation, and CHAP reports

   > `ValueError: URL http://localhost:8000 ... could not be reached as a chapkit service`

   while the endpoint is visibly returning `200 OK` on the line above. The message is wrong
   about what failed and about why. The documented escape hatch,
   `--run-config.is-chapkit-model`, only skips the probe: the same validation error then
   surfaces from `CHAPKitRestAPIWrapper.info()`. The pinned commit is, as it happens, the one
   that *added* `git_revision` to the payload.

   `scripts/info_shim.py` — a stdlib reverse proxy stripping exactly those three keys from
   that one response — is what made the route complete. Neither model nor platform was
   modified, and upgrading chapkit inside chap-core's environment was rejected because it
   would change the platform under test. **Every statement that route A reached an evaluation
   is conditional on that shim.**

3. **The advertised prebuilt image is not publicly pullable.** `docker pull
   ghcr.io/chap-models/chapkit_ghr_model:latest`, which the README and a badge advertise,
   returns 403 on an anonymous token. The image had to be built from the pinned checkout:
   ~22 minutes and 4.98 GB on this arm64 host, under `linux/amd64` emulation, because R-INLA
   is amd64-only.

4. **The working invocation**, with no `--model-configuration-yaml` so that the service
   applies its own published schema defaults (`rainfall` + `mean_temperature`, bym2/rw1/iid,
   1000 draws):

   ```
   chap eval --model-name http://localhost:8010 --run-config.is-chapkit-model \
             --dataset-csv <copy of the Lao csv> \
             --output-file results/eval_lao_ghrmodel.nc \
             --backtest-params.n-splits 7 --backtest-params.n-periods 3 \
             --backtest-params.stride 1 --plot
   chap export-metrics --input-files results/eval_lao_ghrmodel.nc --output-file results/eval_metrics.csv
   ```

   The spatial effect really was fitted on the supplied geometry: `service.log` records
   `f(spatial_id, model='bym2', graph=g, ...)`. The sibling-GeoJSON rule — that CHAP finds
   polygons by matching the CSV's stem — is stated **only** in the docstring of the installed
   `chap_core/cli_endpoints/evaluate.py`, nowhere in `--help`.

5. **CHAP's unused-covariate warnings are wrong here too.** `chap eval` warns that `rainfall`
   and `mean_temperature` are not used by the model; they are. `warn_unused_covariates()`
   compares against the empty configuration CHAP sent and cannot see the service-side
   defaults. The warning is correct only for `mean_relative_humidity`.

6. **The scores, and why they are not to be quoted precisely.** From `results/eval_metrics.csv`:
   MAE 133.28, CRPS 162.42, RMSE 273.65, coverage 10–90 0.836, coverage 25–75 0.667, over
   336000 samples. From `results/eval_metrics_firstrun.csv`, an **identical invocation an hour
   earlier**: MAE 130.00, CRPS 159.99, RMSE 262.17, coverage 10–90 0.824. The 2–4 % spread is
   R-INLA's own non-determinism, which the model's README states, so nothing here should be
   quoted to more than two significant figures. Both runs are kept for exactly that reason.
   The default backtest puts all 7 splits inside 2010 and covers 17 of the 18 admin units;
   `LA-VI` is dropped by CHAP for having no target values at all. The plan's §2 rules out
   comparing these scores against route B's.
