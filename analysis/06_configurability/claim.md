# Claim

Can route A's model be configured through CHAP at all, and does changing its options change what it fits? The model declares eighteen options; this node establishes whether a value set by the operator reaches the model, what has to be interposed for it to, and what several published-alternative configurations produce on the Lao data.

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(Each belongs in the claim collection under `Human-AI-collaboration/claims/` with a pointer
to the result grounding it.)_

**Route A's model cannot be configured through CHAP, and the failure is silent.** The model
declares eighteen options and `chap eval` has `--model-configuration-yaml`, but the two ends
require incompatible shapes and neither reports it:

- chap-core's `ModelConfiguration` is `extra="forbid"` with exactly two fields, so values must
  be **nested** under `user_option_values`; a flat mapping is rejected before any request is made.
- The service stores a **flat** mapping. Handed the nested one it returns HTTP 201, fills every
  option from its own defaults, keeps the operator's values in an inert `user_option_values`
  block, and fits with the defaults.

So the one shape CHAP will send is the one the model discards. The run completes, writes a valid
NetCDF and real metrics, and is **indistinguishable from a configured run by its output alone**.

**The model advertises a schema it does not consume.** Its own `/api/v1/configs/$schema` declares
the nested shape, so chap-core sends exactly what it is told. The defect is reportable against
the model; that CHAP cannot tell an operator their configuration had no effect is a separate,
smaller weakness.

**A configured run exists only through something interposed.**
`scripts/lib/config_proxy.py` rewrites the body of `POST /api/v1/configs`, lifting
`user_option_values` into `data` and forwarding everything else untouched. Neither the model nor
the platform is modified. Establishing the need for it took reading chap-core's installed source,
reading the stored configuration back over HTTP, and comparing fitted formulas — none of it
discoverable from documentation.

**Through the proxy, configuration demonstrably reaches the model** — five variants, all five
confirmed (`results/variants_table.tsv`). The service stores each value flat with no nested
remainder, and for the three variants re-run to capture it, the fitted formula agrees:
`v1_no_spatial` drops the spatial term entirely (`spatial=ABSENT`) where the others fit
`bym2` (`results/variants_formulas.tsv`).

**Configuration changes the answer, by far more than run-to-run noise**
(`results/variants_table.tsv`, against the 2.2% MAE / 3.4% RMSE noise floor measured in
`analysis/05_repeatability/`):

| Variant | Changed | MAE | vs control | RMSE | Coverage 10–90 |
|---|---|---|---|---|---|
| `v0_published_defaults` | — | 126.42 | — | 238.43 | 0.821 |
| `v1_no_spatial` | `re_spatial: none` | 166.51 | +31.7% | 350.25 | 0.819 |
| `v2_seasonal_rw2` | `re_seasonal: rw2` | 124.03 | −1.9% | 234.04 | 0.821 |
| `v3_interannual_rw1` | `re_interannual: rw1` | 134.47 | +6.4% | 267.79 | 0.830 |
| `v4_poisson` | `family: poisson` | 105.47 | −16.6% | 202.76 | **0.238** |

**Three readings, and one non-reading.**

1. **`v2_seasonal_rw2` moved less than the noise floor** (−1.9% MAE, −1.8% RMSE against 2.2% and
   3.4%). On this evidence it did nothing measurable, and reading it as an improvement would be
   reading noise.
2. **`v1_no_spatial` moves the metrics in opposite directions**: MAE +31.7% and RMSE +46.9%, but
   CRPS −25.4% and MAPE −47%. Which metric is consulted changes the sign of the answer.
3. **`v4_poisson` improves point accuracy while its coverage collapses from 0.82 to 0.24.**
   Forcing mean-equals-variance onto overdispersed counts narrows the intervals until they stop
   covering. Selecting on MAE alone would have chosen the configuration whose uncertainty is
   worthless.
4. **No configuration is chosen and none is recommended.** The plan's §3 stops this project if a
   batch begins choosing between model configurations on the basis of Lao scores, because nothing
   is held out to catch selection. Reporting the spread is not selecting on it.
