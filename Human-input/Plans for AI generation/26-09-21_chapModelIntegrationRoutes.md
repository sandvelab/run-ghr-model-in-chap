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
- **Run-to-run variability in the scores is accepted, not controlled for** (human-set,
  2026-09-21). A route whose model does not reproduce its numbers exactly is still a route
  that works. Variability is therefore characterised — how much do the numbers move when the
  same invocation is run again — and reported as a property of the route, and it is never a
  caveat that qualifies whether the route runs. The question a route has to answer is **does
  it run, again, from clean**, not does it produce the same number twice.

**The aim is to conclude, and the conclusion may be an uncertain call.** "Both routes were
about equally hard, and the difference is within what one agent's run can resolve" is a
conclusion. If a route does not reach an evaluation at all, that is reported plainly as its
result, with where it stopped and what it would have needed.

## 2b. What this project must end with

The project is not finished when both routes have run. It ends with **one overview document**
under `AI-generated/overview/`, the project's single entry point, saying what was asked, what
came out and where the detail is. Beyond that narrative it carries two things a reader can act
on without opening anything else:

1. **A from-scratch recipe per route.** For each route, a short literal sequence of Unix
   commands that a reader can paste into a **fresh terminal on a machine holding none of this
   project's state** and end up with a completed CHAP evaluation of that route's model on the
   Lao data. It starts from installing or verifying the platform and obtaining the model and
   the data; it assumes no environment variable, no working directory, no pre-built container
   image and no cached artefact that the commands do not themselves create. Each recipe is
   stored as an executable script in its route's node under `scripts/`, is **verified by being
   run in a clean shell** rather than assembled from the discovery log afterwards, and the
   overview both embeds it and links to it. A recipe that has not been run is not a recipe.
2. **The evaluation each route produced.** Each route runs CHAP's own default evaluation
   entry point — `chap eval`, plus whatever further step that route discovers is needed to
   turn what it writes into figures and metrics — and keeps everything it produces, in
   particular the default predicted-versus-observed plot. **At least one of those figures is
   embedded in the overview**, and the overview links to the full evaluation output file for
   **each** of the two routes. The figures are shown as products of their routes; consistent
   with §2 the predictions themselves are still **not compared across routes**.

Both routes owe a recipe and an evaluation. If a route cannot produce one, the overview says
so plainly in the place it would have gone, and says where the route stopped and what it would
have needed. That is a result, not a gap to be left out quietly.

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
- **Exact reproducibility of scores is not required of a route** (human-set, 2026-09-21).
  Determinism is not a condition of success and its absence is not reported as a weakness. It
  remains recorded: a route that varies is described by its spread rather than by one number,
  and a claim that quotes a score quotes the spread.
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
| **Evaluation platform or harness** | CHAP, `chap-core` **2.3.1**, installed on this machine as a `uv` tool and invoked as `chap`. Batch 1 archives the resolved version and install metadata under `Archive/platform-chap/` with `provenance.md`, and records the resolved `chapkit` and `servicekit` versions explicitly — `chap-core` does not pin `chapkit` tightly in every release, so the version of `chap-core` alone does not determine what a chapkit model service is talking to. What CHAP does with a model is the object of study and is **not** pre-specified here. Agency: `human-set` (platform and version), `agent-retrieved` (the resolved dependency versions). |
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
2. That CHAP is installed on this machine as `chap` at version 2.3.1, and that its task is
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
7. That it must reach CHAP's **default** evaluation output for this model and keep every file
   that produces — metrics and the default predicted-versus-observed plot included — under
   `results/`, finding out for itself what further step beyond `chap eval`, if any, that
   takes (§2b.2).
8. That it must leave behind, at `scripts/run_route.sh`, a script that reproduces its route
   from nothing on a machine holding none of this project's state, and must **run that script
   in a clean shell** and record the outcome rather than writing it from memory at the end
   (§2b.1).

## 4b. Decisions settled during execution

Append-only, oldest first; each entry with its basis and its agency.

### 2026-09-26 — Batch 12, outside the plan: route A again, on the upgraded chapkit

