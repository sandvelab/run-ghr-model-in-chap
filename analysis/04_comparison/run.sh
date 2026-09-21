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

# Sub-analyses: every child runs, in order.
bash "01_effort/run.sh"

# Own scripts
# discovery_log.py is a module, not an entry point, and summarise_discovery.py is called
# by each alternative under 01_effort with that alternative's own arguments -- which is
# what makes the two readings differ. What runs here is the instrument's test suite,
# because every number below it is produced by the code these tests exercise.
"$PYTHON" scripts/test_discovery_log.py
"$PYTHON" scripts/build_comparison.py
