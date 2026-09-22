# Discovery notes — route B, `minimalist_example_uv` as an MLproject directory

Narrative companion to `discovery_log.tsv`. Written as the route was walked.

## The short version

The route had no discovery problem worth the name. The model's own README carries a
working CHAP invocation, that invocation is still valid against the installed
chap-core 2.3.1, and it worked first time on the Lao data with no modification to
anything. From opening the repository page to `eval.nc` on disk was about four
minutes and three substantive commands.

The working invocation, run from inside the model directory:

```
chap eval --model-name . \
          --dataset-csv <dir>/chap_LAO_admin1_monthly.csv \
          --output-file <out>/eval/eval.nc \
          --plot
```

and then, separately:

```
chap export-metrics --input-files <out>/eval/eval.nc --output-file <out>/eval/metrics.csv
```

## What CHAP wants a model to look like, as far as this route reveals it

An `MLproject` file at the root of a directory. It is YAML, and it declares

- `name`
- an environment declaration — here `uv_env: pyproject.toml`
- `entry_points.train` and `entry_points.predict`, each with named `parameters`
  and a `command` template whose placeholders are those parameter names.

`--model-name .` then means "this directory is the model". CHAP's `--help` says
`--model-name` also takes a GitHub URL or a chapkit service URL, so the directory
is one of three shapes it accepts; this route only exercised the directory.

CHAP's contract with the model is entirely file-based and positional-by-name:
it writes `training_data.csv`, `historic_data_<date>.csv` and
`future_data_<date>.csv`, substitutes their paths into the `command` templates,
and reads back the CSV the model writes to `out_file`. The prediction CSV must
carry `time_period`, `location` and one or more `sample_N` columns. Nothing in
the model imports chap-core; there is no SDK to link against.

## Things that were not obvious and had to be found out

**Where the polygons come from.** The run log said `Loading polygons from
.../chap_LAO_admin1_monthly.geojson` although no flag names a GeoJSON and
`chap eval --help` has no polygon option. Reading
`chap_core/cli_endpoints/_common.py` settled it: `discover_geojson()` takes the
`--dataset-csv` path and looks for the same path with `.csv` replaced by
`.geojson`. That is the only reason the Lao boundaries entered the run, and it
means the two data files must sit side by side with matching stems. Anyone who
renames one of them silently loses the polygons.

**`chap eval` does not produce metrics.** It writes the NetCDF and, with
`--plot`, an HTML plot — and that is all. The numbers (MAE, CRPS, RMSE, MAPE,
coverage, Winkler) come from a second command, `chap export-metrics`, which was
not mentioned in the model's README. `chap --help` was where it turned up. This
is the one step beyond `chap eval` that the task asked about.

**The `--plot` output is the default plot type.** `chap plot-backtest --help`
lists six plot types with `evaluation_plot` as the default, and that is what
`--plot` writes. The other five (including `predicted_vs_actual`) are available
from the stored `.nc` without rerunning the backtest.

**The run directory.** CHAP copies the entire model directory into
`runs/<timestamp>_<hash>/` *beside the model* and executes there. So the model
directory must be writable, and the per-split inputs and raw prediction CSVs
end up in that copy, not next to the NetCDF. `run_route.sh` collects that tree
into `results/chap_run_dir/` because it is the only place the model's actual
outputs survive.

## What was confusing

`chap sanity-check-model --model-url .` — the obvious "does CHAP see my model"
check — crashes on a fresh chap-core 2.3.1 install:

```
FileNotFoundError: .../site-packages/example_data/hydromet_5_filtered.csv
```

It defaults to a bundled example dataset that the 2.3.1 wheel does not ship.
This is a chap-core packaging defect, nothing to do with the model. Passing
`--dataset-path <the Lao CSV>` sidesteps it and the check then passes. Logged
as a blocker (opened and resolved) because it is exactly the kind of thing that
would send someone hunting in the wrong place. Worth noting that this is the
*only* failure in the whole route.

## What a page implied that did not quite hold

