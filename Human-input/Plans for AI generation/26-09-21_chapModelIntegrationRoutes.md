# Running two published models through CHAP by its two integration routes, veridically

The plan this repository exists to execute. It is written to be run by an agent that has
none of the conversation behind it in context: everything needed to start is either here or
in `Archive/`.

---

## 1. The aim

**Establish how discoverable and how executable CHAP's two model-integration routes are for
an agent working only from public material, by taking one published model down each route
until it produces a CHAP evaluation on the public Lao admin-1 monthly data.**

What is fixed by this plan:

1. The two routes and the model that stands for each — `chap-models/chapkit_ghr_model`
   (route A, a chapkit-based model service) and `dhis2-chap/minimalist_example_uv`
   (route B, an `MLproject`-declared model run with `uv`). Neither model is modified,
   re-specified or tuned. They are run as published.
2. The platform — CHAP (`chap-core`), at the version pinned in §4, invoked as the `chap`
   command-line tool already installed on this machine.
3. The data — `dhis2/climate-health-data`, directory `lao/`, at the commit pinned in §4.
4. That each route's discovery is carried out by an agent with **no knowledge of the other
   route**, and that its discovery record is written **as it happens**, not reconstructed
   afterwards (§3).

What is open, and is decided during execution as an alternatives node or a logged decision:

1. What each route's correct invocation actually is — this is the object of study, not an
   input to it. Neither the plan nor the executing agent may shortcut it by reading the
   other route's findings.
2. Which CHAP evaluation entry point each route reaches, and on what backtest splits and
   metric. These are route-discovered, and may differ between routes; where they differ,
   the difference is recorded rather than forced into agreement (§2).
3. How effort is measured from a discovery log — the summary statistics computed over the
   log, which are a judgment call and get an alternatives node.
4. Whether a single agent per route is enough evidence, or whether replication changes the
   conclusion (phase D).

Two things are produced at once, and neither is subordinate to the other:

1. **An answer about the two routes** — what it takes to find out how to run each, what it
   takes to actually run it, and where each route costs effort.
2. **The complete veridical record of how that answer came about**, including the raw
   discovery logs the answer is computed from.

**The central comparison this project is built to answer**: route A against route B on the
same three axes — (a) which resources had to be consulted, (b) what the process of finding
out looked like, including dead ends, (c) what the working invocation turned out to be —
with the same platform version, the same data, the same brief to each discovering agent, and
the same log format. A project that reports only that both models ran has not answered its
own question.

## 2. What "earns its place" means

There is no model being improved here, so "better" is a property of a **route**, not of a
prediction. A route is characterised on:

- **Primary**: the discovery cost recorded in that route's `discovery_log.tsv` — the number
  of distinct documentation resources consulted, the number of them that were necessary
  versus consulted-and-discarded, the number of dead ends (an attempted invocation that
  failed and had to be abandoned or corrected), and the number of distinct commands run
  before the first successful evaluation. Computed by a script from the log, never counted
  by hand.
- **Secondary**: whether the route reached a completed CHAP evaluation at all, and what
  prerequisites it imposed beyond CHAP itself (a container runtime, a network registry, a
  build step, credentials).
- **Reported but not compared**: each model's predictive scores. The two routes may land on
  different backtest splits or different metrics; where they do, the scores are reported per
  route with their configuration and **no cross-route performance claim is made**. This is a
  decision of the project's framing, not an oversight.

**The aim is to conclude, and the conclusion may be an uncertain call.** "Both routes were
about equally hard, and the difference is within what one agent's run can resolve" is a
conclusion. If a route does not reach an evaluation at all, that is reported plainly as its
result, with where it stopped and what it would have needed.

## 3. Non-negotiables

These override anything else in this plan.

- **Contamination control.** Route A's and route B's discovery are each carried out by a
  separate agent that is given the identical brief (§4, *Discovering agent brief*) and is
  told nothing about the other route, the other model repository, or any finding from it.
  The orchestrating agent does not pass hints between them, and does not pre-read a route's
  model repository documentation before that route's agent has run. Where the orchestrator
  has unavoidable prior exposure, it is recorded in the route's provenance record as a
  contamination note. A comparison of discovery effort between two contaminated runs is
  worthless, and it fails silently.
- **The discovery log is contemporaneous.** Each discovering agent appends to
  `discovery_log.tsv` at the moment of each step. A log written at the end from memory is
  not admissible evidence for §2's primary measure, and if that happens it is recorded as
  such and the primary measure is reported as unavailable for that route.
