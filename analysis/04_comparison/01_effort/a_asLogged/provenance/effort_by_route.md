# Provenance — results/effort_by_route.tsv, as logged

result: results/effort_by_route.tsv
        sha256:172717268a4c381c88084afd8144d247206dd02d57a5bda3e8cbb7a7d7d083dd
script: scripts/run_aslogged.sh
        sha256:485e9e1cbe9b529f626c848782701853fd7adcff09416550150c939357df8e5d
        ../../scripts/lib/summarise_discovery.py
        sha256:33589969b5cbebcc3341571c92de1f33c16d1a4d6693a620143ff9a01c9f67db
        ../../scripts/lib/discovery_log.py
        sha256:75581b1b38e243929021c881e429ead4d93c7f0606199afd89a1dfb59b3b99f0
invocation: bash scripts/run_aslogged.sh
inputs: ../../../../analysis/02_routeA_chapkit/results/discovery_log.tsv  sha256:c04c44c96cce3d2c3b1c95b00367793285e25ec85e6fbb466bbde9b853a3c5df
        ../../../../analysis/03_routeB_mlproject/results/discovery_log.tsv  sha256:5e1a21e95001cd77e2c37abfafeba6e1eabc5906a6f18d4d3df990bef4c35c77
environment: environment/ (project main)
seeds: project 20260921; no stochastic step
commit: fa3d04d
instructions-commit: d2459b1
produced: 2026-09-22
node: analysis/04_comparison/01_effort/a_asLogged
alternatives-considered: this alternative *is* the rejection of the other one. It reinterprets
  nothing: every row counts as the kind and outcome its own agent gave it, which makes it the
  only purely observational reading of the two. Its known cost is that it reports route A as
  having zero failed commands, when two of route A's commands did fail and the agent recorded
  the failures in later rows instead of rewriting the originals. That is a true statement about
  the log and a false impression of the route, which is why it is not the main path.
  No counting code lives here. Face value is what the shared instrument already computes, and a
  second implementation beside it is exactly what the comparison node exists to prevent.
agency: agent-autonomous
information: agent-retrieved
