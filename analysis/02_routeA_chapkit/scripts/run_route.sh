#!/usr/bin/env bash
# Route A: run the published model chapkit_ghr_model through CHAP and obtain
# CHAP's evaluation of its predictions on the Lao admin-1 monthly data.
#
# Assumes NOTHING but: bash, git, curl, docker (running), and `chap` on PATH.
# No environment variable, no working directory, no cached image, no artefact
# that this script does not itself create. It clones the model, builds its
# image, starts the chapkit service, runs the evaluation, and stops the service.
#
# The model is used exactly as published: nothing in the clone is edited.
#
#   usage: run_route.sh [--data-dir DIR] [--out-dir DIR] [--port N] [--keep-service]
#
# --data-dir  directory holding chap_LAO_admin1_monthly.csv and .geojson
#             (default: <repo>/Archive/data-lao, relative to this script)
# --out-dir   where the evaluation lands
#             (default: <node>/results/route_run)
#
# Wall clock, arm64 host: ~6 min for the evaluation itself, plus the image
# build. A cold build (no BuildKit layer cache) compiles GHRmodel from source
# under emulation and takes far longer; a warm cache makes it seconds.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$NODE_DIR/../.." && pwd)"

MODEL_REPO="https://github.com/chap-models/chapkit_ghr_model"
IMAGE="chapkit-ghr-model:route"
CONTAINER="chapkit-ghr-model-route"
PORT=8000
DATA_DIR="$REPO_ROOT/Archive/data-lao"
OUT_DIR="$NODE_DIR/results/route_run"
KEEP_SERVICE=0

while [ $# -gt 0 ]; do
    case "$1" in
        --data-dir)      DATA_DIR="$2"; shift 2 ;;
        --out-dir)       OUT_DIR="$2";  shift 2 ;;
        --port)          PORT="$2";     shift 2 ;;
        --keep-service)  KEEP_SERVICE=1; shift ;;
        -h|--help)       sed -n '2,25p' "${BASH_SOURCE[0]}"; exit 0 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

say() { printf '\n=== %s\n' "$*"; }

# ---------------------------------------------------------------- preflight --
say "preflight"
for c in git curl docker chap; do
    command -v "$c" >/dev/null 2>&1 || { echo "missing prerequisite: $c" >&2; exit 1; }
done
docker info >/dev/null 2>&1 || { echo "docker daemon is not running" >&2; exit 1; }
chap --version
CSV="$DATA_DIR/chap_LAO_admin1_monthly.csv"
GEOJSON="$DATA_DIR/chap_LAO_admin1_monthly.geojson"
[ -f "$CSV" ]     || { echo "missing $CSV" >&2; exit 1; }
[ -f "$GEOJSON" ] || { echo "missing $GEOJSON" >&2; exit 1; }

mkdir -p "$OUT_DIR"
OUT_DIR="$(cd "$OUT_DIR" && pwd)"

# ------------------------------------------------------------ obtain model --
# A fresh clone every run, into a temporary directory this script owns.
WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/route_a_XXXXXX")"
cleanup() {
    if [ "$KEEP_SERVICE" -eq 0 ]; then
        docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
    fi
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT

say "obtaining the model from $MODEL_REPO"
git clone --depth 1 "$MODEL_REPO" "$WORK_DIR/model"
MODEL_DIR="$WORK_DIR/model"
GIT_REVISION="$(git -C "$MODEL_DIR" rev-parse HEAD)"
echo "model commit: $GIT_REVISION"

# -------------------------------------------------------------------- build --
# The repository also publishes ghcr.io/chap-models/chapkit_ghr_model:latest,
# but that package is not anonymously pullable (HTTP 401), so the route builds
# the published Dockerfile instead. --platform linux/amd64 is mandatory: R-INLA
# ships x86_64 Linux binaries only, so arm64 hosts run it under emulation.
say "building $IMAGE (linux/amd64; emulated on arm64 hosts)"
docker build \
    --platform linux/amd64 \
    --build-arg GIT_REVISION="$GIT_REVISION" \
    --progress=plain \
    -t "$IMAGE" \
    "$MODEL_DIR" 2>&1 | tee "$OUT_DIR/docker_build.log"

echo "build layers CACHED: $(grep -c 'CACHED' "$OUT_DIR/docker_build.log" || true)"

# ------------------------------------------------------------------ service --
say "starting the chapkit service on :$PORT"
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
docker run -d --platform linux/amd64 -p "$PORT:8000" --name "$CONTAINER" "$IMAGE" >/dev/null

for _ in $(seq 1 60); do
    if curl -fsS "http://localhost:$PORT/health" >/dev/null 2>&1; then
        echo "service healthy"; break
    fi
    sleep 3
done
curl -fsS "http://localhost:$PORT/health" >/dev/null || {
    echo "service never became healthy" >&2
    docker logs "$CONTAINER" >"$OUT_DIR/service_startup_failure.log" 2>&1 || true
    exit 1
}

# CHAP resolves a chapkit service URL as a model; this is the cheap check that
# it can read the model's configuration schema before an evaluation is spent.
say "chap model schema"
chap model schema "http://localhost:$PORT" >"$OUT_DIR/model_schema.yaml"

# --------------------------------------------------------------- evaluation --
# CHAP has no --geojson option on eval: it auto-discovers a GeoJSON sitting
# beside the CSV with the same stem (chap_core.cli_endpoints._common.discover_geojson).
# Both files are staged into the output directory so that convention holds
# wherever the source data lives.
say "staging the dataset"
cp "$CSV"     "$OUT_DIR/chap_LAO_admin1_monthly.csv"
cp "$GEOJSON" "$OUT_DIR/chap_LAO_admin1_monthly.geojson"

say "chap eval (CHAP defaults: 7 splits, 3 periods, 1 retrain)"
cd "$OUT_DIR"
chap eval \
    "http://localhost:$PORT" \
    "$OUT_DIR/chap_LAO_admin1_monthly.csv" \
    "$OUT_DIR/evaluation.nc" \
    --run-config.is-chapkit-model \
    --plot 2>&1 | tee "$OUT_DIR/chap_eval.log"

[ -f "$OUT_DIR/evaluation.nc" ] || { echo "no evaluation.nc produced" >&2; exit 1; }

# --input-files is variadic, so both paths must be passed as named flags.
say "chap export-metrics"
chap export-metrics \
    --input-files "$OUT_DIR/evaluation.nc" \
    --output-file "$OUT_DIR/metrics.csv" 2>&1 | tee "$OUT_DIR/chap_export_metrics.log"

say "chap plot-backtest"
chap plot-backtest "$OUT_DIR/evaluation.nc" "$OUT_DIR/predicted_vs_actual.html" \
    --plot-type predicted_vs_actual 2>&1 | tee "$OUT_DIR/chap_plot_backtest.log"

say "done — outputs in $OUT_DIR"
ls -la "$OUT_DIR"
echo
cat "$OUT_DIR/metrics.csv"
