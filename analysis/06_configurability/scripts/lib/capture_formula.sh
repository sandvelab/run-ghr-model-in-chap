#!/usr/bin/env bash
# Recover the model formula each configuration actually fits.
#
# The sweep's own capture came back empty and its containers were gone, so this re-runs two
# variants on a short backtest -- two splits rather than seven -- purely to read what the
# model fitted. The scores it produces are NOT the scores reported anywhere: the backtest is
# different. Only the formula is taken from this.
set -euo pipefail
cd "$(dirname "$0")/../.."
NODE="$(pwd)"
REPO_ROOT="$(cd ../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"
OUT="$NODE/results/formula_check"
mkdir -p "$OUT"

cleanup() { docker rm -f ghrfc >/dev/null 2>&1 || true; [ -n "${PP:-}" ] && kill "$PP" 2>/dev/null || true; }
trap cleanup EXIT

"$PYTHON" scripts/lib/config_proxy.py --listen 8100 --upstream http://localhost:8000 \
    > "$OUT/proxy.log" 2>&1 &
PP=$!
sleep 2

for NAME in v0_published_defaults v4_poisson v1_no_spatial; do
    SRC="$NODE/results/variants/$NAME"
    D="$OUT/$NAME"; mkdir -p "$D"
    cp "$SRC/config.yaml" "$D/config.yaml"
    cp "$REPO_ROOT/Archive/data-lao/chap_LAO_admin1_monthly.csv"     "$D/"
    cp "$REPO_ROOT/Archive/data-lao/chap_LAO_admin1_monthly.geojson" "$D/"

    docker rm -f ghrfc >/dev/null 2>&1 || true
    docker run -d --platform linux/amd64 -p 8000:8000 --name ghrfc chapkit-ghr-model:latest >/dev/null
    for _ in $(seq 1 60); do curl -fsS http://localhost:8000/health >/dev/null 2>&1 && break; sleep 3; done

    echo "[formula] $NAME"
    chap eval http://localhost:8100 "$D/chap_LAO_admin1_monthly.csv" "$D/short.nc" \
        --run-config.is-chapkit-model --model-configuration-yaml "$D/config.yaml" \
        --backtest-params.n-splits 2 > "$D/chap_eval.log" 2>&1 || echo "[formula] $NAME eval failed"

    docker logs ghrfc > "$D/container.log" 2>&1 || true
    grep -oE "disease_cases ~ 1[^\"]{0,250}" "$D/container.log" | sort -u > "$D/fitted_formula.txt" || true
    echo "[formula] $NAME -> $(wc -l < "$D/fitted_formula.txt" | tr -d ' ') formula line(s)"
done
