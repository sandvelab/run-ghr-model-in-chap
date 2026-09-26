# What the two rules changed

Applied to both logs alike. The logs themselves are not edited.

## it2-route-a

43 rows logged, 27 inside the discovery window.

- rule 1: step 12 (docker pull --platform linux/amd64 ghcr.io/chap-models/chapk) reclassified ok -> failed, on the correction carried by step 13
- rule 1: step 28 (chap export-metrics evaluation.nc metrics.csv) reclassified ok -> failed, on the correction carried by step 30
- rule 1: step 30 not counted as a blocker -- its ref is the correction to step 28, not an external condition
- rule 1: step 32 not counted as a blocker -- its ref is the correction to step 28, not an external condition
- rule 2: 16 row(s) after the first evaluation_complete (step 27) are outside the discovery window

## it3-route-a

44 rows logged, 31 inside the discovery window.

- rule 2: 13 row(s) after the first evaluation_complete (step 31) are outside the discovery window
