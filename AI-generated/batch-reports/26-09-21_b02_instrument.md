# Batch 2 — The measurement instrument

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 2

## What this batch was for

This project compares two routes on how much work each one costs. That comparison is only as
good as the thing the work is recorded in, and a log format settled after the first route has
run is a format shaped by that route. So the instrument is fixed first, before either route
is touched, and it is fixed identically for both.

## What was done

**The format.** `AI-internal/skill-references/discovery-log-format.md` specifies
`results/discovery_log.tsv`: six columns (`step`, `ts_utc`, `kind`, `ref`, `outcome`,
`note`), a closed `kind` vocabulary (`resource`, `command`, `decision`, `blocker`,
`milestone`), the outcomes each kind may take, and a **closed list of seven milestones** —
from `first_doc_opened` to `evaluation_complete` or `route_abandoned`. The milestones are
what make two different-looking routes comparable at all: they are stated in terms of what
has been achieved, not of what was typed.

**The code.** `analysis/04_comparison/scripts/discovery_log.py` validates a log against that
specification and computes nineteen statistics from it — resources consulted, used and
discarded; commands run and failed; blockers hit and left unresolved; dead ends; elapsed
minutes in total and to `evaluation_complete`; and the counts of resources and commands
reached *before* completion, so that what a route cost is what it cost to get there rather
than what was read afterwards. `summarise_discovery.py` runs it over both routes' logs and
writes one long file, `results/effort_by_route.tsv`, that every later report reads from.

**The tests.** `scripts/test_discovery_log.py` builds synthetic logs and asserts every
statistic, then asserts that seven kinds of malformed log are rejected rather than repaired:
a disallowed outcome, an invented milestone, an unknown kind, a step sequence that does not
start at 1, a timestamp that goes backwards, a misformatted timestamp, and an empty `ref`.
It is called by the node's `run.sh`, so a full reproduction re-runs it.

**Two integrity statistics.** `n_distinct_timestamps` and `max_rows_sharing_one_timestamp`
exist to expose the one failure that would otherwise be invisible: a log written in one
sitting at the end. A reconstructed log shows up as a handful of timestamps carrying many
rows each. The test asserts this directly — twelve rows collapsed onto one timestamp are
detected — and the plan's §3 requires such a log to be reported as inadmissible for the
effort measures rather than quietly used.

## What was established about the machine

Docker Desktop 27.4.0 is running (server 27.4.0, 8 CPUs, ~8.2 GB). Route A was expected to
need a container runtime, and at the time the anchors were pinned the daemon was down; it is
now up, so nothing blocks batch 3. This and the other unpinnable dependencies are recorded in
`environment/README.md`.

## What was deliberately not done

The plan's batch 2 said to confirm that the Lao data loads into CHAP. It was not done, and
the aim was narrowed on purpose. The data's structure was already established in batch 1 from
the files themselves. Loading it *into CHAP* requires knowing how CHAP wants a dataset
presented — which is part of what each route's agent has to find out, and what the
orchestrating agent must not learn first and then leak. The cost of narrowing is that a
route's agent may spend effort on a data-shaping problem that is not really about its route;
that cost is symmetric across the two routes, and it is visible in both logs, so it can be
read off rather than guessed at.

## Deviations from the plan

`summarise_discovery.py` is written but not yet called by `04_comparison/run.sh`: there are
no logs to summarise until batches 3 and 4 have run, and a script that fails on absent inputs
would break the property that `analysis/run.sh` reproduces the analysis end to end. The call
is wired in batch 5. Recorded in the plan's §4b.
