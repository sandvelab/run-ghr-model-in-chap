# Provenance — results/host_prerequisites.log

result: results/host_prerequisites.log
        sha256:50be0932a1f0b489dcb88e4585daf536f4f1267832015e45d0160c53b4ac5d8d
script: none — a direct capture of the machine's state, not a computed result
invocation: uname -m; docker info --format '{{.ServerVersion}}'; docker info --format '{{.Architecture}}/{{.OSType}}'; docker images -q | wc -l; docker images --format '{{.Repository}}:{{.Tag}}\t{{.Size}}\tcreated {{.CreatedSince}}' | grep -iE 'ghr|chapkit'
inputs: none — the live host
environment: none — the host's own docker client
seeds: project 20260921; no stochastic step
commit: bb806ee
instructions-commit: d2459b1
node: analysis/04_comparison
produced: 2026-09-22
alternatives-considered: regenerating this from `run.sh` like an ordinary result. Rejected:
  it is an observation of the machine at one moment, before either route ran, and re-running
  it after route A has built its image would overwrite the very fact it exists to record.
  It is raw evidence and is treated like a discovery log — captured once, never regenerated.
  It was also considered to leave the Docker state in the batch report only, as a note; it is
  written to a file instead because the reports may need to attribute part of route A's build
  cost to it.
  The remaining exposure is recorded rather than removed: an unrelated chapkit model image
  from the human's other work, `ghcr.io/chap-models/chapkit_ewars_model:latest`, is present.
  It is not route A's model and is not a cached build of it, but if the two images share base
  layers then route A's build will reuse them and its build time will understate a build from
  nothing. Deleting an image belonging to the human's other work was not the agent's to do.
  Batch 3 therefore records how many of route A's build layers came from cache, so the extent
  of the reuse is measured rather than assumed.
agency: agent-autonomous (recording it); human-set (that the route A image itself was deleted
  before this batch, so that route A pays its build again)
information: agent-retrieved
