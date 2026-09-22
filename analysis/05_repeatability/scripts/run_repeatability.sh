#!/usr/bin/env bash
# Does each route run again, from clean?
#
# Each route's own run_route.sh is run once more, into this node's results/ rather than into
# the route's, so a repeat never overwrites the run the reports quote. Then every run this
# repository holds -- these, the ones in the route nodes, and the versions in git history --
# is collected and the spread across them reported.
#
# This is deliberately expensive: it re-runs both routes end to end. That is the question the
# node exists to answer, and an answer assembled from the runs that happened to be lying
# around would not be one.
set -euo pipefail
cd "$(dirname "$0")/.."
NODE="$(pwd)"
REPO_ROOT="$(cd ../.. && pwd)"
PYTHON="$REPO_ROOT/environment/env/bin/python"

mkdir -p "$NODE/results/rerun_routeA" "$NODE/results/rerun_routeB"

echo "[repeat] route A"
if bash "$REPO_ROOT/analysis/02_routeA_chapkit/scripts/run_route.sh" \
        --out-dir "$NODE/results/rerun_routeA" > "$NODE/results/rerun_routeA.log" 2>&1; then
    echo "[repeat] route A completed"
else
    echo "[repeat] route A FAILED -- see results/rerun_routeA.log, kept as the result it is"
fi

echo "[repeat] route B"
if bash "$REPO_ROOT/analysis/03_routeB_mlproject/scripts/run_route.sh" \
        "$REPO_ROOT/Archive/data-lao" "$NODE/results/rerun_routeB" \
        > "$NODE/results/rerun_routeB.log" 2>&1; then
    echo "[repeat] route B completed"
else
    echo "[repeat] route B FAILED -- see results/rerun_routeB.log, kept as the result it is"
fi

cd "$REPO_ROOT"
"$PYTHON" analysis/05_repeatability/scripts/lib/collect_runs.py \
    --metrics "route-a:hand run down the route:analysis/02_routeA_chapkit/results/eval/metrics.csv" \
    --metrics "route-a:run_route.sh in the route node:analysis/02_routeA_chapkit/results/route_run/metrics.csv" \
    --metrics "route-a:re-run from clean:analysis/05_repeatability/results/rerun_routeA/metrics.csv" \
    --metrics "route-b:run_route.sh in the route node:analysis/03_routeB_mlproject/results/eval/metrics.csv" \
    --metrics "route-b:re-run from clean:analysis/05_repeatability/results/rerun_routeB/eval/metrics.csv" \
    --out analysis/05_repeatability/results
