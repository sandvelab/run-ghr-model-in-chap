# Claim

What do the effort statistics say when the two logs' differing codings of the same acts are reconciled by a rule applied identically to both?

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

From `results/effort_by_route.tsv`, under the two normalisation rules — a CLI help invocation
counts as an information source as well as a command (R1); the brief's given inputs and
artefacts the run itself produced are not information sources (R2):

| | Route A (chapkit) | Route B (MLproject/uv) |
|---|---|---|
| Information sources consulted / used / discarded | 9 / 8 / 1 | 5 / 4 / 1 |
| Commands run / failed | 17 / 2 | 8 / 0 |
| Blockers hit / unresolved | 3 / 1 | 0 / 0 |
| Dead ends | 5 | 0 |
| Minutes to `evaluation_complete` | 52.5 | 29.7 |

**The normalisation moves both routes and changes nothing that matters.** It takes route A
from 10 sources to 9 and route B from 4 to 5 — that is, it moves them *towards* each other,
which is what a normalisation correcting for A's more generous coding should do — and route A
still consulted close to twice as many sources. The two rules leave every non-resource
statistic untouched by construction, and the tests assert that they do.
