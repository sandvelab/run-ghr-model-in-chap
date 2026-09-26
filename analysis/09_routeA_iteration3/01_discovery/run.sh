#!/usr/bin/env bash
# Main script for node: 01_discovery
# Generated shape -- edit the "own scripts" block; the child calls are maintained
# by `node.py rebuild`, which enforces the alternatives/sub-analyses semantics.
set -euo pipefail
cd "$(dirname "$0")"
REPO_ROOT="$(cd "../../.." && pwd)"
# Node scripts run under the pinned analysis environment (AGENTS.md §2), not under
# .venv, which is the repository's own machinery. A node needing something beyond it
# declares env/ and overrides PYTHON below.
PYTHON="$REPO_ROOT/environment/env/bin/python"


# Own scripts
# The route itself, as its discovering agent left it. It writes to results/route_run/ and
# leaves results/manual_run/ -- the run made by hand during discovery -- untouched. The model
# fits with R-INLA and is not bit-reproducible, so a re-run moves the scores slightly.
bash scripts/run_route.sh

# Then the values behind the figures CHAP drew. ORDER IS LOAD-BEARING: the extraction reads
# files the route writes, and `node.py rebuild` would put it first alphabetically.
"$PYTHON" scripts/evaluation_plot.py
