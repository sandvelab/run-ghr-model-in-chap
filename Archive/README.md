# Archive

Imported material: data, models, papers, platform documentation, protocols — anything that
came from outside this project. **Never edited in place**, marked `(IS_SHADOW)` on line 2
where the file is text, with a `provenance.md` beside it saying where it came from, at which
commit or version, and how to re-obtain it.

Kept separate so that "what came from outside" is answerable at a glance. Anything that
needs modifying is copied out — into a node under `analysis/`, or into
`Human-AI-collaboration/` — first; the original stays untouched, because it may later be
replaced by an updated import.

## Conventions

- **One folder per import**, with a `README.md` (what it is, what is in it) and a
  `provenance.md` (one section per file: source, commit or version, date, the command that
  fetched it, licence or governance). Append to `provenance.md`; never overwrite a section.
- **Data files carry a checksum manifest**, `sha256sums.txt`, written when they were fetched
  and re-verified by the node that reads them. The `(IS_SHADOW)` line marker cannot be
  applied to a data file — inserting a line would edit it and break its checksum — so the
  folder's `README.md` and `provenance.md` carry the statement instead.
- **Pin by commit, not by branch.** A file fetched from another repository's current state
  depends on that repository; the commit is recorded so a later reader can tell whether the
  source has moved.
- **A modelling resource** (a model library, a reference implementation) is archived the
  same way. It is adapted, if at all, by copying into a node's `scripts/`; the archived copy
  stays as fetched.
- **Where an import has a binary original and a markdown conversion**, they go in `orig/`
  and `md/` respectively; `md/` is the one to read.
- **`plan-as-delivered/`** holds the plan as it stood before the first batch ran, so that the
  live plan's drift can be measured against it.

- **`version_1_old_chapcore/`** is the exception to "imported material": it is this project's
  own iteration 1, frozen whole when the live tree was emptied to re-run the same plan against
  an upgraded platform. It sits here because what Archive guarantees — never edited, never
  read back into the live analysis — is exactly what a superseded iteration needs.

## Currently here

- `data-lao/` — the Lao admin-1 monthly CHAP dataset, `dhis2/climate-health-data` @ `af362d5`,
  with `sha256sums.txt`. No licence declared upstream.
- `model-route-a/` — `chap-models/chapkit_ghr_model` @ `60b16a2`, GPL-3.0.
- `model-route-b/` — `dhis2-chap/minimalist_example_uv` @ `5cd8a12`. No licence declared
  upstream.
- `platform-chap/` — the platform pin for the iteration now running. Re-written per
  iteration; the superseded one goes into that iteration's snapshot.
- `model-route-a-it3/` — `chapkit_ghr_model` re-pinned @ `a9532c7` (v0.1.2) for iteration 3,
  route A only.
- `platform-chap-it3/` — the platform as found for iteration 3: `chap-core` 2.3.1 resolving
  `chapkit` 2.1.2.
- `chapcore-docs-v2.3.1/` — four chap-core documentation files at tag `v2.3.1`, read by the
  iteration-3 route A agent, archived so their lengths can be measured.
- `model-case-c/` — `zlilu/minimal_template_example` @ `9cbc84a`, a third model added as a
  case rather than a route, to test whether an `MLproject` configuration reaches a model. No
  licence declared upstream.
- `plan-as-delivered/` — the plan as it stood before the first batch ever ran.
- `version_1_old_chapcore/` — iteration 1 entire: its plan, its 2.1.0 platform pin, its claim
  tree with both discovery logs, its batch reports and overview, and its claims.
