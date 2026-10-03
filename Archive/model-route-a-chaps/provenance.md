# Provenance — chapkit_ghr_model, batch 14 pin (through chaps)
(IS_SHADOW)

One section per file. Append; never overwrite an existing section.

## repo/

- **What it is**: route A's model repository as published at `dfb2e3f`, `.git` removed.
- **Source**: https://github.com/chap-models/chapkit_ghr_model
- **Pinned at commit**: `dfb2e3fdd25cbf7a369cf078361814056e7fe709` (2026-10-02, "chore: release
  0.1.3 on chapkit 2.2.0 (#9)"). Upstream HEAD at clone time.
- **Obtained by**: `git clone <remote> repo`, then `rm -rf repo/.git`, on 2026-10-03 after the
  batch 14 discovering agent had handed back.
- **Licence**: GPL-3.0.
- **How it may be used**: run as published (plan §3). The route never cloned it: chaps served
  the published image `ghcr.io/chap-models/chapkit_ghr_model:sha-dfb2e3f`, which loaded as
  image id `sha256:cf686a4edb71…` (repo digest `sha256:517f261c…`), recorded in
  `analysis/10_routeA_chaps/01_discovery/results/image_id.txt`.
- **Agency**: `human-set` (the human chose chaps' default pin over iteration 3's, 2026-10-02);
  `agent-retrieved` (commit, licence).

## git-metadata.txt, diff-since-it3-pin.patch, diff-stat-since-it3-pin.txt

- **What they are**: clone metadata, and `git diff a9532c7 dfb2e3f` in full and as a stat,
  taken before `.git` was removed. Three files change: `main.py` (3 lines), `pyproject.toml`
  (chapkit 2.1.2 → 2.2.0) and `uv.lock`.
- **Agency**: `agent-retrieved`.
