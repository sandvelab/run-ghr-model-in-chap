#!/usr/bin/env bash
# Route A through chaps: serve chapkit_ghr_model with chaps, evaluate it with chap 2.3.1
# on the public Lao admin-1 monthly dataset, and write CHAP's default evaluation output
# (NetCDF, default evaluation_plot, aggregate metrics CSV).
#
# Needs only: bash, curl, tar, shasum (or sha256sum), and a running Docker with
# Compose v2, plus fetch_image_oci.sh from the same directory. Everything else (uv, chap-core 2.3.1, chaps, the data) is fetched into
# WORK. The model image (~2.1 GB compressed, amd64; emulated on arm64) is pulled by
# chaps on first use.
#
# Usage: run_route.sh [OUT_DIR] [WORK_DIR]
#   OUT_DIR   where the evaluation files land (default: ./route_output)
#   WORK_DIR  scratch for tools and data   (default: a fresh mktemp -d)
# Env:  PORT (default 5060) host port for the model service
#       KEEP_MODEL=1 leaves the model service running afterwards
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"   # fetch_image_oci.sh lives beside this script

OUT="${1:-$PWD/route_output}"
WORK="${2:-$(mktemp -d)}"
PORT="${PORT:-5060}"
MODEL_REPO="https://github.com/chap-models/chapkit_ghr_model"
CHAP_VERSION="2.3.1"
DATA_BASE="https://raw.githubusercontent.com/dhis2/climate-health-data/refs/heads/main/lao"
CSV_SHA="19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56"
GEO_SHA="cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389"

mkdir -p "$OUT" "$WORK"
OUT="$(cd "$OUT" && pwd)"; WORK="$(cd "$WORK" && pwd)"
echo "== out: $OUT"; echo "== work: $WORK"

# Docker lives outside /usr/bin:/bin on macOS (Docker Desktop).
for d in /usr/local/bin /opt/homebrew/bin /Applications/Docker.app/Contents/Resources/bin; do
  [ -d "$d" ] && PATH="$PATH:$d"
done
export PATH="$WORK/bin:$PATH"
command -v docker >/dev/null || { echo "docker not found" >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "docker daemon not running" >&2; exit 1; }

sha256() { if command -v shasum >/dev/null; then shasum -a 256 "$1"; else sha256sum "$1"; fi | cut -d' ' -f1; }

# 1. Tools: chaps (the route), uv + chap-core (the evaluation CLI), all inside WORK.
mkdir -p "$WORK/bin"
curl -fsSL https://raw.githubusercontent.com/winterop-com/chaps/main/install.sh \
  | sh -s -- --dir "$WORK/bin"
curl -LsSf https://astral.sh/uv/install.sh \
  | env UV_INSTALL_DIR="$WORK/bin" UV_NO_MODIFY_PATH=1 sh
export UV_TOOL_DIR="$WORK/uv-tools" UV_TOOL_BIN_DIR="$WORK/bin" \
       UV_CACHE_DIR="$WORK/uv-cache" UV_PYTHON_INSTALL_DIR="$WORK/uv-python"
uv tool install --python 3.13 "chap-core==$CHAP_VERSION"
chaps self version
chap --version
chaps doctor || true

# 2. Data: the public Lao admin-1 monthly CSV and its same-stem GeoJSON (auto-discovered).
mkdir -p "$WORK/data"
for ext in csv geojson; do
  curl -fsSL -o "$WORK/data/chap_LAO_admin1_monthly.$ext" "$DATA_BASE/chap_LAO_admin1_monthly.$ext"
done
[ "$(sha256 "$WORK/data/chap_LAO_admin1_monthly.csv")" = "$CSV_SHA" ] || { echo "CSV hash mismatch" >&2; exit 1; }
[ "$(sha256 "$WORK/data/chap_LAO_admin1_monthly.geojson")" = "$GEO_SHA" ] || { echo "GeoJSON hash mismatch" >&2; exit 1; }

# 3. Serve the model with chaps (marketplace model chapkit_ghr_model, its reviewed pin).
#    On a slow link ghcr.io cuts the 1.42 GB layer and `docker pull` (which chaps uses)
#    restarts it from zero every time, so the image chaps pins is fetched first with
#    resumable, digest-checked curl and docker-loaded under its own tag; chaps then
#    finds it locally. Set SKIP_PREFETCH=1 to let chaps pull it itself.
IMAGE_TAG="sha-dfb2e3f"   # the tag chaps 0.99.4's marketplace pin for chapkit_ghr_model 0.1.3 uses
if [ "${SKIP_PREFETCH:-0}" != 1 ]; then
  bash "$HERE/fetch_image_oci.sh" chap-models/chapkit_ghr_model "$IMAGE_TAG" "$WORK"
fi
cleanup() { [ "${KEEP_MODEL:-0}" = 1 ] || chaps stop chapkit_ghr_model || true; }
trap cleanup EXIT
chaps run "$MODEL_REPO" --port "$PORT" --timeout 7200
curl -fsS "http://localhost:$PORT/health" && echo

# 4. CHAP's default evaluation: eval (default backtest params), then plot-backtest
#    (default plot type evaluation_plot), then export-metrics (all aggregate metrics).
cd "$OUT"
chap eval \
  --model-name "http://localhost:$PORT" \
  --dataset-csv "$WORK/data/chap_LAO_admin1_monthly.csv" \
  --output-file "$OUT/eval.nc" \
  --run-config.is-chapkit-model
chap plot-backtest --input-file "$OUT/eval.nc" --output-file "$OUT/evaluation_plot.html"
chap export-metrics --input-files "$OUT/eval.nc" --output-file "$OUT/metrics.csv"
cat "$OUT/metrics.csv"
echo "== done: $OUT"
