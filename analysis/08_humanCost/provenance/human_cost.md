# Provenance — the human-cost estimate

result: results/summary.tsv
        sha256:a7cdcd65eae630f0312237b8d7555b3cde952f182c2bdcf4dca6446820c0388f
        results/doc_sizes.tsv
        sha256:b85e9c10ab146ae4d01779dba2b4d79830ba01d9256d6e59c23dfedc756c1d5e
        results/machine_waits.tsv
        sha256:8ceceff10fccf42d429a2f57e1a5f3f1c4e4feaaa9fb6cee9bc268d9d7318ac5
        results/prereq_exposure.tsv
        sha256:4442a9a22f200dc947c42c81b03db7264371785173191fc8de612999f585a60d
        results/walkthrough_engineer_route-a.tsv
        sha256:b5883e3eb493f564afdb43baacc1eacf8ee1d593874d4f45d40b4b1f292521e8
        results/walkthrough_engineer_route-b.tsv
        sha256:482d9872d049b84fb5fc61587ce1986c40e10bf6895d178ff6ed1ccf02ed3d49
        results/walkthrough_statistician_route-a.tsv
        sha256:e78fae3739f5c2a726a7dd046c6de96537a5db9713770925c3421f159d4f98e8
        results/walkthrough_statistician_route-b.tsv
        sha256:161105dcf5fa76f50ce803ac78cdb2632073d7ea34c5b546560b7f1360e20fc7
        results/help_text/chap_help.txt
        sha256:9c0a277d0309aa3f1aafe73a8f2c045f087d772244612a412b52a00780879716
        results/help_text/chap_eval_help.txt
        sha256:468a807b7030bb60c4e3ca69a0a75e68b1025d42bd95a37c97793b8d72edda56
        results/help_text/chap_export_metrics_help.txt
        sha256:a30de75667762cb8172017a74eceea3769456a3d774d1b7942ebdf4899ab3ea1
        results/help_text/chap_plot_backtest_help.txt
        sha256:849ff402de84be367cbe746c9f6c2da7ba6617d5eddf649a020353d91b7b2ef8
script: scripts/run_humancost.sh
        sha256:b4c8656dcac4f67a83c529bf7264710b9aa8af7244a17c1d3c860b705d4c7cd9
        scripts/lib/measure_inputs.py
        sha256:16805028e3d4ce209edbc2801b30e340651c90f894bd0bd3c81bc65bf6e3aefb
        scripts/lib/human_cost.py
        sha256:ea5e6084fae5d85e444e2456a344e2690d88c39b13cae42ad9a8b546d740cb09
