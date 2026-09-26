# Provenance — CHAP platform, iteration 3
(IS_SHADOW)

One section per file. Append; never overwrite an existing section.

## install-metadata.txt, chap-tool-freeze.txt, freeze-diff-vs-it2.txt

- **What they are**: the live installation read on 2026-09-26 — `chap --version`, the
  resolved versions of `chap-core`, `chapkit`, `servicekit`, `pydantic`, `fastapi`, the
  `uv tool list`, the `uv` receipt with the home directory replaced by `<HOME>`, the full
  freeze, and its diff against iteration 2's freeze.
- **Obtained by**: `uv pip freeze --python ~/.local/share/uv/tools/chap-core/bin/python`,
  `uv tool list`, `stat` on the `chapkit-2.1.2.dist-info` directory (it reports
  2026-09-26 14:26 local time, when the upgrade was installed).
- **Not done by this project**: the upgrade itself. The human upgraded the installation before
  iteration 3 began; this folder records the result.
- **Agency**: `human-set` (the upgrade); `agent-retrieved` (everything recorded here).
