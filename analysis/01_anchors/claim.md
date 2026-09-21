# Claim

What exactly is being run: which CHAP version, which two model repositories at which commits, and which Lao data files -- and are they intact and licensed for redistribution?

## Children

kind: sub-analyses
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

Yielded by `results/anchor_manifest.tsv`, `results/lao_characterisation.tsv` and
`results/anchor_discrepancies.tsv`, all written by `scripts/verify_anchors.py`.

1. **What is being run is fixed and re-checkable.** The platform is `chap-core` 2.1.0,
   captured as an install receipt plus a 174-package freeze; route A is
   `chapkit_ghr_model` at commit `60b16a2`; route B is `minimalist_example_uv` at commit
   `5cd8a12`; the data is the Lao admin-1 monthly panel at commit `af362d5` of
   `dhis2/climate-health-data`. All three data files' sha256 digests hold on re-verification.

2. **The target is `disease_cases`** — reported dengue cases from OpenDengue — on an 18-unit,
   156-month admin-1 panel running 1998-01 to 2010-12, 2808 rows, complete on every column
   except the target, which is empty in 233 rows. 1380 of the 2575 present values are zero
   and the maximum is 2643.

3. **Four discrepancies are recorded and none is patched.** The schema's `row_count` counts
   target-present rows rather than rows; the schema names a boundary file that was renamed
   upstream; 233 rows have no target value; and route B's repository declares no licence.
   The first three are left exactly as published because how a route copes with them is part
   of what this project observes. The fourth blocks release, not analysis.

4. **Two anchors are not established for redistribution.** Neither `minimalist_example_uv`
   nor `dhis2/climate-health-data` declares a licence. This is a question for the human
   before anything is pushed, not a question this node can settle.
