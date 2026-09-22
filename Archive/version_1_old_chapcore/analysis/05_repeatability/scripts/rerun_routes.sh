#!/usr/bin/env bash
# Re-run both routes end to end, from each route's own deliverable script, and keep every
# run's metrics.
#
# This is the thing that answers "does it still run". It is deliberately NOT called by this
# node's run.sh: each invocation costs a container build and a full backtest, and its output
# is *accumulated evidence* rather than a derivation -- a run that happened is not something
# a later run regenerates. Call it when you want to add a run; run.sh then reports over
# everything collected so far.
#
# Scores are expected to move between runs and that is not a fault (plan §2, §3). What is
# recorded is whether each route completed and what its numbers did.
set -uo pipefail

NODE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$NODE_DIR"
export PATH="$HOME/.local/bin:$PATH"

LEDGER="results/run_ledger.tsv"
[[ -f "$LEDGER" ]] || printf 'route\tattempt_utc\tscript\texit_code\tseconds\tcompleted\tmetrics_archived_as\n' > "$LEDGER"

archive() {   # archive <route letter> <source metrics csv> <label>
    local route="$1" src="$2" label="$3"
    [[ -f "$src" ]] || { echo "  (no $src to archive)"; return 1; }
    local dest="results/history/${route}/$(date -u +%Y%m%dT%H%M%SZ)_${label}.csv"
    cp "$src" "$dest"
    echo "$dest"
}

run_route() {  # run_route <letter> <node dir> <metrics csv, relative to node dir>
    local route="$1" node="$2" metrics="$3"
    echo "== route $route: archiving what is already there =="
    for existing in "$node"/results/eval_metrics*.csv; do
        [[ -f "$existing" ]] || continue
        local base; base="$(basename "$existing" .csv)"
        # Only archive a file this node has not already taken a copy of.
        if ! grep -q "$(shasum -a 256 "$existing" | cut -c1-16)" results/history/"$route"/.digests 2>/dev/null; then
            local dest; dest="$(archive "$route" "$existing" "prior_${base}")"
            shasum -a 256 "$existing" | cut -c1-16 >> results/history/"$route"/.digests
            echo "  archived $existing -> $dest"
        fi
    done

    echo "== route $route: re-running $node/scripts/run_route.sh =="
    local start end code
    start=$(date +%s)
    ( bash "$node/scripts/run_route.sh" ) > "results/rerun_route${route}.log" 2>&1
    code=$?
    end=$(date +%s)

    local completed="no" archived="-"
    if [[ $code -eq 0 && -f "$node/$metrics" ]]; then
        completed="yes"
        archived="$(archive "$route" "$node/$metrics" "rerun")"
        shasum -a 256 "$node/$metrics" | cut -c1-16 >> results/history/"$route"/.digests
    fi
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$route" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$node/scripts/run_route.sh" \
        "$code" "$((end - start))" "$completed" "$archived" >> "$LEDGER"
    echo "== route $route: exit $code, $((end - start))s, completed=$completed =="
}

# Route A leaves a named container behind; remove it so the re-run starts from clean.
docker rm -f chapkit-ghr-model-route-a >/dev/null 2>&1 || true

run_route A ../02_routeA_chapkit results/eval_metrics.csv
run_route B ../03_routeB_mlproject results/eval_metrics.csv

docker rm -f chapkit-ghr-model-route-a >/dev/null 2>&1 || true
echo "== done; see $LEDGER =="
