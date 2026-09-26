# Claim

What would the re-discovered route A cost the software engineer and the statistician personas of batch 10, costed by batch 10's model and authored rates unchanged, over the new route's act sequence?

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_

*A model over measured structure, not a measurement: no human has been timed.*

**Engineer: 110 minutes expected (72–216). Statistician: 436 minutes expected (243–1026).**
Both are complete totals: they include the image pull, and no term is excluded
(`results/summary.tsv`).

**Nothing on the path is a diagnosis any more.** Diagnosis time is zero for both personas,
because the agent's path held no failure to diagnose. The time a human spends not following
instructions, which batch 10 called struggle, is now 12% for the engineer and 44% for the
statistician. All of it is learning prerequisites the route assumes.

**The statistician is still charged for five prerequisites they lack**
(`results/prereq_exposure.tsv`), about 180 minutes of learning between them:
- Docker (90)
- CPU architecture (35)
- compose files (20)
- the model as a running service (20)
- image registries (15)

Route A still needs a container runtime and an amd64 image before anything else.
