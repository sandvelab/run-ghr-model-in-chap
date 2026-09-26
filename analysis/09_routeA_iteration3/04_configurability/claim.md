# Claim

On chapkit 2.1.2 with the model at a9532c7, does a configuration given to chap eval --model-configuration-yaml reach the model, with nothing interposed? Batch 8b's five one-option variants are re-run directly against the published image, and each is judged by what the service stored and what the model fitted.

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_

**Yes: route A's model is now configurable through CHAP as published, with nothing
interposed.** All five of batch 8b's one-option variants went straight through
`chap eval --model-configuration-yaml`, and all five demonstrably reached the model
(`results/configurability_facts.tsv`, `results/variants_table.tsv`):

- **What the model fitted.** Each fitted formula carries exactly the terms asked for.
  `v1_no_spatial` has no spatial term, `v2` fits `rw2` seasonality, and `v3` fits `rw1`
  interannually (`results/variants_formulas.tsv`).
- **What the service stored.** Each stored configuration holds the values flat, with no
  nested remainder left behind. This covers `family: poisson` for `v4`, which the formula
  does not show.

**The shape an operator writes has not changed.** The values still go nested under
`user_option_values`. What changed is that the service now applies that shape instead of
parking it:
- Its `/api/v1/configs/$schema` lists the 20 options directly and no longer declares a
  `user_option_values` block.
- A flat YAML is still refused by CHAP itself, loudly and before any request: exit 1,
  pydantic `extra_forbidden`, and 0 config POSTs reach the service.

So the one shape CHAP will send is now the one the model applies. The silent failure is gone.

**The settings do what batch 8b's proxied runs showed they do** (`results/configurability_then_and_now.tsv`):

| Variant | Direct, MAE vs control | Batch 8b via proxy |
|---|---|---|
| `v1_no_spatial` | +29.8% | +31.7% |
| `v4_poisson` | −17.5%, with coverage 10–90 collapsing to 0.24 | −16.6%, 0.24 |
| `v3_interannual_rw1` | +4.5% | +6.4% |
| `v2_seasonal_rw2` | −6.6% | −1.9% |

`v2` is the one variant whose shift differs between the batches by more than the control's
own run-to-run spread (about 2.4%). No configuration is chosen, as in batch 8b (plan §3).
