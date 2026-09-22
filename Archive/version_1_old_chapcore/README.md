# version_1_old_chapcore

(IS_SHADOW)

Iteration 1 of this project, frozen whole. It was run against **`chap-core` 2.1.0**, whose
environment resolved **`chapkit` 1.1.0 / `servicekit` 1.0.1**, and under that platform route A
(chapkit) did not run as published: `chapkit` 1.1.0's `MLServiceInfo` is `extra="forbid"` and
the model service's `chapkit` 2.0.0 sends three fields it does not know, so CHAP reported the
service as unreachable and the route completed only through an interposed proxy.

Iteration 2 runs the same plan against `chap-core` 2.3.1 / `chapkit` 2.1.0. This folder is
what iteration 1 concluded, kept so that the live tree can be emptied and re-run without
destroying it.

**Nothing here is read by the live analysis, and nothing here is edited.** Iteration 2's
discovering agents are not given it, and its findings do not enter iteration 2's reports —
the two runs are independent measurements, not a before/after pair.

## What is in it

- `plan/` — the plan and `readme-at-start.md` exactly as they stood when iteration 1 ended.
- `platform-chap/` — the 2.1.0 platform pin: install metadata and the 174-package freeze.
- `analysis/` — the whole claim tree: both routes' contemporaneous discovery logs and notes,
  the effort comparison with its alternatives node, and the repeatability node.
- `AI-generated/` — batch reports 1, 2, 5, 6 and overview version 1. The generated
  hierarchical report's HTML is gitignored and is not here; its `provenance.md` is.
- `claims/` — the claim collection as it stood.
- `git-commit.txt` — the commit the snapshot was taken from, and when.
