#!/usr/bin/env bash
# Main script for node: b_normalised
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
"$PYTHON" ../../scripts/summarise_discovery.py --normalise \
    --not-a-source Archive/data-lao \
    --not-a-source results/ \
    --not-a-source runs/ \
    --route A=../../../02_routeA_chapkit/results/discovery_log.tsv \
    --route B=../../../03_routeB_mlproject/results/discovery_log.tsv \
    --out results/effort_by_route.tsv
