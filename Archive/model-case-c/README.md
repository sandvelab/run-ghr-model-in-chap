# model-case-c

(IS_SHADOW)

A third model, added at the human's request to settle a question the first two could not:
**does the `MLproject` route actually deliver a configuration to a model?**

`zlilu/minimal_template_example` @ `9cbc84a`, a Ridge regression whose `MLproject` declares a
tunable `alpha` under `user_options` and an `hpo_search_space` beside it, and whose `train` and
`predict` entry points both take `{model_config}` as a command parameter.

It is not a fourth route and it is not compared with route A or route B on effort or on
predictions. It exists because route A's model exposes eighteen options that cannot be set
through CHAP, and route B's model exposes none at all, so neither could show what a working
configuration looks like on the `MLproject` mechanism.

**No licence is declared in the repository.** Redistribution of this archived copy is not
established, exactly as for the route B model and the data.

## In it

- `repo/` — the clone as fetched, with `.git` removed so this repository versions it.
- `git-metadata.txt` — the remote, the pinned commit, and when it was fetched.
