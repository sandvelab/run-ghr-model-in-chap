# Claim

What does it take to find out how to run the published model minimalist_example_uv through CHAP, and to actually run it, working only from public material? The route is taken until CHAP has written an evaluation of the model's predictions on the Lao admin-1 monthly data, and what it took is logged as it happens.

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(Each belongs in the claim collection under `Human-AI-collaboration/claims/` with a pointer
to the result grounding it.)_

**The route completes, and the model runs as published.** CHAP wrote an evaluation of
`minimalist_example_uv` on the Lao admin-1 monthly data. The model was not modified and
nothing was interposed; the only workaround in the route is a command-line flag that avoids a
defect in the platform, not in the model.

**Nothing had to be built.** `minimalist_example_uv` is already a CHAP model: it ships an
`MLproject` file declaring `uv_env: pyproject.toml` and `train`/`predict` entry points, so
CHAP runs it through its command-line runner and `uv` builds the model's environment on the
host. **No container is involved at any point** — Docker was confirmed to be running and was
never invoked (`results/discovery_log.tsv`; the resolved environment is kept as
`results/chap_run_dir/uv.lock`).

**The working invocation**, run from inside the model directory:

```
chap eval --model-name . \
          --dataset-csv <dir>/chap_LAO_admin1_monthly.csv \
          --output-file <out>/eval/eval.nc --plot
chap export-metrics --input-files <out>/eval/eval.nc --output-file <out>/eval/metrics.csv
```

**The model's own README carried a working invocation**, and it still worked despite its own
caveat that it had been verified against earlier chap-core versions. Four resources were
opened and all four contributed; two of them are the model's repository page and its README.

**One command failed in the whole route, and the fault is the platform's.**
`chap sanity-check-model --model-url .` dies on a clean chap-core 2.3.1 with
`FileNotFoundError: .../site-packages/example_data/hydromet_5_filtered.csv` — it defaults to a
bundled dataset that the wheel does not ship. Passing `--dataset-path` with the Lao CSV
sidesteps it and the check then passes. This is a packaging defect in chap-core, not a
property of the MLproject route, and it is worth reporting upstream.

**What the evaluation reported** *(`results/eval/metrics.csv`)*. 17 of 18 locations — CHAP
rejected `LA-VI`, which has no target values — over 7 rolling splits, 3-period horizon, one
retrain, `climatology` future weather, all CHAP defaults. MAE 171.96, RMSE 358.93, CRPS
171.96, MAPE 383.16, **coverage 10–90 exactly 0.0**. **These are not compared against any
other route** (plan §2).

**The zero coverage is not a bug in the evaluation; it is what the model is.** CRPS equals MAE
to the last digit and both coverage figures are zero because the model emits a single
deterministic sample: a point prediction has no spread for an interval to cover. The plotted
values show it directly — `q_10` through `q_90` are the same number in every row
(`results/eval/evaluation_plot.tsv`). The `log1p` metrics additionally raise
`invalid value encountered in log1p`, because an ordinary least-squares fit predicts negative
case counts.

**The recipe was verified twice**, under `env -i` from `/` with every inherited variable
stripped and `chap` off the path, so the script's own chap-core bootstrap actually executed.
Both runs completed in about 50 seconds and produced metrics identical to the hand run. One
branch is unverified and recorded as such: the `curl … astral.sh/uv/install.sh` path never
fired, because running it would have upgraded the host's `uv` as a side effect.

**CHAP executes the model somewhere else than where you point it.** It copies the whole model
directory to a timestamped working directory and runs there, so the per-split
`training_data.csv`, `historic_data_*.csv`, `future_data_*.csv` and `predictions_*.csv` — what
the model was actually handed and what it actually returned — land in that copy and nowhere
near the NetCDF. That tree is kept in full as `results/chap_run_dir/`.