invocation: bash scripts/run_humancost.sh
inputs (measured, from files this repository already held):
        ../02_routeA_chapkit/results/discovery_log.tsv  sha256:c04c44c96cce3d2c3b1c95b00367793285e25ec85e6fbb466bbde9b853a3c5df
        ../03_routeB_mlproject/results/discovery_log.tsv  sha256:5e1a21e95001cd77e2c37abfafeba6e1eabc5906a6f18d4d3df990bef4c35c77
        ../../Archive/model-route-a/repo/README.md  sha256:1a4b6e7caaba0be5c0aefd0c5bfcc3f687e74124f9527b3afbdede1291562506
        ../../Archive/model-route-b/repo/README.md  sha256:8555a990e3b7b0c9edc469afe2a86d8a7b965ed5729b436c9c74aab7d66bda26
        ../../Archive/data-lao/chap_LAO_admin1_monthly_schema.json  sha256:ff750db4202c32fc187b26bb3566b4f981b94467664502e76cbd09977dd06210
        the installed chap-core 2.3.1 cli_endpoints/_common.py and evaluate.py
        chap --help, chap eval --help, chap export-metrics --help, chap plot-backtest --help
        ../05_repeatability/results/rerun_routeB/  (file mtimes, for route B's evaluation span)
inputs (authored, this project's assumptions about human pace and human knowledge):
        scripts/inputs/steps.tsv  sha256:b4e814c605e49374a1a80b5a575e14e598ce4fae8cbdcb032cb90b5fc8af43c1
        scripts/inputs/personas.tsv  sha256:2a7f6e1e4150db723ad473a0804e04046abe4017d685031187014a8efce16a98
        scripts/inputs/prerequisites.tsv  sha256:bedd69b93be0b82aa34e808d494bf01200db59c87037d78d2ecc03b8dfe01ed9
        scripts/inputs/act_costs.tsv  sha256:496b72cc2290f5102f4f7ac87f6988fb7dc0303b5d2740ab7e5dbd9b3e7e290d
        scripts/inputs/reading_rates.tsv  sha256:f9bf2f23e574611ebacd2766d5db21dba12d58ec084a624a98b3cb45131abe7e
        scripts/inputs/modifiers.tsv  sha256:3103b5bad9ac682a4631d4f695f39f9ac2c813365473ecf9c096eb56c28dcbc4
        scripts/inputs/divergences.tsv  sha256:6d653cb8575a3cab47781237001fbe1434046087e9c5e527dc38825398732e54
        scripts/inputs/documents.tsv  sha256:ef0f45caf7470533b59bc6ac2957c5f9142e60439c4e07d9201da5a4dc83fe21
environment: environment/ (project main)
seeds: project 20260921; no stochastic step — the model is deterministic
commit: 4d11398 (tree at the start of batch 10)
produced: 2026-09-23
node: analysis/08_humanCost

what this result is, and is not:
  It is a **model over measured structure**, not a measurement of anyone. No human has been
  timed on either route. The act sequence, the document lengths and the machine waits are
  measured; the pace, the knowledge sets and the divergence rules are authored by this
  session. The two are in separate files so that the authored half can be replaced without
  touching the measured half, and so that a reader who disagrees with the pace can re-run
  rather than argue.

alternatives-considered:
  **A fresh agent run down each route, instrumented to log what it already knew.** Rejected as
  the basis for the timings and kept as a possible later check on the prerequisite inventory
  only. A second agent run yields agent minutes, which is the one quantity that does not
  transfer to a human; and a more capable model carries more silent prior knowledge, so
  capability is a confound in that instrument rather than a quality dial.
  **A single number per route.** Rejected. The spread between the two personas is larger than
  the spread between the two routes, so one number would have hidden the result.
  **Point estimates.** Rejected for a three-point low/expected/high, because the cost of a
  blocker to a person who lacks the prerequisite has a long upper tail and no anchor here.
  **Filling in route A's cold image build.** Rejected. Every build this repository logged ran
  against a warm layer cache, so the tree grounds nothing; it is carried as an excluded term
  with a flag in the summary rather than estimated.
  **Charging Docker knowledge on route B**, because route B's agent ran `docker info`.
  Rejected once the model made the consequence visible: it added 90 minutes to the
  statistician's route B and inverted this study's own finding that route B needs no container
  runtime. The rule now written down — a prerequisite is charged only where the route cannot
  proceed without it — is in `scripts/inputs/README.md`.
  **Letting the personas' multipliers compound across a step's prerequisites.** Rejected for
  the worst single gate: a step is not made four times harder by four familiar prerequisites
  and one unfamiliar one.

agency: agent-autonomous (the model, its parameters and the divergence rules)
        human-set (that the estimate should be made at all; the two personas; the
        defaults-only scope)
information: agent-retrieved

## Appended 2026-09-26 — `human_cost.py` gains an optional `wait_key` column

script: scripts/lib/human_cost.py
        sha256:491ef488e114cc6b220b0391bcb588d3128e89d6b8505ee99abe2d67f0def746
change: a step may name which machine wait it draws in a `wait_key` column; absent or `-`,
  the wait is keyed by the route, exactly as before. Added so that iteration 3's route A
  (`analysis/09_routeA_iteration3/02_humanCost`), which has an image pull and an evaluation,
  can be costed by this one implementation rather than a copy.
verification: re-running this script on this node's unchanged inputs and committed
  `doc_sizes.tsv`/`machine_waits.tsv` reproduced every file in `results/` byte for byte.
  The results above were **not** regenerated: this node's `run.sh` also re-captures
  `chap --help` live, and on the platform refreshed on 2026-09-26 (`cyclopts` 5.0.0)
  `chap eval --help` is 654 words rather than 645, which moves every figure slightly. The
  committed results stay as iteration 2's record; a full `analysis/run.sh` today would
  overwrite them, and that is a known reproduction caveat of this node.
commit: b524390
produced: 2026-09-26
agency: agent-autonomous
