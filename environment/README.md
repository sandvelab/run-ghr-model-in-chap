# environment

The **one main environment** for the whole analysis, used generally. A node overrides it
only where it genuinely needs something else, in that node's `env/`, with the reason
recorded in that node's `claim.md`.

| File | What it is |
|---|---|
| `environment.yml` | Declarative — the interpreter version and the libraries the analysis asks for, one line each, with a comment saying what each is for. |
| `install-env.sh` | The build. Creates `env/` **from `lock.txt`**, and re-resolves from `environment.yml` only with `RESOLVE=1`, reporting any difference between what it built and the lockfile. Uses `uv`. |
| `lock.txt` | Resolved — every package with its exact version (`uv pip freeze`). **This is what reproduces.** Written by `RESOLVE=1 bash environment/install-env.sh`, which is what `/pin-environment` runs. Absent in a fresh copy. |
| `Dockerfile` | The image layer, where the analysis matters enough to outlive its dependencies or depends on a platform-specific runner. Absent until a project decides it needs one, and the decision is recorded here either way. |
| `env/` | The built environment. Not tracked; rebuild with `install-env.sh`. |

Invoke directly, as `environment/env/bin/python` — never by activating it — matching the
convention `AGENTS.md` §8 sets for `.venv`. Note this is *not* the `.venv` at the repository
root, which runs the repository's own machinery (`node.py`, `check_invariants.py`). A node's
`run.sh` sets `PYTHON` to this interpreter; `node.py` writes that line.

## What is pinned here, and what deliberately is not

Pinned on 2026-09-21: **Python 3.13.0, no third-party dependencies.** `environment.yml`
declares none and `lock.txt` is empty, because this project's own scripts read CSV and JSON
logs and count over them, and the standard library covers that. An empty lockfile is a
statement, not an omission: it says that nothing outside the interpreter can change these
results. It is re-pinned, with an entry in the plan's §4b, the first time a node genuinely
needs a library.

**The models' environments are not pinned here, and that is the point.** Each of the two
routes under study brings its own dependency mechanism — that is much of what distinguishes
them — and pinning them centrally would replace the thing being measured with a copy of it.
What each route installs, and how, is recorded in that route's node.

## What cannot be pinned

- **CHAP itself.** It is an external installation on this machine (`chap-core` 2.1.0, a `uv`
  tool), not a dependency of `environment/`. What makes it reconstructible is the 174-package
  freeze in `Archive/platform-chap/chap-tool-freeze.txt`, not this lockfile.
- **The container runtime.** Docker Desktop 27.4.0 (server 27.4.0, 8 CPUs, ~8.2 GB) was
  confirmed running on 2026-09-21. A route that needs a container needs a daemon, and a
  daemon is not something a lockfile can supply; whether a route needs one at all is one of
  the findings this project is after.
- **Anything either route pulls at run time** — an image from a registry, a package index, a
  git remote. A route that depends on a network resource is recorded as depending on it.
