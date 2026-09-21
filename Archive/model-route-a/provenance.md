# Provenance — chapkit_ghr_model (route a)

One section per file. Append; never overwrite an existing section.

## repo/

- **What it is**: the model repository for route A — a chapkit-based model service, as published, with its `.git`
  directory removed so that the tree is versioned by *this* repository rather than being an
  invisible nested repository.
- **Source**: https://github.com/chap-models/chapkit_ghr_model
- **Pinned at commit**: `60b16a2e929405ce95fae2043a63d7e27292ca0f` (see `git-metadata.txt` for the remote, the commit date and
  the subject line).
- **Obtained by**: `git clone <remote> repo && git -C repo checkout 60b16a2e929405ce95fae2043a63d7e27292ca0f`, then
  `rm -rf repo/.git`, on 2026-09-21.
- **Licence**: GPL-3.0 (LICENSE in the repository)
- **How it may be used**: run as published (plan §3). It is not modified, re-specified or
  tuned. The discovering agent for this route works from the public repository itself; this
  copy exists so that a later reader can see the exact code that was run even if upstream
  moves.
- **Agency**: `human-pointed` (the human named this repository); `agent-retrieved` (commit,
  licence).

## git-metadata.txt

- **What it is**: remote, commit, commit date, subject and clone timestamp, written at clone
  time because the `.git` directory was then removed.
- **Obtained by**: `git remote get-url origin`, `git rev-parse HEAD`, `git log -1` in the
  clone before detaching it.
- **Agency**: `agent-retrieved`.
