# Batch 8c — a third case: does the `MLproject` route deliver a configuration?

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 2

Outside the plan, at the human's request. Batch 8b established that route A's model cannot be
configured through CHAP. This batch asks whether the other mechanism can, using a third model
because neither of the project's own two can answer it.

---

## Why a third model was needed

| | Declares options | Can show a configuration arriving |
|---|---|---|
| Route A — `chapkit_ghr_model` | **18** | no — they are accepted and discarded |
| Route B — `minimalist_example_uv` | **0** | no — there is nothing to deliver |
| **Case C — `zlilu/minimal_template_example`** | **1** (`alpha`) | **yes** |

Without a model that both declares an option and can be seen to receive it, "the `MLproject`
mechanism delivers configuration" rested on reading chap-core's source. This batch replaces that
inference with a file.

**It is a case, not a third route.** It was not discovered by an isolated agent on the §4 brief,
so it has no admissible discovery log, and it is not compared with either route on effort or on
predictions. Archived at `Archive/model-case-c/`, commit `9cbc84a`. **No licence declared.**

## What it is

An `MLproject` template implementing Ridge regression. Its `MLproject` file declares:

```yaml
user_options:
  alpha:
    type: float
    default: 1e-5
hpo_search_space:
  alpha:
    values: [1e-5, 1e-4]
```

and both entry points take `{model_config}` as a command parameter. All of that is readable in
the repository without running anything.

## What happened

*(`analysis/07_configurableMLproject/results/config_delivery.tsv`)*

| Run | `alpha` asked | delivered to the model | completed | MAE |
|---|---|---|---|---|
| `alpha_1e-5` | 1e-5 | **1e-5** | yes | 171.9631 |
| `alpha_1e2` | 1e2 | **1e2** | yes | 171.9640 |
| `alpha_1e5` | 1e5 | **1e5** | yes | 174.5322 |
| `chap_example_shape` | 1e-5 | 1e-5 | **no** | — |

**All three configured runs delivered, and nothing was interposed.** The evidence is direct:
CHAP writes `model_configuration_for_run.yaml` into the model's own run directory, and that file
carries the value asked for. Three distinct metric vectors across three runs, so the setting
reached the fit rather than merely the disk. The two small values barely separate, which is what
a ridge penalty far below the scale of the data should do; the large one clearly does.

## The fourth run is the point

`chap model schema --example` emits `user_option_values: {alpha: 1e-5}` — a bare scalar — while
this model's own `config.yaml` and its `train.py` both read `alpha.values`. Run with CHAP's own
generated example, the model stops:

```
AttributeError: 'str' object has no attribute 'get'
Command 'uv run python train.py training_data.csv model model_configuration_for_run.yaml'
failed with return code 1
```

**Both mechanisms can disagree with a model about the shape of a configuration. They fail
completely differently.**

| | chapkit (route A) | `MLproject` (case C) |
|---|---|---|
| What happens | HTTP 201; defaults applied; model fits them | run halts |
| What you get | a valid NetCDF, real metrics, a real plot | nothing |
| What you are told | **nothing** | the failing command, its output, and the exception |
| How you would notice | by reading the fitted formula or the stored config | immediately |

The `MLproject` failure is the better one by a wide margin. A stopped run with a named cause
costs an operator minutes. A completed run from a configuration that was never applied costs
them whatever they go on to conclude from it.

## What this does and does not establish

- **Does**: the `MLproject` transport delivers an operator's configuration to a model that
  declares one, and the value reaches the fit.
- **Does not**: that every `MLproject` model is configurable. A template declaring no
  `user_options`, as route B's does, has nothing to deliver.
- **Does not**: anything about which `alpha` is better. Three widely separated values were used
  to make delivery unmistakable, not to search. §3 forbids selecting between configurations on
  Lao scores.

## State

- Batch 8c **done**. `/validate invariants`: all eight checks pass.
- One defect of the batch's own: the first attempt ran the model inside `results/`, and because
  CHAP copies an MLproject model into `runs/<timestamp>/` and builds a `uv` environment there,
  each run left ~800 MB of dependencies — including scipy's PNG test fixtures — under a results
  directory. The checker reported two dozen figures with no plotted values and no plotting
  script, correctly. The model now runs in a temporary directory outside the repository.
