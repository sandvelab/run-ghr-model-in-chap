#!/usr/bin/env python3
"""The measured half of the human-cost model, for iteration 3's route A.

Document lengths are counted by batch 10's own `measure_documents`, imported rather than
copied, so both iterations are measured by one implementation. The two machine waits:

- `eval` -- the discovery log's own timestamps, `evaluation_started` to `evaluation_complete`,
  exactly as batch 10 measured iteration 2's route A.
- `pull` -- the clean-shell run of the route script, from `input_sha256.txt` (written just
  before `docker pull`) to `image_id.txt` (written just after). It includes one
  `chap validate`, a few seconds. The discovery run's own pull is bounded by its log only
  loosely, because the agent worked while it ran, so it is recorded alongside, not used.
  mtimes do not survive a fresh clone; like batch 10, this fails loudly rather than guess.

Standard library only.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[5]
sys.path.insert(0, str(REPO / "analysis/08_humanCost/scripts/lib"))
import measure_inputs as m08  # noqa: E402

LOG = "analysis/09_routeA_iteration3/01_discovery/results/discovery_log.tsv"
RUN = "analysis/09_routeA_iteration3/01_discovery/results/route_run"


def ts(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out-docs", required=True)
    ap.add_argument("--out-waits", required=True)
    a = ap.parse_args()
    out_docs = Path(a.out_docs)

    docs, missing = m08.measure_documents(REPO, m08.read_tsv(Path(a.manifest)), out_docs.parent)
    if missing:
        raise SystemExit("unmeasurable documents: " + "; ".join(missing))
    m08.write_tsv(out_docs, docs, ["doc_key", "words", "source"])

    rows = m08.read_tsv(REPO / LOG)
    by_ref = {r["ref"]: r for r in rows if r["kind"] == "milestone"}
    span_eval = (ts(by_ref["evaluation_complete"]["ts_utc"])
                 - ts(by_ref["evaluation_started"]["ts_utc"])).total_seconds()
    start_f, end_f = REPO / RUN / "input_sha256.txt", REPO / RUN / "image_id.txt"
    if not (start_f.is_file() and end_f.is_file()):
        raise SystemExit("pull wait not measurable: route_run outputs absent")
    span_pull = end_f.stat().st_mtime - start_f.stat().st_mtime
    decided = next(r for r in rows if r["kind"] == "decision" and "GHCR" in r["ref"])
    pulled = next(r for r in rows if r["kind"] == "command" and r["ref"].startswith("docker pull"))
    span_pull_disc = (ts(pulled["ts_utc"]) - ts(decided["ts_utc"])).total_seconds()
    for name, v in (("eval", span_eval), ("pull", span_pull)):
        if not 30 <= v <= 3600:
            raise SystemExit(f"{name} wait implausible: {v} s")
    waits = [
        {"wait_key": "eval", "seconds": round(span_eval), "used": "yes",
         "method": "discovery-log timestamps, evaluation_started to evaluation_complete",
         "source": LOG},
        {"wait_key": "pull", "seconds": round(span_pull), "used": "yes",
         "method": "clean-shell route run, mtime of input_sha256.txt to image_id.txt",
         "source": RUN},
        {"wait_key": "pull_discovery_upper_bound", "seconds": round(span_pull_disc), "used": "no",
         "method": "discovery log, decision to use the published image to the pull's own row; "
                   "the agent worked in parallel, so an upper bound on the first pull",
         "source": LOG},
    ]
    m08.write_tsv(Path(a.out_waits), waits, ["wait_key", "seconds", "used", "method", "source"])
    print(f"measured {len(docs)} documents; waits eval={round(span_eval)} s pull={round(span_pull)} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
