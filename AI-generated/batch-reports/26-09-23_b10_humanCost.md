# Batch 10 — what each route costs a human

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 2

Outside the plan, at the human's request. Everything this study has measured so far is agent
effort. This batch asks the question a reader will actually have — *can I do this, and what
will it cost me* — for two named personas, with configuration out of scope: both routes are
followed only as far as a CHAP evaluation on CHAP's defaults.

**Read this first: none of the minutes below were measured on a person.** What is measured is
the *structure* of each encounter — which documents were opened, which commands were run,
where the route stopped and had to be diagnosed — and that structure belongs to the route, not
to the agent that met it. The pace is authored. Measured and authored inputs are in separate
files, and the authored ones can be replaced and the whole thing re-run without touching a
measured value: `analysis/08_humanCost/scripts/inputs/`.

---

## Why agent minutes could not simply be converted

Route A's headline figure is 13.0 minutes to a written evaluation. Of that, **410 seconds are
the machine's** — the span from `evaluation_started` to `evaluation_complete` in the route's
own discovery log. Under half the figure is the agent doing anything a human would also do,
and what the agent does, it does at reading speeds no person has. The clock does not scale.

What does transfer is the act sequence. Both routes were re-walked step by step over the
normalised discovery window — 27 route-A steps and 22 route-B steps, the same window the
effort comparison uses — with each step classified, costed per persona, and gated on what the
route requires its follower to already know.

## The two personas

| | **Engineer** | **Statistician** |
|---|---|---|
| Background | A few years past a CS degree; programming and software engineering practice are daily work | Basic programming; statistics is the expertise, software engineering is not |
| Brings outright | Containers, registries, HTTP, shell and PATH, packaging, virtual environments, reading an installed library's source | The command line, inspecting a CSV, cloning a repository, JSON — **and GeoJSON, which the engineer only half knows** |
| Half-knows | Registry authentication, CPU architecture and emulation, GeoJSON | `--help` output, GitHub navigation, `uv`, where a tool writes its outputs |
| Does not have | — | Docker, compose, registries and their 401s, CPU architecture, `curl` and HTTP, the idea of a model as a running service, PATH, Python packaging, reading library source |

The personas are not a ladder. The statistician reads a GeoJSON feature collection more
comfortably than the engineer does; it is the one place the ordering reverses, and it matters,
because GeoJSON is where both routes hide their worst trap.

## Route B, step by step

**Engineer — 46 minutes expected (27 low, 99 high).**

| | Step | Expected |
|---|---|---|
| 1 | install `uv` — *not in any agent log; the agent's host already had it* | 6.0 |
| 5 | read the model README (981 words, measured) | 5.8 |
| 9 | `chap --help` and `chap eval --help` (944 words, measured) | 5.6 |
| 12 | `uv run isolated_run.py` — the model trains on its own sample data | 0.8 |
| 14–15 | **`chap sanity-check-model` crashes on a clean install** — diagnose | 7.0 |
| 19 | read installed `chap-core` source to find how the geometry is loaded | 8.3 |
| 22–23 | `chap eval`, then wait (60 s, measured) | 1.8 |

Nothing here is hard for this persona. The only real friction is a tool that fails on a
missing bundled dataset, and they read `FileNotFoundError … site-packages/example_data/` as a
packaging fault in seconds.

**Statistician — 221 minutes expected (101 low, 594 high).**

The same path, but two steps carry three-quarters of it:

| | Step | Expected | Why |
|---|---|---|---|
| 15 | `chap sanity-check-model` crashes | **80.0** | A traceback pointing into `site-packages` reads, to someone who has never packaged Python, as *I installed it wrong* — and the correct conclusion is that the tool shipped broken |
| 22+ | the run rejects the data, and **nothing says a `.geojson` must sit beside the `.csv`** | **50.0** | Not in the README, not in `--help`, not in the error. The agent found it by opening library source; this persona would not, so they meet it as a failure with nothing to diagnose it from |
| 1 | install `uv` | 26.0 | |

Route B never requires a container runtime, so none is charged — even though the discovering
agent ran `docker info`. That correction is written into the model's rules: *a prerequisite is
charged only where the route cannot proceed without it.* Before it, the model was adding 90
minutes of Docker learning to route B and inverting one of this study's own findings.

## Route A, step by step

**Engineer — 119 minutes expected (70 low, 272 high), plus the cold image build.**

