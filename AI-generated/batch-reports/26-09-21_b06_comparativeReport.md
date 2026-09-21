# Batch 6 — Comparing the two routes

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 4

Route A is `chapkit_ghr_model`, a chapkit model service. Route B is `minimalist_example_uv`,
an `MLproject` model run with `uv`. Both were taken through CHAP 2.1.0 to an evaluation on the
same Lao admin-1 monthly data, by two agents that knew nothing of each other and worked from
identical briefs. Predictive results are **not** compared: the two models are instances of two
integration mechanisms, not competing predictions, and the plan rules that comparison out.

Every number here is read from `analysis/04_comparison/results/comparison_table.tsv`, which is
built by script from the effort statistics on the main path of the alternatives node below it.

---

## The numbers

| | Route A (chapkit) | Route B (MLproject/uv) | Ratio |
|---|---|---|---|
| Information sources consulted | 9 | 5 | 1.80 |
| …of which contributed | 8 | 4 | 2.00 |
| Commands run | 17 | 8 | 2.12 |
| Commands that failed | 2 | 0 | — |
| Blockers hit / left unresolved | 3 / 1 | 0 / 0 | — |
| **Dead ends** | **5** | **0** | — |
| Sources consulted before completion | 9 | 4 | 2.25 |
| Commands run before completion | 13 | 6 | 2.17 |
| Minutes to `evaluation_complete` | 52.5 | 29.7 | 1.77 |

Route B is cheaper on **every statistic that orders**. The ratios cluster around two, and the
one statistic where the routes are equal — one discarded source each — is equal by accident
rather than by anything meaningful.

These are the normalised figures. The two agents coded some of the same acts differently, so
the alternatives node keeps both readings; taking each log at face value instead moves route A
from 9 sources to 10 and route B from 5 to 4, and changes nothing else. **The conclusion does
not depend on that judgment call.**

## (a) Which resources had to be found, and how findable they were

This is the sharpest difference, and it is not really about quantity.

**Route B's answer was in the model's own README** — a literal, copy-pasteable `chap eval`
line, stated to have been verified against chap-core 2.1.0, and accurate. One file, correct,
at the obvious address.

**Route A's answer was in a docstring inside the installed Python package.** The recipe for
running a chapkit-served model appears in `chap_core/cli_endpoints/evaluate.py`. Nothing on
the web and nothing in the model's own repository carries it: route A's README never mentions
`chap eval` at all — it documents `make run` and stops at "ready to plug into chap-core". That
docstring is also the *only* place where the rule that CHAP discovers the GeoJSON as the
sibling `<stem>.geojson` is written down, and route A's model needs the geometry for its
spatial random effect.

So the gap in (a) is not that route A needed nine sources instead of five. It is that route A
required reading the platform's **source code** to get both the invocation and the reason it
failed, while route B required reading one README. A documented route and an undocumented one
are different in kind, not in degree.

One thing was identical across the two routes, and it is the most transferable finding of the
exercise: both agents started at `chap --help` and `chap eval --help` rather than the web
documentation, on the same reasoning — the installed binary is more authoritative about its
own flags than any page — and for both routes that was the right call. Route B's agent
consulted the hosted documentation once and discarded it as adding nothing over the CLI help.

## (b) What the process of finding out looked like

**Route B was a straight line.** Read the help, fetch the model, read its README and
`MLproject`, run the model standalone for 50 seconds to separate "the model is broken" from
"the integration is broken", validate, evaluate. Zero failed commands, zero blockers, zero
dead ends. The only confusion was a warning that four columns were "not used by the model",
which looked like a blocker and was not: the warning reports **declaration, not delivery**.
What settled it was not reasoning but reading the CSV CHAP actually wrote for the model.

**Route A was a diagnosis.** Its five dead ends were: an advertised prebuilt image that is not
publicly pullable (403 on an anonymous GHCR token, forcing a 22-minute, 4.98 GB local build
under emulation); chapkit *directory* mode, which runs `uv run fastapi dev` on the host and so
needs R and INLA there; `chap model schema` as an entry point, which has no `--run-config`
override; and two failed commands, of which one is the centre of the route:

> `ValueError: URL http://localhost:8000 … could not be reached as a chapkit service. Ensure
> the server is running and exposes /api/v1/info, or use --run-config.is-chapkit-model to skip
> auto-detection.`

