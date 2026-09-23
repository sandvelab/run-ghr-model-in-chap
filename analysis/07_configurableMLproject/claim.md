# Claim

Does the MLproject route deliver an operator's configuration to the model, where the chapkit route does not? A third published template declaring a tunable hyperparameter is run through CHAP at several values, and what the model reports receiving is compared against what was asked for.

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(Each belongs in the claim collection under `Human-AI-collaboration/claims/` with a pointer
to the result grounding it.)_

**Yes. On the `MLproject` route an operator's configuration reaches the model, and nothing has
to be interposed for it to.** Three values of `alpha` were asked for and all three arrived
(`results/config_delivery.tsv`). The evidence is direct rather than inferred: CHAP writes
`model_configuration_for_run.yaml` into the model's own run directory, and that file carries the
value that was asked for — `alpha: {values: 1e5}` when `1e5` was asked for, and so on for each.

**The setting changes the predictions.** Three completed runs, three distinct metric vectors;
MAE 171.9631, 171.9640, 174.5322 for `alpha` of 1e-5, 1e2 and 1e5. The two small values barely
separate, which is what a ridge penalty far below the scale of the data should do, and the large
one clearly does.

**This is exactly what the chapkit route could not do.** There the operator's values are
accepted, stored in an inert block and discarded, and the model fits its defaults. Same
platform, same command, same `--model-configuration-yaml` flag; the difference is the transport.
On `MLproject` the configuration is a **file CHAP writes and the model reads** — one writer, one
reader, nothing negotiated. On chapkit it is a **payload POSTed against a schema the service
advertises and does not honour**.

**The `MLproject` route is not free of the same class of disagreement — but it fails loudly.**
`chap model schema --example` emits `user_option_values: {alpha: 1e-5}`, a bare scalar, while
this model's own `config.yaml` and its `train.py` both read `alpha.values`. Run with CHAP's own
generated example, the model stops with
`AttributeError: 'str' object has no attribute 'get'`, and CHAP reports the failing command and
its output. **Nothing is written and nothing is scored.**

That contrast is the finding worth keeping. Both mechanisms can disagree with a model about the
shape of a configuration. On `MLproject` the disagreement halts the run and names itself; on
chapkit it produces a complete evaluation, a valid NetCDF and real metrics from a configuration
that was never applied. The second is far more dangerous than the first.

**A caveat on scope.** This is one model, chosen because it declares a tunable option and reads
it in a way that can be observed. It shows the `MLproject` mechanism delivering, not that every
`MLproject` model is configurable — a template declaring no `user_options`, as route B's does,
has nothing to deliver. Nor is this model compared with route A or route B on effort or on
predictions; it is a third case, not a third route.