- **No number reaches a claim except through a file** (`AGENTS.md` §1). Every count in the
  reports is computed by a script from a log file on disk and read back from the script's
  output file. No count is carried from terminal output or from an agent's summary message.
- **No sealed holdout, and this is a deliberate deviation.** `AGENTS.md` §0 and the template
  assume model development, where a holdout protects against selection on the data. Nothing
  here is selected or tuned on the data: both models are run as published, once per route,
  with the route's own splits. A sealed holdout would protect against a risk this project
  does not run. The deviation is recorded here, in `readme-at-start.md`, and in the root
  claim. **If any batch begins choosing between model configurations on the basis of Lao
  scores, this deviation is void and the work stops until the human re-decides.**
  Agency: `human-set`.
- **The models are not modified.** If a model does not run as published, that is a finding
  and is recorded as one. Patching the model's own code to make it run is permitted only as
  an explicitly logged decision with the diff stored, and the route is then reported as
  "ran only after modification", never as "ran".
- **If an anchor turns out to be wrong** — the platform's behaviour differing from its
  documentation, a model repository that does not run as documented, a defect in the
  archived data — **stop and report it** rather than silently patching around it.
- **Every judgment call is a node or a logged decision, never silent.** Foreseen here: the
  effort statistics computed from the logs; the choice of CHAP evaluation entry point where
  a route offers more than one; the handling of a route that needs a prerequisite the
  machine lacks; whether to replicate a route.
- **Agency is recorded on every decision**: `human-set`, `agent-on-human-assessment`, or
  `agent-autonomous`; for information gathering, `agent-retrieved` or `human-pointed`.
- **Failures are kept.** A route that stalls, an invocation that does not work, a
  documentation page that turned out to be wrong: all stay in the record with what happened.

## 4. Decisions already made

| | Decision |
|---|---|
| **Evaluation platform or harness** | CHAP, `chap-core` **2.1.0**, installed on this machine as a `uv` tool and invoked as `chap`. Verified present at planning time (`chap --version` → `2.1.0`). Batch 1 archives the resolved version and install metadata under `Archive/platform-chap/` with `provenance.md`. What CHAP does with a model is the object of study and is **not** pre-specified here. Agency: `human-set` (platform), `agent-retrieved` (version). |
| **Metric** | Whatever the route's own CHAP evaluation entry point reports, taken from the file CHAP writes, per route. No metric is imposed across routes, and no cross-route performance claim is made (§2). |
| **Backtest or split scheme** | Route-discovered; recorded as a file per route in that route's `results/`. If both routes land on the same scheme, that is recorded as a finding, not assumed. |
| **Required baselines** | None. The comparison is between integration routes, not between predictions. CHAP's own built-in baseline, if the evaluation entry point produces one by default, is reported as it comes. |
| **Reference model** | None. Neither model is a reference for the other; they are instances of two routes. |
| **Modelling resources to start from** | Route A: `https://github.com/chap-models/chapkit_ghr_model`, licence GPL-3.0, pinned by commit in batch 1, archived at `Archive/model-route-a/`. Route B: `https://github.com/dhis2-chap/minimalist_example_uv`, pinned by commit in batch 1, archived at `Archive/model-route-b/`. Both are run **as published** (§3). Agency: `human-pointed` (both repositories named by the human). |
| **Data** | `https://github.com/dhis2/climate-health-data`, directory `lao/`: `chap_LAO_admin1_monthly.csv`, `chap_LAO_admin1_monthly.geojson`, `chap_LAO_admin1_monthly_schema.json`. Pinned by commit in batch 1, archived at `Archive/data-lao/` with `sha256sums.txt` and `provenance.md`. Agency: `human-pointed`. |
| **Target** | Whatever the Lao CHAP dataset declares as its target column at admin-1 monthly resolution; read from the schema file in batch 1 and recorded, not assumed here. |
| **Development data** | The whole Lao slice. There is no development/holdout partition — see §3. |
| **Held-out data** | None. Deliberate deviation, recorded in §3. |
| **Project seed** | `20260921`. Component seeds derive from it by the construction in `AI-internal/skill-references/provenance-record.md`. Most of this project is not stochastic; where a model's own run is, the seed is recorded whether or not it can be set. |
| **Environment** | One main environment under `environment/`, pinned per Rule 3 in batch 2 once the analysis scripts' needs are known. It holds the Python that runs this project's own summarising and reporting scripts. The **models'** environments are the routes' business and are pinned by whatever mechanism each route uses — that mechanism is part of what is being studied. Docker: required by route A on present evidence; the daemon is started by the human. |
| **Tracking level** | **Standard** (`AGENTS.md` §6). Full tracking is not warranted for a study whose expensive object is a log file, but every route result and every computed statistic gets a provenance record. |
| **Compute budget for stability work** | One replicate per route in phase D, each a fresh isolated agent on the identical brief. If a replicate exceeds the effort of the original run by more than roughly a factor of two, it is cut and the cut is recorded. |
| **Storage budget** | Not a constraint. The Lao geojson is ~8 MB; the archived model repositories are small. |
| **Data governance** | Public and redistributable. Route A is GPL-3.0; route B's licence is unstated upstream and must be established in batch 1 before anything from it is redistributed. The Lao data's licence is established in batch 1. |
| **Scope of the tree** | The whole analysis is in `analysis/`. Nothing important happens outside it. |
| **Git remote** | Not set. The human is asked for owner/organisation and repository name before any remote is created; nothing is pushed without instruction. |

