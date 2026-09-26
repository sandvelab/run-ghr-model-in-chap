# Provenance — iteration 2's route A against iteration 3's

result: results/comparison.tsv
          sha256:a6931551aeb56fd3663d85678275cf8590a48c996413ef8f4f381a2c7e68ae21
        results/effort_aslogged.tsv
          sha256:495422ec0343ca5a11bb6459bd3b0daa96b549f801fb74e94723fbb233dd0dc5
        results/effort_normalised.tsv
          sha256:1e1809ac59667dd1c57bf804b182b7ee869987b2126eacc31b3f6a59080ba248
        results/what_the_rules_changed.md
          sha256:15cf18d2de9ad6e16277fad0f11e9cb27e669f5046ad67565c39f0ac53531242
script: scripts/run_comparison.sh
          sha256:464e74a8ac1a2a0bd98e7d7ad9455aa961c4ecd1ae9c424fcaec1577e464e543
        scripts/lib/compare.py
          sha256:51b509268a6e4101f7a28b323bd00dc5cfca1db414fe168eccd6bcc5a80c0e5a
        ../../04_comparison/scripts/lib/summarise_discovery.py
          sha256:33589969b5cbebcc3341571c92de1f33c16d1a4d6693a620143ff9a01c9f67db
        ../../04_comparison/scripts/lib/discovery_log.py
          sha256:75581b1b38e243929021c881e429ead4d93c7f0606199afd89a1dfb59b3b99f0
        ../../04_comparison/01_effort/b_normalised/scripts/lib/normalise_logs.py
          sha256:441408bd508780967ee846b8ee296ac0c2b7533026e2474f2da373ef86fc82f1
invocation: bash scripts/run_comparison.sh (from the node)
inputs: analysis/02_routeA_chapkit/results/discovery_log.tsv, eval/metrics.csv, route_run/metrics.csv; analysis/08_humanCost/results/summary.tsv; ../01_discovery/results/{discovery_log.tsv,agent_usage.tsv,manual_run/metrics.csv,route_run/metrics.csv}; ../02_humanCost/results/{summary.tsv,machine_waits.tsv}
environment: environment/ (project main)
seeds: none — deterministic
commit: b524390
instructions-commit: d2459b1
node: analysis/09_routeA_iteration3/03_versusIteration2
produced: 2026-09-26
alternatives-considered: the as-logged reading is computed beside the normalised one and not used in the table, as in batch 6. Estimating an iteration-2 token figure — rejected; there is none on disk and the cell is NA. Confounds that one pair of runs cannot separate, and that every difference in the table carries: the model (0.1.0 to 0.1.2), the whole refreshed platform (25 packages, cyclopts 4 to 5), the discovering agent's model version (unrecorded in iteration 2), the Docker cache state (warm to cold), and one agent per iteration
agency: agent-autonomous
information: agent-retrieved
