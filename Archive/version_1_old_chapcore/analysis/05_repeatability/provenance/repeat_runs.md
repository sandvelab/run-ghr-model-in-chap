result: results/run_ledger.tsv, results/rerun_routeA.log, results/rerun_routeB.log
        results/history/A/.digests
        results/history/A/20260921T135429Z_prior_eval_metrics.csv
        results/history/A/20260921T135429Z_prior_eval_metrics_firstrun.csv
        results/history/A/20260921T142003Z_rerun.csv
        results/history/B/.digests
        results/history/B/20260921T142003Z_prior_eval_metrics.csv
        results/history/B/20260921T142136Z_rerun.csv
script: scripts/rerun_routes.sh
        sha256:93b46300967f0ca873ad4e044271f1132bd0be334e272ff785de4269a52b8517
invocation: bash scripts/rerun_routes.sh
            (archives each route's current eval_metrics*.csv into results/history/<route>/,
             then runs ../02_routeA_chapkit/scripts/run_route.sh and
             ../03_routeB_mlproject/scripts/run_route.sh end to end, archiving the fresh
             metrics and appending a ledger row per route)
inputs: ../02_routeA_chapkit/scripts/run_route.sh  sha256:2b3aaaf124ceb82e5427d1d122c30dfbe1adcdde0026e8a60889c233d18852da
        ../03_routeB_mlproject/scripts/run_route.sh  sha256:aa3bd580399d93f9ecda65adb3077879041c2551e4a22891fc1725eba06bf100
        the archived Lao data, via each route's own script
environment: each route's own -- route A's locally built Docker image, route B's uv-built
  environment. Deliberately not environment/: what a route installs is part of what is
  measured.
seeds: project 20260921; component none. Route A sets no seed and cannot: it fits with
  R-INLA, which is not bit-reproducible. Under the plan's §2 and §3 as amended on 2026-09-21
  that is accepted rather than treated as a defect, and the spread is reported instead.
commit: ea3a485
instructions-commit: d2459b1
node: analysis/05_repeatability
produced: 2026-09-21
what-it-establishes: both routes ran again, from clean, to a written evaluation. Route A took
  1534 s including its container build; route B took 92 s. Neither failed.
alternatives-considered: this node's run.sh deliberately does **not** call this script. A run
  that happened is accumulated evidence, not something a later run regenerates, and calling
  it from run.sh would mean every full reproduction paid for a container build and two
  backtests in order to recompute a table it could read from files already on disk. The
  originally planned phase D -- one replicate *discovery* agent per route -- was dropped on
  the human's reframing: it would have sharpened the effort measurement, whereas the question
  is now whether the routes run. Re-running each route's own deliverable script answers that
  directly and tests the deliverable at the same time.
agency: agent-on-human-assessment (the human reframed the question; the design of the check
  is the agent's)
information: agent-retrieved
