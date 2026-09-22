# Provenance — results/anchor_manifest.tsv

result: results/anchor_manifest.tsv
        sha256:da520320d06c10957d6f702bd32da20813c8fd36d80fbe414eec18068d3a16fd
script: scripts/verify_anchors.py
        sha256:3ad924577b011d7ca2b473cf4165cd91f4e25f0c5556000bedd31a9ba069f749
invocation: ../../environment/env/bin/python scripts/verify_anchors.py --archive ../../Archive --out results
inputs: ../../Archive/data-lao/sha256sums.txt  sha256:1b942cc34c0cff472803a1fb039b3b2d32e4393d06265ae381af8ff5e65f069e
        ../../Archive/data-lao/chap_LAO_admin1_monthly.csv  sha256:19488aa1fc4d961ae1a6aeb75b874789576877664fce47713628f497a06fff56
        ../../Archive/data-lao/chap_LAO_admin1_monthly.geojson  sha256:cc823bf48dd3fc74f36bd8a652e03f51ca832e96ef42ebe5e098a94ca07e3389
        ../../Archive/data-lao/chap_LAO_admin1_monthly_schema.json  sha256:ff750db4202c32fc187b26bb3566b4f981b94467664502e76cbd09977dd06210
        ../../Archive/model-route-a/git-metadata.txt  sha256:2ffe8e38f7379317944f907ca96cbe1cdb4aa700897ba824ad240d28aab834e2
        ../../Archive/model-route-b/git-metadata.txt  sha256:e37d744c0b6a3d3a32bcb46e7669567cb277664aaa96c9591496dc8f7fe4a73b
        ../../Archive/platform-chap/install-metadata.txt  sha256:59a0e9f757f20faa7cd228491a341eed901766069e0222e8c305bfa0c7668b35
        ../../Archive/platform-chap/chap-tool-freeze.txt  sha256:dad886c18ff3c190f21e05913ae086106080838aad02ad02baa563abbf24e00e
environment: environment/ (project main)
seeds: project 20260921; component 20260921-verify-anchors (no stochastic step; recorded for completeness)
commit: 11899b7
instructions-commit: d2459b1
node: analysis/01_anchors
produced: 2026-09-22
alternatives-considered: re-cloning both model repositories and re-fetching the Lao data
  rather than verifying the archived copies. Rejected in the plan's §4b: the platform is
  meant to be the only anchor that differs from the previous iteration, and a re-fetch risks
  the upstream repositories having moved, which would confound a difference in route cost
  with a difference in the model or the data. The archived clones' recorded commits are
  reported as the pin, and the data files are re-hashed against the manifest written when
  they were fetched, so a silent change to either would surface as a MISMATCH. It would also
  have been reasonable to check the recorded commits still exist upstream; that is a network
  call this node deliberately does not make, so that it runs offline.
agency: agent-autonomous (the checks); human-set (that the platform is re-pinned to 2.3.1
  and the other two anchors are not re-fetched)
information: agent-retrieved (the installed platform's versions, read from the live
  installation into Archive/platform-chap/ before this script ran); human-pointed (both
  model repositories and the data directory were named by the human)
