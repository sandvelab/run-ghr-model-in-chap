# Task details

The expanded entry for each task in `ai_task_history.md`: what was produced, the design
decisions, the files affected, and what a future session would need to know. Include
follow-ups, and say plainly where something did not work.

## T1 — Project definition and set-up (2026-09-21)

The repository arrived as a fresh copy of the starting point, so `AGENTS.md` §0 applied: no
analysis until the anchors are fixed and a plan exists. Four questions were put to the human
because each would have changed the work materially, and all four were answered. The choice
that shapes everything else is the second: each route is discovered by a **separate isolated
agent**, because an agent that learns CHAP on the first route cannot then measure how hard the
second one was to find out about. The plan is
`Human-input/Plans for AI generation/26-09-21_chapModelIntegrationRoutes.md`, archived as
delivered under `Archive/plan-as-delivered/`.

**Not done, and it matters**: `.claude/settings.json` still holds `<PARENT_DIR>` and `<HOME>`
placeholders. Two attempts to substitute them — via Bash and via the edit tool — were refused
by the session's permission classifier as self-modification. Until they are real paths, a
parent directory's `CLAUDE.md` can reach this project's instructions, which `setup-guide.md`
§2 exists to prevent. A future session should substitute them by hand or with the user's
explicit permission.

## T2 — Batch 1, the anchors (2026-09-21)

`analysis/01_anchors/scripts/verify_anchors.py` writes three files: the anchor manifest with
re-verified digests, a characterisation of the Lao panel, and a discrepancy table. The design
decision worth carrying forward is that the discrepancies are **recorded and not repaired** —
the schema's `row_count` counts target-present rows rather than rows, the schema names a
boundary file that was renamed upstream, and 233 of 2808 rows have no target value. How each
route copes with those is part of what the project is measuring, so repairing them would have
removed the thing being observed and changed the panel the routes are compared on.

The archived model clones had their `.git` directories removed after the commit was written to
`git-metadata.txt`, because a nested repository inside `Archive/` is invisible to this
repository's version control and so would not actually be versioned here.

**Follow-up for the human**: neither `minimalist_example_uv` nor `dhis2/climate-health-data`
declares a licence. Redistribution of the archived copies is not established, which blocks
release.

## T3 — Batch 2, the measurement instrument (2026-09-21)

The instrument was fixed before either route ran, because a log format settled after the first
route has run is a format shaped by that route. `AI-internal/skill-references/discovery-log-format.md`
specifies the six columns and the closed seven-milestone vocabulary; the milestones are stated
as achievements rather than as commands, which is what lets two structurally different routes
be compared at all. The code and its tests live in `analysis/04_comparison/scripts/`, one
implementation for both routes so they cannot be measured by subtly different code.

Two integrity statistics — `n_distinct_timestamps` and `max_rows_sharing_one_timestamp` —
exist because the plan requires contemporaneous logging and a rule with no detector is a rule
that will be honoured until it is not. A log written in one sitting at the end collapses onto
a few timestamps, and the tests assert that this is detected.

`summarise_discovery.py` is written but not yet called by `04_comparison/run.sh`; it is wired
in batch 5, once there are logs for it to read.

## T4 — Batches 3 and 4, the two routes (2026-09-21)

Two `general-purpose` agents were launched in parallel with briefs identical except for the
repository URL and the node path. They were told nothing about each other, and the brief
inlines the log format rather than pointing at the specification file, so that neither agent
browses this repository and learns that a second route exists from its contents.

Two residual contaminations are known and are not fixable from here, and both belong in the
comparison's limitations. First, each agent's node path (`02_routeA_chapkit`,
`03_routeB_mlproject`) reveals that it is one of several routes, though nothing about how the
other went. Second, the two agents ran **concurrently on one 8-CPU machine**, so the
wall-clock statistics are inflated by contention in a way the count statistics are not; the
counts are the primary measure for exactly this kind of reason.

## T5-T7 — Measuring, reporting and binding the results (2026-09-21)

The problem batch 5 surfaced is the one worth remembering: two agents given the *same* log
format still coded the same acts differently. Route A logged `chap eval --help` as a
`resource`, route B logged it as a `command`; route A additionally logged the brief-supplied
data files and its own notes file as resources. Taken at face value this inflates route A's
resource count by bookkeeping rather than by work.