| Decision | Basis | Agency |
|---|---|---|
| **Route A is re-discovered from nothing, re-costed for batch 10's two personas, and compared with iteration 2's route A** — in node `analysis/09_routeA_iteration3` | The human asked for it after chapkit was upgraded. Between iteration 2 and now, chapkit 2.1.1 and 2.1.2 were released (23 and 25 September), and the route A model gained three commits, one titled "require chapkit 2.1 so chap-core model configurations are applied" | `human-set` |
| This is **iteration 3, route A only**, and unlike iteration 2 it **is** compared with its predecessor | The human asked what is different from last time, so the comparison is the point. What stays uncompared is iteration 1, and route B is not re-run | `human-set` (the comparison); `agent-autonomous` (the scope) |
| The route A model is **re-pinned to `a9532c7`** (v0.1.2) and archived at `Archive/model-route-a-it3/`; iteration 2's pin stays where it was | Put to the human with the alternative of keeping `60b16a2`. Upstream's latest commit is the model as published now, and the old image carries chapkit 2.0.0 inside it, so keeping it would test only half of the upgrade | `human-set` |
| The platform is recorded as found — `chap-core` 2.3.1 resolving `chapkit` 2.1.2 — at `Archive/platform-chap-it3/`. **25 packages** differ from iteration 2's freeze, including `cyclopts` 4.25.3 → 5.0.0 | The upgrade reinstalled the tool environment. Any difference in route A therefore belongs to the whole refreshed platform plus the new model, not to chapkit alone, and that is said wherever the difference is reported | `agent-retrieved` |
| **The Docker build is made fully cold**: route A's two tagged images are removed and the BuildKit cache pruned before the agent starts. Unrelated images are left alone | Batch 10 left the cold build as an unmeasured, excluded term. Put to the human, who chose it over the batch-3 starting state (images removed, cache warm). As a result the two iterations' build times are **not** like for like, and this is stated in the comparison | `human-set` |
| The orchestrator started Docker Desktop, which the plan otherwise leaves to the human | Asked and permitted for this batch only | `human-set` |
| The discovering agent gets the §4 brief **verbatim**, as batch 3's did, with the same override of `CLAUDE.md` and the same closed reading list. The only substitutions are the node path and the model repository URL (which is the same) | The comparison with iteration 2 is only meaningful if the brief is fixed. The agent is told nothing about iteration 1 or 2 | `agent-autonomous` |
| **Time and tokens are recorded from two sources, kept apart**: the discovery log's own timestamps (as in iteration 2) and the harness's usage report for the agent (total tokens, tool calls, wall-clock), written to a file as reported | The human asked for tokens. No earlier batch recorded tokens, so there is **no token figure for iteration 2 to compare against**, and the comparison says so rather than estimating one | `agent-autonomous` |
| The discovering agent runs on **Claude Opus 5.5** (`claude-opus-5-5`), the model of the orchestrating session | Batch 3's agent is recorded only as "Claude Opus", with no version. A change of model is therefore a confound that cannot be ruled out, and is named as one | `agent-retrieved` |
| Batch 10's human-cost model is re-used with **every authored rate unchanged**; only the act sequence (`steps.tsv`) and the divergence anchors are re-authored for the new log, and the measured inputs are re-measured from the new archive | A difference in the human estimate should come from the route, not from re-tuning the model. The new step mapping is the one authored input that cannot be carried over | `agent-autonomous` |

### 2026-09-23 — The remote, corrected: it exists, it is public, and it is this project's own

| Decision | Basis | Agency |
|---|---|---|
| **`origin` is `github.com/sandvelab/run-ghr-model-in-chap`, it is public, and it is this project's repository** | The human confirms it. Three places in this repository said otherwise — `readme-at-start.md` recorded *Git remote: not set* and, separately, that `origin` pointed at the starting-point template *with nothing pushed*; the entry above from earlier the same day recorded the decision that nothing would be pushed to `origin` as it stood. All three were wrong by the time they were read: the remote is not a template (`isTemplate: false`), it is named for this project, and it already carried the full history through commit `4d11398`, pushed at 14:43 UTC on 2026-09-23 | `human-set` |
| The earlier entry is **superseded, not edited** | §4b is append-only, and the earlier decision was a real decision that was true when it was taken. What is recorded here is that it stopped being true, and when | `agent-autonomous` |
| **That the record went stale silently is itself recorded** | The repository was published, and its own front-door file went on saying it had not been, through a working session and eleven batch reports. Nothing failed and nothing looked wrong — which is the failure mode `AGENTS.md` §5 exists for, arriving in the one file no automated check reads. `/validate invariants` checks the tree, the hashes and the git state; it does not check whether prose about the project is true | `agent-autonomous` |
| **The release scan becomes a per-push obligation, not a one-off before an imagined first publication** | Rule 10 was written for a repository that becomes public once. This one already is, and every push is a publication. The three commits pushed in this session were scanned for credentials, keys, absolute home paths and the human's email address before going out, and were clean; that is now the standing expectation rather than a courtesy | `agent-autonomous` |

### 2026-09-23 — Batch 10, outside the plan: what each route would cost a *human*

