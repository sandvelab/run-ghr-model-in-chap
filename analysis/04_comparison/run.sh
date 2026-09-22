#!/usr/bin/env bash
# Main script for node: 04_comparison
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

# The instrument gates the node: if the tests that define what a discovery log means do not
# pass, no statistic computed from a log is worth reading, so the run stops here.
"$PYTHON" scripts/test_discovery_log.py

# summarise_discovery.py and build_comparison.py are wired in by batch 5, once both routes
# have logs. A call to them now would fail on absent inputs and break the property that
# analysis/run.sh runs end to end.
