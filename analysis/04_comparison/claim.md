# Claim

How do the two routes compare on what it took to find out how to run each and to actually run it? Route A against route B on the resources that had to be consulted, the process of finding out including its dead ends, and the working invocation each arrived at -- computed by one implementation from both routes' logs, so the two are never measured by subtly different code. Each route's predictive scores are reported here but never compared across routes.

## Children

kind: sub-analyses
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(Each belongs in the claim collection under `Human-AI-collaboration/claims/` with a pointer
to the result grounding it.)_

**The instrument is in place and both routes will be measured by it.** `scripts/`
holds `discovery_log.py` — the reader, validator and statistics for a `discovery_log.tsv` —
and `summarise_discovery.py`, which runs it over both routes' logs into one file. The counts
live here rather than in either route's node so that the two routes cannot be measured by
subtly different code; a route's node holds only its raw log, which is that route's result.
The format itself is specified in `AI-internal/skill-references/discovery-log-format.md` and
is not restated in the code.

**Two of the twenty statistics are definitions and are stated as such.** A *dead end* is a
`command` row that failed, plus each **distinct** blocker hit — a blocker logged `open` and
later `resolved` counts once, because the route still had to go round it. *Elapsed minutes*
are wall-clock, reported because they are cheap and explicitly not the primary measure.

**A reconstructed log has a visible signature, and it is computed rather than trusted.**
`n_distinct_timestamps` and `max_rows_sharing_one_timestamp` go into the output for every
route. A log written in one sitting at the end shows up as a handful of timestamps carrying
many rows each, which the plan's §3 requires be reported as inadmissible rather than quietly
used. 15 tests cover the format, the statistics and this signature, and the node's `run.sh`
runs them as a gate: if they fail, nothing downstream is worth reading.

**The machine provides what route A will need** (`results/host_prerequisites.log`). Docker
27.4.0 is running, serving `linux/aarch64` on an `arm64` host, and **no build of route A's
model is cached** — it will pay for its image. One unrelated chapkit model image from other
work is present and is recorded, because shared base layers would let route A's build reuse
some of it; how much is measured in batch 3 rather than assumed.
