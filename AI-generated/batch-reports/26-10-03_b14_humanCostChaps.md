# Batch 14 — route A through chaps, costed for a human

Generated from [[26-09-21_chapModelIntegrationRoutes]] — iteration 3, outside the plan

The human asked whether `chaps` (`winterop-com/chaps`, a Docker Compose wrapper that serves
CHAP and chapkit models) makes route A easy and quick now, relative to route B, the MLproject
route, and including for a statistician. Batch 10's question was asked again: a fresh agent
discovered the route, and batch 10's human-cost model, with every rate unchanged, re-costed
what it did.

**As in batch 10, none of the minutes below were measured on a person.** The act sequence is
measured from the agent's log; the pace and the personas are batch 10's, unchanged
(`analysis/10_routeA_chaps/02_humanCost/scripts/inputs/`, checked byte-identical on every run).

---

## The answer

| Expected minutes (low–high) | **Engineer** | **Statistician** |
|---|---|---|
| Route B, MLproject (batch 10) | **46** (27–99) | **221** (101–594) |
| Route A without chaps (batch 12) | 110 (72–216) | 436 (243–1,026) |
| **Route A through chaps (this batch)** | **130** (87–249) | **483** (273–1,120) |
| Through chaps ÷ route B | 2.8 | 2.2 |

From `analysis/10_routeA_chaps/03_versusRouteB/results/comparison.tsv` and
`ratios_to_route_b.tsv`.

**chaps does not make route A quicker for a human, and route B stays at about half the cost
for both personas.** For an agent the chaps route is short. For a person, chaps swaps two
`docker` commands for one `chaps run` and adds its own documentation to read. That
documentation stops before the evaluation, so the evaluation still comes from chap-core's own
pages. Docker is still the statistician's largest single cost.

## What the agent found

A fresh agent on the §4 brief verbatim, with item 1 naming chaps as the route
(`analysis/10_routeA_chaps/01_discovery/`):

```
curl -fsSL https://raw.githubusercontent.com/winterop-com/chaps/main/install.sh | sh -s -- --dir <bin>
chaps run https://github.com/chap-models/chapkit_ghr_model --port 5060
chap eval --model-name http://localhost:5060 --dataset-csv chap_LAO_admin1_monthly.csv \
     --output-file eval.nc --run-config.is-chapkit-model
chap plot-backtest --input-file eval.nc --output-file evaluation_plot.html
chap export-metrics --input-files eval.nc --output-file metrics.csv
```

- **chaps recognised the repository URL** as its marketplace model and served the pinned
  image `sha-dfb2e3f` (GHR 0.1.3, chapkit 2.2.0) unchanged. The loaded image id is the
  published digest (`results/image_id.txt`).
- **chaps' documentation does not cover evaluating on your own data.** Its agent page covers
  serving a model and a backtest on sample data the model generates. The `chap eval` step came
  from `chap eval --help` and chap-core's `evaluation-workflow.md` and `chapkit.md`.
- **The evaluation**, on CHAP's defaults, covered 17 of 18 provinces (LA-VI has no cases):
  CRPS 149.2, MAE 124.1, RMSE 238.9, 10–90 coverage 0.815 (`results/metrics.csv`). The
  clean-shell re-run from the agent's own script gave CRPS 149.8 (`results/clean_run/`, exit
  0). Batch 12's 0.1.2 gave 151.4; that is the same model behaviour.
- **What it cost the agent**: 143,158 tokens to the first evaluation, against 139,417 without
  chaps; 178,763 in all (`results/agent_usage.tsv`).

### The download failed through chaps

The model image is 2.1 GB, and one 1.42 GB layer accounts for most of it. On this batch's
link (about 0.5 MB/s), ghcr.io kept cutting that layer:

- chaps pulls the image twice, first to probe its user id and then through Compose.
- Docker throws away a partial layer when a pull fails, so each retry started from zero.
- After 93 minutes `chaps run` stopped with "fix that, then … tries again".

The agent wrote a resumable, digest-checked fetcher (`scripts/fetch_image_oci.sh`) and loaded
the image, which took 90 minutes. After that, `chaps run` started the model in 2 seconds. The
model was not changed. The first attempt at this batch, the day before, stalled the same way
at slower speeds and is kept, unused (`analysis/10_routeA_chaps/results/attempt1_stalled/`).

## The chaps route, step by step

**Engineer — 130 minutes expected (87–249).**

