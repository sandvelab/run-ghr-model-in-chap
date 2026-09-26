# Provenance — chap-core documentation at v2.3.1
(IS_SHADOW)

- **What it is**: the four chap-core documentation files the iteration-3 route A agent read
  (log rows 13, 15–17): the repository `README.md` (discarded by the agent) and
  `docs/chap-cli/eval-reference.md`, `docs/chap-cli/evaluation-workflow.md`,
  `docs/external_models/chapkit.md` (used). Kept as fetched, with `sha256sums.txt`.
- **Source**: https://github.com/dhis2-chap/chap-core, tag `v2.3.1` = commit `bb9b593ff55a16e36fe539fa0431ad932f0e657d`.
- **Obtained by**: `curl https://raw.githubusercontent.com/dhis2-chap/chap-core/<commit>/<path>`
  on 2026-09-26, after the agent had run, so that the human-cost model can count their words.
- **Why no IS_SHADOW line in the files themselves**: inserting one would change the word
  counts being measured; this file and the folder listing carry the statement instead.
- **Licence**: chap-core's own (AGPL-3.0 per its repository), redistributed unmodified.
- **Agency**: `agent-retrieved`.
