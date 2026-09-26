# Provenance — the human-cost estimate, iteration 3 route A

result: results/doc_sizes.tsv
          sha256:1719ca9aca65f432a4cde5b0bc15ebfced55cbf59edd3e4474618a768ca732e1
        results/help_text/chap_eval_help.txt
          sha256:5f351d8044cc7598de6c3f8d73c1cb4a4a3a60b329693dc76fef74849b7c09ef
        results/help_text/chap_export_metrics_help.txt
          sha256:a30de75667762cb8172017a74eceea3769456a3d774d1b7942ebdf4899ab3ea1
        results/help_text/chap_plot_backtest_help.txt
          sha256:849ff402de84be367cbe746c9f6c2da7ba6617d5eddf649a020353d91b7b2ef8
        results/machine_waits.tsv
          sha256:c36d5ab7c41c86e9bff7efd504ed29d3150bd36f84001fdf2d24009b3c64a119
        results/prereq_exposure.tsv
          sha256:1036687d7e96c6f4b7b199e9db35213801f1970390763bc35c1a0a7d1763615b
        results/summary.tsv
          sha256:79718050223080556201c5748505932723b890fa4135e43095e487ad709b6e01
        results/walkthrough_engineer_route-a-it3.tsv
          sha256:8fc8a7a2bd4a55a5f9c31958a9aac8f881b8e94d5e4d2f9a95e6327330994a2a
        results/walkthrough_statistician_route-a-it3.tsv
          sha256:65a1bbe8146ef3de944120ebafd880357ca670bdb217b664ae4e05040c892a66
script: scripts/run_humancost.sh
          sha256:ed50727ed3c211a503c6183fb5eea1808bdb673fd686d0498012cb77e0ec4856
        scripts/lib/measure_inputs_it3.py
          sha256:c8acc3f4241c91824f1c1c90fe697b454b2310f8eda8bbcca0db0bed6558c3f7
        ../../08_humanCost/scripts/lib/human_cost.py
          sha256:491ef488e114cc6b220b0391bcb588d3128e89d6b8505ee99abe2d67f0def746
        ../../08_humanCost/scripts/lib/measure_inputs.py
          sha256:16805028e3d4ce209edbc2801b30e340651c90f894bd0bd3c81bc65bf6e3aefb
        scripts/inputs/steps.tsv
          sha256:6661a248eeb79aa1ebbf23cae7f31cbcc5091eaaa9968760e473d382839a84d7
        scripts/inputs/divergences.tsv
          sha256:b4c93e296d50977d1c3e3733d8fa1b9308fcbffb31dc9d752f265ab82d108b60
        scripts/inputs/documents.tsv
          sha256:881c597f9c571a8095d862a543b03ec08736aee4acba71399db2cad5689380b4
        scripts/inputs/act_costs.tsv
          sha256:496b72cc2290f5102f4f7ac87f6988fb7dc0303b5d2740ab7e5dbd9b3e7e290d
        scripts/inputs/personas.tsv
          sha256:2a7f6e1e4150db723ad473a0804e04046abe4017d685031187014a8efce16a98
        scripts/inputs/prerequisites.tsv
          sha256:bedd69b93be0b82aa34e808d494bf01200db59c87037d78d2ecc03b8dfe01ed9
        scripts/inputs/modifiers.tsv
          sha256:3103b5bad9ac682a4631d4f695f39f9ac2c813365473ecf9c096eb56c28dcbc4
        scripts/inputs/reading_rates.tsv
          sha256:f9bf2f23e574611ebacd2766d5db21dba12d58ec084a624a98b3cb45131abe7e
invocation: bash scripts/run_humancost.sh (from the node; it refuses to run unless the five rate and knowledge files are byte-identical to analysis/08_humanCost/scripts/inputs/)
inputs: ../01_discovery/results/discovery_log.tsv; ../01_discovery/results/route_run/{input_sha256.txt,image_id.txt} (mtimes); Archive/model-route-a-it3/repo/ and Archive/chapcore-docs-v2.3.1/ (word counts); chap --help output captured live to results/help_text/
environment: environment/ (project main)
seeds: none — deterministic
commit: b524390
instructions-commit: d2459b1
node: analysis/09_routeA_iteration3/02_humanCost
produced: 2026-09-26
alternatives-considered: (1) Re-authoring the per-act rates for the new route — rejected: a difference must come from the route, not from re-tuning, so the rates are batch 10's byte for byte and the wrapper checks it. (2) Copying batch 10's scripts — rejected in favour of calling them, so both iterations are costed by one implementation; human_cost.py gained an optional wait_key column so a route can have two machine waits, and re-running it on batch 10's inputs gives byte-identical outputs (checked). (3) Using the discovery run's pull (849 s, an upper bound because the agent worked in parallel) rather than the clean-shell pull (333 s) — the clean one is used and the difference, 8.6 min, is carried as a sensitivity row in 03_versusIteration2. (4) Keeping batch 10's divergence D1 (the sibling-GeoJSON convention met as a failure) — dropped, because chap-core's docs/chap-cli/eval-reference.md at v2.3.1 documents it and the new agent learned it there; D3 (the registry 401) dropped because the image now pulls anonymously; D4 added so a persona who would not read a model's source is not charged for learning to, on a step nothing depends on. (5) No arm64 diagnose step: the iteration-3 agent logged no blocker for the architecture, only a note; the cpu-architecture learning cost is still charged at the README. A reproduction caveat found on the way: node 08 captures --help live, and on the refreshed platform (cyclopts 5) chap eval --help is 654 words rather than 645, so node 08 does not reproduce its own numbers today; its committed results were restored and are left as iteration 2's record
agency: agent-autonomous (the step mapping and divergences); human-set (the personas, from batch 10)
information: agent-retrieved
