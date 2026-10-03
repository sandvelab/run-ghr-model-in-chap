# Provenance — the discovery record, batch 14 (route A through chaps, attempt 2)

result: results/discovery_log.tsv
          sha256:4d2ae39c41dd35685d876b00a9a56f45b3b4987428db258813a6a51bb450c71a
        results/discovery_notes.md
          sha256:d9be3f11401ce61636e5319ba2ddd222ccbf6d7d0916b202daf876f6daa572fe
        results/agent_usage.tsv
          sha256:631c1600473d72d9f43b5758aa376ca65d9c706bd837494255cf808c3d964034
        results/agent_usage_interim.tsv
          sha256:ebe0271091f4c9954cb3c7c10e7e28c4ef6df2536942228e5df8d757bc916d47
        results/agent_launched_utc.txt
          sha256:1018fa7751f15c3a7bcb01fed302a19e5715045c18fa9220728214ac1b099435
        results/docker_state_before_run.txt
          sha256:d3c207e5c0a15475c9fe76f3bb358eece64ccba1cee562b37c9638642ddc8548
        results/image_id.txt
          sha256:7e1da779064ae1913a0c8b4172326e6b7f2d9a7a418cbd00204653a6cd9b23dc
script: none of this project's for the log and notes — written step by step by the discovering agent through AI-internal/useful-scripts/log_step.py. docker_state_before_run.txt and agent_launched_utc.txt were written by the orchestrator before launch; agent_usage.tsv and agent_usage_interim.tsv by the orchestrator from the harness's usage blocks as they arrived; image_id.txt by the orchestrator with `docker image inspect` after the hand-back
invocation: one invocation of log_step.py per row, at the moment of the step; the agent was launched once, as a general-purpose subagent, with results/brief_as_given.md (provenance/brief.md) as its entire prompt
inputs: the public internet and the platform on this machine; Archive/data-lao/ (three files); the brief
environment: none of this project's — the route supplies its own. chaps 0.99.4 (Archive/tool-chaps/), installed by the agent with its install.sh into the session scratchpad. chap-core 2.3.1 as installed for iteration 3 (Archive/platform-chap-it3/). The model runs in the published image ghcr.io/chap-models/chapkit_ghr_model:sha-dfb2e3f (Archive/model-route-a-chaps/; linux/amd64 under emulation on this arm64 host; service reports 0.1.3, chapkit 2.2.0)
seeds: project 20260921; no component seed reaches this route — R-INLA is not bit-reproducible and CHAP offers no seed for a chapkit service
commit: 459c7f9
instructions-commit: ea5aa2f
node: analysis/10_routeA_chaps/01_discovery
produced: 2026-10-03
alternatives-considered: using attempt 1 (2026-10-02), which stalled before the model image arrived — kept as a failed attempt in ../results/attempt1_stalled/ and not used for any figure (../provenance/attempt1_stalled.md). Editing row 48, whose milestone `model_obtained` was written three hours after the event it records — rejected: the log is never edited; the row's note dates the event to row 31 and the human-cost model reads it there. Treating the 11:55–14:45Z gap as route effort — rejected: the agent found the host had slept (pmset), logged it as a blocker after the fact, and the human-cost model excludes it
contamination: the agent was a fresh agent given brief_as_given.md and nothing else, and its log names only resources on its closed list or on the public internet. **Exposures caused by the orchestrator**: (1) docker_state_before_run.txt, which the brief let it read, gave the measured throughput to ghcr.io and the image size, from which the agent worked out "~70 min pull expected" (row 2) and set `--timeout 7000` (row 14); without it chaps' default 300 s timeout would have failed the first run sooner and differently. The same file named the image tag `sha-dfb2e3f` before chaps did; chaps chose that tag on its own (row 11, its marketplace pin), so the route is unchanged by it. (2) The orchestrator had read the chaps README, docs/ai.md, docs/models.md and the marketplace entry before writing the plan's §4b, but none of that reached the brief beyond the sentence naming chaps. (3) Attempt 1's files sit in ../results/attempt1_stalled/, outside the node the brief opened, and the session scratchpad was emptied before launch; the log shows no read of either. Attempt 2's resumable fetcher was written afresh (scripts/fetch_image_oci.sh, curl) and differs from attempt 1's (fetch_oci.py, Python). Not an exposure but worth recording: row 18 reads installed chap-core library source (cli_endpoints/_common.py), the same file iteration 2's route B read and iteration 3's route A did not need
agency: human-set (route A through chaps, chaps' default model pin, the cold Docker state, the re-run after attempt 1); agent-autonomous (every judgment inside the route, logged as decision rows, including the image-fetch workaround)
information: agent-retrieved — every resource in the log; human-pointed only for the model repository URL, the chaps URL and the data files
