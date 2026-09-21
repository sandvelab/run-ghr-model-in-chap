# Provenance — CHAP platform

One section per file. Append; never overwrite an existing section.

## install-metadata.txt

- **What it is**: the state of the CHAP installation on the machine this project runs on:
  `chap --version`, the resolved path of the entry point, the `uv tool list` output and the
  `uv` install receipt for `chap-core`.
- **Obtained by**: reading the live installation on 2026-09-21 — `chap --version`,
  `which chap`, `uv tool list`, and `cat ~/.local/share/uv/tools/chap-core/uv-receipt.toml`.
- **Version pinned**: `chap-core` 2.1.0.
- **Agency**: `human-set` that CHAP is the platform; `agent-retrieved` for the version and
  install details.

## chap-tool-freeze.txt

- **What it is**: `uv pip freeze` of the interpreter behind the `chap` entry point — 174
  packages with exact versions. This is what makes the platform reconstructible if the
  installation is lost.
- **Obtained by**: `uv pip freeze --python ~/.local/share/uv/tools/chap-core/bin/python`
  on 2026-09-21.
- **What cannot be pinned this way**: CHAP's own runtime behaviour depends on more than its
  Python dependencies — a container runtime for models that need one, and any registry it
  pulls from. Those are properties of the routes and are observed, not pinned.
- **Agency**: `agent-retrieved`.
