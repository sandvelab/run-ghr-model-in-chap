result: results/anchor_discrepancies.tsv
script: scripts/verify_anchors.py
        sha256:1f0e95e17129d66d9e89f3caac204b8751e0363454bf114bfbf7bea9dbd374a2
invocation: ../../environment/env/bin/python scripts/verify_anchors.py
            (called by run.sh, which sets PYTHON to the pinned environment)
inputs: ../../Archive/data-lao/sha256sums.txt  sha256:1b942cc34c0cff472803a1fb039b3b2d32e4393d06265ae381af8ff5e65f069e
        ../../Archive/data-lao/chap_LAO_admin1_monthly.csv  sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        ../../Archive/data-lao/chap_LAO_admin1_monthly_schema.json  sha256:ff750db4202c32fc187b26bb3566b4f981b94467664502e76cbd09977dd06210
        ../../Archive/model-route-a/git-metadata.txt  sha256:2ffe8e38f7379317944f907ca96cbe1cdb4aa700897ba824ad240d28aab834e2
        ../../Archive/model-route-b/git-metadata.txt  sha256:e37d744c0b6a3d3a32bcb46e7669567cb277664aaa96c9591496dc8f7fe4a73b
        ../../Archive/platform-chap/install-metadata.txt  sha256:e9de559295ec1652322fe1500a1bd751b0df918a8e0d89b29f19a4dffb0f38b5
        ../../Archive/platform-chap/chap-tool-freeze.txt  sha256:5450e303781d77a8f8faa5a6fbf6fe12c4190311b1e561f9a21b34600f9e04a2
environment: environment/ (project main; stdlib-only Python 3.13.0, environment/lock.txt empty)
seeds: project 20260921; component none -- the script is deterministic and draws no randomness
commit: 8ac3c8f
instructions-commit: d2459b1
node: analysis/01_anchors
produced: 2026-09-21
alternatives-considered: each of the four discrepancies could have been resolved instead of
  recorded -- the schema's row_count corrected, the geojson renamed to what the schema names,
  the 233 target-missing rows dropped, the unlicensed repository excluded. All four were
  rejected under plan §3: the models are run as published on the data as published, and how
  a route copes with an inconsistent schema or a gappy target is part of what this project
  is measuring. Dropping the missing rows would additionally have changed the panel the two
  routes are compared on. The licence gap blocks release, not analysis, and is raised with
  the human rather than decided here.
agency: agent-autonomous (recording); the disposition of the licence gap is human-set pending
information: agent-retrieved
