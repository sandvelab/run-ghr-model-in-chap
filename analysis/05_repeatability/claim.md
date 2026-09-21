# Claim

Does each route run again, from clean, and how far do its scores move between runs when nothing about the invocation changes?

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

From `results/completion.tsv`, `results/score_spread.tsv` and `results/as_published_probe.log`.

1. **Both routes run again, from clean, and neither failed.** Each route's own deliverable
   script was executed end to end: route A completed in 1534 s including its container build,
   route B in 92 s. Both exited 0 and both wrote an evaluation. The re-run therefore tests the
   deliverable as well as the route.

2. **Route A's scores move by a few per cent; route B's do not move at all.** Over three
   route-A runs: MAE 126.85–133.28 (4.94 % of the mean), RMSE 7.00 %, MAPE 7.16 %, CRPS
   1.51 %, both coverage figures about 1.4 %. Over two route-B runs every metric is identical
   to the last digit. Route A fits with R-INLA, which is not bit-reproducible; route B fits an
   ordinary least-squares model with no stochastic component. **Neither is a defect**, and
   under the plan as amended on 2026-09-21 the spread is a property to report rather than a
   threshold to pass.

3. **The difference between the routes is not variability.** Route A's spread is a fact about
   its model's inference method, not about the chapkit mechanism. What separates the routes is
   established in `results/as_published_probe.log`, reproduced here first-hand rather than
   taken from the discovering agent's report: pointed straight at the running chapkit service,
   CHAP exits 1 with `could not be reached as a chapkit service` **while that service answers
   `/api/v1/info` with HTTP 200**; and with `--run-config.is-chapkit-model`, the escape hatch
   the error message recommends, it exits 1 again with three pydantic `extra_forbidden` errors
   on `git_revision`, `chapkit_version` and `servicekit_version`. The service declares chapkit
   2.0.0 / servicekit 2.0.2; chap-core 2.1.0's own environment holds chapkit 1.1.0 /
   servicekit 1.0.1.

4. So: **both routes run, and one of them runs only with an interposition.** Route A's three
   completions were all reached through the proxy in its own `run_route.sh`. Without it the
   route does not start, and that is a version incompatibility, not a tolerance.
