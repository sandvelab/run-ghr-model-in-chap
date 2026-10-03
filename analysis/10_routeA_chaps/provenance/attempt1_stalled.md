# Provenance — batch 14, attempt 1: the discovery run that stalled on the network

result:
        results/attempt1_stalled/agent_launched_utc.txt
          sha256:1cf3c6f96cf229b3bb6e03dfc845b38bf9efeef7a4fa96dceb69c7e3bcbee603
        results/attempt1_stalled/discovery_log.tsv
          sha256:94fa1515bd70c60ce1d81d3e4ea0d642b2a5d40c718dfd12b926bab783e88b99
        results/attempt1_stalled/discovery_notes.md
          sha256:b44205f20c357af29484410e21584b9113693d2ba111a0ecb45c5d7c06593d1b
        results/attempt1_stalled/docker_state_before_run.txt
          sha256:555a8e3ed16378376cfc64c9dd0eb7e43f8db8e6464f3d8b45d55379dc5e75f7
        results/attempt1_stalled/run_route_draft.sh
          sha256:e7d97e506d850447286b8a07b4fe76b0a173c3f80f5e5c2bf6f1fa9da42cd151
        results/attempt1_stalled/scratch/chaps_deployments.yaml
          sha256:121d6dcffa419d1441c417497b04c683e052c58ac72e32d3e0678278c6dc1cc1
        results/attempt1_stalled/scratch/chaps_run.log
          sha256:2fafe1dbb46e0b490e68fdc240f1e7924a18ede48698e0808f9e9c2aef261086
        results/attempt1_stalled/scratch/compose.marketplace.yml
          sha256:f3226603f3301c4d5022432db10d8814dc676bb318b9a7885f8d1736260af85a
        results/attempt1_stalled/scratch/fetch_oci.py
          sha256:a4df0da10688c5488c5fb42a1a913c1981f35256b9cb8d769c186018b332e922
        results/attempt1_stalled/scratch/fetch.log
          sha256:bf0d6dff66cca34a1ff44a74ec3c9646506a53ed22e704e2472d6b7708c4e6fa
        results/attempt1_stalled/scratch/log.sh
          sha256:8a84060a3a0f5c49ef5fc81b103fd159ea18536199c395982d9b8e6bb587a210
        results/attempt1_stalled/scratch/pull.log
          sha256:75a36e47f86f1353b196edf21789eed882b6d08ea82802292cc86c368e12cd52
        results/attempt1_stalled/scratch/pull1.log
          sha256:9549983620733a033f12136983c63c964b5f07698f7d7c726fc31f84d71ca212
script: none of this project's. discovery_log.tsv and discovery_notes.md were written step by step by the discovering agent through AI-internal/useful-scripts/log_step.py; run_route_draft.sh is the agent's unfinished route script, never run clean; scratch/ holds the agent's working files from the session scratchpad, copied unchanged (its resumable blob fetcher fetch_oci.py, the docker pull and chaps run logs, its logging helper, and the deployment files chaps wrote); docker_state_before_run.txt and agent_launched_utc.txt were written by the orchestrator before launch
invocation: the agent was launched once, as a general-purpose subagent, with 01_discovery/results/brief_as_given.md as its entire prompt, at 2026-10-02T16:19:55Z. The harness stopped it at about 2026-10-02T20:35Z with "Agent stalled: no progress for 600s"; its last log row is 2026-10-02T20:03:27Z
inputs: the public internet and the platform on this machine; Archive/data-lao/ (three files); the brief
environment: chaps v0.99.4 (installed by the agent into the session scratchpad, since deleted); chap-core 2.3.1 as the uv tool; Docker Desktop 27.4.0, arm64, 8 GB. The model image ghcr.io/chap-models/chapkit_ghr_model:sha-dfb2e3f never arrived
seeds: project 20260921; none reached anything
commit: 35af552
instructions-commit: 35af552
node: analysis/10_routeA_chaps
produced: 2026-10-02
outcome: **no evaluation.** The route as far as it got — the plan of `chaps run` for the model service and `chap eval` against its URL (log row 16, 16:21:47Z), the installer, `chaps doctor` and `chaps run` — worked. Everything after 16:22Z was the 2.14 GB compressed image (one 1.42 GB layer) failing to download: chaps run cancelled by the agent's own 30-minute timeout; two docker pull attempts ending in "unexpected EOF" on layer 7c4627a62657, which docker restarts from zero on every retry; then a resumable HTTP-range fetcher of the agent's own writing, which had 424 MB on disk when it died. The agent measured throughput at about 57 KB/s (19:18Z) and found from pmset that the laptop had slept on battery from about 18:30Z; the orchestrator measured 9 KB/s at 20:38Z
not admissible for: the human-cost model and the elapsed-time statistics. Its elapsed time measures this machine's connection and power state that evening, not the route. The steps before the stall are route evidence and are kept as such, but the batch's figures come from a fresh agent on a fresh run
agent usage: the harness's notification for the stalled agent carried no token, tool-use or duration figures; none are recorded, and none are estimated
contamination: the agent shared the orchestrating session's scratchpad, where the orchestrator's own clone of chaps sat; whether the agent read it is not recorded in its log, which names only GitHub URLs for chaps documents. Everything the agent left in the scratchpad, and the orchestrator's clone, was deleted after this record was made, so the next agent cannot meet them
alternatives-considered: resuming the same agent later — offered to the human and declined, because its log would carry hours of network noise and a home-made image fetcher no persona would write. Deleting the attempt — rejected; failures are kept (§3)
agency: human-set (keep as attempt 1, re-run fresh on a good network); agent-autonomous (every judgment inside the attempt, logged as decision rows; this record)
