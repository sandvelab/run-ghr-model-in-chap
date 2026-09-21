result: results/effort_by_route.tsv
script: ../../scripts/summarise_discovery.py
        sha256:b1b861b032a557dbb3f719655737fed3bf97d26567c44810d44904b41f299bca
        ../../scripts/discovery_log.py
        sha256:af552cd16e53b99e1957ab81ef4120cd656db8d7f16d682da8c9042db626af7a
invocation: "$PYTHON" ../../scripts/summarise_discovery.py --normalise \
            --not-a-source Archive/data-lao --not-a-source results/ --not-a-source runs/ \
            --route A=../../../02_routeA_chapkit/results/discovery_log.tsv \
            --route B=../../../03_routeB_mlproject/results/discovery_log.tsv \
            --out results/effort_by_route.tsv
inputs: ../../../02_routeA_chapkit/results/discovery_log.tsv  sha256:a26966f22189a4c4b2ca9512939c077fc8a232dc1dede54fef3dcae96e9771fd
        ../../../03_routeB_mlproject/results/discovery_log.tsv  sha256:1a7c67c99c43c0908d5e4dbb7e7d58bdaf4b0cc94d197d0282a0565b0543eb10
environment: environment/ (project main; stdlib-only Python 3.13.0)
seeds: project 20260921; component none -- the computation is deterministic
commit: 87b5afa
instructions-commit: d2459b1
node: analysis/04_comparison/01_effort/b_normalised
produced: 2026-09-21
reading: normalised -- R1 counts a CLI help invocation as an information source as well as a command; R2 excludes the brief's given inputs and artefacts the run itself produced
alternatives-considered: taking each log at face value, which is the sibling `a_asLogged`. Two other
  normalisations were possible and were rejected. A hand-curated list of specific rows to
  adjust would have been simpler and is what the differences first suggested; it was rejected
  because the result would then depend on which rows a reader happened to notice, and no rule
  would constrain the next log. Recoding route B's help invocations from `command` to
  `resource` was rejected because they genuinely were commands, and moving them would have
  made the command counts wrong to fix the resource counts. The rule chosen adds rather than
  moves, and is applied to both logs alike. Its cost is that `--not-a-source` is a declared
  list of substrings, so it is only as good as what is declared; the list is written out in
  this node's run.sh rather than buried in the code, so it can be argued with.
agency: agent-autonomous
information: agent-retrieved (the coding differences were found by reading both logs after
  the routes had run, not anticipated when the format was fixed)