### Discovering agent brief

Identical for both routes, and the only place a route-specific value appears is the model
repository URL. A discovering agent is given, and is given nothing else:

1. The model repository URL for its route, and nothing about any other route or model.
2. That CHAP is installed on this machine as `chap` at version 2.1.0, and that its task is
   to find out how to run **this** model through CHAP and obtain an evaluation of its
   predictions.
3. The absolute paths of the three archived Lao data files, and that the evaluation is to be
   on that data.
4. The absolute path of its own node directory, and the requirement to append to
   `results/discovery_log.tsv` at the moment of each step, in the column format fixed in
   batch 2, and to write `results/discovery_notes.md` as narrative.
5. That it must not modify the model (§3), and must record rather than patch around a
   failure.
6. That it works only from public material it retrieves itself, plus the platform installed
   on the machine.

## 4b. Decisions settled during execution

Append-only, oldest first; each entry with its basis and its agency.

### 2026-09-21 — Batch 2, settled while fixing the instrument

| Decision | Basis | Agency |
|---|---|---|
| The discovery-log format is fixed before either route runs, with a closed seven-milestone vocabulary | A format settled after the first route has run is a format shaped by that route; the milestones are stated as achievements rather than as commands so that two structurally different routes are comparable | `agent-autonomous` |
| The log-summarising code lives in `04_comparison` and the route nodes hold only their raw logs | The raw log is the route's result; the statistics computed over both logs are the comparison's result. One implementation, so the two routes cannot be measured by subtly different code | `agent-autonomous` |
| Two integrity statistics (`n_distinct_timestamps`, `max_rows_sharing_one_timestamp`) are computed and asserted in tests | The plan's §3 requires contemporaneous logging, and a rule with no detector is a rule that will be honoured until it is not; a reconstructed log has a visible signature | `agent-autonomous` |
| "Confirm the Lao data loads into CHAP" was dropped from batch 2 | Doing it requires learning how CHAP wants a dataset presented, which is part of what each route's agent must discover; the orchestrator learning it first is exactly the contamination §3 forbids. Structural well-formedness was established in batch 1 from the files themselves | `agent-autonomous` |
| `summarise_discovery.py` is written in batch 2 but wired into `run.sh` in batch 5 | There are no logs until batches 3 and 4; a script failing on absent inputs would break the property that `analysis/run.sh` runs end to end | `agent-autonomous` |
| Docker Desktop 27.4.0 confirmed running; route A is unblocked | Started by the human after the anchors were pinned | `human-set` |

### 2026-09-21 — Batch 1, settled while pinning the anchors

