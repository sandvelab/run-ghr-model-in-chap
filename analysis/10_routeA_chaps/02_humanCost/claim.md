# Claim

What would the chaps route cost batch 10's software engineer and statistician personas, costed by batch 10's model over the new route's act sequence?

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_

**Estimated, not measured.** Batch 10's model, with every rate byte-identical, over the chaps
route's 32-step act sequence *(`results/summary.tsv`)*:

| persona | expected min (low–high) | human / machine | unguided share | prerequisites lacked |
|---|---|---|---|---|
| engineer | 130 (87–249) | 117 / 13 | 0.10 | 0 (2 partial) |
| statistician | 483 (273–1,120) | 470 / 13 | 0.42 | 6 (2 partial) |

**What drives it** *(`results/walkthrough_*_route-a-chaps.tsv`)*. Reading is the engineer's
largest cost: chaps' agent page (4,465 words) and the model README (2,833 words) are 58 of the
130 minutes, the README's share including 9 minutes learning about CPU architectures. For the statistician, Docker comes first: installing and learning it is 128
minutes before any document is opened. The prerequisites lacked are docker-basics,
cpu-architecture, rest-service-model, docker-compose, container-registry and http-curl
*(`results/prereq_exposure.tsv`)*.

**The pull wait is borrowed and the link matters.** chaps completed no pull on this batch's
link, so the main figure uses batch 12's measured pull on a working link (333 s;
`results/machine_waits.tsv`). On this batch's link, chaps' route failed. Costed up to that
point, it is 190 minutes for the engineer and 566 for the statistician, 93 of them waiting,
and it ends blocked: the agent's workaround, a resumable image fetcher, is not a persona step
(route `route-a-chaps-slowlink`).

**Sensitivities** (each changes one input; `results/sensitivity/`):
- **Docker priced lighter** (learning 15/30/60 rather than 45/90/240): statistician 423,
  engineer unchanged at 130.
- **`docs/run.md` read in place of the agent page**: engineer 111, statistician 446, which is
  batch 12's level.