| Decision | Basis | Agency |
|---|---|---|
| **The project estimates, for two named personas, the time and the prior knowledge each route demands of a human following it to a default CHAP evaluation** | The human asked for it. Everything measured so far is agent effort, and agent minutes do not convert: route A's 13.0 minutes to evaluation contains a ~6.8-minute evaluation the machine spent, and an agent reads a README in seconds. The question a reader of this study will actually have — can *I* do this, and what will it cost me — is not answered anywhere in the tree | `human-set` |
| The estimate is a **model over measured structure**, and is labelled as such everywhere it appears | No human has been timed on either route. What the discovery logs hold is the *sequence of acts*, which is route-intrinsic and transfers; what they do not hold is any human's pace. Presenting modelled minutes as if they were measured would be the exact failure `AGENTS.md` §1 exists to prevent | `agent-autonomous` |
| Three of the model's inputs are **measured**, and the rest are **authored** | Measured: document lengths in words, counted from `Archive/` and from the installed `chap-core`; machine wait times, computed from the discovery logs' own timestamps; and the act sequence itself, taken from the normalised discovery window. Authored: the per-act times, the persona knowledge sets and the divergence rules. The split is written to a file per category so a reader can replace the authored half without touching the measured half | `agent-autonomous` |
| Scope is **defaults only**: from first document opened to first completed evaluation | The human set it. Configuration is excluded, so the batch-8b and 8c findings play no part here. This is exactly the normalised discovery window (`04_comparison/01_effort/b_normalised`), 27 route-A steps and 22 route-B steps, which means the human estimate is built on the same window as the agent effort figures and the two are comparable in structure if not in units | `human-set` (the scope); `agent-autonomous` (the mapping to the normalised window) |
| Two personas, both reported, **neither a main path** | The human named them: (a) a software engineer a few years past a CS degree, fluent with Docker, programming and software engineering practice; (b) a statistician with basic programming, no advanced software engineering. They are conditions of one analysis, not competing readings of it, so they are parameters rather than an alternatives fork | `human-set` (the personas); `agent-autonomous` (that they are parameters, not a fork) |
| A human's path is **not** the agent's path, and the differences are stated as named rules rather than written into the narrative | The logs record what an agent did with the knowledge an agent had. Where a persona lacks a prerequisite the agent silently held, the path changes shape — most sharply at route A's undiscoverable GeoJSON convention, which route A's agent found by reading installed library source, and which a persona who would not open library source meets as a failure instead. Each such divergence is one row in a rules file, applied by the script, so the human path can be audited against the agent path line by line | `agent-autonomous` |
| **Cognitive struggle is given a computable definition** rather than an adjective | "Hard" is not a finding. What the model can compute is the share of a persona's total time spent *not following instructions* — diagnosing blockers and acquiring missing prerequisites — plus the count of load-bearing prerequisites the persona does not hold. Both come out of the same walkthrough file as the minutes | `agent-autonomous` |
| The cold Docker image build for route A is a **stated unknown**, not an estimate dressed as a measurement | This repository has never measured it: every build it logged ran against a warm layer cache (8 of 8 layers `CACHED` in the verification run). The route-A totals therefore carry an explicitly separated build term with a range and a note that nothing in this tree grounds it | `agent-autonomous` |

### 2026-09-23 — The model behind the discovery agents, recorded late

| Decision | Basis | Agency |
|---|---|---|
| **Batches 3 and 4 were run on Claude Opus**, and this is now recorded | The human states it. Until now no file in this repository named the model, version or effort setting behind the two discovering agents, while the study's headline effort figures — 13.0 and 4.8 minutes, 5:4 resources, 3:2 dead ends — are all attributed to "an agent". For a project whose method is part of its result (`AGENTS.md` §3, Rule 4), that was a gap in the method record, not a detail | `human-set` |
| It is recorded as the human's statement, without a version or effort setting | Neither is recoverable from any file here, and inventing the precision would be worse than the gap. What a later reader gets is the model family and who said so | `agent-autonomous` |

### 2026-09-23 — The licence question, settled by the human

| Decision | Basis | Agency |
|---|---|---|
| **Redistribution of the three archived resources that declare no licence is established as permitted**, and they stay in the repository as fetched | The human states they have checked it. This unblocks release, which has been blocked on this point since batch 1. The three are `dhis2-chap/minimalist_example_uv`, `dhis2/climate-health-data` (`lao/`), and `zlilu/minimal_template_example`; the fourth, `chap-models/chapkit_ghr_model`, is GPL-3.0 and was never in question | `human-set` |
| The basis is recorded as the human's assessment rather than as a licence found in the repositories | None of the three repositories carries a licence file, and this project did not establish permission from any document it can cite. What is recorded is therefore *who* decided and *when*, not a licence — so a later reader can see exactly what the claim rests on | `agent-autonomous` |
| Nothing is pushed to `origin` as it stands | `origin` is the starting-point template repository this vault was copied from, and it is public. The human has asked for a new repository to be named instead. §4 requires the owner and name to come from the human and forbids inferring either | `human-set` |

### 2026-09-23 — The overview is reordered around its own finding

| Decision | Basis | Agency |
|---|---|---|
| The overview's bottom line leads with the configuration finding, not with the effort counts | The human asked whether it was visible, and it was not: the headline buried it in a subordinate clause, the third case sat below the table as an afterthought, and the loud-versus-silent contrast — the sharpest result here — first appeared a hundred lines down. A front door that does not state the finding is not a front door | `human-set` (the question); `agent-on-human-assessment` (the reordering) |
| Version 4's status block **narrated the process** — what an earlier version "argued from source" — and that is removed rather than kept | `AGENTS.md` §7 forbids it explicitly: the reader never saw our iterations, and what changed belongs in this plan and in the chat reply, never in the document. The rule was broken and the fix is a new version, not an edit | `agent-autonomous` |
| The correction is a new version, not an edit to version 4 | `AGENTS.md` §1: a produced file is never edited. For a hand-written document a new version is what a re-run is for a result, and the superseded wording stays visible | `agent-autonomous` |
| Five versions in one day is recorded as a cost | Each is kept and none is pruned, so the overview folder now holds more history than finding. Worth raising with the human rather than resolving silently | `agent-autonomous` |

