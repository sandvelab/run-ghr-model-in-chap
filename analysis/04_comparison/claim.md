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

---

### What the comparison itself yielded

**Both routes reached a CHAP evaluation, and both models ran as published.** Neither model was
modified and nothing was interposed between CHAP and either of them
(`results/comparison_table.tsv`).

**Route A cost more on every effort statistic that orders, and the gap is consistent rather
than dramatic.** 5 information sources to 4, 11 commands to 9, 3 dead ends to 2, 13.0 minutes
to a written evaluation against 4.8. Both readings of the logs order the routes the same way;
the normalisation narrows the gap and reverses nothing (`01_effort/`).

**The difference that is not a matter of degree is the prerequisite.** Route A needs a
container runtime, a container image build and a container registry; route B needs none of the
three. That is a property of the *mechanism* — serving a model over HTTP means shipping and
running an image — rather than of this particular model.

**Route A's largest single cost is a property of its model, not of its route.** The image is
amd64-only because R-INLA ships x86_64 binaries, so on this arm64 host it runs under emulation
throughout; that blocker was hit and never resolved. A chapkit model without a compiled
statistical backend would not pay it. The build-time figures understate a cold build, because
the host's layer cache was already warm and stayed warm on every re-run.

**Three things turned up independently in both logs, written by agents that never
communicated** — which is what makes them findings about CHAP rather than about a route:

1. **The GeoJSON has no command-line option.** CHAP finds polygons by matching the CSV's stem
   in the same directory (`chap_core.cli_endpoints._common.discover_geojson`). Both agents had
   to read the installed source to establish it; neither model's documentation says so. Move
   or rename the CSV alone and the geometry is silently lost.
2. **`chap eval` writes a file, not an answer.** Metrics require a separate
   `chap export-metrics`, and the evaluation plot appears only if `--plot` is passed. Neither
   model's README mentions either.
3. **One admin unit is silently dropped.** `LA-VI` has no target values, so both evaluations
   cover 17 of 18 units, announced in a warning inside a long log.

**Both routes needed the platform's installed source code to finish.** Neither route's answer
was fully available from public documentation. That is the same cost on both sides, and it is
CHAP's rather than either model's.

**Each route's scores are reported and not compared.** The two models are different models
fitted by different methods; the plan's §2 forbids a cross-route performance claim, and the
table fences those rows into a block labelled accordingly.
