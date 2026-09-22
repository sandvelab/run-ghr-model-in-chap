#!/usr/bin/env bash
# The comparison node's own work, in one entry point.
#
# `node.py` regenerates a node's run.sh by calling every file directly under scripts/ with no
# arguments, so anything needing arguments is driven from here and lives in scripts/lib/,
# which node.py treats as supporting material rather than as callable steps.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO_ROOT="$(cd ../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"

# The instrument gates the node: if the tests that define what a discovery log means do not
# pass, no statistic computed from a log is worth reading, so the run stops here.
"$PYTHON" scripts/lib/test_discovery_log.py

# The comparison table reads the effort file of the 01_effort fork's MAIN PATH only.
# analysis/run.sh follows the main path at every fork, so naming a non-main alternative's
# output here would name a file a full reproduction never regenerates.
"$PYTHON" scripts/lib/build_comparison.py \
    --effort 01_effort/b_normalised/results/effort_by_route.tsv \
    --route route-a="Route A (chapkit)":"$REPO_ROOT/analysis/02_routeA_chapkit/results/discovery_log.tsv":"$REPO_ROOT/analysis/02_routeA_chapkit/results/eval/metrics.csv" \
    --route route-b="Route B (MLproject)":"$REPO_ROOT/analysis/03_routeB_mlproject/results/discovery_log.tsv":"$REPO_ROOT/analysis/03_routeB_mlproject/results/eval/metrics.csv" \
    --out results/comparison_table.tsv
