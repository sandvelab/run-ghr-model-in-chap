#!/usr/bin/env python3
"""The measured half of the human-cost model, for route A through chaps (batch 14).

Document lengths are counted by batch 10's own `measure_documents`, imported rather than
copied, so every batch is measured by one implementation. The machine waits:

- `eval` -- the discovery log's own timestamps, `evaluation_started` to `evaluation_complete`,
  as batches 10 and 12 measured it.
- `pull` -- **not measurable in this batch**: chaps never completed a pull on this link. The
  main figure uses batch 12's measured pull of the same model's image on a working link (its
  `machine_waits.tsv`, read here, not retyped), and says so.
- `pull_failed` -- this link: `chaps run` launched (log row 14) to its failure, rc=18 (row 26).
  Used only by the slow-link route.
- `image_fetch_workaround` -- this link: the agent's resumable fetcher, launch (row 28) to the
  loaded image (row 31). Recorded, not used: the workaround is not a persona step.

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

LOG = "analysis/10_routeA_chaps/01_discovery/results/discovery_log.tsv"
B12_WAITS = "analysis/09_routeA_iteration3/02_humanCost/results/machine_waits.tsv"


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

    rows = {r["step"]: r for r in m08.read_tsv(REPO / LOG)}
    milestones = {r["ref"]: r for r in rows.values() if r["kind"] == "milestone"}

    def span(a_step: str, b_step: str, a_expect: str, b_expect: str) -> int:
        ra, rb = rows[a_step], rows[b_step]
        # Refuse to measure if the log rows are not the ones this script was written against.
        if not (ra["ref"].startswith(a_expect) and rb["ref"].startswith(b_expect)):
            raise SystemExit(f"log rows {a_step}/{b_step} are not the expected commands")
        return round((ts(rb["ts_utc"]) - ts(ra["ts_utc"])).total_seconds())

    span_eval = round((ts(milestones["evaluation_complete"]["ts_utc"])
                       - ts(milestones["evaluation_started"]["ts_utc"])).total_seconds())
    span_failed = span("14", "26", "chaps run", "chaps run")
    if rows["26"]["outcome"] != "failed":
        raise SystemExit("log row 26 is not the failed chaps run")
    span_fetch = span("28", "31", "scripts/fetch_image_oci.sh", "scripts/fetch_image_oci.sh")
    b12 = {r["wait_key"]: r for r in m08.read_tsv(REPO / B12_WAITS)}
    pull = int(b12["pull"]["seconds"])
    if not 30 <= span_eval <= 3600:
        raise SystemExit(f"eval wait implausible: {span_eval} s")

    waits = [
        {"wait_key": "eval", "seconds": span_eval, "used": "yes",
         "method": "discovery-log timestamps, evaluation_started to evaluation_complete",
         "source": LOG},
        {"wait_key": "pull", "seconds": pull, "used": "yes",
         "method": "borrowed: batch 12's clean-shell pull of the same model's image (sha-a9532c7) "
                   "on a working link; chaps completed no pull on this batch's link",
         "source": B12_WAITS},
        {"wait_key": "pull_failed", "seconds": span_failed, "used": "slow-link route only",
         "method": "discovery log, chaps run launched (row 14) to its failure rc=18 (row 26)",
         "source": LOG},
        {"wait_key": "image_fetch_workaround", "seconds": span_fetch, "used": "no",
         "method": "discovery log, the agent's resumable fetcher launched (row 28) to the image "
                   "loaded (row 31); a workaround, not a persona step",
         "source": LOG},
    ]
    m08.write_tsv(Path(a.out_waits), waits, ["wait_key", "seconds", "used", "method", "source"])
    print(f"measured {len(docs)} documents; waits eval={span_eval} s pull={pull} s (borrowed) "
          f"pull_failed={span_failed} s image_fetch_workaround={span_fetch} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
