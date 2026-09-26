#!/usr/bin/env bash
# Batch 8b's five one-option configuration variants of route A's model, re-run on the
# upgraded pair (chapkit 2.1.2, the model at a9532c7) with NOTHING interposed: each goes
# through `chap eval --model-configuration-yaml` straight to the published image.
#
# The control sets the model's published defaults explicitly, so it travels the same path as
# every variant. A fresh container per variant keeps each log to one run's fitted formula,
# which is the evidence that a setting took effect; the stored configuration is read back as
# the second line of evidence. A sixth run gives CHAP a FLAT mapping, expected to be refused.
set -euo pipefail
cd "$(dirname "$0")/.."
NODE="$(pwd)"
REPO_ROOT="$(cd ../../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"
DATA="$REPO_ROOT/Archive/data-lao"
IMAGE="ghcr.io/chap-models/chapkit_ghr_model:sha-a9532c7"
PORT=8000
export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

OUT="$NODE/results/variants"
mkdir -p "$OUT"

VARIANTS=(
"v0_published_defaults|  re_spatial: bym2\n  re_seasonal: rw1\n  re_interannual: iid\n  family: nbinomial"
"v1_no_spatial|  re_spatial: none\n  re_seasonal: rw1\n  re_interannual: iid\n  family: nbinomial"
"v2_seasonal_rw2|  re_spatial: bym2\n  re_seasonal: rw2\n  re_interannual: iid\n  family: nbinomial"
"v3_interannual_rw1|  re_spatial: bym2\n  re_seasonal: rw1\n  re_interannual: rw1\n  family: nbinomial"
"v4_poisson|  re_spatial: bym2\n  re_seasonal: rw1\n  re_interannual: iid\n  family: poisson"
)

cleanup() { docker rm -f ghrvariant >/dev/null 2>&1 || true; }
trap cleanup EXIT

docker pull --platform linux/amd64 "$IMAGE" >/dev/null
docker image inspect "$IMAGE" --format '{{.Id}} {{json .RepoDigests}}' > "$NODE/results/image_id.txt"

start_service() {
    docker rm -f ghrvariant >/dev/null 2>&1 || true
    docker run -d --platform linux/amd64 -p "$PORT:8000" --name ghrvariant "$IMAGE" >/dev/null
    for _ in $(seq 1 60); do
        curl -fsS "http://localhost:$PORT/health" >/dev/null 2>&1 && return 0
        sleep 3
    done
    echo "service did not become healthy" >&2; return 1
}

# What the service says it accepts, once.
start_service
curl -s "http://localhost:$PORT/api/v1/configs/\$schema" > "$NODE/results/config_schema.json"
curl -s "http://localhost:$PORT/api/v1/info" > "$NODE/results/service_info.json"

run_one() {  # name, dir; config.yaml already written
    local NAME="$1" VDIR="$2"
    start_service
    cp "$DATA/chap_LAO_admin1_monthly.csv" "$DATA/chap_LAO_admin1_monthly.geojson" "$VDIR/"
    set +e
    chap eval --model-name "http://localhost:$PORT" \
        --dataset-csv "$VDIR/chap_LAO_admin1_monthly.csv" \
        --output-file "$VDIR/evaluation.nc" \
        --run-config.is-chapkit-model \
        --model-configuration-yaml "$VDIR/config.yaml" > "$VDIR/chap_eval.log" 2>&1
    local rc=$?
    set -e
    echo "$rc" > "$VDIR/chap_eval_exit_code.txt"
    if [ "$rc" = 0 ]; then
        chap export-metrics --input-files "$VDIR/evaluation.nc" \
            --output-file "$VDIR/metrics.csv" >> "$VDIR/chap_eval.log" 2>&1
        echo "[variants] $NAME completed"
    else
        echo "[variants] $NAME exited $rc -- kept as the result it is"
    fi
    docker logs ghrvariant 2>&1 | sed 's/\x1b\[[0-9;]*m//g' > "$VDIR/service.log"
    grep -oE "disease_cases ~ 1[^\"]{0,250}" "$VDIR/service.log" | sort -u > "$VDIR/fitted_formula.txt" || true
    curl -s "http://localhost:$PORT/api/v1/configs" > "$VDIR/stored_config.json" || true
}

for entry in "${VARIANTS[@]}"; do
    NAME="${entry%%|*}"; BODY="${entry#*|}"
    VDIR="$OUT/$NAME"; mkdir -p "$VDIR"
    printf 'user_option_values:\n' > "$VDIR/config.yaml"
    printf "$BODY\n" >> "$VDIR/config.yaml"
    echo "[variants] === $NAME ==="; cat "$VDIR/config.yaml"
    run_one "$NAME" "$VDIR"
done

# The flat shape, outside the variants directory so the collector does not read it as one.
FLAT="$NODE/results/flat_shape"; mkdir -p "$FLAT"
printf 're_spatial: none\nre_seasonal: rw1\nre_interannual: iid\nfamily: nbinomial\n' > "$FLAT/config.yaml"
echo "[variants] === flat shape (expected to be refused) ==="
run_one flat_shape "$FLAT"

docker rm -f ghrvariant >/dev/null 2>&1 || true

# Batch 8b's own collector, unchanged, so "applied" means the same thing in both batches.
"$PYTHON" "$REPO_ROOT/analysis/06_configurability/scripts/lib/collect_variants.py" \
    --variants-dir "$OUT" --out "$NODE/results"

# Beside batch 8b's proxied variants, and the shape facts.
"$PYTHON" scripts/lib/compare_with_8b.py
