# Claim

What would it cost an agent, and the two personas of batch 10, to take chapkit_ghr_model to a default CHAP evaluation on the Lao data through chaps, the Docker Compose deployment tool for CHAP, and how does that compare with route B, the MLproject route?

## Children

kind: sub-analyses
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_

**Route A through chaps works, and it is not quicker for a human than route A without it; route
B, the MLproject route, stays about half the cost.** Estimated human minutes, expected
(low–high): engineer 130 (87–249) against route B's 46; statistician 483 (273–1,120) against
route B's 221. Route A without chaps (batch 12) was 110 and 436 *(`03_versusRouteB/results/comparison.tsv`)*.

- **For an agent it is a short route**: install chaps, `chaps run <repository URL>`, then
  `chap eval` against the URL. 143,158 tokens to the first evaluation, against 139,417 without
  chaps *(`01_discovery/results/agent_usage.tsv`)*.
- **chaps stops before the evaluation.** Its documentation serves a model and backtests it on
  sample data the model generates; evaluating on one's own data still comes from chap-core's
  docs *(`01_discovery/claim.md`)*.
- **On a slow link chaps' download fails** and the route completes only with a workaround that
  no persona is shown. Costed to the failure, it is 190 and 566 minutes, ending blocked
  *(`02_humanCost/claim.md`)*.
- **What would close the gap** is on the human side, not the agent's: a chaps page that goes
  from `chaps run` to `chap eval` on a user's CSV, and a resumable image download. Docker
  remains the statistician's largest single cost, and chaps does not remove it.

