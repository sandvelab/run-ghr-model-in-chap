# Discovery notes: route A through chaps (chapkit_ghr_model on the Lao data)

Written while working, by the discovering agent. The step numbers refer to
`discovery_log.tsv`.

## What I did, in order

1. **Read the log specification** (step 1). I also read the one non-brief file in my node
   folder, `docker_state_before_run.txt`. It shows the orchestrator removed the chap-core,
   worker and GHR images before this run, so nothing about this model was cached locally.
   No route information came from it.
2. **chaps README, then `docs/ai.md`** (steps 3-6). The README sends AI agents to
   `docs/ai.md`. That page offers 18 "options". None of them is "evaluate a model on my
   own CSV". The closest are option 2 (chap-core plus models, no DHIS2), option 7 (one
   model service on its own, `chaps run`) and option 11 (my own model). Its "What to try
   next without DHIS2" section suggests `chaps models test --all --backtest`. That runs a
   backtest on *sample data the model generates itself*, not on a dataset the user
   supplies, so it does not meet the brief.
3. **Model README** (step 9). It says the model is a chapkit service with an image on ghcr,
   is monthly and amd64-only, and by default uses `rainfall`, `mean_temperature` and
   `population`. All three columns are in the Lao CSV. It also says geometry is strict: a
   GeoJSON that does not match the locations is an error. The Lao GeoJSON's
   `shapeISO`/feature ids (`LA-AT`, ...) match the CSV's `location` column.
4. **Installed `chap eval --help` and its source** (steps 10, 20). `MODEL-NAME` accepts "a
   chapkit service URL", and chapkit is detected automatically by probing `/api/v1/info`.
   The GeoJSON is found automatically when it has the same stem as the CSV, which ours
   does. `--plot` writes the default `evaluation_plot` as HTML next to the `.nc`.
   `chap plot-backtest` (default plot type `evaluation_plot`) and `chap export-metrics`
   are the post-eval commands for the plot and the metrics CSV.
5. **chaps `docs/run.md`** (step 14) shows `chaps run https://github.com/chap-models/chapkit_ghr_model`
   verbatim as an example. That decided the route (step 16): chaps starts the model service
   and prints its URL, then `chap eval <URL> <csv> <out.nc>`.
6. The vendored marketplace entry (step 15) shows that the repository URL resolves to the
   marketplace's pinned version 0.1.3, image `sha-dfb2e3f`, which is the model repository's
   current HEAD commit `dfb2e3f`. So "this model" and the chaps pin agree.
7. Installed chaps v0.99.4 with its documented installer into a scratch directory
   (step 17). `chaps doctor`: 10 ok, 1 warn (Apple Silicon, so amd64 images run under
   Rosetta).

## What was confusing / what did not hold

- `docs/ai.md` is written for a person setting up Chap and the Modeling App. It does not
  say how to evaluate a model on your own data. The bridge to the `chap` CLI (a chapkit
  service URL as `chap eval`'s model argument) is documented in chap-core's `--help`, not
  in chaps.
- chaps' own evaluation path (`chaps models test --backtest`) sounds like the answer but
  runs on model-generated sample data.
