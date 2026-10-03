#!/usr/bin/env bash
# Batch 10's model, unchanged, over route A taken through chaps (batch 14), plus two
# sensitivities that each change one input.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO_ROOT="$(cd ../../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"
MODEL="$REPO_ROOT/analysis/08_humanCost/scripts/lib/human_cost.py"

# The rates and persona knowledge are batch 10's, byte for byte. Refuse to run otherwise:
# a difference in the estimate must come from the route, not from re-tuning the model.
for f in act_costs personas prerequisites modifiers reading_rates; do
    cmp -s "scripts/inputs/$f.tsv" "$REPO_ROOT/analysis/08_humanCost/scripts/inputs/$f.tsv" \
        || { echo "scripts/inputs/$f.tsv differs from batch 10's" >&2; exit 1; }
done

# `chaps run --help` is measured from the release the agent used. Put a chaps v0.99.4 binary on
# PATH (its install.sh --dir <dir>, then CHAPS_BIN=<dir>), or this stops.
[ -n "${CHAPS_BIN:-}" ] && PATH="$CHAPS_BIN:$PATH"
PATH="$HOME/.local/bin:$PATH"
chaps self version 2>/dev/null | grep -q 'v0.99.4' \
    || { echo "chaps v0.99.4 not on PATH (set CHAPS_BIN)" >&2; exit 1; }

"$PYTHON" scripts/lib/measure_inputs_b14.py \
    --manifest scripts/inputs/documents.tsv \
    --out-docs results/doc_sizes.tsv \
    --out-waits results/machine_waits.tsv

"$PYTHON" "$MODEL" --inputs scripts/inputs --results results

for s in docker_lighter run_doc_not_ai_page; do
    out="$("$PYTHON" scripts/lib/sensitivities.py --inputs scripts/inputs --results results --name "$s")"
    "$PYTHON" "$MODEL" --inputs "$out/inputs" --results "$out"
done