| | Step | Expected |
|---|---|---|
| 1 | install a container runtime — *not in any agent log* | 6.0 |
| 5 | read the model README (2833 words, measured — three times route B's) | 32.1 |
| 6 | the host is arm64, the model is amd64-only — diagnose | 12.6 |
| 11 | read the Makefile and both compose files | 3.3 |
| 12–14 | choose the published image; **it returns 401 and is not anonymously pullable** | 19.7 |
| 16–17 | build the Dockerfile instead, and wait — **the cold build is not estimated** | 1.1 + ? |
| 20 | read installed `chap-core` source for the geometry convention | 14.5 |
| 22–24 | run the service, `curl` its health endpoint, resolve it as a model | 2.4 |
| 26–29 | `chap eval`, then wait (410 s, measured) | 7.6 |

**Statistician — 649 minutes expected (313 low, 1743 high), plus the cold image build.**

Route A asks this persona to learn seven things before it will run:

| Prerequisite | First needed at | Expected cost |
|---|---|---|
| Docker — install it, build an image, run a container, map a port | step 1, before anything | **90.0** |
| amd64 against arm64, and emulation | reading the README | 35.0 |
| diagnosing a registry 401 and concluding it is not your fault | the failed pull | 25.0 |
| compose files | the repository's own tooling | 20.0 |
| a model as a *running service* CHAP talks to over HTTP | `chap eval --help` | 20.0 |
| image registries | the Makefile | 15.0 |
| `curl` and HTTP | the health check | 15.0 |

Route B asks for one: reading a `site-packages` traceback as a packaging fault.

## Summary

Every figure from `analysis/08_humanCost/results/summary.tsv`. Minutes, expected, with the
low–high band.

| | **Route A — chapkit** | **Route B — MLproject** | A ÷ B |
|---|---|---|---|
| **Engineer** | **119** (70–272) | **46** (27–99) | 2.6 |
| **Statistician** | **649** (313–1743) | **221** (101–594) | 2.9 |
| Statistician ÷ engineer | 5.5 | 4.8 | |
| — of which the machine's own waiting | 6.8 | 1.0 | |
| — of which arm64 hosts only | 12.6 / 60.0 | 0 | |
| — cold image build | **excluded, additive** | none | |

**The persona matters more than the route.** Changing route moves the estimate by 2.6–2.9×.
Changing who is holding the keyboard moves it by 4.8–5.5×. A study reporting one number per
route reports the smaller of the two effects.

### Cognitive struggle, as something computable

"Hard" is not a finding. What the walkthroughs can compute is the share of a person's time
spent **not following instructions** — diagnosing blockers and acquiring prerequisites the
route assumes:

| | Route A | Route B |
|---|---|---|
| Engineer | **38 %** | 16 % |
| Statistician | **61 %** | **64 %** |

This is the result that does not follow the clock. Route B is between three and five times
quicker for the statistician, and **no less bewildering per minute** — slightly more so. Its
speed comes from having fewer steps, not from those steps making more sense. Two-thirds of the
statistician's route B is spent stuck, and both places they are stuck are defects: a CLI that
crashes on a clean install, and a file-naming convention that exists only in library source.

For the engineer the two routes genuinely differ in kind: route B is mostly instruction-
following, route A is a third troubleshooting.

### The one fact that costs the most, on both routes

That a `.geojson` must sit beside the `.csv` with the same stem, and never appears on a
command line. It is in no README, no `--help` and no error message. Both discovering agents
recovered it by opening `chap_core/cli_endpoints/_common.py`. Priced at 50 minutes for a
persona who would not open library source, it is the largest single non-learning cost in the
statistician's route B — larger than everything the documentation asks them to do.

## What this does not say

- **No human has been timed.** The estimate is a model. One real person walked through route B
  would do more for its credibility than any further agent work.
- **Route A's cold image build is unmeasured and excluded.** Every build in this repository ran
  against a warm layer cache. It is additive to every route-A figure above.
- **Sixty of the statistician's route-A minutes are the host, not the route.** On an x86_64
  machine the architecture problem does not arise.
- **The high ends are not worst cases.** They are a plausible bad run. A persona who concludes
  from the 401 that the model is simply unavailable, or from the GeoJSON failure that their
  data is malformed, does not appear in these numbers at all — they stop, and the route records
  no time.
- **Configuration is out of scope**, so the finding that a chapkit model cannot be configured
  through CHAP costs nobody anything here. In practice it lands after all of it.

---

## Where the detail is

| For | Go to |
|---|---|
| Every step, per persona per route, with its gate and its band | `analysis/08_humanCost/results/walkthrough_<persona>_<route>.tsv` |
| The totals and the struggle measure | `analysis/08_humanCost/results/summary.tsv` |
| What each persona had to learn, and when | `analysis/08_humanCost/results/prereq_exposure.tsv` |
| The measured half — document lengths, machine waits | `analysis/08_humanCost/results/doc_sizes.tsv`, `machine_waits.tsv` |
| The authored half — pace, knowledge, divergence rules | `analysis/08_humanCost/scripts/inputs/` and its `README.md` |
| Why each modelling choice was made, and what was rejected | `analysis/08_humanCost/provenance/human_cost.md` |
| To re-cost both routes under your own assumptions | edit `scripts/inputs/`, then `bash analysis/08_humanCost/run.sh` |
