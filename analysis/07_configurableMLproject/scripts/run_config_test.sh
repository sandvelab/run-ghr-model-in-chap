#!/usr/bin/env bash
# Does the MLproject route deliver a configuration to the model?
#
# Route A's model declares eighteen options that cannot be set through CHAP; route B's model
# declares none. Neither can show a configuration arriving. This third template declares one
# tunable option, `alpha`, and -- decisively -- its train.py PRINTS the configuration dict it
# was handed. So the question is answered by reading what the model says it received, not by
# inferring it from scores.
#
# Nothing is interposed. If this works, it works the way an operator would do it.
set -euo pipefail
cd "$(dirname "$0")/.."
NODE="$(pwd)"
REPO_ROOT="$(cd ../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"
MODEL="$REPO_ROOT/Archive/model-case-c/repo"
DATA="$REPO_ROOT/Archive/data-lao"
OUT="$NODE/results/runs"
mkdir -p "$OUT"

# The value asked for, per run. Widely separated so that if the model is really receiving them,
# the fitted ridge penalty -- and therefore the predictions -- cannot help but differ.
ALPHAS=("1e-5" "1e2" "1e5")

# Archive/ is read-only (AGENTS.md §8), so the model is copied out before being run -- and
# OUTSIDE the repository, because CHAP runs an MLproject model by copying the whole directory
# into runs/<timestamp>/ beside itself and building a uv environment there. Under results/ that
# is ~800 MB of the model's dependencies per run, including scipy's test fixtures, which the
# invariant checker rightly reads as unexplained figures sitting in a results directory.
WORK="$(mktemp -d "${TMPDIR:-/tmp}/caseC.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
cp -R "$MODEL/." "$WORK/"

cp "$DATA/chap_LAO_admin1_monthly.csv"     "$OUT/"
cp "$DATA/chap_LAO_admin1_monthly.geojson" "$OUT/"

# What CHAP itself says a configuration for this template should look like.
chap model schema "$WORK" --example > "$NODE/results/chap_example_config.yaml" 2>/dev/null || \
    echo "(chap model schema --example failed)" > "$NODE/results/chap_example_config.yaml"

for A in "${ALPHAS[@]}"; do
    D="$OUT/alpha_$A"; mkdir -p "$D"
    # The shape the model's own config.yaml uses.
    printf 'user_option_values:\n    alpha:\n        values: %s\n' "$A" > "$D/config.yaml"

    echo "[case-c] alpha=$A"
    if (cd "$WORK" && chap eval --model-name . \
            --dataset-csv "$OUT/chap_LAO_admin1_monthly.csv" \
            --output-file "$D/eval.nc" \
            --model-configuration-yaml "$D/config.yaml") > "$D/chap_eval.log" 2>&1; then
        chap export-metrics --input-files "$D/eval.nc" --output-file "$D/metrics.csv" \
            >> "$D/chap_eval.log" 2>&1
        echo "[case-c] alpha=$A completed"
    else
        echo "[case-c] alpha=$A FAILED -- kept as the result it is"
    fi

    # The file CHAP wrote into the model's run directory, which the model then reads. This is
    # the direct evidence that the value arrived.
    find "$WORK/runs" -name model_configuration_for_run.yaml -newer "$D/config.yaml" \
        -exec cp {} "$D/model_configuration_for_run.yaml" \; 2>/dev/null || true
done

# A fifth run, in the shape CHAP's own `chap model schema --example` emits for this template --
# a bare scalar rather than the `values:` mapping the model reads. Kept because what happens is
# the point: the same class of disagreement as route A's, and it behaves completely differently.
D="$OUT/chap_example_shape"; mkdir -p "$D"
printf 'user_option_values:\n  alpha: 1e-5\nadditional_continuous_covariates: []\n' > "$D/config.yaml"
echo "[case-c] chap example shape"
if (cd "$WORK" && chap eval --model-name . \
        --dataset-csv "$OUT/chap_LAO_admin1_monthly.csv" \
        --output-file "$D/eval.nc" \
        --model-configuration-yaml "$D/config.yaml") > "$D/chap_eval.log" 2>&1; then
    chap export-metrics --input-files "$D/eval.nc" --output-file "$D/metrics.csv" \
        >> "$D/chap_eval.log" 2>&1
    echo "[case-c] chap example shape completed"
else
    echo "[case-c] chap example shape FAILED -- which is the result"
fi
find "$WORK/runs" -name model_configuration_for_run.yaml -newer "$D/config.yaml" \
    -exec cp {} "$D/model_configuration_for_run.yaml" \; 2>/dev/null || true

# Keep the configuration files CHAP wrote for the model -- the evidence -- and nothing else
# from the working copy.
"$PYTHON" scripts/lib/collect_config_test.py --runs "$OUT" --out "$NODE/results"
