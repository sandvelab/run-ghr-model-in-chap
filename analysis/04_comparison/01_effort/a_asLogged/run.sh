#!/usr/bin/env bash
# Main script for node: a_asLogged
# Generated shape -- edit the "own scripts" block; the child calls are maintained
# by `node.py rebuild`, which enforces the alternatives/sub-analyses semantics.
set -euo pipefail
cd "$(dirname "$0")"
REPO_ROOT="$(cd "../../../.." && pwd)"
# Node scripts run under the pinned analysis environment (AGENTS.md §2), not under
# .venv, which is the repository's own machinery. A node needing something beyond it
# declares env/ and overrides PYTHON below.
PYTHON="$REPO_ROOT/environment/env/bin/python"


# Own scripts -- add calls here as scripts/ fills up.
# This alternative stores no script of its own: taking each log at face value is exactly what
# the instrument already does, so the reading is the summariser run on the raw logs. A copy of
# it here would be a second implementation of the thing the comparison node exists to keep
# single.
"$PYTHON" ../../scripts/summarise_discovery.py \
    --log route-a="$REPO_ROOT/analysis/02_routeA_chapkit/results/discovery_log.tsv" \
    --log route-b="$REPO_ROOT/analysis/03_routeB_mlproject/results/discovery_log.tsv" \
    --out results/effort_by_route.tsv