— emitted while that endpoint was visibly returning `200 OK`. The message is wrong about what
failed, wrong about why, and the remedy it offers does not work. chap-core 2.1.0 pins
**chapkit 1.1.0**, whose `MLServiceInfo` declares `extra="forbid"`; the model is built on
**chapkit 2.0.0**, whose `/api/v1/info` adds three fields. The validation error is swallowed
and re-reported as unreachability, and `--run-config.is-chapkit-model` only skips the probe
before the same error surfaces from the wrapper. Diagnosing that required reading
`chap_core/models/utils.py` and `external_chapkit_model.py`.

The difference in *kind* matters more than the 1.77× difference in elapsed minutes. Route B's
agent was following instructions. Route A's agent was debugging an integration between two
components whose versions do not fit, with an error message pointing the wrong way. The first
is a cost that documentation can remove; the second is a cost that only a version bump or a
compatible release can remove.

## (c) What the working invocation turned out to be

| | Route A | Route B |
|---|---|---|
| Commands to run the model | 2, plus a container build, a container run and a proxy | 2 |
| Registration step | none as such — the URL *is* the model name | none — `MLproject` in a local directory *is* the registration |
| Container runtime | **required** (R-INLA, amd64 only; ~22 min build, 4.98 GB) | not needed; `uv_env` means CHAP builds on the host |
| Ran as published | **no** | yes |

Both mechanisms end in the same two CHAP commands — `chap eval` then `chap export-metrics` —
and neither has a registration step in the sense of a separate registry action. That is a real
similarity and it is worth stating, because it means the cost difference is almost entirely
*upstream* of CHAP: in getting the model to a state CHAP can talk to.

**The decisive asymmetry is that route A did not complete as published.** It completes through
`info_shim.py`, a standard-library reverse proxy that strips exactly three keys from one JSON
response. The model was not modified and the platform was not modified — the interposition
sits outside both — but every statement that route A reached an evaluation is conditional on
it. Route B needed nothing of the kind.

## Which was easier — the answer, and what it is worth

**Route B, on every measure, and by more than the ratios show.** It was easier to find out
about because its documentation was correct, present and in the first place anyone would look.
It was easier to carry out because it required no container, no build, no emulation, and no
workaround — and because it worked on the first attempt.

Three qualifications, and they are not small.

1. **This compares two routes, but each route is represented by one model and one run.** Route
   A's largest costs are properties of *this* model — R-INLA's amd64-only binaries, a 4.98 GB
   image, a GHCR package that is not public — rather than of the chapkit mechanism. A chapkit
   model without a compiled statistical backend would not pay them. What *is* attributable to
   the mechanism is the version-compatibility surface: serving a model over REST means two
   independently versioned packages must agree on a payload schema, and here they did not.
   An `MLproject` model has no such surface.
2. **The elapsed-minute figures are contaminated.** Both agents ran concurrently on one 8-CPU
   machine, so wall-clock is inflated by contention in a way the counts are not. That is why
   counts are the primary measure, and it is why the 1.77× timing ratio should carry less
   weight than the 5-versus-0 dead-end count.
3. **Route A's difficulty is dated.** It is a mismatch between chap-core 2.1.0's pinned chapkit
   1.1.0 and the model's chapkit 2.0.0. A chap-core shipping chapkit 2.x would remove most of
   route A's cost at a stroke. The finding is about a specific pair of versions, not about
   REST-served models in general — though the fact that the failure presents as "could not be
   reached" rather than as a version mismatch is a property of the platform's error handling,
   and that will outlive the version pair.

## What both routes agree on

Four things showed up identically in both logs, which is what independent replication is for:

- **CHAP's unused-covariate warnings are unreliable.** Both routes were told covariates were
  not used by the model; both were wrong. In route B the check cannot see through an
  undeclared-covariate `MLproject`; in route A it cannot see the chapkit service's own config
  defaults. The warning reports what CHAP declared, not what CHAP delivered.
- **The GeoJSON has no command-line flag** and is matched by basename beside the CSV — stated
  only in an installed docstring.
- **`chap eval` yields a file, not an answer.** Metrics need the separate `chap
  export-metrics` step, which neither model's README mentions.
- **One admin unit is silently dropped.** `LA-VI` has no target values at all, so both
  evaluations cover 17 of 18 units, announced in a WARNING inside a long log.

That these four recur across two independent agents, two mechanisms and two models makes them
findings about CHAP rather than about either route.
