#!/usr/bin/env python3
"""Extract the chapkit REST contract CHAP actually depends on, from a run's own log.

Route A works only if chap-core and the model's chapkit service agree on the payload of every
endpoint below. That set is what an `MLproject` model has no equivalent of, so counting it is
the concrete form of "serving a model over HTTP adds a compatibility surface".

Read from the log of a real evaluation rather than from chap-core's source, because what the
platform *can* call and what it *does* call on a route are different questions.

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

CALL = re.compile(r"HTTP Request: (GET|POST|PUT|PATCH|DELETE) (https?://[^\s]+)")
OPAQUE_ID = re.compile(r"[0-9A-Z]{20,}")

# What each endpoint has to agree about, which is the point of the exercise.
CONTRACT = {
    "/api/v1/info": "service identity and version fields; chap-core validates this payload",
    "/api/v1/configs/$schema": "the JSON schema the service advertises for its configuration",
    "/api/v1/configs": "the configuration payload itself -- where the two ends disagree",
    "/api/v1/ml/$train": "the training request and the dataset encoding",
    "/api/v1/ml/$predict": "the prediction request, per forecast window",
    "/api/v1/jobs/{id}": "asynchronous job status, polled until a job finishes",
    "/api/v1/artifacts/{id}": "the trained artefact handed between train and predict",
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--log", type=Path, required=True, help="a chap eval log from route A")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    counts: Counter[tuple[str, str]] = Counter()
    for method, url in CALL.findall(a.log.read_text(errors="replace")):
        path = re.sub(r"^https?://[^/]+", "", url)
        path = OPAQUE_ID.sub("{id}", path)
        counts[(method, path)] += 1

    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["method", "path", "calls_in_one_evaluation", "what_must_agree"])
        for (method, path), n in sorted(counts.items(), key=lambda kv: -kv[1]):
            w.writerow([method, path, n, CONTRACT.get(path, "")])

    print(f"{len(counts)} distinct endpoints over {sum(counts.values())} calls -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
