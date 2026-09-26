# Provenance — chapkit_ghr_model, iteration 3 pin
(IS_SHADOW)

One section per file. Append; never overwrite an existing section.

## repo/

- **What it is**: route A's model repository as published at `a9532c7`, `.git` removed.
- **Source**: https://github.com/chap-models/chapkit_ghr_model
- **Pinned at commit**: `a9532c7cdd9eba93d7b5a1445d4bc742551e7585` (2026-09-25, "rebuild on
  the fixed chapkit-r-inla base and bump the version to 0.1.2").
- **Obtained by**: `git clone <remote> repo && git -C repo checkout a9532c7c`, then
  `rm -rf repo/.git`, on 2026-09-26.
- **Licence**: GPL-3.0.
- **How it may be used**: run as published (plan §3). The orchestrator did not read its
  documentation before the iteration-3 discovering agent ran (§3); it read only the commit
  subjects and the diff stat.
- **Agency**: `human-set` (the human chose to re-pin to upstream's latest commit, 2026-09-26);
  `agent-retrieved` (commit, licence).

## git-metadata.txt, diff-since-it2-pin.patch, diff-stat-since-it2-pin.txt

- **What they are**: clone metadata, and `git diff 60b16a2 a9532c7` in full and as a stat,
  taken before `.git` was removed.
- **Agency**: `agent-retrieved`.
