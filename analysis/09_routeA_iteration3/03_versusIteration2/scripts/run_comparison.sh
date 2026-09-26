#!/usr/bin/env bash
# Iteration 2's and iteration 3's route A logs through the one effort instrument, both readings.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO_ROOT="$(cd ../../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"
IT2="$REPO_ROOT/analysis/02_routeA_chapkit/results/discovery_log.tsv"
IT3="$REPO_ROOT/analysis/09_routeA_iteration3/01_discovery/results/discovery_log.tsv"
"$PYTHON" "$REPO_ROOT/analysis/04_comparison/scripts/lib/summarise_discovery.py" \
    --log it2-route-a="$IT2" --log it3-route-a="$IT3" --out results/effort_aslogged.tsv
"$PYTHON" "$REPO_ROOT/analysis/04_comparison/01_effort/b_normalised/scripts/lib/normalise_logs.py" \
    --log it2-route-a="$IT2" --log it3-route-a="$IT3" \
    --out results/effort_normalised.tsv --changes results/what_the_rules_changed.md
"$PYTHON" "scripts/lib/compare.py"
