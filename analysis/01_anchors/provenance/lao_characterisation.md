# Provenance — results/lao_characterisation.tsv

result: results/lao_characterisation.tsv
        sha256:1076b511b703e049ed2334af61f0a6c4137a348d17e00ef7e744151d18fffc60
script: scripts/verify_anchors.py
        sha256:3ad924577b011d7ca2b473cf4165cd91f4e25f0c5556000bedd31a9ba069f749
invocation: ../../environment/env/bin/python scripts/verify_anchors.py --archive ../../Archive --out results
inputs: ../../Archive/data-lao/sha256sums.txt  sha256:1b942cc34c0cff472803a1fb039b3b2d32e4393d06265ae381af8ff5e65f069e
        ../../Archive/data-lao/chap_LAO_admin1_monthly.csv  sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        ../../Archive/data-lao/chap_LAO_admin1_monthly.geojson  sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
        ../../Archive/data-lao/chap_LAO_admin1_monthly_schema.json  sha256:ff750db4202c32fc187b26bb3566b4f981b94467664502e76cbd09977dd06210
environment: environment/ (project main)
seeds: project 20260921; component 20260921-verify-anchors (no stochastic step)
commit: 11899b7
instructions-commit: d2459b1
node: analysis/01_anchors
produced: 2026-09-22
alternatives-considered: loading the CSV through CHAP's own dataset reader rather than with
  the standard library, which would have described the data as CHAP sees it rather than as it
  sits on disk. Rejected: learning how CHAP wants a dataset presented is part of what each
  route's discovering agent must find out, and the orchestrator doing it first is the
  contamination the plan's §3 forbids. The `covariates` row is therefore a reading of the CSV
  header, not a statement about what either model will consume. Every value here is read from
  the schema or counted from the CSV, and the row says which.
agency: agent-autonomous
information: agent-retrieved
