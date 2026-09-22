# Provenance — results/anchor_discrepancies.tsv

result: results/anchor_discrepancies.tsv
        sha256:5b2e62ff6694a3b3ca20ec3d5babf291f9169129d85ebf8f2b4fa26c457f5570
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
alternatives-considered: repairing the three discrepancies before either route sees the data
  -- correcting the schema's row count, renaming the boundary file to the name the schema
  gives, and dropping or imputing the unit with no target values. All rejected, and this is
  the substantive judgment call of this node: how each route copes with a schema that does
  not match its own data, with a boundary file named under a different name, and with a gappy
  target is part of what the project is measuring. Repairing them would remove the thing being
  observed and would change the panel the two routes are compared on. The discrepancies are
  recorded here so that a route's handling of them can be attributed rather than discovered
  twice.
agency: agent-autonomous
information: agent-retrieved