### 2026-09-23 — Batch 8c, outside the plan: a third case, to test configuration delivery

The human named `zlilu/minimal_template_example` and asked whether a configuration could be
passed to it, since that is what route A could not do.

| Decision | Basis | Agency |
|---|---|---|
| A third model is archived and run, as a **case** and not as a third route | Neither existing model can answer the question: route A's declares eighteen options that never arrive, route B's declares none at all. Without a model that both declares an option and can be seen to receive it, "the MLproject mechanism delivers configuration" rests on reading chap-core's source rather than on evidence | `human-set` (the repository); `agent-on-human-assessment` (that it enters as a case) |
| It is **not compared with route A or route B** on effort or on predictions | It was not discovered by an isolated agent on the §4 brief, so it has no admissible discovery log, and its scores answer a different question. Putting it in the comparison table would silently mix a measured route with an unmeasured one | `agent-autonomous` |
| The evidence of delivery is `model_configuration_for_run.yaml`, the file CHAP writes into the model's run directory | The model prints the configuration it receives, which was the first plan, but CHAP does not forward a subprocess's stdout at default verbosity. The file CHAP wrote is better evidence than the model's report of it, and it is what the model actually reads | `agent-autonomous` |
| Three widely separated `alpha` values, not a sweep | The question is whether a value arrives and does something, not which value is best. Five orders of magnitude cannot be confused with noise, and §3 forbids selecting between configurations on Lao scores in any case | `agent-autonomous` |
| A fourth run is made in the shape `chap model schema --example` emits, **expecting it to fail**, and the failure is kept | It is the comparison that matters. The same class of disagreement that produces a silent, complete, wrongly-configured evaluation on chapkit produces a halted run and a named cause on MLproject. Reporting only the runs that worked would have hidden the more useful half | `agent-autonomous` |
| The model is run in a temporary directory outside the repository | CHAP copies an MLproject model into `runs/<timestamp>/` and builds a `uv` environment there — about 800 MB per run, including scipy's test fixtures. The first attempt put that under `results/`, and `/validate invariants` correctly reported two dozen unexplained figures in a results directory | `agent-autonomous` |
| The third model declares **no licence**, and this is recorded beside the other two undeclared ones | Redistribution of the archived copy is not established. Blocks release, not analysis | `agent-on-human-assessment` (pending the human's decision) |

### 2026-09-23 — MLproject configuration, and a correction to what was claimed about it

| Decision | Basis | Agency |
|---|---|---|
| The claim that an `MLproject` model "has no such surface" is **corrected**: `MLproject` templates declare `user_options` as a first-class field, and that is how a ConfiguredModel is made from a ModelTemplate | The human pointed it out, and chap-core's source confirms it — `ModelTemplateInformation.user_options`, plus `hpo_search_space` beside it. What `MLproject` lacks is a *negotiated REST payload*, not configuration. The earlier wording conflated the two | `human-set` (the correction); `agent-retrieved` (the mechanism, from chap-core's source and route B's own run directory) |
| The correction is made in a new overview version, not by editing the batch report that carries the overstatement | A batch report is an account of a batch and is not reissued; rewriting it would destroy the record of what was claimed when. `AGENTS.md` §1 forbids editing produced files, and the overview is versioned precisely so that a superseded statement stays visible | `agent-autonomous` |
| The configuration comparison is grounded in each mechanism's own artefacts rather than in effort counts | `model_configuration_for_run.yaml` in route B's run directory, `user_options` in the MLproject schema, route A's README option table and its `example_data/config.yml`, and the eight-endpoint contract surface. The two mechanisms differ in kind, and counting commands would not have shown it | `agent-autonomous` |
| Route A's model is reported as **well documented and correctly implemented**, with the defect located in chap-core's REST bridge | Its README carries all 18 options with the R-INLA latent models explained, and its `example_data/config.yml` states it is "in the flat layout chapkit's ShellModelRunner writes". The model implements chapkit's file convention; `chap eval` uses the REST one. Neither document is wrong, and saying the model is at fault would be | `agent-on-human-assessment` |
| Version 3 is executive length, with the detail moved to an appendix of pointers | The human asked for it. A front door that takes twenty minutes to read is not a front door | `human-set` |

### 2026-09-22 — Batch 8b, outside the plan: is route A's model configurable at all?

The human asked whether several configurations of route A's model could be run on this data,
and for the prediction results of each. Settled while doing it.

| Decision | Basis | Agency |
|---|---|---|
| The work is done, and is framed as **a property of the route** — can an operator configure this model through CHAP — rather than as model selection | §3 stops the work if a batch "begins choosing between model configurations on the basis of Lao scores", because that would void the no-holdout deviation. Asking whether a setting reaches the model at all is a question about the integration route, which is what this project studies. The human was told the distinction before the batch ran | `human-set` (that it is done); `agent-on-human-assessment` (the framing that keeps §3 intact) |
| **No best configuration is chosen and none is recommended.** Each variant's scores are reported descriptively, beside the control, and the report says in the same breath that they do not license a choice | The moment a variant is picked because its Lao MAE is lowest, this project has selected on the data it reports on, with no holdout to catch it. Reporting the spread is not selecting | `agent-autonomous` |
| A reverse proxy, `config_proxy.py`, is interposed to flatten the configuration payload | Established by direct test: chap-core's `ModelConfiguration` is `extra="forbid"` with two fields, so it will only send values **nested** under `user_option_values`; the model's service stores a **flat** mapping, returns HTTP 201 for the nested one, fills its own defaults and fits with them. The one shape CHAP will send is the one the model discards, so without something interposed there is no configured run to report. Neither the model nor CHAP is modified | `agent-autonomous` |
| Each variant changes **one** option from the model's published defaults, and the control sets those defaults explicitly | One factor at a time is what makes a difference attributable. The control travels the identical path through the proxy, so it controls for the proxy as well as for the data | `agent-autonomous` |
| Every variant records the **model formula it actually fitted**, and that is the evidence the configuration took effect | A configured run of this model is indistinguishable from an unconfigured one by its outputs: both write a valid NetCDF and real metrics. Scores alone cannot tell you whether a setting was applied, so the claim rests on what the model fitted, not on what moved | `agent-autonomous` |
| The node is in the tree and `analysis/run.sh` therefore costs about thirty minutes more | It is an analytical result and belongs where results live. The cost is stated rather than avoided by parking the work outside the tree | `agent-autonomous` |

### 2026-09-22 — Iteration 2: the same plan, re-run against an upgraded platform

| Decision | Basis | Agency |
|---|---|---|
| The whole of iteration 1 is frozen to `Archive/version_1_old_chapcore/`, the live tree emptied, and this plan re-run from batch 1 | The human's instruction. Iteration 1 ran on `chap-core` 2.1.0, whose environment had resolved `chapkit` 1.1.0, and route A's central result — that it does not run as published — is a property of that resolved pair rather than of the chapkit mechanism. Re-running is the only way to find out what the two routes cost on a current platform | `human-set` |
| The platform anchor is re-pinned to `chap-core` **2.3.1**, resolving `chapkit` 2.1.0 and `servicekit` 2.0.2, already installed on the machine when iteration 2 began | It is the current release, and it is the first `chap-core` whose requirement is `chapkit>=2.1.0,<3`; 2.2.0 and 2.3.0 both cap `chapkit<2` | `human-set` |
| The data anchor and both model anchors are **not** re-fetched: they stay at the commits iteration 1 pinned | The platform is meant to be the only anchor that differs between the two iterations. Re-fetching risks the upstream repositories having moved and would confound a difference in route cost with a difference in the model or the data | `agent-autonomous` |
| Iteration 1's findings are given to neither discovering agent, are read by none of iteration 2's reports, and the new overview makes **no** before/after comparison with iteration 1 | §3's contamination rule applies between iterations as it does between routes: an agent told that route A failed last time is not discovering route A. The human chose additionally that the overview stand alone, so iteration 2 is an independent measurement rather than half of a pair | `human-set` (that the overview stands alone); `agent-on-human-assessment` (extending §3 across iterations) |
| The route A container image left on disk by iteration 1 was deleted before batch 3 | An image already built is ~22 minutes of route A's cost not paid, and §2b.1 requires a recipe verified from nothing. Measuring route A against a warm cache would understate it and would leave the recipe's build path untested | `human-set` |
| **The orchestrating agent is contaminated for iteration 2** — it knows both routes' iteration-1 findings in full — and this is recorded rather than worked around | §3 anticipates unavoidable orchestrator exposure and requires a contamination note instead of a pretence. The mitigation is that each discovering agent is a fresh agent given the §4 brief verbatim and nothing else, so the discovery itself is uncontaminated; what the orchestrator cannot certify is that its own choices about what to hand over carried nothing extra. The note goes in both route provenance records | `agent-autonomous` |
| The two discovering agents are run **one after the other**, not concurrently | Running them at the same time on one machine makes them contend for it, and the elapsed-minute figures then measure the contention as much as the route. Counts remain the primary measure either way; running sequentially costs wall-clock, which this plan does not budget, and buys an elapsed figure that can actually be read | `agent-autonomous` |
| Both agents log through one shared implementation, `AI-internal/useful-scripts/log_step.py`, which stamps each row with the current UTC second and refuses a row the format does not allow | A logging helper written per route is two dialects of the instrument. Refusing a malformed row at the moment it is written is the only point at which it can still be corrected; `summarise_discovery.py` rejects the whole log, and discovering that at the end of a route is discovering it too late | `agent-autonomous` |
| The discovering agents are told explicitly that `CLAUDE.md`'s instruction to read `readme-at-start.md` is overridden for their task, and are given a closed list of three things they may read inside the repository | `readme-at-start.md` names both models and states what each route cost; an agent following the repository's own standing instruction would be contaminated before it began, and would not know it. This is the one place where the repository's own method and the plan's §3 actively conflict, and §3 wins | `agent-autonomous` |
| A git remote **is** configured — `origin` at `sandvelab/agentic-model-development-start`, the starting-point template this repository was copied from — although §4 records the remote as not set, and the branch is ahead of it. Nothing is pushed, and the human is asked before anything is | §4 says the human is asked for owner and repository before any remote is created, and this one was not created by that route: it is the template's own origin, inherited by the copy. Pushing would put this project's content, including archived data whose licence is not established, into the template repository | `agent-autonomous` (recording it); referred to the human |
| The project now ends with one overview carrying, per route, a from-scratch recipe verified in a clean shell and the route's default CHAP evaluation with at least one figure embedded — the new §2b | The human's instruction. Iteration 1's overview said what the routes cost but left a reader who wanted to run one themselves to reconstruct the commands from a discovery log, and reported metrics without ever showing what the models predicted | `human-set` |

### 2026-09-22 — An overview document, requested outside the plan

| Decision | Basis | Agency |
|---|---|---|
| The project gets one overview document, at `AI-generated/overview/`, linked from `readme-at-start.md` as the designated first read | Asked for by the human: the batch reports and the hierarchical report between them answered every question except "where do I start". The hierarchical report is a navigator, not a narrative | `human-set` |
| It is numbered as a version and superseded rather than edited, with old versions kept | The human asked for it to be marked as version 1 and expected to change; and a front door that is quietly rewritten leaves no record of what it said when a reader last used it | `human-set` |
| Exactly one overview, which points at the other documents rather than restating them | `AGENTS.md` §9 rules out accumulating parallel summaries of the same material, and a second overview is how that starts | `agent-on-human-assessment` |
| It is written under the current framing even though the batch reports it draws on were written under the previous one, and says so in its status block | The alternative — rewriting the batch reports — would destroy the record of what was reported when. A batch report is an account of a batch and is not reissued | `agent-autonomous` |

### 2026-09-21 — Reframing: variability accepted, the question is whether both routes run

| Decision | Basis | Agency |
|---|---|---|
| Run-to-run variability in the scores is accepted and embraced; it is no longer a caveat on whether a route works | The human's instruction: a route that produces slightly different numbers each time is still a working route, and the project's question is ease of getting a model up and running | `human-set` |
| §2 gains a clause and §3 gains a non-negotiable saying exactly this, so a later session cannot quietly reinstate a determinism requirement | A reframing that lives only in a report is a reframing that lasts until the next batch | `agent-on-human-assessment` |
| Phase D changes from "one replicate discovery agent per route" to "re-run each route's own script from clean" | The replicate agents would have sharpened the *effort measurement*; the question is now whether the routes run, which a re-run answers directly and much more cheaply | `agent-on-human-assessment` |
| The re-run is allowed to overwrite each route's stored evaluation, which the previous iteration deliberately prevented | Under the previous framing the reports quoted point scores that a re-run would invalidate; under this one they quote spreads, so a fresh run adds evidence instead of destroying it. The prior scores are snapshotted into the repeatability node first, so nothing is lost | `agent-on-human-assessment` |

### 2026-09-21 — Batches 3-6, settled while running and comparing the routes

| Decision | Basis | Agency |
|---|---|---|
| Route A is reported as **not having run as published**; the interposed `info_shim.py` is a finding, not a detail | chap-core 2.1.0 pins chapkit 1.1.0 (`extra="forbid"`) and the model is built on chapkit 2.0.0; the route completes only with three keys stripped from one response. Reporting it as "ran" would hide the result | `agent-autonomous` |
| chapkit was **not** upgraded inside chap-core's virtual environment, although it would probably have removed the need for the shim | That changes the platform under test, and the incompatibility is itself the finding | `agent-autonomous` |
| Both of route A's runs are kept, and its scores are not quoted beyond two significant figures | Two identical invocations gave MAE 130.00 and 133.28: R-INLA is not bit-reproducible, as the model's own README states, so one run would overstate precision | `agent-autonomous` |
| The differing codings between the two logs become an **alternatives node**, not an edit to the logs and not a hand-curated row correction | A per-row correction would depend on which rows a reader noticed and would constrain no future log; two rules applied to both logs alike can be argued with. The logs are never edited (`AGENTS.md` §1) | `agent-autonomous` |
| `b_normalised` is the main path | The question is a comparison, and the normalisation is what makes two differently-coded logs comparable; `a_asLogged` stays runnable as the only purely observational reading | `agent-autonomous` |
| `build_comparison.py` reads only the main path's effort file | `analysis/run.sh` follows the main path at every fork, so a table naming a non-main alternative's output would name a file a full reproduction never regenerates | `agent-autonomous` |
| A full `analysis/run.sh` was started and stopped after about two minutes; the three route-A log files it had begun overwriting were restored from the last commit | An end-to-end run re-fits route A with INLA, which is not bit-reproducible, so it would have silently replaced the numbers the reports cite with slightly different ones. A clean full reproduction needs to be a deliberate act with its outputs compared rather than overwritten, which is phase D's business | `agent-autonomous` |

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

### Iteration 2 — `chap-core` 2.3.1 (live)

| Batch | Phase | Aim | Status |
|---|---|---|---|
| 1 | A — Orient & set up | Read `readme-at-start.md`, `AGENTS.md`, `MOTIVATION.md`. Re-pin and archive the platform anchor: `chap --version`, the resolved `chapkit`/`servicekit` versions, the install metadata and the dependency freeze, under `Archive/platform-chap/` with `provenance.md`. Confirm the data and both model anchors are present and unchanged at their pinned commits, and re-verify the data checksums. Re-read the Lao schema and record the target and resolution from the file. Write the root `analysis/claim.md` and the tree's top level. No model is run. | done |
| 2 | A (cont.) | Re-establish the instrument: the `discovery_log.tsv` column format and the log-summarising script with its test, so both routes log into the same shape and are measured by one implementation. Confirm the Docker daemon state and that no route A image is cached. | done |
| 3 | B — Route A | Node `analysis/02_routeA_chapkit`. An isolated agent, on the §4 brief verbatim, discovers how to run `chapkit_ghr_model` through CHAP, obtains its default evaluation on the Lao data, logs contemporaneously, and leaves a from-scratch `run_route.sh` it has itself run in a clean shell (§2b). The orchestrator stores what comes back, writes provenance including the contamination note of §4b, and does not correct the route's findings. | done |
| 4 | B — Route B | Node `analysis/03_routeB_mlproject`. The same, for `minimalist_example_uv`, by a second isolated agent that knows nothing of batch 3 or of iteration 1. | done |
| 5 | C — Per-route reports | Per route: (a) resources used, (b) the process of finding out, (c) the working invocation, (d) the results obtained — every count in (a)–(b) read from the summarising script's output file, every result in (d) read from the file CHAP wrote. | done |
| 6 | C (cont.) — Comparative report | Route A against route B on (a), (b) and (c), with (d) reported per route and not compared. Which was easier to find out about, which easier to carry out, the evidence for each statement, and what one run per route can and cannot resolve. | done |
| 7 | D — Repeatability | Does each route run again, from clean? Re-run each route's own `run_route.sh` end to end; record whether it completes, what it cost the second time, and how far the scores moved. Variability is characterised, not controlled for (§2, §3). This batch is also what verifies each recipe against §2b.1. | done |
| 8 | E — The overview | Write the overview document §2b specifies: the narrative, both routes' verified from-scratch recipes, and both routes' default evaluations with at least one figure embedded and the full output linked. Standing alone — no comparison with iteration 1. Wire it in from `readme-at-start.md`. | done |
| 8b | D (cont.) | **Outside the plan, at the human's request**: establish whether route A's model can be configured through CHAP at all, run several published-alternative configurations on the Lao data, and report what each fitted and what each scored — descriptively, with no configuration selected (§4b). | done |
| 8c | D (cont.) | **Outside the plan, at the human's request**: archive `zlilu/minimal_template_example` and establish whether the `MLproject` route delivers an operator's configuration to a model, which neither route A's nor route B's model can show. A case, not a third route (§4b). | done |
| 9 | F — Claims, validation & release | Build the claim collection (`/claims`); generate the hierarchical report (`/hierarchical-report`); `/validate invariants`, `/validate cleanroom`, `/validate outsider`; fix what they find. Then the manuscript section(s) this project supports, the release scan, and the human's decision on the remote. | open |
| 10 | D (cont.) | **Outside the plan, at the human's request**: estimate what each route costs a *human* who follows it to a default CHAP evaluation, for two named personas — (a) a software engineer a few years past a CS degree, fluent with Docker and software engineering practice; (b) a statistician with basic programming and no advanced software engineering. Node `analysis/08_humanCost`. Build a cost model over the normalised discovery window whose measured inputs (document lengths, machine wait times, act sequence) are separated on disk from its authored inputs (per-act times, persona knowledge sets, divergence rules); emit a step-by-step path per persona per route, totals, a prerequisite inventory, and a computed measure of cognitive struggle. Defaults only — configuration is out of scope (§4b). The result is a model over measured structure, labelled as such wherever it appears; no human has been timed. | done |
| 11 | — | **Outside the plan, at the human's request**: correct the repository's record of its own remote. `origin` is `sandvelab/run-ghr-model-in-chap`, public, this project's own repository, and already pushed — against three statements here that said the remote was unset, or a template, or unpushed. Fix `readme-at-start.md`, supersede the earlier §4b decision rather than editing it, and record that the release scan is owed on every push. No analysis. | done |
| 12 | D (cont.) | **Outside the plan, at the human's request**: iteration 3, route A only. chapkit is upgraded to 2.1.2 and the model re-pinned to `a9532c7`. A fresh isolated agent re-discovers route A on the §4 brief from a fully cold Docker state, logging contemporaneously, with its time and tokens recorded; batch 10's human-cost model re-costs the new act sequence for both personas; a comparison with iteration 2's route A on success, agent time, tokens and estimated human time. Node `analysis/09_routeA_iteration3` (§4b). | open |

### Iteration 1 — `chap-core` 2.1.0 (complete, archived to `Archive/version_1_old_chapcore/`)

Kept for the record of what was run and in what order. Its outputs are not in the live tree
and are not read by iteration 2.

| Batch | Phase | Aim | Status |
|---|---|---|---|
| 1 | A — Orient & set up | Read `readme-at-start.md`, `AGENTS.md`, `MOTIVATION.md`. Pin and archive the three anchors: CHAP's installed version and install metadata; both model repositories at a named commit; the Lao data files with `sha256sums.txt`. Establish each one's licence. Read the Lao schema and record the target and resolution. Write the root `analysis/claim.md` and the tree's top level. Raise what is still open. No model is run. | done |
| 2 | A (cont.) | Fix the `discovery_log.tsv` column format and write the log-summarising script and its test, so both routes log into the same shape. Confirm the Lao data loads and is well-formed, without running any model. Confirm the Docker daemon state and record it. | done |
| 3 | B — Route A | Node `analysis/02_routeA_chapkit`. An isolated agent, on the §4 brief, discovers how to run `chapkit_ghr_model` through CHAP and obtains an evaluation on the Lao data, logging contemporaneously. The orchestrator stores the returned logs and results, writes provenance including a contamination note, and does not correct the route's findings. | done |
| 4 | B — Route B | Node `analysis/03_routeB_mlproject`. The same, for `minimalist_example_uv`, by a second isolated agent that knows nothing of batch 3. | done |
| 5 | C — Per-route reports | For each route, a report with (a) resources used, (b) the process of finding out, (c) the working invocation, (d) the results obtained — every count in (a)–(b) read from the summarising script's output file, every result in (d) read from the file CHAP wrote. | done |
| 6 | C (cont.) — Comparative report | Route A against route B on (a), (b) and (c), with (d) reported per route and not compared. Emphasis on which was easier to find out about and which was easier to carry out, with the evidence for each statement and an explicit statement of what one run per route can and cannot resolve. | done |
| 7 | D — Repeatability | **Does each route run again, from clean?** Re-run each route's own `run_route.sh` end to end and record whether it completes, what it cost the second time, and how far the scores moved. Variability is characterised, not controlled for (§2, §3). The replicate *discovery* agents originally planned here are dropped: the question is now whether the routes run, not how precisely the effort was measured. | done |
| 7b | D (cont.) | **Outside the plan, at the human's request**: write the project's single entry point — one overview saying what was asked, what came out and where the detail is — and wire it in from `readme-at-start.md`. Named as a version, because it is superseded rather than edited. | done |
| 8 | F — Claims & report | Build the claim collection from the tree (`/claims`); generate the hierarchical report (`/hierarchical-report`); `/validate invariants`, `/validate cleanroom`, `/validate outsider`; fix what they find. | open |
| 9 | F — Release | Write the manuscript section(s) this project supports; run the release scan; ask the human for the remote; push only on instruction. | open |

## Batch ledger — reports

*(One link per completed batch, added by `/do`. Never overwritten.)*

### Iteration 2 — reports

- [[26-09-22_b01_anchors]]
- [[26-09-22_b03b04_routesDiscovered]]
- [[26-09-22_b05_routeReports]]
- [[26-09-22_b06_comparativeReport]]
- [[26-09-22_overviewV1]]
- [[26-09-23_b08b_configurability]]
- [[26-09-23_overviewV2]]
- [[26-09-23_b08c_thirdCase]]
- [[26-09-23_overviewV3]]
- [[26-09-23_overviewV4]]
- [[26-09-23_overviewV5]]
- [[26-09-23_b10_humanCost]]

### Iteration 1 — reports, archived with the run

The documents these link to are under `Archive/version_1_old_chapcore/AI-generated/`.

#### `/do` run 1

- [[26-09-21_b01_anchors]]

#### `/do` run 2

- [[26-09-21_b02_instrument]]

#### `/do` run 3

- [[26-09-21_b05_routeReports]]

#### `/do` run 4

- [[26-09-21_b06_comparativeReport]]

#### `/do` run 5

- [[26-09-22_overviewV1]]
- [[26-09-23_b08b_configurability]]
- [[26-09-23_overviewV2]]
- [[26-09-23_b08c_thirdCase]]
- [[26-09-23_overviewV3]]
- [[26-09-23_overviewV4]]
- [[26-09-23_overviewV5]]
