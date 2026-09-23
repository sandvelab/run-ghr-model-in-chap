#!/usr/bin/env bash
# Measure the model's grounded inputs, then carry both personas down both routes.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO_ROOT="$(cd ../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"

# The measured half: document lengths, machine waits. Fails loudly rather than
# costing an unmeasurable document as zero.
"$PYTHON" scripts/lib/measure_inputs.py \
    --repo-root "$REPO_ROOT" \
    --manifest scripts/inputs/documents.tsv \
    --out-docs results/doc_sizes.tsv \
    --out-waits results/machine_waits.tsv

# The authored half joins the measured half here.
"$PYTHON" scripts/lib/human_cost.py \
    --inputs scripts/inputs \
    --results results
