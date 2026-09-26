#!/usr/bin/env bash
# Batch 10's model, unchanged, over iteration 3's route A act sequence.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO_ROOT="$(cd ../../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"

# The rates and persona knowledge are batch 10's, byte for byte. Refuse to run otherwise:
# a difference in the estimate must come from the route, not from re-tuning the model.
for f in act_costs personas prerequisites modifiers reading_rates; do
    cmp -s "scripts/inputs/$f.tsv" "$REPO_ROOT/analysis/08_humanCost/scripts/inputs/$f.tsv" \
        || { echo "scripts/inputs/$f.tsv differs from batch 10's" >&2; exit 1; }
done

"$PYTHON" scripts/lib/measure_inputs_it3.py \
    --manifest scripts/inputs/documents.tsv \
    --out-docs results/doc_sizes.tsv \
    --out-waits results/machine_waits.tsv

"$PYTHON" "$REPO_ROOT/analysis/08_humanCost/scripts/lib/human_cost.py" \
    --inputs scripts/inputs --results results
