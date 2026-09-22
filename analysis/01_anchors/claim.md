# Claim

Are the three anchors this project is bound to actually what the plan says they are, and what does the Lao dataset contain? The platform's installed version and its resolved integration-relevant dependencies, both model repositories at their pinned commits, and the data files at their recorded checksums, each verified from the files on disk rather than from the plan; and the target column, resolution and shape read out of the CHAP schema.

## Children

kind: -
main-path: -

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(Each belongs in the claim collection under `Human-AI-collaboration/claims/` with a pointer
to the result grounding it.)_

**All three anchors are what the plan says they are.** Eight checks, all passing
(`results/anchor_manifest.tsv`). The three Lao data files re-hash to the digests recorded in
`sha256sums.txt` when they were fetched. Both model clones are present at their pinned
commits — route A `chap-models/chapkit_ghr_model` @ `60b16a2`, route B
`dhis2-chap/minimalist_example_uv` @ `5cd8a12`. The platform reports `chap --version` 2.3.1,
agreeing with the `chap-core` entry in its own 176-package freeze.

**The platform pin needs three versions, not one.** `chapkit` 2.1.0 and `servicekit` 2.0.2
are recorded beside `chap-core` 2.3.1, because a chapkit model service negotiates with
`chapkit` and `chap-core`'s version does not determine which `chapkit` sits behind it — its
requirement has been unbounded above in one release and capped below 2 in others. A pin
naming only `chap-core` would be ambiguous in exactly the place the two routes differ.

**The data is an 18-unit, 156-month admin-1 panel for Laos, 1998-01 to 2010-12, 2808 rows**
(`results/lao_characterisation.tsv`). The target is `disease_cases` — reported dengue cases
from OpenDengue — at monthly resolution, keyed on `location` + `time_period`. Beside it the
CSV carries `population`, `rainfall`, `mean_temperature` and `mean_relative_humidity`, none
with a missing value. 233 rows have no target value.

**The published data does not agree with itself in three places, and none is repaired**
(`results/anchor_discrepancies.tsv`). The schema's `row_count` of 2575 is the number of rows
that *have* a target value, not the 2808 rows in the file. The schema names its boundary file
`LAO_ADM1.geojson`, while the file shipped beside the CSV is
`chap_LAO_admin1_monthly.geojson`. And one admin unit, `LA-VI`, has no target value at any
period, so only 17 of 18 units carry a target at all. How each route copes with these is part
of what is being measured, which is why they are recorded rather than fixed.

**No model was run at this node, and CHAP was not asked to read the data.** Establishing how
CHAP wants a dataset presented is what each route's discovering agent has to find out, so the
characterisation above is a reading of the files on disk and says nothing about what either
model will be given.
