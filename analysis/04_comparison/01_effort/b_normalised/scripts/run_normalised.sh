#!/usr/bin/env bash
# The normalised reading: two rules applied to both logs alike, then counted.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO_ROOT="$(cd ../../../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"

"$PYTHON" scripts/lib/normalise_logs.py \
    --log route-a="$REPO_ROOT/analysis/02_routeA_chapkit/results/discovery_log.tsv" \
    --log route-b="$REPO_ROOT/analysis/03_routeB_mlproject/results/discovery_log.tsv" \
    --out results/effort_by_route.tsv \
    --changes results/what_the_rules_changed.md
