result: results/effort_by_route.tsv
script: ../../scripts/summarise_discovery.py
        sha256:b1b861b032a557dbb3f719655737fed3bf97d26567c44810d44904b41f299bca
        ../../scripts/discovery_log.py
        sha256:af552cd16e53b99e1957ab81ef4120cd656db8d7f16d682da8c9042db626af7a
invocation: "$PYTHON" ../../scripts/summarise_discovery.py \
            --route A=../../../02_routeA_chapkit/results/discovery_log.tsv \
            --route B=../../../03_routeB_mlproject/results/discovery_log.tsv \
            --out results/effort_by_route.tsv
inputs: ../../../02_routeA_chapkit/results/discovery_log.tsv  sha256:a26966f22189a4c4b2ca9512939c077fc8a232dc1dede54fef3dcae96e9771fd
        ../../../03_routeB_mlproject/results/discovery_log.tsv  sha256:1a7c67c99c43c0908d5e4dbb7e7d58bdaf4b0cc94d197d0282a0565b0543eb10
environment: environment/ (project main; stdlib-only Python 3.13.0)
seeds: project 20260921; component none -- the computation is deterministic
commit: 87b5afa
instructions-commit: d2459b1
node: analysis/04_comparison/01_effort/a_asLogged
produced: 2026-09-21
reading: as-logged -- every `resource` row counts, exactly as its agent coded it
alternatives-considered: the normalisation taken by the sibling `b_normalised`, which is the main path. This
  reading is kept because it is the only one that is purely observational: it adds no
  judgment of the agents' coding, and so it is the reading against which the normalisation's
  effect can be seen. Its weakness is that it compares two logs whose agents coded the same
  acts differently -- route A logged `chap eval --help` as a resource and route B as a
  command, and route A logged the brief-supplied data files and its own notes as resources --
  so a difference in the resource count is partly a difference in bookkeeping.
agency: agent-autonomous
information: agent-retrieved (the coding differences were found by reading both logs after
  the routes had run, not anticipated when the format was fixed)