| | Step | Expected |
|---|---|---|
| 1 | install Docker Desktop and start it | 6.0 |
| 5 | read the chaps README (1,291 words) | 7.6 |
| 6 | read chaps' `docs/ai.md` (4,465 words), where the README sends AI agents | **26.3** |
| 7 | read the model README (2,833 words; includes 9 min on CPU architectures) | **32.1** |
| 8 | install chaps | 6.0 |
| 9–16 | `chaps doctor`, `chap eval --help`, `chaps run --help`, `chaps models list`, two decisions, `chaps run` | 12.2 |
| 17 | wait for the image (333 s, borrowed from batch 12; see below) | 5.5 |
| 20–24 | check the data; read chap-core source and two chap-core docs pages | 25.5 |
| 27–31 | `curl` the service, `chap eval`, wait (430 s, measured) | 8.8 |

The engineer holds almost everything the route asks for, so the cost is reading. Two
documents take 58 of the 130 minutes. Read chaps' `docs/run.md` (1,262 words) instead of its
page for AI agents, and the engineer's figure drops to 111, level with route A without chaps.

**Statistician — 483 minutes expected (273–1,120).**

| | Step | Expected | Why |
|---|---|---|---|
| 1 | install Docker Desktop and start it | **127.5** | 90 minutes of it is learning Docker, before any document is opened |
| 7 | read the model README | **94.0** | the README assumes containers and CPU architectures; 35 minutes are learning the latter |
| 6 | read chaps' `docs/ai.md` | 54.1 | |
| 11 | `chap eval --help` | 33.6 | the idea of a model as a running service CHAP talks to |
| 15 | weigh a full chaps deployment, and reject it | 31.2 | compose files |
| 16, 27 | `chaps run`; `curl` the service | 20.5 each | registries; HTTP |

The statistician skips the library-source read; the docs they do read document the GeoJSON
convention, so nothing is lost by it (divergence D4). Six prerequisites are lacked, all of
them about containers and services: docker-basics, cpu-architecture, rest-service-model,
docker-compose, container-registry, http-curl (`02_humanCost/results/prereq_exposure.tsv`).
Route B asks this persona for one.

## On a slow link

chaps finished no pull on this link, so the main figure borrows batch 12's measured pull on a
working link. Costed instead as it went here, up to the point where chaps fails, the route
comes to **190 minutes for the engineer and 566 for the statistician**. Of that, 93 minutes
are waiting, and it ends blocked: the fix is a hand-written image fetcher, which neither
persona is shown and which is not costed as one of their steps (route
`route-a-chaps-slowlink`).

## Sensitivities

Each changes one input and is reported beside the main figure, never instead of it:

| | Engineer | Statistician |
|---|---|---|
| main | 130 | 483 |
| Docker priced lighter (learn 15/30/60, not 45/90/240) — chaps needs Docker installed, not used by hand | 130 | 423 |
| `docs/run.md` read in place of the agent page | 111 | 446 |
| *Route B:* the D2 GeoJSON trap removed | 46 | 246 |
| *Route B:* D2 removed and the documented convention read in place of library source | 45 | 186 |

**Removing D2 alone makes route B dearer for the statistician, not cheaper.** Without the trap,
the persona has to read library source, as the agent did. Only reading the convention where
chap-core now documents it brings route B down, to 186. On no reading does the chaps route
come near route B.

## What this cannot separate

- **Route B was not re-discovered.** Its figures are batch 10's, from iteration 2's logs.
- **The model version changed**: batch 12 ran 0.1.2, and this batch ran chaps' pin 0.1.3. The
  code diff is a version string and a monitoring hook
  (`Archive/model-route-a-chaps/diff-stat-since-it3-pin.txt`).
- **The agent knew the link speed** from the orchestrator's pre-run note, and passed chaps a
  long timeout because of it. chaps' default 300-second timeout would have failed sooner
  (`01_discovery/provenance/discovery.md`).
- **The clean-shell re-run found the image already loaded**, so the download did not run inside
  it. During that run the host also slept for 2.8 hours, which is not counted as route time.

## What would change the answer

On the human side, a chaps page that goes from `chaps run` to `chap eval` on a user's own CSV
would replace the 4,465-word agent page and the two chap-core pages. A resumable or
single-pass image pull would remove the slow-link failure. Neither would remove Docker, which
on route A is the statistician's entry fee and does not exist on route B.
