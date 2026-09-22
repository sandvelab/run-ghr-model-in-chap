#!/usr/bin/env bash
# Main script for node: 02_routeA_chapkit
# Generated shape -- edit the "own scripts" block; the child calls are maintained
# by `node.py rebuild`, which enforces the alternatives/sub-analyses semantics.
set -euo pipefail
cd "$(dirname "$0")"
REPO_ROOT="$(cd "../.." && pwd)"
# Node scripts run under the pinned analysis environment (AGENTS.md §2), not under
# .venv, which is the repository's own machinery. A node needing something beyond it
# declares env/ and overrides PYTHON below.
PYTHON="$REPO_ROOT/environment/env/bin/python"


# Own scripts -- add calls here as scripts/ fills up.

# The route itself. It writes to results/route_run/, leaving results/eval/ -- the run made by
# hand down the route as it was discovered -- untouched, so a reproduction adds a run rather
# than replacing the one the reports quote. The model fits with R-INLA and is not
# bit-reproducible, so the two will not agree to the last digit; that is the repeatability
# node's subject, not a defect.
bash scripts/run_route.sh
