# Claim

What do the effort statistics say when each log is taken exactly as its agent coded it?

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

From `results/effort_by_route.tsv`, taking each log exactly as its agent coded it:

| | Route A (chapkit) | Route B (MLproject/uv) |
|---|---|---|
| Resources consulted / used / discarded | 10 / 9 / 1 | 4 / 3 / 1 |
| Commands run / failed | 17 / 2 | 8 / 0 |
| Blockers hit / unresolved | 3 / 1 | 0 / 0 |
| Dead ends | 5 | 0 |
| Minutes to `evaluation_complete` | 52.5 | 29.7 |

This reading adds no judgment of the agents' bookkeeping, which is its point and also its
weakness: the two logs code some of the same acts differently, so part of the gap in the
resource count is a difference in how the two agents recorded, not in what they did. The
sibling `b_normalised` reconciles that by rule and is the main path.
