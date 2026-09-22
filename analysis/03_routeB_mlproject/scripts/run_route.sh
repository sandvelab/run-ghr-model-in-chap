#!/usr/bin/env bash
# Route B: run the published model dhis2-chap/minimalist_example_uv through CHAP
# as an MLproject directory, and obtain CHAP's default evaluation of its
# predictions on the Lao admin-1 monthly data.
#
# This script assumes nothing but a POSIX shell, git, curl and a network
# connection. It creates every artefact it uses: it installs `uv` and
# `chap-core` if they are missing, clones the model itself, and lets `uv`
# build the model's own environment. No environment variable is required,
# the working directory does not matter, and nothing is read from a cache
# that the script did not create.
#
# There is NO container build in this route: the model's MLproject declares
# `uv_env: pyproject.toml`, so CHAP runs train/predict through uv on the host
# via its command-line runner. Docker is never invoked.
#
# Usage:
#   run_route.sh [DATA_DIR] [OUT_DIR]
#
#   DATA_DIR  directory holding chap_LAO_admin1_monthly.csv and the
#             like-named .geojson (CHAP discovers the GeoJSON by that name;
#             it is not passed on the command line).
#             Default: <repo>/Archive/data-lao
#   OUT_DIR   where the evaluation is written.
#             Default: <node>/results

set -euo pipefail

# ---- pinned inputs ----------------------------------------------------------
MODEL_REPO="https://github.com/dhis2-chap/minimalist_example_uv.git"
# Commit this route was discovered and verified against. Set to the branch name
# to follow the model's head instead.
MODEL_REF="5cd8a1267362d945491353fba1c63a408462fa17"
CHAP_VERSION="2.3.1"

# ---- paths ------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$NODE_DIR/../.." && pwd)"

DATA_DIR="${1:-$REPO_ROOT/Archive/data-lao}"
OUT_DIR="${2:-$NODE_DIR/results}"

DATASET_CSV="$DATA_DIR/chap_LAO_admin1_monthly.csv"
[ -f "$DATASET_CSV" ] || { echo "no dataset at $DATASET_CSV" >&2; exit 1; }

mkdir -p "$OUT_DIR/eval"

# ---- prerequisite: uv (the model's own environment manager) -----------------
if ! command -v uv >/dev/null 2>&1; then
    echo "[route] installing uv"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
command -v uv >/dev/null 2>&1 || { echo "uv not on PATH after install" >&2; exit 1; }

# ---- prerequisite: chap-core ------------------------------------------------
if ! command -v chap >/dev/null 2>&1; then
    echo "[route] installing chap-core==$CHAP_VERSION"
    uv tool install "chap-core==$CHAP_VERSION"
    export PATH="$HOME/.local/bin:$PATH"
fi
command -v chap >/dev/null 2>&1 || { echo "chap not on PATH after install" >&2; exit 1; }
echo "[route] chap version: $(chap --version)"

# ---- obtain the model -------------------------------------------------------
# CHAP copies the model directory into a runs/<timestamp>/ tree beside it and
# executes there, so the clone must live somewhere writable that is not the
# output directory.
WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/routeB.XXXXXX")"
trap 'rm -rf "$WORK_DIR"' EXIT
MODEL_DIR="$WORK_DIR/minimalist_example_uv"

echo "[route] cloning $MODEL_REPO"
git clone --quiet "$MODEL_REPO" "$MODEL_DIR"
git -C "$MODEL_DIR" checkout --quiet "$MODEL_REF"
git -C "$MODEL_DIR" rev-parse HEAD > "$OUT_DIR/model_commit.txt"

# ---- evaluate ---------------------------------------------------------------
# --model-name is the MLproject directory; CHAP reads MLproject, builds the uv
# environment from pyproject.toml, and drives the train/predict entry points.
# --plot writes CHAP's default evaluation plot (plot-type evaluation_plot)
# next to the NetCDF.
echo "[route] running chap eval"
(
  cd "$MODEL_DIR"
  chap eval \
      --model-name . \
      --dataset-csv "$DATASET_CSV" \
      --output-file "$OUT_DIR/eval/eval.nc" \
      --plot
) 2>&1 | tee "$OUT_DIR/eval/chap_eval.log"

# ---- metrics ----------------------------------------------------------------
# chap eval writes only the NetCDF and the plot; the metrics table is a
# separate step.
echo "[route] exporting metrics"
chap export-metrics \
    --input-files "$OUT_DIR/eval/eval.nc" \
    --output-file "$OUT_DIR/eval/metrics.csv" \
    2>&1 | tee "$OUT_DIR/eval/chap_export_metrics.log"

# ---- keep what CHAP produced ------------------------------------------------
# CHAP's per-split inputs and the model's raw prediction CSVs live in the
# run directory it created inside the (temporary) model clone.
RUN_TREE="$(ls -d "$MODEL_DIR"/runs/*/ | tail -1)"
rm -rf "$OUT_DIR/chap_run_dir"
mkdir -p "$OUT_DIR/chap_run_dir"
( cd "$RUN_TREE" && tar cf - --exclude=.git --exclude=.venv --exclude=__pycache__ --exclude=runs . ) \
    | ( cd "$OUT_DIR/chap_run_dir" && tar xf - )

echo "[route] done"
echo "[route] evaluation : $OUT_DIR/eval/eval.nc"
echo "[route] plot       : $OUT_DIR/eval/eval.html"
echo "[route] metrics    : $OUT_DIR/eval/metrics.csv"