| Decision | Basis | Agency |
|---|---|---|
| The analysis environment is pinned in batch 1, not batch 2 | Node scripts run under `environment/env/bin/python`, and batch 1 has a node script; the environment cannot be deferred past the first node | `agent-autonomous` |
| The pinned environment declares no dependencies (stdlib-only Python 3.13.0) | This project's own scripts read CSV and JSON logs and count over them; declaring libraries not yet needed would pin a fiction. Re-pinned with a §4b entry the first time a node needs one | `agent-autonomous` |
| The archived model clones have their `.git` directories removed, with the commit written to `git-metadata.txt` | A nested repository inside `Archive/` is invisible to this repository's version control, so the archived copy would not in fact be versioned here | `agent-autonomous` |
| The three schema/data discrepancies in the Lao dataset are recorded, not repaired | How each route copes with an inconsistent schema and a gappy target is part of what is being measured; repairing them would remove the thing being observed, and would change the panel both routes are compared on | `agent-autonomous` |
| The licence gap on `minimalist_example_uv` and on `dhis2/climate-health-data` blocks release, not analysis, and is referred to the human | Neither declares a licence; redistribution of the archived copies is not established | `agent-on-human-assessment` (pending the human's decision) |

### 2026-09-21 — Framing and the four setup questions

| Decision | Basis | Agency |
|---|---|---|
| The research object is the usability of the two integration routes, not the models' predictive performance | The human's aim is a comparison of how each is found out about and carried out; differences in predictive results are explicitly out of scope for the comparative report | `human-set` |
| Each route's discovery is done by a separate isolated agent | Otherwise the second route is discovered by an agent that already learned CHAP from the first, and "which was easier to find out about" is unmeasurable | `human-set` (chosen from options put by the agent) |
| The Docker daemon is started by the human when route A needs it | The daemon was down at planning time; route A ships a `Dockerfile` and `compose.yml` | `human-set` |
| No sealed holdout; the deviation is recorded in §3 | Nothing is tuned or selected on the data, so the rule protects against a risk this project does not run | `human-set` (chosen from options put by the agent) |
| Both model repositories and the Lao data directory were confirmed to exist and their top-level file listings read, before planning | Needed to put well-formed options to the human; recorded because it is prior exposure the orchestrator has and the discovering agents will not | `agent-retrieved` |

## 5. How this plan is used

This plan is edited as it runs: §6 is the live batch ledger, and sketched phases become
concrete batches as they are reached. The plan as it stands before the first batch is
archived to `Archive/plan-as-delivered/` so later drift is measurable. A request that
arrives outside the plan still gets a ledger row and a §4b entry (`AGENTS.md` §8).

## 6. Batch ledger

| Batch | Phase | Aim | Status |
|---|---|---|---|
| 1 | A — Orient & set up | Read `readme-at-start.md`, `AGENTS.md`, `MOTIVATION.md`. Pin and archive the three anchors: CHAP's installed version and install metadata; both model repositories at a named commit; the Lao data files with `sha256sums.txt`. Establish each one's licence. Read the Lao schema and record the target and resolution. Write the root `analysis/claim.md` and the tree's top level. Raise what is still open. No model is run. | done |
| 2 | A (cont.) | Fix the `discovery_log.tsv` column format and write the log-summarising script and its test, so both routes log into the same shape. Confirm the Lao data loads and is well-formed, without running any model. Confirm the Docker daemon state and record it. | done |
| 3 | B — Route A | Node `analysis/02_routeA_chapkit`. An isolated agent, on the §4 brief, discovers how to run `chapkit_ghr_model` through CHAP and obtains an evaluation on the Lao data, logging contemporaneously. The orchestrator stores the returned logs and results, writes provenance including a contamination note, and does not correct the route's findings. | open |
| 4 | B — Route B | Node `analysis/03_routeB_mlproject`. The same, for `minimalist_example_uv`, by a second isolated agent that knows nothing of batch 3. | open |
| 5 | C — Per-route reports | For each route, a report with (a) resources used, (b) the process of finding out, (c) the working invocation, (d) the results obtained — every count in (a)–(b) read from the summarising script's output file, every result in (d) read from the file CHAP wrote. | open |
| 6 | C (cont.) — Comparative report | Route A against route B on (a), (b) and (c), with (d) reported per route and not compared. Emphasis on which was easier to find out about and which was easier to carry out, with the evidence for each statement and an explicit statement of what one run per route can and cannot resolve. | open |
| 7 | D — Stability | One replicate per route, fresh isolated agents on the identical brief, reported as a distribution over the effort measures rather than as a single number. Perturbations considered and not run are recorded with why. Cut at the §4 budget. | open |
| 8 | F — Claims & report | Build the claim collection from the tree (`/claims`); generate the hierarchical report (`/hierarchical-report`); `/validate invariants`, `/validate cleanroom`, `/validate outsider`; fix what they find. | open |
| 9 | F — Release | Write the manuscript section(s) this project supports; run the release scan; ask the human for the remote; push only on instruction. | open |

## Batch ledger — reports

*(One link per completed batch, added by `/do`. Never overwritten.)*

### Iteration 1

- [[26-09-21_b01_anchors]]

### Iteration 2

- [[26-09-21_b02_instrument]]
