#!/usr/bin/env bash
# The as-logged reading: each log counted exactly as its own agent wrote it.
#
# This alternative adds no counting code of its own -- face value is what the shared
# instrument already computes, and a second implementation here is precisely what the
# comparison node exists to avoid. The script is a one-line call to that instrument.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO_ROOT="$(cd ../../../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"

"$PYTHON" "$REPO_ROOT/analysis/04_comparison/scripts/lib/summarise_discovery.py" \
    --log route-a="$REPO_ROOT/analysis/02_routeA_chapkit/results/discovery_log.tsv" \
    --log route-b="$REPO_ROOT/analysis/03_routeB_mlproject/results/discovery_log.tsv" \
    --out results/effort_by_route.tsv
