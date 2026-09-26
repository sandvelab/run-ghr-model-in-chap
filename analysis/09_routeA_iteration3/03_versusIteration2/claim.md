# Claim

What differs between iteration 2's and iteration 3's route A, in whether it succeeded, in agent effort, time and tokens, and in estimated human time?

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_

*(Every figure below is from `results/comparison.tsv`.)*

**Success.** Both iterations reached an evaluation and ran from clean. Iteration 3 did so
with 0 failed commands, 0 blockers and 0 dead ends, against 1, 2 and 3 in iteration 2.

**Agent time.** Time to evaluation rose from 13.0 to 22.8 minutes, and all of the rise is
machine waiting:
- The pull took up to 14.2 minutes of iteration 3's window (849 s, `../02_humanCost/results/machine_waits.tsv`),
  because Docker started fully cold.
- Iteration 2's build hit a warm layer cache.

**Agent effort.** The agent read more (12 resources, against 5) and ran fewer commands (9,
against 11).

**Tokens.** 139,417 tokens and 59 tool calls for the whole run, including the agent's own
clean-shell verification. There is no iteration-2 figure to set against it.

**Human estimate.** The engineer's figure falls from 119 to 110 minutes (0.92×). The
statistician's falls from 649 to 436 (0.67×). Iteration 2's figures exclude an unmeasured cold
build; iteration 3 needs none. The fall is diagnosis removed:
- 170 → 0 minutes for the statistician
- 25 → 0 for the engineer

For the engineer, most of the saving is offset by the extra documentation now read.

**What one pair of runs cannot separate.** The model changed (0.1.0 → 0.1.2), the whole
platform was refreshed, the agent's model version may differ, and the Docker cache went from
warm to cold. It is one agent per iteration.

**One thing is certain rather than confounded.** The GeoJSON convention batch 10 priced as
undiscoverable was documented at the same chap-core tag all along.
