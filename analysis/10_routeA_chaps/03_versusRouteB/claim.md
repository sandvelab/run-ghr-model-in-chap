# Claim

How does the chaps route compare with route B (MLproject, batch 10) and with route A without chaps (batch 12), for each persona, in estimated human minutes, unguided share and prerequisites lacked?

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_

**Route B stays the cheaper route for both personas; chaps does not narrow the gap**
*(`results/comparison.tsv`, `results/ratios_to_route_b.tsv`)*. Expected minutes, low–high in
brackets; all are model estimates:

| | engineer | statistician |
|---|---|---|
| route B, MLproject (batch 10) | 46 (27–99) | 221 (101–594) |
| route B, GeoJSON convention from the docs (sensitivity) | 45 | 186 |
| route A without chaps (batch 12) | 110 (72–216) | 436 (243–1,026) |
| **route A through chaps (batch 14)** | **130 (87–249)** | **483 (273–1,120)** |
| route A through chaps, run.md in place of the agent page | 111 | 446 |
| route A through chaps, Docker priced lighter | 130 | 423 |
| route A through chaps on this batch's link, to the failure | 190, blocked | 566, blocked |

- **Against route B**, the chaps route is about 2.8× for the engineer (+84 min) and 2.2× for
  the statistician (+262 min).
- **Against route A without chaps**, it is 20 and 48 minutes dearer. chaps replaces two
  `docker` commands with one `chaps run`, but its documentation adds reading and stops before
  the evaluation, which still comes from chap-core's docs. Read docs/run.md in place of the
  agent page and the two are level. The model version differs between the two runs (0.1.2
  against 0.1.3; the code diff is a version string and a monitoring hook) — a named confound.
- **Unguided share**: the statistician's falls from 0.64 on route B to 0.42 on the chaps route.
  Route B's share is dominated by diagnosis; the chaps route's cost is mostly learning Docker.
- **Prerequisites lacked by the statistician**: 1 on route B (reading library source), 6 on
  the chaps route, all of them about containers and services.

**Removing D2 alone makes route B dearer for the statistician (246, not 221)**: without the
GeoJSON trap, the persona pays to read library source as the agent did. Only when the
documented convention replaces the source read does route B get cheaper (186). Route B was not
re-discovered on today's platform.
