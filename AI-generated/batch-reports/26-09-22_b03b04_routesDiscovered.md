# Batches 3 and 4 — the two routes, discovered

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 2

Phase B. Each route was taken from nothing to a completed CHAP evaluation by a separate agent
that knew nothing of the other route, of the other model, or of any previous work in this
repository. This report is an account of how that was set up and what came back. What the
routes *cost* is batch 5 and 6's business.

---

## The brief, and what was done to keep it clean

Both agents were given the plan's §4 brief with exactly two substitutions: the model
repository URL and the node path. Everything else — the platform and its version, the three
data file paths, the logging obligation, the prohibition on modifying the model, the two
deliverables §2b adds — was word-for-word identical.

**One instruction had to be overridden, and it is the repository's own.** `CLAUDE.md` tells
any agent opening this repository to read `readme-at-start.md` first. That file names both
models and says what each route costs. An agent following the repository's standing
instruction would therefore have been contaminated before it began, and would have had no way
to know. Each brief states the override explicitly and gives a closed list of three things the
agent may read here: its own node, the discovery-log specification, and the three data files.
This is the one place where the repository's method and the plan's §3 actively conflict, and
§3 wins.

**The agents were run one after the other, not concurrently.** Two agents working at once on
one machine contend for it, and the elapsed-minute figures then measure the contention as much
as the route. Counts are the primary measure either way; sequencing costs wall-clock and buys
an elapsed figure that can be read.

**The orchestrating agent is contaminated and this is recorded rather than worked around.** It
holds a previous iteration's findings for both routes in full. §3 anticipates exactly this and
requires a note instead of a pretence. The mitigation is that each discovering agent is a
fresh agent given the brief and nothing else, so the discovery itself is uncontaminated; what
cannot be certified is that the orchestrator's choices about what to hand over carried nothing
extra. The note is in both routes' provenance records.

**One incidental exposure is reported, by route A's agent, against itself**: `docker images`
listed an unrelated chapkit model image belonging to other work on this host. It did not
inspect or use it. Route B's agent reports none.

## Logging, and how it was made hard to get wrong

Both agents logged through one implementation, `AI-internal/useful-scripts/log_step.py`, which
stamps each row with the current UTC second and the next step number and **refuses** a row the
format does not allow. A logging helper written per route would be two dialects of the
instrument; and the moment a row is written is the only point at which a malformed one can
still be corrected, since the summariser rejects a whole log.

The contemporaneity signature was computed for both, and both pass:

| | Route A | Route B |
|---|---|---|
| Rows | 43 | 33 |
| Distinct timestamps | 26 | 18 |
| Most rows sharing one timestamp | 4 | 3 |

A log written in one sitting at the end shows up as a handful of timestamps carrying many rows
each. Neither does.

**Route B's log was verified to have grown by append only.** It was committed mid-run at 19
rows while its agent was still working; the final file adds 14 lines and removes none.

## What came back

Both routes reached a completed CHAP evaluation on the Lao data. **Both models ran as
published**: neither was modified, and nothing was interposed between CHAP and either of them.
Each node holds its contemporaneous log, its narrative notes, everything CHAP wrote, and a
`run_route.sh` that its own agent ran in a clean shell.

## One thing each agent was asked for that it could not fully deliver

§2b requires a from-scratch recipe *verified by being run*, and both were run — but each has
one branch that did not execute, and both said so rather than claiming otherwise.

- **Route A**: the container build never ran cold. The host's BuildKit layer cache was already
  warm before the route began — 7 of 8 layers cached on the first build, 8 of 8 on every run
  since — so the expensive path, which clones a third-party GitLab dependency and compiles it
  under emulation alongside two CRAN installs, was never exercised. Deleting the model's image
  before the batch was not enough; the layer cache survives it.
- **Route B**: the `curl … astral.sh/uv/install.sh` branch never fired, because running it
  would have upgraded the host's `uv` as a side effect. Everything downstream of it ran.

Recording both was the right outcome. Verifying route A's recipe also found a real defect that
a recipe written out of the log at the end would have shipped invisibly: it failed its own
preflight check under `env -i` because `docker` is not on a minimal `PATH`.

## State

- Batches 3 and 4 **done**. `/validate invariants`: all eight checks pass.
- Five provenance records across the two nodes, each with its `alternatives-considered` and
  its contamination note.
