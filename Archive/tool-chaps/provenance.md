# Provenance — chaps v0.99.4
(IS_SHADOW)

One section per file. Append; never overwrite an existing section.

## repo/, git-metadata.txt

- **What it is**: the chaps repository as published at `v0.99.4`, `.git` removed.
- **Source**: https://github.com/winterop-com/chaps
- **Pinned at commit**: `ba38f7c9ec336d95a5e3ce22926ac2b55f555102` (2026-10-02, "chore: release
  v0.99.4"). Upstream HEAD was this same commit both when the batch 14 discovering agent ran
  (2026-10-03, 08:41–15:09Z; it installed 0.99.4 through `install.sh`) and at clone time.
- **Obtained by**: `git clone <remote> repo` at HEAD (= the tag), then `rm -rf repo/.git`, on
  2026-10-03 after the agent had handed back. `README.md`, `docs/ai.md` and `install.sh` were
  checked byte-identical to `raw.githubusercontent.com/winterop-com/chaps/main/<path>` the same
  day, which is where the agent read and fetched them.
- **Licence**: AGPL-3.0 (`repo/LICENSE`), redistributed unmodified.
- **How it may be used**: as published. The chaps binary itself is not archived: the route
  installs it with `install.sh`, which downloads the release asset for the tag.
- **Agency**: `human-pointed` (the human named chaps, 2026-10-02); `agent-retrieved` (commit,
  licence).

## sha256sums.txt

- **What it is**: sha256 of the files under `repo/` whose words the batch 14 human-cost model
  counts (`analysis/10_routeA_chaps/02_humanCost/`), written at archiving time.
- **Agency**: `agent-retrieved`.
