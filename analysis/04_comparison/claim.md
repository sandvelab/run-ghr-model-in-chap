# Claim

Which of the two routes was easier to find out about and easier to carry out, and what can one run per route resolve?

## Children

kind: sub-analyses
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

From `results/comparison_table.tsv`, built from the main path of `01_effort`.

1. **Route B was easier on every statistic that orders**, by ratios clustering around two:
   information sources 9 vs 5, commands 17 vs 8, commands before completion 13 vs 6, minutes
   to `evaluation_complete` 52.5 vs 29.7. The starkest figure is not a ratio: **5 dead ends
   against 0**, and 3 blockers against 0.

2. **The difference is one of kind, not degree.** Route B's working invocation was in the
   model's own README, copy-pasteable and correct. Route A's was in a docstring inside the
   installed Python package — nothing on the web and nothing in the model's repository carries
   it — and the reason route A failed was only findable by reading the platform's source.
   Route B's agent was following instructions; route A's was diagnosing an integration.

3. **Route A did not complete as published.** chap-core 2.1.0 pins chapkit 1.1.0, whose
   `MLServiceInfo` forbids extra fields; the model is built on chapkit 2.0.0, which sends
   three more. The route completes only through an interposed proxy that strips them. Route B
   needed nothing of the kind, and needed no container at all.

4. **The conclusion is robust to the one judgment call made in measuring it.** Taking each log
   at face value instead of normalising moves route A from 9 sources to 10 and route B from 5
   to 4, and changes nothing else. It is *not* established to be robust to anything else: each
   route is one model and one run, and phase D is what tests that.

5. **Four findings are about CHAP rather than about either route**, because they recur in both
   logs, written by agents that knew nothing of each other: the unused-covariate warnings
   report declaration rather than delivery and are wrong on both routes; the GeoJSON has no
   command-line flag and is matched by basename; `chap eval` writes a file and no metrics, so
   `chap export-metrics` is a required second step neither model's README mentions; and one
   admin unit is silently dropped, so both evaluations cover 17 of 18 units.

6. **What this cannot settle.** Route A's largest costs — an amd64-only R-INLA image, a 4.98 GB
   build, a GHCR package that is not publicly pullable — belong to *this model*, not to the
   chapkit mechanism. What belongs to the mechanism is the version-compatibility surface: two
   independently versioned packages must agree on a payload schema, and an `MLproject` model
   has no such surface. The elapsed-minute figures are additionally contaminated by the two
   agents having run concurrently on one machine, which is why counts are the primary measure.
