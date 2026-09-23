# Claim

What would each route cost a human who follows it to a default CHAP evaluation, and what must that human already know? Two personas are carried through the same act sequence the discovering agents logged: a software engineer a few years past a CS degree, and a statistician with basic programming and no advanced software engineering.

## Children

kind: sub-analyses
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_

**Who you are matters more than which route you take.** Between the two routes, the expected
estimate moves by a factor of about 2.6 for the engineer (119.0 against 45.9 minutes) and 2.9
for the statistician (648.6 against 221.2). Between the two personas on the same route it
moves by 5.5 (route A) and 4.8 (route B). A study that reports one number per route reports
the smaller of the two effects. `results/summary.tsv`.

**Both routes are a morning or less for the engineer, and route A is a working week's evening
for the statistician.** Expected: route B 46 minutes and route A 119 minutes for the engineer;
route B 221 minutes and route A 649 minutes for the statistician. The low–high bands are wide
on purpose — route A for the statistician spans 313 to 1743 minutes — because the cost of a
blocker to someone lacking its prerequisite has a long upper tail and nothing in this
repository anchors it. `results/summary.tsv`.

**Route A's ordering over route B survives both personas, and its margin comes from one
thing: it needs a container runtime.** Installing one, and the seven prerequisites the
statistician lacks on route A against one on route B, account for most of the gap.
`results/prereq_exposure.tsv`.

**Sixty of the statistician's route-A minutes are a property of the host, not of the route.**
The arm64/amd64 diagnosis arises only on an arm64 machine and vanishes on an x86_64 one; it is
reported in its own column rather than folded into the total. `summary.tsv`,
`arm64_host_only_min_exp`.

**The cognitive load does not track the clock.** Measured as the share of human time spent
*not* following instructions — diagnosing blockers and acquiring missing prerequisites — the
engineer spends 38 % on route A and 16 % on route B, while the statistician spends 61 % and
64 %. Route B is four times quicker for the statistician but no less bewildering per minute:
its single sharp failure (`chap sanity-check-model` crashing on a clean install) lands on
someone with no way to read it as a packaging fault rather than their own mistake.
`results/summary.tsv`, `unguided_share`.

**The single most expensive undocumented fact on either route is the same fact.** That a
`.geojson` must sit beside the `.csv` with the same stem appears in no README, no `--help`
output and no error message. Both discovering agents found it by opening installed library
source. A persona who would not do that meets it as a failure with nothing to diagnose it
from, at an expected 50 minutes on either route — the largest single non-learning cost in the
statistician's route B. `scripts/inputs/divergences.tsv`, rules D1 and D2.

**Route A's image build from cold is not estimated.** Every build this repository logged ran
against a warm layer cache. It is carried as an excluded term, flagged per route in
`summary.tsv` (`cold_build_excluded`), and it is additive to every route-A figure here.

**None of these minutes were measured on a person.** What is measured is the act sequence, the
lengths of the documents read, and the machine's own waiting time. The pace, the personas'
knowledge and the divergence rules are this project's assumptions, in
`scripts/inputs/`, replaceable without touching a measured value.
