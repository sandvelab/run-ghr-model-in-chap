# platform-chap-it3 — the CHAP platform as found on 2026-09-26
(IS_SHADOW)

The platform anchor for iteration 3: `chap-core` 2.3.1, now resolving `chapkit` **2.1.2**
(iteration 2: 2.1.0) and `servicekit` 2.0.2. The installation was refreshed, not only
chapkit: 25 packages differ from iteration 2's freeze, `cyclopts` 4.25.3 → 5.0.0 among them.

- `install-metadata.txt` — versions, entry point, `uv` receipt, when chapkit 2.1.2 landed.
- `chap-tool-freeze.txt` — the full `uv pip freeze` of the `chap` interpreter.
- `freeze-diff-vs-it2.txt` — `diff` against `../platform-chap/chap-tool-freeze.txt`.
- `provenance.md` — how each was obtained.
