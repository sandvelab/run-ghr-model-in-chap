# Provenance — version_1_old_chapcore

One section per item. Append; never overwrite an existing section.

## The snapshot as a whole

- **What it is**: iteration 1 of this project, copied out of the live tree so the live tree
  could be emptied and the same plan re-run against an upgraded platform.
- **Obtained by**: `git archive HEAD <paths> | tar -x -C Archive/version_1_old_chapcore`,
  taken from commit `805350a05be351acbabe579866a079823c01f3c1` with a clean working tree, on
  2026-09-22. Using `git archive` rather than `cp` means the snapshot is exactly the
  committed state and carries none of the gitignored build products (a 201 MB `uv`
  environment under route B's run directories, `__pycache__`).
- **What is deliberately not here**: `AI-generated/hierarchical-report/`'s generated HTML,
  which is gitignored and regenerable; the `Archive/` anchors for the data and the two
  models, which are unchanged between iterations and stay in their own folders so that the
  only anchor differing between the two iterations is the platform.
- **Why it exists**: the human asked for iteration 1 to be preserved whole and the results
  wiped, so that the same plan could be re-run against `chap-core` 2.3.1. The reason to
  expect a different result is recorded in the plan's §4b.
- **Agency**: `human-set` (that iteration 1 is archived and the tree re-run);
  `agent-autonomous` (the snapshot's layout and the use of `git archive`).

## plan/26-09-21_chapModelIntegrationRoutes.md and plan/readme-at-start.md

- **What they are**: the plan and the project's front-matter file as they stood at the end of
  iteration 1, before the §4b entry and ledger rows that iteration 2 added to the live copies.
- **Obtained by**: the same `git archive` at commit `805350a`.
- **Agency**: `agent-autonomous`.

## platform-chap/

- **What it is**: iteration 1's platform anchor — `chap-core` 2.1.0, `chapkit` 1.1.0,
  `servicekit` 1.0.1, with the 174-package freeze of the `uv` tool environment behind the
  `chap` entry point. Its own `provenance.md` is carried over unchanged.
- **Why it moved here**: `Archive/platform-chap/` holds the platform the live analysis runs
  against, and iteration 2 re-pins it to 2.3.1. Appending a second version to that folder
  would leave two platforms in the place a reader looks for one.
- **Agency**: `agent-autonomous`.
