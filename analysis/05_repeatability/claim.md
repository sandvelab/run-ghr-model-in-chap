# Claim

Does each route run again, from clean, and how far do its numbers move when it does? The question is whether the route works repeatably, not whether it produces the same number twice: a route whose scores shift by a few per cent is a working route, and the shift is characterised rather than corrected for.

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(Each belongs in the claim collection under `Human-AI-collaboration/claims/` with a pointer
to the result grounding it.)_

**Both routes run again, from clean, and neither has failed once.** Across every run this
repository holds — each route's own `run_route.sh` re-run into this node, the runs in the
route nodes, and the versions recovered from git history — **route A completed 4 times out of
4 and route B 2 times out of 2**, each writing a full evaluation (`results/completion.tsv`,
`results/run_ledger.tsv`).

**Route A's numbers move, by between 0.45% and 3.4%** (`results/score_spread.tsv`): MAE
125.75–128.48 (2.2%), RMSE 237.19–245.42 (3.4%), CRPS 147.69–150.40 (1.8%), coverage 10–90
0.8095–0.8244 (1.8%). The model fits with R-INLA, which its own README states is not
bit-reproducible even single-threaded, and nothing in the route sets a seed — CHAP offers none
for a chapkit service.

**Route B's numbers do not move at all.** Two runs, identical to the last digit, on every
metric. It fits ordinary least squares and emits one deterministic sample, so there is nothing
to vary.

**This difference is a property of the two models' inference methods, not of the two
integration mechanisms**, and it is reported rather than corrected for. A route whose numbers
shift a few per cent is a working route. The practical consequence is narrow: route A's scores
should not be quoted to more than three significant figures.

**Re-running is what makes this an answer.** An earlier version of this node assembled the
same table from metrics files already in the tree and in git history, without running
anything. It was rejected: a route that had quietly stopped working would have looked identical
in a table of old files.
