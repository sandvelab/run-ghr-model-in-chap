#!/usr/bin/env bash
# Main script for node: 03_routeB_mlproject
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

bash scripts/run_route.sh

# Then the values behind the figure CHAP just drew, read out of the figure itself.
# ORDER IS LOAD-BEARING and this block is hand-written: `node.py rebuild` regenerates the
# own-scripts block in alphabetical order, which would put the extraction before the route
# that produces the file it reads.
"$PYTHON" scripts/evaluation_plot.py
