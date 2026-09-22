result: results/as_published_probe.log
script: scripts/probe_as_published.sh
        sha256:a18801b29f33ff00f017c75edeefc370c6c047539687039127e53c3db74d8b30
invocation: bash scripts/probe_as_published.sh
            (requires route A's container up on :8000, which scripts/rerun_routes.sh leaves
             running while it works; the probe submits no job and disturbs no evaluation)
inputs: the running chapkit_ghr_model service at 60b16a2 on localhost:8000
        /tmp/chapdata/chap_LAO_admin1_monthly.csv (route A's working copy of the archived data)
environment: the platform's own -- chap-core 2.1.0 (Archive/platform-chap/) -- and the model's
  Docker image built from the pinned commit
seeds: project 20260921; component none -- the probe is a pair of failing calls and draws no
  randomness
commit: f1daae5
instructions-commit: d2459b1
node: analysis/05_repeatability
produced: 2026-09-21
what-it-establishes: that route A does not run as published, first-hand and re-runnably,
  rather than on the report of the agent that discovered it. The service answers HTTP 200 on
  /api/v1/info and declares chapkit 2.0.0 / servicekit 2.0.2; chap-core 2.1.0's own
  environment holds chapkit 1.1.0 / servicekit 1.0.1. Pointed straight at the service, CHAP
  exits 1 with "URL http://localhost:8000 ... could not be reached as a chapkit service".
  With the escape hatch that message recommends, --run-config.is-chapkit-model, it exits 1
  again with three pydantic extra_forbidden errors on git_revision, chapkit_version and
  servicekit_version. Both exit codes are recorded in the log.
alternatives-considered: taking the discovering agent's account as established, which would
  have been reasonable and was not done: the claim that a route does not run as published is
  the load-bearing one in this project, and a ten-second reproduction is cheap next to it.
  Probing with `chap eval` alone was also possible; `chap model schema` is included as well
  because it is the path with no --run-config override, and the two failures are different
  and worth showing side by side.
agency: agent-autonomous
information: agent-retrieved (run here, not reported from elsewhere)
