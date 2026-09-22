# Provenance — results/comparison_table.tsv

result: results/comparison_table.tsv
        sha256:39782c8eafdb57c490c66465e90d69019921ec0a1febeb9c9a7255e456d2d7ea
script: scripts/run_comparison.sh
        sha256:27abd5b451940bb0c353d6ab18f8fd25075976644522cf30e0cbdeab1c3e79fd
        scripts/lib/build_comparison.py
        sha256:8f735fd36545d5619272da4945315432ff166d62427480d53410a7d515b63d28
        scripts/lib/discovery_log.py
        sha256:75581b1b38e243929021c881e429ead4d93c7f0606199afd89a1dfb59b3b99f0
        scripts/lib/test_discovery_log.py
        sha256:82a8902b1ad496a56a78e4def4ec6c385d5fd0ab8af54639cdf4c8139b0b43b9
invocation: bash scripts/run_comparison.sh
inputs: 01_effort/b_normalised/results/effort_by_route.tsv  sha256:500531dcc506dde5c1ca0a57c1abcb874f370065e848e135fc0966fd41257ced
        ../02_routeA_chapkit/results/discovery_log.tsv  sha256:c04c44c96cce3d2c3b1c95b00367793285e25ec85e6fbb466bbde9b853a3c5df
        ../03_routeB_mlproject/results/discovery_log.tsv  sha256:5e1a21e95001cd77e2c37abfafeba6e1eabc5906a6f18d4d3df990bef4c35c77
        ../02_routeA_chapkit/results/eval/metrics.csv  sha256:0ca96e54c693d0f033c199bf5cfbbdaf25c9d747981d903fa9fd88facb229673
        ../03_routeB_mlproject/results/eval/metrics.csv  sha256:aa9e21db52d7db03aef89a052f597dd08daf1cece15c8c56ec0869caa2241fab
environment: environment/ (project main)
seeds: project 20260921; no stochastic step
commit: fa3d04d
instructions-commit: d2459b1
node: analysis/04_comparison
produced: 2026-09-22
alternatives-considered: reading both alternatives' effort files and showing them side by
  side. Rejected: `analysis/run.sh` follows the main path at every fork, so a table naming a
  non-main alternative's output would name a file that a full reproduction never regenerates.
  The other reading is one directory away and runnable, and the fork's own claim.md reports
  what it says.
  The prerequisite rows are derived from each route's own log rather than asserted, and one
  derivation was wrong and was corrected: matching `docker ` anywhere in a command line
  reported route B as needing a container runtime because it ran `docker info` to check the
  daemon was up. Checking is not depending, so the test is now for `docker run`, `docker
  build`, `docker compose` or `docker start`. This is the kind of defect that survives
  indefinitely if nobody reads the table against the logs.
  The metric rows are fenced into their own block and labelled as not compared. The plan's §2
  forbids a cross-route performance claim, and the surest way to make one by accident is to
  put two columns of metrics beside each other with no label saying what they are not for.
agency: agent-autonomous
information: agent-retrieved
