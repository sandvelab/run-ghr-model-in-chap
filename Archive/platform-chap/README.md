# platform-chap

The evaluation platform anchor: CHAP as installed on the machine this project runs on.

- `install-metadata.txt` — `chap --version` (2.1.0), entry-point path, `uv tool list`, and
  the `uv` install receipt for `chap-core`.
- `chap-tool-freeze.txt` — 174 exactly-versioned packages behind the `chap` entry point.
- `provenance.md` — how both were captured, and what about the platform cannot be pinned
  this way.

No copy of CHAP's source is kept here: the platform is an external installation, and what
this project needs to record is which one was used. What CHAP *does* with a model is the
object of study and is deliberately not documented in advance.
