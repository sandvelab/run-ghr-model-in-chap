#!/usr/bin/env bash
# run_route.sh -- Route B: run the MLproject/uv model `minimalist_example_uv`
# through CHAP and produce a backtest evaluation on the Lao admin-1 monthly data.
#
# Re-runnable from a clean checkout. It re-downloads the model at the pinned
# commit, re-copies the read-only data, and re-runs the evaluation.
#
# Prerequisites on the machine:
#   - chap-core 2.1.0 on PATH (installed via `uv tool install chap-core`)
#   - uv (CHAP builds the model's virtualenv with it, per `uv_env:` in MLproject)
#   - network access (GitHub tarball + PyPI for the model's deps)
# Docker is NOT needed for this route: the MLproject declares `uv_env`, so CHAP
# runs the model locally through uv, not in a container.

set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

NODE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$NODE_DIR"

MODEL_REPO="dhis2-chap/minimalist_example_uv"
MODEL_COMMIT="5cd8a1267362d945491353fba1c63a408462fa17"
MODEL_DIR="model/minimalist_example_uv"

DATA_SRC="/Users/geirksa_1_2_3/ai/special-purpose vaults/run-ghr-model-in-chap/Archive/data-lao"
DATA_STEM="chap_LAO_admin1_monthly"

echo "== chap version =="
chap --version

# --- 1. Get the model, at the pinned commit -------------------------------
# Deliberately a tarball, not `git clone`: this route is run without git.
echo "== fetching model $MODEL_REPO @ $MODEL_COMMIT =="
mkdir -p model
rm -rf "$MODEL_DIR" /tmp/chap_route_b_model
mkdir -p /tmp/chap_route_b_model
curl -sSL -o /tmp/chap_route_b_model/model.tar.gz \
  "https://codeload.github.com/${MODEL_REPO}/tar.gz/${MODEL_COMMIT}"
tar xzf /tmp/chap_route_b_model/model.tar.gz -C model
mv "model/minimalist_example_uv-${MODEL_COMMIT}" "$MODEL_DIR"
# The model is used exactly as published -- nothing below edits it.

# --- 2. Copy the read-only input data -------------------------------------
# The originals under Archive/data-lao/ must never be touched; CHAP writes
# alongside its inputs, so we work on copies.
echo "== copying input data =="
mkdir -p data
cp "$DATA_SRC/${DATA_STEM}.csv"     "data/${DATA_STEM}.csv"
cp "$DATA_SRC/${DATA_STEM}.geojson" "data/${DATA_STEM}.geojson"
# CHAP picks the .geojson up automatically because it shares the CSV's basename;
# there is no CLI flag for it on `chap eval`.

# --- 3. Sanity check: does CHAP accept model + data together? -------------
echo "== validating dataset against the model =="
chap validate \
  --dataset-csv "data/${DATA_STEM}.csv" \
  --model-name "$MODEL_DIR" \
  2>&1 | tee results/validate.log
# Expect 4 warnings of the form "Column 'X' is present in the dataset but not
# used by the model". They are spurious for this model -- see discovery_notes.md.

# --- 4. The evaluation ----------------------------------------------------
mkdir -p results
echo "== running backtest evaluation =="
chap eval \
  --model-name "$MODEL_DIR" \
  --dataset-csv "data/${DATA_STEM}.csv" \
  --output-file results/eval.nc \
  --plot \
  2>&1 | tee results/eval_run.log
# Backtest params left at CHAP's defaults: 7 splits, 3-period horizon,
# stride 1, retrained once.

# --- 5. Metrics out of the NetCDF -----------------------------------------
echo "== exporting metrics =="
chap export-metrics \
  --input-files results/eval.nc \
  --output-file results/eval_metrics.csv \
  2>&1 | tee results/export_metrics.log

echo
echo "== done =="
echo "  results/eval.nc           backtest forecasts + observations (NetCDF)"
echo "  results/eval.html         evaluation plot"
echo "  results/eval_metrics.csv  aggregate metrics"
