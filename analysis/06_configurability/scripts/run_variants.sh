#!/usr/bin/env bash
# Run several published-alternative configurations of route A's model on the Lao data.
#
# Each variant changes ONE option from the model's own published defaults, so that whatever
# moves can be attributed. The control sets those defaults explicitly, which means it travels
# the same path through the proxy as every variant and controls for the proxy itself.
#
# The configuration cannot reach the model without something interposed -- chap-core will only
# send a nested mapping and the service only honours a flat one -- so scripts/lib/config_proxy.py
# sits between them and rewrites the config POST. Neither the model nor CHAP is modified.
#
# The container is restarted for each variant so its log holds exactly one run's fitted
# formula, which is how each run is checked to have actually used its configuration.
set -euo pipefail
cd "$(dirname "$0")/.."
NODE="$(pwd)"
REPO_ROOT="$(cd ../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"
DATA="$REPO_ROOT/Archive/data-lao"
IMAGE="chapkit-ghr-model:latest"
PORT=8000
PROXY_PORT=8100

OUT="$NODE/results/variants"
mkdir -p "$OUT"

# name|yaml body (one option per line, two-space indented under user_option_values)
VARIANTS=(
"v0_published_defaults|  re_spatial: bym2\n  re_seasonal: rw1\n  re_interannual: iid\n  family: nbinomial"
"v1_no_spatial|  re_spatial: none\n  re_seasonal: rw1\n  re_interannual: iid\n  family: nbinomial"
"v2_seasonal_rw2|  re_spatial: bym2\n  re_seasonal: rw2\n  re_interannual: iid\n  family: nbinomial"
"v3_interannual_rw1|  re_spatial: bym2\n  re_seasonal: rw1\n  re_interannual: rw1\n  family: nbinomial"
"v4_poisson|  re_spatial: bym2\n  re_seasonal: rw1\n  re_interannual: iid\n  family: poisson"
)

cleanup() {
    docker rm -f ghrvariant >/dev/null 2>&1 || true
    [ -n "${PROXY_PID:-}" ] && kill "$PROXY_PID" 2>/dev/null || true
}
trap cleanup EXIT

echo "[variants] starting the config proxy on :$PROXY_PORT"
"$PYTHON" scripts/lib/config_proxy.py --listen "$PROXY_PORT" \
    --upstream "http://localhost:$PORT" > "$OUT/proxy.log" 2>&1 &
PROXY_PID=$!
sleep 2

for entry in "${VARIANTS[@]}"; do
    NAME="${entry%%|*}"
    BODY="${entry#*|}"
    VDIR="$OUT/$NAME"
    mkdir -p "$VDIR"

    printf 'user_option_values:\n' > "$VDIR/config.yaml"
    printf "$BODY\n" >> "$VDIR/config.yaml"

    echo "[variants] === $NAME ==="
    cat "$VDIR/config.yaml"

    # A fresh container per variant, so its log carries exactly this run's fitted formula.
    docker rm -f ghrvariant >/dev/null 2>&1 || true
    docker run -d --platform linux/amd64 -p "$PORT:8000" --name ghrvariant "$IMAGE" >/dev/null
    for _ in $(seq 1 60); do
        curl -fsS "http://localhost:$PORT/health" >/dev/null 2>&1 && break
        sleep 3
    done

    cp "$DATA/chap_LAO_admin1_monthly.csv"     "$VDIR/"
    cp "$DATA/chap_LAO_admin1_monthly.geojson" "$VDIR/"

    if chap eval "http://localhost:$PROXY_PORT" \
            "$VDIR/chap_LAO_admin1_monthly.csv" \
            "$VDIR/evaluation.nc" \
            --run-config.is-chapkit-model \
            --model-configuration-yaml "$VDIR/config.yaml" \
            > "$VDIR/chap_eval.log" 2>&1; then
        chap export-metrics --input-files "$VDIR/evaluation.nc" \
            --output-file "$VDIR/metrics.csv" >> "$VDIR/chap_eval.log" 2>&1
        echo "[variants] $NAME completed"
    else
        echo "[variants] $NAME FAILED -- kept as the result it is"
    fi

    # What the model actually fitted. This is the check that the configuration took effect.
    docker logs ghrvariant 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
        | grep -oE "disease_cases ~ 1[^\"]{0,400}" | sort -u > "$VDIR/fitted_formula.txt" || true
    # And what the service ended up storing, as it reports it back.
    curl -s "http://localhost:$PORT/api/v1/configs" > "$VDIR/stored_config.json" || true
done

docker rm -f ghrvariant >/dev/null 2>&1 || true
kill "$PROXY_PID" 2>/dev/null || true
PROXY_PID=""

"$PYTHON" scripts/lib/collect_variants.py --variants-dir "$OUT" --out "$NODE/results"
