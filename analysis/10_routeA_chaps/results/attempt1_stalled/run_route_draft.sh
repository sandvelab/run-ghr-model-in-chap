#!/usr/bin/env bash
# Route A through chaps: run chap-models/chapkit_ghr_model as a chapkit service with
# chaps (winterop-com/chaps), then evaluate it on the Lao admin-1 monthly data with the
# installed chap CLI (chap-core 2.3.1) and produce CHAP's default outputs.
#
# Needs on the machine: Docker (daemon running, Compose v2.24.4+), curl, and the `chap`
# command (chap-core 2.3.1). Nothing else from this project: chaps is downloaded here.
#
# Usage: run_route.sh DATA_DIR OUT_DIR
#   DATA_DIR holds chap_LAO_admin1_monthly.csv and chap_LAO_admin1_monthly.geojson
#            (same stem: chap eval discovers the GeoJSON beside the CSV by name).
#   OUT_DIR  receives the evaluation NetCDF, its HTML plot, a PNG of the same default
#            plot, and the metrics CSV.
# Env: CHAP (path to the chap command; default: `chap` on PATH),
#      WORK (scratch directory for the chaps binary and its data; default: mktemp -d).
set -euo pipefail

DATA_DIR=$(cd "${1:?DATA_DIR}" && pwd)
mkdir -p "${2:?OUT_DIR}"
OUT_DIR=$(cd "$2" && pwd)
CHAP=${CHAP:-chap}
WORK=${WORK:-$(mktemp -d)}
mkdir -p "$WORK/bin"
export CHAPS_DATA_DIR="$WORK/chapsdata"   # keep chaps' run groups out of ~/.local/share
export PATH="$WORK/bin:$PATH"

echo "== 1. install chaps (newest release) into $WORK/bin"
curl -fsSL https://raw.githubusercontent.com/winterop-com/chaps/main/install.sh | sh -s -- --dir "$WORK/bin"
chaps self version
chaps doctor || true

echo "== 2. start the GHR model service with chaps (marketplace pin of this repository)"
chaps run https://github.com/chap-models/chapkit_ghr_model --port auto --timeout 3600 --json > "$WORK/run.json"
cat "$WORK/run.json"
URL=$(sed -n 's/.*"url": *"\([^"]*\)".*/\1/p' "$WORK/run.json" | head -1)
[ -n "$URL" ] || { echo "no service URL from chaps run" >&2; exit 1; }
curl -fsS "$URL/api/v1/info"; echo

echo "== 3. chap eval against the service URL, with CHAP's default backtest parameters"
cd "$WORK"   # chap writes its runs/ directory into the working directory
"$CHAP" eval "$URL" "$DATA_DIR/chap_LAO_admin1_monthly.csv" "$OUT_DIR/evaluation.nc" --plot

echo "== 4. CHAP's default post-eval outputs: metrics CSV and the default plot as PNG"
"$CHAP" export-metrics "$OUT_DIR/evaluation.nc" "$OUT_DIR/metrics.csv"
"$CHAP" plot-backtest "$OUT_DIR/evaluation.nc" "$OUT_DIR/evaluation_plot.png"

echo "== 5. stop the model and remove its chaps group"
chaps stop --all --purge || true
ls -l "$OUT_DIR"
