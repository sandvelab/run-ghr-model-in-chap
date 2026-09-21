#!/usr/bin/env bash
# Point CHAP at the running chapkit service *directly*, with no shim, and record what
# happens. This is the evidence for the claim that route A does not run as published: it
# turns a statement in a report into something a reader can re-run in ten seconds.
#
# It needs route A's container up on :8000 (scripts/rerun_routes.sh leaves it running while
# it works). It submits no job: the failure, if it is the one described, happens while CHAP
# is still reading /api/v1/info, so this costs nothing and disturbs no running evaluation.
set -uo pipefail
NODE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$NODE_DIR"
export PATH="$HOME/.local/bin:$PATH"
OUT=results/as_published_probe.log

{
  echo "== probe run at $(date -u +%Y-%m-%dT%H:%M:%SZ) =="
  echo
  echo "-- 1. is the service answering? --"
  curl -sS -o /tmp/info.json -w 'HTTP %{http_code}\n' http://localhost:8000/api/v1/info
  echo "-- the payload the service sends --"
  python3 -m json.tool /tmp/info.json
  echo
  echo "-- 2. which chapkit does the service run? which does chap-core pin? --"
  echo "service:   $(python3 -c 'import json;d=json.load(open("/tmp/info.json"));print(d.get("chapkit_version"),"/ servicekit",d.get("servicekit_version"))')"
  echo "chap-core: $("$HOME/.local/share/uv/tools/chap-core/bin/python" -c 'import importlib.metadata as m; print(m.version("chapkit"), "/ servicekit", m.version("servicekit"))' 2>&1)"
  echo
  echo "-- 3. CHAP pointed straight at the service, no shim --"
  chap model schema http://localhost:8000 --example 2>&1 | tail -20
  echo "   exit: ${PIPESTATUS[0]}"
  echo
  echo "-- 4. and with the documented escape hatch --"
  chap eval --model-name http://localhost:8000 --run-config.is-chapkit-model \
    --dataset-csv /tmp/chapdata/chap_LAO_admin1_monthly.csv \
    --output-file /tmp/as_published_probe.nc \
    --backtest-params.n-splits 1 --backtest-params.n-periods 3 2>&1 | tail -20
  echo "   exit: ${PIPESTATUS[0]}"
} > "$OUT" 2>&1
echo "wrote $OUT"
tail -60 "$OUT"