The README says the model "assumes and works only with a single region". That
reads as a hard restriction; it is not one. `train.py` pools every row into one
linear regression and `predict.py` copies `time_period` and `location` straight
through from the future-data frame, so a multi-region dataset runs fine — it
just fits one global relationship rather than per-region ones. The Lao run
covers 17 regions without complaint. The sentence is about the model's
statistical honesty, not its mechanics.

The README's troubleshooting section says the guide "has been verified for
version 1.4.0 and 2.1.0". The installed version is 2.3.1, so the invocation was
formally unverified for it. It worked unchanged.

## What the evaluation says

Defaults: 7 rolling splits, 3-period forecast horizon, stride 1, retrained once,
`climatology` future-weather provider. Backtest window ends 2010-10, with 72
periods of historical context carried for plotting.

CHAP rejected `LA-VI` (Vientiane prefecture) for having no target values across
the whole training period, leaving 17 of 18 regions.

Aggregate metrics (`results/eval/metrics.csv`):

| metric | value |
|---|---|
| MAE | 171.96 |
| RMSE | 358.93 |
| CRPS | 171.96 |
| CRPS (log1p) | 1.639 |
| MAPE | 383.16 |
| ratio above truth | 0.449 |
| coverage 10–90 | 0.0 |
| coverage 25–75 | 0.0 |

Two of these are worth reading carefully rather than at face value. CRPS equals
MAE exactly, and both interval coverages are 0.0, because the model emits a
single deterministic `sample_0` — a one-point "distribution" has no spread, so
CRPS degenerates to absolute error and no prediction interval ever contains the
observation. The `log1p` metrics emit `invalid value encountered in log1p`
warnings, which is the linear regression predicting negative case counts.
MAPE of 383 is likewise inflated by the many months with very low or zero
observed cases. None of this is a failure of the route; it is the model being,
as its own README says, not meant to capture anything interesting.

## Container build

There is none. `uv_env: pyproject.toml` routes the model through CHAP's
`command_line_runner`, which calls `uv` on the host. Docker was checked as
available (27.4.0, daemon up) and never used. There are therefore no build
layers to report as cached versus fresh. `uv` did build the model's virtual
environment — 10 packages, ~120 ms on a warm uv cache — and `uv.lock` from that
resolution is preserved in `results/chap_run_dir/uv.lock`.

## `run_route.sh`

`scripts/run_route.sh` clones the model at the pinned commit
`5cd8a1267362d945491353fba1c63a408462fa17`, installs `uv` and `chap-core==2.3.1`
if either is absent, runs the evaluation into a temporary clone, exports the
metrics and collects everything. It takes optional `DATA_DIR` and `OUT_DIR`
arguments and reads no environment variable.

It was run twice in `env -i` from `/` with a PATH of
`/usr/bin:/bin:/usr/sbin:/sbin` plus a directory containing only a symlink to
`uv` — so every inherited variable was stripped and `chap` was off the PATH,
forcing the chap-core bootstrap branch to execute. Both runs completed; the
metrics row was byte-identical between them and to the hand-run evaluation. The
second run produced the contents of `results/` as delivered.

**Unverified part:** the `curl -LsSf https://astral.sh/uv/install.sh | sh` branch
never fired, because running it would have upgraded the host's `uv` (0.5.26) as
a side effect. Everything downstream of it was exercised.

## Contamination notes

None to record. Every fact used here came from the model repository, the output
of `chap --help` and friends, and the chap-core source installed on this machine.
The only repository files read outside the node's own directory were the
discovery-log format spec (as instructed), the three Lao data files, and
`chap_core/cli_endpoints/_common.py` in the installed chap-core, which is not
part of this repository. Inside the node, `claim.md` and the generated `run.sh`
were read; `claim.md` restates the task and says nothing about how to do it.

## What I would tell the next person

1. Read the model's README first and try its invocation verbatim. For this model
   it is correct and current.
2. Do not use `chap sanity-check-model` without `--dataset-path` on 2.3.1.
3. Keep the `.geojson` next to the `.csv` with the same stem, or you lose the
   polygons without being told.
4. `chap eval --plot` gives you the picture; `chap export-metrics` gives you the
   numbers. You need both commands.
5. Run from inside the model directory, and make sure it is writable — CHAP
   copies itself into `runs/` there.
