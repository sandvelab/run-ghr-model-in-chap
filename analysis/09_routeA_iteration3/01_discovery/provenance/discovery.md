# Provenance — the discovery record, iteration 3

result: results/discovery_log.tsv
          sha256:91f15c8ebe2a543e06f864ee1dab3e0c5674372bdebb47f4dee9653542998562
        results/discovery_notes.md
          sha256:69bbb144558b712563ff85e563e9f2e3b4c045b05b7980e5053e6f26eedbb190
        results/brief_as_given.md
          sha256:83fa386a0ff09729616cbc792b0dc8b9ceec679f4685c814f09d84c65c8d6e2a
        results/agent_usage.tsv
          sha256:35bdf96fbd70fa27ca6a0615b3e6ded813b99dac9ed4136af6928a697ede59cf
        results/docker_state_before_run.txt
          sha256:3023651a7754bd76eb84120235ea0c51e1febebf95ad8e0f02a2f6e746477859
script: none of this project's for the log and notes — written step by step by the discovering agent through AI-internal/useful-scripts/log_step.py (unchanged since iteration 2). brief_as_given.md, agent_usage.tsv and docker_state_before_run.txt were written by the orchestrator: the brief before launch, the Docker state by the commands it lists, the usage from the harness's usage blocks as reported
invocation: one invocation of log_step.py per row, at the moment of the step; the agent was launched once, as a general-purpose subagent, with brief_as_given.md as its entire prompt
inputs: the public internet and the platform on this machine; Archive/data-lao/ (three files); the brief
environment: none of this project's — the route supplies its own. Platform as archived at Archive/platform-chap-it3/: chap-core 2.3.1, chapkit 2.1.2, servicekit 2.0.2. The model runs in the published image ghcr.io/chap-models/chapkit_ghr_model:sha-a9532c7 (linux/amd64, under emulation on this arm64 host)
seeds: project 20260921; no component seed reaches this route — R-INLA is not bit-reproducible and CHAP offers no seed for a chapkit service
commit: b524390
instructions-commit: d2459b1
node: analysis/09_routeA_iteration3/01_discovery
produced: 2026-09-26
alternatives-considered: reusing iteration 2's route A agent brief from memory rather than storing it — rejected; batch 3's brief was never saved verbatim, and this one is, so a later iteration can be run on exactly this text. Leaving Docker as found (two route A images and 2.67 GB of build cache present) — rejected by the human in favour of a fully cold start; consequence: the two iterations' elapsed times are not like for like (iteration 2 warm, iteration 3 cold). Editing the log where row 26's note says the pull took about 15 minutes while its own timestamp span is shorter — rejected: the pull ran in the background while the agent worked, and the log is never edited
contamination: the agent was a fresh agent given brief_as_given.md and nothing else, and read only its closed list. **One exposure was caused by the orchestrator**: the node's own claim.md, which the brief allowed the agent to read, named commit a9532c7 and chapkit 2.1.2. The agent pinned to a9532c7 because of it (rows 2–3). Upstream HEAD was that same commit, so the agent would have got the same code without it; what the claim did hand over is the knowledge that the upgrade was the point of the run. It carried nothing about iteration 2's findings. Incidental: docker images listed unrelated images from other work on this host. The orchestrator is fully contaminated (it holds iterations 1 and 2 in full) and contributed the brief, the Docker state and the storage of what came back
agency: human-set (that route A is re-run on the upgraded platform, the re-pin, the cold Docker state); agent-autonomous (every judgment inside the route, logged as decision rows)
information: agent-retrieved — every resource in the log; human-pointed only for the model repository URL and the data files
