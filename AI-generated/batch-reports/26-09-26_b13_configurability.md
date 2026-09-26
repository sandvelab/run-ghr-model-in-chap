# Batch 13 — route A configuration after the chapkit upgrade

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 3, route A only

Batch 8b found that GHRmodel could not be configured through CHAP. Every configured value was
accepted, stored, silently ignored, and the model fitted with its defaults. The only way to get
a configured run was to put a proxy between them. This batch asks whether that is still true on
`chapkit` 2.1.2 with the model at `a9532c7` (the published image). It runs batch 8b's own five
variants with **nothing interposed**, and judges them by batch 8b's own collector.

Every figure is from `analysis/09_routeA_iteration3/04_configurability/results/`.

## The answer: the status has changed

**The model is now configurable through CHAP as published.**

| | Batch 8b — chapkit 2.1.0, model `60b16a2` | Batch 13 — chapkit 2.1.2, model `a9532c7` |
|---|---|---|
| What an operator writes | values nested under `user_option_values` | the same |
| What CHAP sends | the nested shape | the same |
| What the service does with it | HTTP 201; stores its own defaults; parks the values in an inert nested block | stores the values as sent, flat, with **no nested remainder** (0 of 5) |
| What the model fits | its defaults, whatever was asked | **exactly what was asked**, 5 of 5 |
| Does the operator find out? | no — a complete, valid, wrongly configured evaluation | nothing to find out |
| The service's own schema | declares a nested `user_option_values` block | lists its 20 options directly; no nested block |
| A configured run needs | an interposed proxy | nothing |

The fix is on the model and chapkit side of the boundary. CHAP behaves as before:
- It accepts only the nested shape.
- It refuses a flat YAML loudly, before any request: exit 1, pydantic `extra_forbidden`, and
  0 config requests reaching the service (`results/configurability_facts.tsv`).

The upgrade has brought the service into line with what CHAP sends. This matches the
model's own commit: "fix: require chapkit 2.1 so chap-core model configurations are applied".

## The evidence, per variant

Each variant changes one option from the published defaults, and the control sets the
defaults explicitly. Each ran in a fresh container, so each service log holds one run's
fitted formula.

| Variant | Asked | Fitted (from the model's log) | Stored |
|---|---|---|---|
| `v0_published_defaults` | bym2 · rw1 · iid · nbinomial | bym2 · rw1 · iid | nbinomial |
| `v1_no_spatial` | **none** · rw1 · iid | **no spatial term** · rw1 · iid | nbinomial |
| `v2_seasonal_rw2` | bym2 · **rw2** · iid | bym2 · **rw2** · iid | nbinomial |
| `v3_interannual_rw1` | bym2 · rw1 · **rw1** | bym2 · rw1 · **rw1** | nbinomial |
| `v4_poisson` | bym2 · rw1 · iid · **poisson** | bym2 · rw1 · iid | **poisson** |

The formula does not name the likelihood, so `v4` rests on the stored configuration. Its
behaviour corroborates it: coverage collapses exactly as batch 8b's poisson run did.

## And the settings do what they did through the proxy

Movement against each batch's own control (`results/configurability_then_and_now.tsv`).
The scores are shown only to establish that each setting took effect. **No configuration
is chosen or recommended**; the plan's §3 forbids selecting on Lao scores.

| Variant | MAE, direct now | MAE, batch 8b via proxy | Coverage 10–90, now / then |
|---|---|---|---|
| `v1_no_spatial` | +29.8 % | +31.7 % | 0.82 / 0.82 |
| `v2_seasonal_rw2` | −6.6 % | −1.9 % | 0.82 / 0.82 |
| `v3_interannual_rw1` | +4.5 % | +6.4 % | 0.83 / 0.83 |
| `v4_poisson` | −17.5 % | −16.6 % | **0.24 / 0.24** |

Four of the five move as they did before, well beyond run-to-run noise. The control's own
spread on this pair is about 2.4 % in MAE. `v2` moves further now than it did then.

Batch 8b's warnings about reading these scores therefore still stand:
- Poisson improves point accuracy while its intervals stop covering.
- Removing the spatial term raises MAE and RMSE but lowers CRPS and MAPE.

What those cautions are about has changed. They no longer describe what a proxy made
possible. They describe what an operator can now do with a single CHAP flag.

## What remains

- **CHAP still does not tell an operator what the model applied.** The run is correct now,
  but the evidence of that is in the service's stored configuration and its container log,
  not in anything CHAP writes. Were the two ends to drift apart again, the failure would be
  silent again.
- **CHAP's covariate warning is still wrong**: every variant's log says `rainfall` and
  `mean_temperature` are "not used by the model", and every fitted formula uses both.
- **The before-state was not re-run.** Batch 8b's no-proxy failure was established by direct
  test and is recorded in its report and provenance. The old image was deleted for batch 12's
  cold start, so this batch compares against that record rather than re-creating it.
- **One pair of batches.** The model, chapkit and the refreshed `chap` environment all changed
  together. What the evidence fixes is the outcome — configuration now arrives — not which
  change delivered it. The model's own commit history names the chapkit requirement.
