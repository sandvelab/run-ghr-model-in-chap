#!/usr/bin/env bash
# Route A, iteration 3: run chapkit_ghr_model (commit a9532c7) through CHAP 2.3.1
# and produce CHAP's default evaluation output on the Lao admin-1 monthly data.
#
# Reproduces the route from nothing. Prerequisites on the host (not this project):
#   - docker (daemon running; linux/amd64 emulation on arm64 hosts is fine but slow)
#   - chap-core 2.3.1 providing the `chap` command. If `chap` is not on PATH the
#     script installs it with `uv tool install chap-core==2.3.1` (needs `uv`).
#   - curl
#
# Inputs (override by env):
#   DATA_DIR  directory holding chap_LAO_admin1_monthly.csv and .geojson
#             (default: fetched from the public dhis2/climate-health-data repo)
#   OUT_DIR   where every output lands (default: ../results/route_run next to this script)
#   PORT      host port for the model service (default 8765)
#
# Usage: bash run_route.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="${OUT_DIR:-$SCRIPT_DIR/../results/route_run}"
PORT="${PORT:-8765}"
IMAGE="ghcr.io/chap-models/chapkit_ghr_model:sha-a9532c7"
CONTAINER="chapkit-ghr-route-a-$$"
CHAP_VERSION="2.3.1"

export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin:$PATH"

mkdir -p "$OUT_DIR"
OUT_DIR="$(cd "$OUT_DIR" && pwd)"
echo ">>> outputs -> $OUT_DIR"

# ---- 1. Platform ---------------------------------------------------------
if ! command -v chap >/dev/null 2>&1; then
  echo ">>> chap not found; installing chap-core==$CHAP_VERSION with uv"
  uv tool install "chap-core==$CHAP_VERSION"
fi
got="$(chap --version)"
[ "$got" = "$CHAP_VERSION" ] || { echo "chap $got found, $CHAP_VERSION required" >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "docker daemon not reachable" >&2; exit 1; }

# ---- 2. Data -------------------------------------------------------------
# chap eval auto-discovers the GeoJSON by the CSV's basename, so both must sit
# side by side with the same stem.
IN_DIR="$OUT_DIR/input"
mkdir -p "$IN_DIR"
if [ -n "${DATA_DIR:-}" ]; then
  cp "$DATA_DIR/chap_LAO_admin1_monthly.csv" "$DATA_DIR/chap_LAO_admin1_monthly.geojson" "$IN_DIR/"
else
  base="https://raw.githubusercontent.com/dhis2/climate-health-data/refs/heads/main/lao"
  curl -fsSL "$base/chap_LAO_admin1_monthly.csv" -o "$IN_DIR/chap_LAO_admin1_monthly.csv"
  curl -fsSL "$base/chap_LAO_admin1_monthly.geojson" -o "$IN_DIR/chap_LAO_admin1_monthly.geojson"
fi
CSV="$IN_DIR/chap_LAO_admin1_monthly.csv"
shasum -a 256 "$IN_DIR"/* | tee "$OUT_DIR/input_sha256.txt"
chap validate "$CSV"

# ---- 3. Model service ----------------------------------------------------
docker pull --platform linux/amd64 "$IMAGE"
docker image inspect "$IMAGE" --format '{{.Id}} {{json .RepoDigests}}' > "$OUT_DIR/image_id.txt"
cleanup() { docker logs "$CONTAINER" > "$OUT_DIR/service.log" 2>&1 || true; docker rm -f "$CONTAINER" >/dev/null 2>&1 || true; }
trap cleanup EXIT
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --platform linux/amd64 -p "$PORT:8000" --name "$CONTAINER" "$IMAGE" >/dev/null
echo ">>> waiting for http://localhost:$PORT/health"
for i in $(seq 1 120); do
  if curl -fsS "http://localhost:$PORT/health" >/dev/null 2>&1; then echo "    healthy"; break; fi
  [ "$i" = 120 ] && { echo "service did not become healthy" >&2; exit 1; }
  sleep 5
done
curl -fsS "http://localhost:$PORT/api/v1/info" > "$OUT_DIR/service_info.json" || true

# ---- 4. Evaluation (CHAP defaults: 7 splits, 3 periods, stride 1) --------
# (--run-config.log-file was tried in discovery and wrote nothing, so stdout is teed.)
cd "$OUT_DIR"
chap eval \
  --model-name "http://localhost:$PORT" \
  --dataset-csv "$CSV" \
  --output-file "$OUT_DIR/eval.nc" \
  --run-config.is-chapkit-model \
  --plot 2>&1 | tee "$OUT_DIR/chap_eval.log"
[ "${PIPESTATUS[0]}" = 0 ] || { echo "chap eval failed" >&2; exit 1; }
[ -s "$OUT_DIR/eval.nc" ] || { echo "chap eval wrote no eval.nc" >&2; exit 1; }

# ---- 5. Default plot and metrics (the steps beyond chap eval) -------------
chap plot-backtest --input-file "$OUT_DIR/eval.nc" --output-file "$OUT_DIR/evaluation_plot.html"
chap plot-backtest --input-file "$OUT_DIR/eval.nc" --output-file "$OUT_DIR/evaluation_plot.png"
chap export-metrics --input-files "$OUT_DIR/eval.nc" --output-file "$OUT_DIR/metrics.csv"

echo ">>> done"
ls -la "$OUT_DIR"
