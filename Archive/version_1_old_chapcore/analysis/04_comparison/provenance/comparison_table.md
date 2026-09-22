result: results/comparison_table.tsv
script: scripts/build_comparison.py
        sha256:db337edb7d650d3026eb9debf90c5db6ecfaec671a1c4489cc46b33019425ff1
invocation: "$PYTHON" scripts/build_comparison.py
inputs: 01_effort/b_normalised/results/effort_by_route.tsv  sha256:f6c5f9807a2a5ab1044bc9f1ec541cb4f1b6e33336ab805af3ec8aec110b24d7
environment: environment/ (project main; stdlib-only Python 3.13.0)
seeds: project 20260921; component none -- the computation is deterministic
commit: 87b5afa
instructions-commit: d2459b1
node: analysis/04_comparison
produced: 2026-09-21
alternatives-considered: the table could have been built from both readings at once, showing
  that the conclusion survives the normalisation; rejected because `analysis/run.sh` follows
  the main path at every fork, so a table naming the non-main alternative's output would name
  a file a full reproduction never regenerates. Whether the conclusion moves between the two
  readings is the stability node's question and is answered there. A direction column was
  included and a "winner" column deliberately was not: which route is easier is a reading of
  these numbers together with what the logs say happened, and it belongs where it can be
  argued with rather than in a cell.
agency: agent-autonomous
information: agent-retrieved
