# Provenance — CHAP platform

One section per file. Append; never overwrite an existing section.

## install-metadata.txt

- **What it is**: the state of the CHAP installation on the machine this project runs on:
  `chap --version`, the resolved path of the entry point, the resolved versions of
  `chap-core`, `chapkit`, `servicekit`, `pydantic` and `fastapi`, the `uv tool list` output,
  and the `uv` install receipt for `chap-core`.
- **Obtained by**: reading the live installation on 2026-09-22 — `chap --version`,
  `which chap`, `uv pip freeze --python ~/.local/share/uv/tools/chap-core/bin/python`,
  `uv tool list`, and `cat ~/.local/share/uv/tools/chap-core/uv-receipt.toml`.
- **Version pinned**: `chap-core` 2.3.1, resolving `chapkit` 2.1.0 and `servicekit` 2.0.2.
- **Why the dependency versions are recorded as part of the pin**: `chap-core` has not
  constrained `chapkit` consistently across releases — 2.1.0 required `chapkit>=0.27.0` with
  no upper bound, 2.2.0 and 2.3.0 required `chapkit<2`, and 2.3.1 requires
  `chapkit>=2.1.0,<3`. A pin naming only `chap-core` therefore does not identify what a
  chapkit model service is talking to. Established by reading the released package metadata
  on PyPI.
- **Agency**: `human-set` that CHAP is the platform and that 2.3.1 is the version;
  `agent-retrieved` for the resolved dependency versions and the release constraints.

## chap-tool-freeze.txt

- **What it is**: `uv pip freeze` of the interpreter behind the `chap` entry point — 176
  packages with exact versions. This is what makes the platform reconstructible if the
  installation is lost.
- **Obtained by**: `uv pip freeze --python ~/.local/share/uv/tools/chap-core/bin/python`
  on 2026-09-22.
- **What cannot be pinned this way**: CHAP's runtime behaviour depends on more than its
  Python dependencies — a container runtime for models that need one, and any registry it
  pulls from. Those are properties of the routes and are observed, not pinned.
- **Agency**: `agent-retrieved`.
