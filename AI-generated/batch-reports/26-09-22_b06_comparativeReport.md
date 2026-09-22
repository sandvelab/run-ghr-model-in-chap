# Batch 6 — route A against route B

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 2

Phase C. The comparison the project was built to make: which route was easier to find out
about, which was easier to carry out, the evidence for each statement, and an explicit
statement of what one run per route can and cannot resolve.

Every count is read from `analysis/04_comparison/results/comparison_table.tsv`, which a script
computes from both logs by one implementation.

---

## The short answer

**Both routes run, and both models ran as published.** Route A costs more on every effort
statistic that orders, and the gap is consistent rather than dramatic. The difference that is
*not* a matter of degree is the prerequisite: route B needs nothing beyond CHAP itself.

## (a) and (b) — what had to be read, and what the process looked like

| | Route A (chapkit) | Route B (MLproject) |
|---|---|---|
| Reached a CHAP evaluation | yes | yes |
| Information sources consulted | 5 | 4 |
| …that contributed | 5 | 4 |
| Commands run | 11 | 9 |
| …that failed | 1 | 1 |
| Blockers hit | 2 | 1 |
| …left unresolved | **1** | 0 |
| **Dead ends** | **3** | **2** |
| Judgment calls logged | 3 | 1 |
| Minutes to a written evaluation | 13.0 | 4.8 |

The ratios sit between 1.2 and 2.7. Route A is harder, but not in the way a broken route is
harder: it reaches an evaluation by a documented mechanism, with the model unmodified and
nothing interposed.

### How effort is read is itself a judgment call, and it is a fork in the tree

Taken at face value, route A has **zero** failed commands and route B has one. That is a true
statement about the logs and a false impression of the routes: route A's agent marked two
commands `ok` before reading their output and recorded the failures in later rows.

So `analysis/04_comparison/01_effort/` is an alternatives node. `a_asLogged` takes each log
exactly as its agent wrote it and is the only purely observational reading. `b_normalised` is
the main path and applies two rules to both logs alike:

1. **Failure attribution.** A row that names an earlier step as a correction *and* says that
   step failed reclassifies that command to `failed`. A correcting row that is itself a blocker
   whose `ref` is the correction is then not counted as a blocker as well — that would charge
   the route twice for one mistake. A correction that does not allege a failure changes
   nothing, which is why route B's one correction (of a factual claim) is left alone.
2. **The discovery window.** Everything is counted up to the first `evaluation_complete`. Both
   logs run on past it, unequally — 16 further rows for route A, 11 for route B — and what
   follows is verifying a script and reading a plot format, not finding out how to run a model.

Everything the rules touched is written to `b_normalised/results/what_the_rules_changed.md`,
so the reading can be audited rather than trusted. **The logs themselves are never edited**:
the rules are applied in memory. Both readings order the routes identically; normalisation
narrows the gap (dead ends 4:2 → 3:2, sources 6:4 → 5:4) and reverses nothing.

Rule 2 is the more contestable of the two, and it is kept contestable on purpose: someone could
reasonably argue that verifying a script is part of what a route costs. Both readings stay
runnable.

## (c) The working invocation, and what separates the two

| | Route A | Route B |
|---|---|---|
| Needs a container runtime | **yes** | no |
| Needs a container image build | **yes** | no |
| Hits a container registry | **yes** | no |
| Ran the model outside CHAP first | no | yes |
| Needed the platform's installed source | yes | yes |

**This is the structural difference, and it is attributable to the mechanism rather than to
these two models.** Serving a model over HTTP means an image has to be built, shipped and run,
and it means two independently versioned packages have to agree on a payload schema. An
`MLproject` model has neither surface: `uv_env` builds on the host and CHAP invokes it
directly.

**Route A's single largest cost belongs to its model, not to its route.** The image is
amd64-only because R-INLA ships x86_64 binaries, so on an arm64 host it runs under emulation
throughout — the one blocker that was hit and never resolved. A chapkit model without a
compiled statistical backend would not pay it.

## What is true of CHAP regardless of route

Three things turned up **independently in both logs**, written by agents that never
communicated, which is what makes them findings about the platform:

1. **The GeoJSON has no command-line flag.** CHAP matches the CSV's stem in the same directory
   (`chap_core.cli_endpoints._common.discover_geojson`). Both agents established it by reading
   installed source; neither model's documentation says so. Rename or move the CSV alone and
   the geometry is silently lost.
2. **`chap eval` writes a file, not an answer.** Metrics need a separate `chap export-metrics`,
   and the default plot appears only if `--plot` is passed. Neither README mentions either.
3. **One admin unit is silently dropped.** `LA-VI` has no target values, so both evaluations
   cover 17 of 18 units, announced in a warning inside a long log.

**Both routes needed the platform's installed source code to finish.** Neither route's answer
was fully available from public documentation. That is the same cost on both sides.

Route B additionally found a defect worth reporting upstream: `chap sanity-check-model` crashes
on a clean chap-core 2.3.1 because it defaults to a bundled dataset the wheel does not ship.

## (d) Results, reported per route and not compared

| Metric | Route A | Route B |
|---|---|---|
| MAE | 126.07 | 171.96 |
| RMSE | 242.77 | 358.93 |
| CRPS | 150.25 | 171.96 |
| Coverage 10–90 | 0.82 | 0.00 |

**No cross-route performance claim is made, and these two columns do not support one.** They
are two different models fitted by different methods on the same panel. Route B's zero
coverage is not a worse route; it is a model that emits one deterministic sample, so there is
no interval to cover. The plan's §2 fixes this and the table fences these rows into a block
labelled accordingly.

## What one run per route cannot resolve

- **Each route is one model, one agent, one machine.** Route A's costs — the amd64-only image,
  the build, the registry that refuses anonymous pulls — belong to *this* model as much as to
  the chapkit mechanism.
- **The build-time figures are not cold-build figures.** The host's layer cache was warm before
  the batch began and stayed warm on every re-run, so the expensive path was never exercised.
  Deleting the image was not enough; the layer cache survives it.
- **Elapsed minutes are cleaner than they would otherwise be** — the two agents were run one
  after the other rather than concurrently — but they still do not include an agent's own
  thinking time, and counts remain the primary measure.
- **A single failed command on each side is a thin basis for a ratio.** The honest form of the
  conclusion is directional: route A is consistently the more expensive route, and the one
  clear difference in kind is that it needs a container runtime and route B does not.

## State

- Batch 6 **done**. `/validate invariants`: all eight checks pass.
