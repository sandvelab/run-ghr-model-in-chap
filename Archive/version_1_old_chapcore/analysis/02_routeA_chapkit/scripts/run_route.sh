#!/usr/bin/env bash
# Route A -- run chapkit_ghr_model (pinned commit 60b16a2) as a chapkit REST service
# in Docker and evaluate it with CHAP's rolling-origin backtest (`chap eval`) on the
# CHAP-harmonised Lao admin-1 monthly dataset.
#
# Re-runnable from scratch: clones the model, builds the image if it is not already
# present, starts the service, starts the compatibility shim, runs the evaluation,
# exports the metrics and tears everything down.
#
#   scripts/run_route.sh [N_SPLITS] [N_PERIODS]
#
# Defaults are chap eval's own: 7 splits x 3 periods, stride 1.
#
# Two things here are NOT in anyone's documentation, and the run does not work
# without them:
#
#  1. The published image ghcr.io/chap-models/chapkit_ghr_model:latest is NOT
#     publicly pullable (anonymous GHCR token -> 403), so the image is built locally.
#     --platform linux/amd64 is mandatory: R-INLA ships x86_64 binaries only, so on
#     an arm64 host everything below runs under qemu emulation.
#
#  2. chap-core 2.1.0 pins chapkit 1.1.0 in its own venv and validates the service's
#     GET /api/v1/info with that version's MLServiceInfo, which is extra="forbid".
#     The model is built on chapkit 2.0.0, whose /api/v1/info carries three extra
#     fields, so chap-core rejects the service ("could not be reached as a chapkit
#     service") -- and --run-config.is-chapkit-model does NOT rescue it, because the
#     same strict model is used again by CHAPKitRestAPIWrapper.info(). scripts/
#     info_shim.py is a transparent proxy that strips exactly those three keys.
#     The model image itself is run entirely unmodified.
set -euo pipefail

N_SPLITS="${1:-7}"
N_PERIODS="${2:-3}"

HERE="$(cd "$(dirname "$0")" && pwd)"
NODE="$(cd "$HERE/.." && pwd)"
RESULTS="$NODE/results"
mkdir -p "$RESULTS"

# --- pins -------------------------------------------------------------------
MODEL_REPO="https://github.com/chap-models/chapkit_ghr_model"
MODEL_COMMIT="60b16a2e929405ce95fae2043a63d7e27292ca0f"
IMAGE="chapkit-ghr-model:60b16a2"
CONTAINER="chapkit-ghr-model-route-a"
SVC_PORT="${SVC_PORT:-8000}"   # the container
SHIM_PORT="${SHIM_PORT:-8010}" # what CHAP talks to
SRC_DIR="${SRC_DIR:-/tmp/ghrmodel}"

# The three source files are READ-ONLY and are only ever copied from.
DATA_SRC="/Users/geirksa_1_2_3/ai/special-purpose vaults/run-ghr-model-in-chap/Archive/data-lao"
WORK_DATA="${WORK_DATA:-/tmp/chapdata}"

export PATH="$HOME/.local/bin:$PATH"
echo ">>> chap $(chap --version)"

# --- 1. model source at the pinned commit -----------------------------------
if [ ! -d "$SRC_DIR/.git" ]; then
  echo ">>> Cloning $MODEL_REPO into $SRC_DIR"
  git clone --quiet "$MODEL_REPO" "$SRC_DIR"
fi
git -C "$SRC_DIR" fetch --quiet origin || true
git -C "$SRC_DIR" checkout --quiet "$MODEL_COMMIT"
echo ">>> Model at $(git -C "$SRC_DIR" rev-parse HEAD)"

# --- 2. image ---------------------------------------------------------------
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo ">>> Building $IMAGE (slow: ~1.4GB base + CRAN + GHRmodel from BSC GitLab;"
  echo "    ~22 min on an M3 under emulation)"
  docker build --platform linux/amd64 \
    --build-arg GIT_REVISION="$MODEL_COMMIT" \
    -t "$IMAGE" "$SRC_DIR" 2>&1 | tee "$RESULTS/docker_build.log"
fi

# --- 3. data ----------------------------------------------------------------
# chap eval takes no geometry argument: it auto-discovers <csv stem>.geojson next to
# the CSV. So both files are copied side by side under the same stem.
mkdir -p "$WORK_DATA"
cp "$DATA_SRC/chap_LAO_admin1_monthly.csv"     "$WORK_DATA/"
cp "$DATA_SRC/chap_LAO_admin1_monthly.geojson" "$WORK_DATA/"
chmod u+w "$WORK_DATA"/chap_LAO_admin1_monthly.*
chap validate "$WORK_DATA/chap_LAO_admin1_monthly.csv"

# --- 4. service + shim ------------------------------------------------------
SHIM_PID=""
cleanup() {
  [ -n "$SHIM_PID" ] && kill "$SHIM_PID" 2>/dev/null || true
  docker logs "$CONTAINER" > "$RESULTS/service.log" 2>&1 || true
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
echo ">>> Starting the chapkit service on :$SVC_PORT"
docker run -d --platform linux/amd64 -p "$SVC_PORT:8000" --name "$CONTAINER" "$IMAGE" >/dev/null

for _ in $(seq 1 120); do
  curl -fsS "http://localhost:$SVC_PORT/health" >/dev/null 2>&1 && break
  sleep 5
done
curl -fsS "http://localhost:$SVC_PORT/health" >/dev/null || { echo "service never became healthy"; exit 1; }
echo "    healthy"
curl -fsS "http://localhost:$SVC_PORT/api/v1/info" > "$RESULTS/service_info.json"

echo ">>> Starting the chapkit 2.0 -> chap-core 2.1.0 info shim on :$SHIM_PORT"
python3 "$HERE/info_shim.py" "$SHIM_PORT" "http://localhost:$SVC_PORT" > /tmp/info_shim.log 2>&1 &
SHIM_PID=$!
for _ in $(seq 1 30); do
  curl -fsS "http://localhost:$SHIM_PORT/api/v1/info" >/dev/null 2>&1 && break
  sleep 1
done

# CHAP now sees the service as a model:
chap model schema "http://localhost:$SHIM_PORT" --example > "$RESULTS/model_schema_example.yaml"

# --- 5. evaluation ----------------------------------------------------------
# No --model-configuration-yaml on purpose: an empty configuration makes the chapkit
# service apply its own schema defaults (rainfall + mean_temperature, bym2/rw1/iid,
# 1000 posterior draws), which is exactly the model as published.
OUT="$RESULTS/eval_lao_ghrmodel.nc"
echo ">>> chap eval ($N_SPLITS splits x $N_PERIODS periods)"
chap eval \
  --model-name "http://localhost:$SHIM_PORT" \
  --run-config.is-chapkit-model \
  --dataset-csv "$WORK_DATA/chap_LAO_admin1_monthly.csv" \
  --output-file "$OUT" \
  --backtest-params.n-splits "$N_SPLITS" \
  --backtest-params.n-periods "$N_PERIODS" \
  --backtest-params.stride 1 \
  --plot 2>&1 | tee "$RESULTS/chap_eval.log" | grep -vE "HTTP Request|status: running" || true

# --- 6. headline metrics ----------------------------------------------------
chap export-metrics --input-files "$OUT" --output-file "$RESULTS/eval_metrics.csv"
echo ">>> Wrote:"
echo "    $OUT"
echo "    ${OUT%.nc}.html"
echo "    $RESULTS/eval_metrics.csv"
