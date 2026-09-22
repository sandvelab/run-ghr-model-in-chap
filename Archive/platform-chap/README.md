# platform-chap

(IS_SHADOW)

The platform anchor: CHAP as it is installed on the machine this project runs on, pinned at
**`chap-core` 2.3.1**, installed as a `uv` tool and invoked as `chap`.

What CHAP does with a model is the object of study and is deliberately not described here.
This folder records only *which* CHAP, precisely enough to reconstruct it.

## In it

- `install-metadata.txt` — `chap --version`, the resolved entry point, the `uv tool` listing
  and install receipt, and the resolved versions of the packages a model service actually
  negotiates with: `chapkit` 2.1.0, `servicekit` 2.0.2, `pydantic` 2.13.5.
- `chap-tool-freeze.txt` — a 176-package freeze of the interpreter behind the `chap` entry
  point. This is what makes the platform reconstructible if the installation is lost.

## Why the resolved `chapkit` version is pinned separately

A chapkit model service talks to `chapkit`, not to `chap-core`, and `chap-core`'s version
does not determine which `chapkit` is behind it: 2.1.0 required `chapkit>=0.27.0` with no
upper bound, so two installations of the same `chap-core` made on different days could hold
different `chapkit` majors. Recording only `chap-core` would leave the pin ambiguous in
exactly the place the routes differ.
