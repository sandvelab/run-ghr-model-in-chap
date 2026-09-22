# Provenance — results/effort_by_route.tsv, normalised (main path)

result: results/effort_by_route.tsv
        sha256:500531dcc506dde5c1ca0a57c1abcb874f370065e848e135fc0966fd41257ced
        results/what_the_rules_changed.md
        sha256:4a5d3aabd2a773682662d52f084f1891bd1c6b7e6fa2f5abd11e48a763a98c4b
script: scripts/run_normalised.sh
        sha256:ead1175989d009c92d19c0ae35c589f6cca0b8c37891ffd6dc3d5b871fc0147e
        scripts/lib/normalise_logs.py
        sha256:441408bd508780967ee846b8ee296ac0c2b7533026e2474f2da373ef86fc82f1
        ../../scripts/lib/discovery_log.py
        sha256:75581b1b38e243929021c881e429ead4d93c7f0606199afd89a1dfb59b3b99f0
invocation: bash scripts/run_normalised.sh
inputs: ../../../../analysis/02_routeA_chapkit/results/discovery_log.tsv  sha256:c04c44c96cce3d2c3b1c95b00367793285e25ec85e6fbb466bbde9b853a3c5df
        ../../../../analysis/03_routeB_mlproject/results/discovery_log.tsv  sha256:5e1a21e95001cd77e2c37abfafeba6e1eabc5906a6f18d4d3df990bef4c35c77
environment: environment/ (project main)
seeds: project 20260921; no stochastic step
commit: fa3d04d
instructions-commit: d2459b1
produced: 2026-09-22
node: analysis/04_comparison/01_effort/b_normalised
alternatives-considered: the sibling `a_asLogged` takes both logs at face value and stays
  runnable; this alternative argues that two specific codings are artefacts of who wrote the
  log rather than facts about the route, and states the rules that remove them.
  A per-row hand correction was considered and rejected: it would depend on which rows a
  reader happened to notice and would constrain no future log. Two rules applied to both logs
  alike can be argued with, and everything they touched is written to
  `results/what_the_rules_changed.md` so the reading can be audited instead of trusted.
  Editing the logs themselves was never on the table (AGENTS.md §1): the rules are applied in
  memory and the raw logs stay as their agents wrote them.
  Rule 2 is the larger and the more contestable of the two. Cutting the count at the first
  `evaluation_complete` discards 16 route-A rows and 11 route-B rows, and someone could
  reasonably argue that verifying a script is part of what a route costs. The counter-argument
  is that the question is how hard the route was to *find out how to run*, and that the two
  logs continue past that point by different amounts for reasons that have nothing to do with
  the routes. Both readings are kept precisely because this is arguable.
  Neither rule changes the ordering: route A costs more than route B on every statistic that
  orders, under both readings.
agency: agent-autonomous
information: agent-retrieved
