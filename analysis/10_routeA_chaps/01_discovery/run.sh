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
# The route itself, as its discovering agent left it. It writes to results/clean_run/ and
# leaves the run made by hand during discovery (results/*.nc, *.html, metrics.csv) untouched.
# It installs chaps, uv and chap-core 2.3.1 into a fresh work dir, fetches the model image with
# scripts/fetch_image_oci.sh when Docker lacks it (about 1.5 h on a slow link; SKIP_PREFETCH=1
# lets chaps pull it instead), and needs Docker running. R-INLA is not bit-reproducible, so a
# re-run moves the scores slightly.
bash scripts/run_route.sh results/clean_run
