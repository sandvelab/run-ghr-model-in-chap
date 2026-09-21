# Read this first

The first thing to read in a new session, human or agent. It says what *this particular*
project is. When it stops matching reality it is worse than nothing.

Then read `AGENTS.md` — the standing instructions, and the single source of truth for how
work is done here.

---

## The project

**Establish how discoverable and how executable CHAP's two model-integration routes are for
an agent working only from public material, by taking one published model down each route —
`chapkit_ghr_model` as a chapkit model service, `minimalist_example_uv` as an
`MLproject`/`uv` model — until each produces a CHAP evaluation on the public Lao admin-1
monthly data.** The object of study is the route, not the prediction: the models are run as
published and their predictive scores are reported per route but never compared against each
other. Full aim, success criteria and non-negotiables:
`Human-input/Plans for AI generation/26-09-21_chapModelIntegrationRoutes.md`.

## Where the project starts from

The three anchors every project here is bound to. Each is pinned, archived under `Archive/`
with a `provenance.md`, and named here so that no session has to rediscover it.

| Anchor | This project |
|---|---|
| Evaluation platform or harness | CHAP, `chap-core` 2.1.0, installed as a `uv` tool and invoked as `chap`. Archived metadata at `Archive/platform-chap/`. What CHAP does with a model is the object of study and is not pre-specified. |
| Metric | Whatever each route's own CHAP evaluation entry point writes to file. Not imposed across routes; no cross-route performance claim is made. |
| Backtest or split scheme | Route-discovered, recorded as a file in each route's `results/`. |
| Required baselines | None — the comparison is between integration routes, not between predictions. |
| Reference model | None, and neither model is a reference for the other. |
| Modelling resources to start from | Route A: `chap-models/chapkit_ghr_model` (GPL-3.0), at `Archive/model-route-a/`. Route B: `dhis2-chap/minimalist_example_uv`, at `Archive/model-route-b/`. Both pinned by commit in batch 1 and run as published. |
| Data | `dhis2/climate-health-data`, directory `lao/` — `chap_LAO_admin1_monthly.{csv,geojson}` and `..._schema.json`; pinned by commit in batch 1, at `Archive/data-lao/` with `sha256sums.txt`. |
| Target | Read from the Lao CHAP schema in batch 1; admin-1, monthly. |
| Development data | The whole Lao slice. There is no development/holdout partition. |
| Held-out data | **None — a deliberate, recorded deviation.** Nothing here is tuned or selected on the data, so a sealed holdout would guard against a risk this project does not run. The plan's §3 states the condition that voids the deviation. |

## The article

- **Target venue**: not yet decided.
- **Status**: batches 1–6 done. Both routes reached a CHAP evaluation on the Lao data, and
  route B (MLproject/uv) cost less on every effort statistic that orders — 5 dead ends to 0
  being the starkest. Route A (chapkit) **did not complete as published**: chap-core 2.1.0's
  pinned chapkit 1.1.0 rejects the chapkit 2.0.0 service's `/api/v1/info`, and the route
  completes only through an interposed proxy. Open: phase D (one replicate per route), the
  hierarchical report and clean-room validation, and the human's decision on the two
  undeclared licences.
- **Manuscript**: `Human-AI-collaboration/manuscript/` (empty).
- **The plan being executed**: `Human-input/Plans for AI generation/26-09-21_chapModelIntegrationRoutes.md`.
  It carries the batch ledger (§6); `/do` runs the next open batch and stops.

## Settings this project has fixed

| Setting | Value |
|---|---|
| Project random seed | `20260921`. Every component seed derives from it (`AI-internal/skill-references/provenance-record.md`). Most of this project is not stochastic. |
| Main environment | Pinned in batch 2: the Python that runs this project's own summarising and reporting scripts. Installed from `environment/lock.txt` by `environment/install-env.sh`; invoked as `environment/env/bin/python`. No Docker image for the analysis itself — but route A requires a container runtime, which is a property of the route and part of what is being measured. |
| Repository machinery interpreter | `.venv`, per `setup-guide.md` §3. |
| Tracking level | `standard` (`AGENTS.md` §6). |
| Compute budget for stability work | One replicate agent per route; cut if a replicate exceeds roughly twice the original run's effort, with the cut recorded. |
| Storage budget | Not a constraint. |
| Data governance | Public and redistributable; route B's and the data's licences are established in batch 1 before anything is redistributed. |
| Git remote | Not set. The human is asked for owner/repository before any remote is created; `/release` runs the secrets and data-permission scan before anything becomes public. |

## What must not happen

These override everything else here; the plan's §3 states them in full for this project.

1. **The two routes are discovered independently.** Each route's discovering agent is given
   the identical brief and told nothing about the other route or any finding from it. A
   comparison of discovery effort between two contaminated runs is worthless, and it fails
   silently.
2. **The discovery log is written as the discovery happens**, not reconstructed afterwards.
   A reconstructed log is not admissible for the effort measures.
3. **No number reaches a claim except through a file.** Every count in the reports is
   computed by a script from a log on disk and read back from that script's output.
4. **The models are not modified.** A model that does not run as published is a finding, not
   a thing to be patched.
5. **Every judgment call is a node or a logged decision, never silent**, and **agency is
   recorded on every decision**.
6. **Failures are kept**: a stalled route, a wrong documentation page, an invocation that
   never worked — all stay in the record.