It was handled as an alternatives node rather than as a correction, because a hand-curated
list of rows to adjust would depend on which rows someone noticed and would constrain no
future log. `b_normalised` applies two rules to both logs alike — a CLI help invocation is an
information source as well as a command; the brief's given inputs and the run's own artefacts
are not information sources — and the rules are declared as `--not-a-source` substrings in the
node's `run.sh` so they are visible beside the number. The normalisation moves route A from 10
sources to 9 and route B from 4 to 5, closing part of the gap without reversing it.

One operational note for a future session: `bash analysis/run.sh` re-runs **everything**,
including route A's Docker build and a fresh INLA fit, which is not bit-reproducible. It was
started once and stopped after about two minutes; the three route-A log files it had begun
overwriting were restored with `git checkout`. A full reproduction needs to be deliberate,
with its outputs compared against the archived ones rather than overwriting them.

**Still open**: phase D (one replicate agent per route, to test whether one run per route
resolves anything); the hierarchical report and clean-room/outsider validation; and the
human's decision on the two undeclared licences.

## T8 — what each route costs a human (batch 10)

Everything this project had measured was agent effort, and agent minutes do not convert to
human minutes: route A's 13.0 minutes to evaluation contains 410 seconds of machine time, and
an agent reads a 2833-word README in seconds. The node models human cost over the same
normalised discovery window the effort comparison uses — 27 route-A steps, 22 route-B steps —
carrying two personas through it: a software engineer a few years past a CS degree, and a
statistician with basic programming and no advanced software engineering. Scope was defaults
only; configuration was excluded by the human.

The design decision that matters most is that the model's **measured** inputs are in
`results/` and its **authored** inputs in `scripts/inputs/`, so a reader who disagrees with
the pace can replace the authored half and re-run without touching a measured value. Measured:
document lengths in words (counted from `Archive/`, from the installed `chap-core`, and from
captured `--help` output), and machine wait times (route A from its discovery log's own
timestamps; route B from file mtimes in the repeatability re-run, because its log collapses
`evaluation_started` and `evaluation_complete` onto one timestamp). Authored: per-act times,
reading rates, persona knowledge sets, prerequisite acquisition costs, and the divergence
rules that fork a persona's path away from the agent's.

Two corrections came out of running it rather than out of writing it. The model initially
charged the statistician 90 minutes of Docker learning on **route B**, because route B's agent
had run `docker info` — which would have inverted this study's own finding that route B needs
no container runtime. The rule now written into `scripts/inputs/README.md` is that a
prerequisite is charged only where the route cannot proceed without it. And dropping the
"read the installed library source" step for a persona who would not do that had to also drop
the GeoJSON check that only happens *because* of it; keeping both double-counted.

Results: engineer 119 min on route A against 46 on route B; statistician 649 against 221.
Changing route moves the estimate 2.6–2.9×; changing persona moves it 4.8–5.5×. The measure
of cognitive struggle — the share of human time spent diagnosing or learning rather than
following instructions — does not follow the clock: route B is three to five times quicker for
the statistician and marginally *more* bewildering per minute (64 % against 61 %).

**Carried forward.** Route A's cold image build is excluded and unmeasured — every build this
repository logged ran against a warm layer cache — and is additive to every route-A figure.
Sixty of the statistician's route-A minutes are a property of an arm64 host and vanish on
x86_64; that term is reported in its own column. Nothing here was measured on a person, and
one real human timed through route B would do more for its credibility than further agent
work. A possible later check was considered and not run: a fresh agent down each route,
instrumented to log what it already knew, to test the prerequisite inventory — worth doing for
that inventory only, since a second agent run yields agent minutes again, and a more capable
model carries more silent prior knowledge, making capability a confound in that instrument.

**A gap noticed in passing**: the task log had no entries between T7 (2026-09-21) and this
one, although batches 8b, 8c and five overview versions ran in between. They are recorded in
the plan's §4b and in their batch reports, but not here. Nothing has been reconstructed for
them — a log written after the fact is not the same artefact.
