# Batch 12 — route A, iteration 2 against iteration 3

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 3, route A only

What differs between route A on `chapkit` 2.1.0 with the model at `60b16a2` (iteration 2,
2026-09-22) and route A on `chapkit` 2.1.2 with the model at `a9532c7` (iteration 3,
2026-09-26). Both routes were discovered by a fresh agent on the same brief. Every figure is
from `analysis/09_routeA_iteration3/03_versusIteration2/results/comparison.tsv`.

## Did it succeed?

**Yes, both times, and this time without a single thing going wrong.**

| | Iteration 2 | Iteration 3 |
|---|---|---|
| Reached a CHAP evaluation | yes | yes |
| Route script ran clean from nothing | yes | yes |
| Failed commands | 1 | **0** |
| Blockers hit / left open | 2 / 1 | **0 / 0** |
| Dead ends | 3 | **0** |
| Resources read | 5 | 12 |
| Commands to first evaluation | 11 | 9 |

Two iteration-2 obstacles have gone.

The published image **pulls anonymously** and is tagged by commit, so no build is needed.
In iteration 2 the pull returned 401 and the image had to be built locally.

The invocation was found in **chap-core's own documentation** rather than in installed
library source. The three pages that carry it — including the sibling-GeoJSON convention —
exist at the same tag, `v2.3.1`, that iteration 2 ran on. So the convention was documented
all along. Batch 10's report said it appears in "no README, no `--help` and no error
message", and priced it as undiscoverable; that missed chap-core's documentation. The new
agent's path to it was different, not the documentation.

## How much time?

| | Iteration 2 | Iteration 3 |
|---|---|---|
| Agent minutes to first evaluation, by its log | 13.0 | 22.8 |
| of which image pull (iteration 3) | — | up to 14.2 |
| of which the evaluation itself | 6.8 | 5.7 |
| Docker state at the start | layer cache warm | fully cold |
| Tokens | not recorded | 139,417 |
| Tool calls | not recorded | 59 |
| Agent wall-clock, whole run | not recorded | 37.6 min |

**The agent took longer, and the image pull alone can account for it.** The rise is 9.8
minutes; the pull took up to 14.2. Iteration 3 started from nothing: no image and an empty
build cache. Iteration 2's build found its layers already cached. The agent kept working
while the pull ran, so its own working time cannot be separated from the machine's in the log.

No earlier batch recorded tokens, so there is no token comparison to make. Iteration 3's
figure covers the whole run, including about 12 minutes of the agent waiting on its own
clean-shell verification.

## How much human time?

Batch 10's model, with every rate and persona definition unchanged, over each iteration's
act sequence. **Modelled, not measured.**

| | Iteration 2 | Iteration 3 | Ratio |
|---|---|---|---|
| **Engineer**, expected (low–high) | 119 min (70–272) + cold build | **110 min** (72–216) | 0.92 |
| **Statistician**, expected (low–high) | 649 min (313–1743) + cold build | **436 min** (243–1026) | 0.67 |
| Diagnosing, engineer / statistician | 25 / 170 min | **0 / 0** | |
| Prerequisites the statistician lacks | 7 | 5 | |
| Share of time not following instructions, engineer / statistician | 38 % / 61 % | 12 % / 44 % | |

In iteration 2, the cold image build was unmeasured and excluded. Iteration 3's totals are
complete: the image pull is in them, and nothing is left out.

**The statistician gains most.** Every minute of the 170 they spent diagnosing is gone. Two
things they had to learn are no longer asked of them:
- telling a registry 401 from their own mistake
- `curl`

They still have to learn Docker, CPU architecture, compose files, image registries and the
idea of a model as a running service — 180 minutes. Route A still needs a container runtime
before anything else.

**The engineer gains little.** They lose 25 minutes of diagnosing and spend most of it again
reading the documentation the new path runs through.

## What one pair of runs cannot say

Every difference above carries five confounds together. No single change can be credited
with it:
1. The model changed, 0.1.0 → 0.1.2.
2. The whole `chap` environment was refreshed: 25 packages, `cyclopts` 4 → 5.
3. The agent's model version may differ: iteration 2's is recorded only as "Claude Opus".
4. The Docker cache went from warm to cold.
5. There is one agent per iteration.

One effect belongs to the release. The model's three new commits require chapkit 2.1, then
2.1.2, then rebuild the image on a fixed base. The image the agent pulled is that release's
image, and it is anonymously pullable. The other effect —
finding the documentation — belongs to the agent, not to the upgrade.

**Configuration was not tested.** The model's history includes a fix titled "require chapkit
2.1 so chap-core model configurations are applied", which bears directly on batch 8b's
finding that route A silently ignored every configured value. Whether it holds is a separate
question, and this batch did not ask it.
