# Provenance — Lao CHAP dataset

One section per file. Append; never overwrite an existing section.

## chap_LAO_admin1_monthly.csv, .geojson, _schema.json

- **What they are**: the harmonised climate–health dataset for Laos published by DHIS2 —
  an admin-1, monthly panel covering 1998-01 to 2010-12, 18 admin units, 2808 rows. Target
  column `disease_cases` (reported dengue cases, OpenDengue); covariates `rainfall`,
  `mean_temperature`, `mean_relative_humidity` (ERA5-Land); plus `population` and
  `location_name`. Boundaries from OCHA COD-AB / HDX.
- **Source**: `https://github.com/dhis2/climate-health-data`, directory `lao/`.
- **Pinned at commit**: `af362d5260c6e7de1739f3d05314a844bd272613` (2026-04-22, "chore:
  rename admin boundaries for Chap compatibility (#11)").
- **Obtained by**: `curl -o <file> https://raw.githubusercontent.com/dhis2/climate-health-data/af362d5260c6e7de1739f3d05314a844bd272613/lao/<file>`
  for each of the three files, on 2026-09-21.
- **Checksums**: `sha256sums.txt`, written by `shasum -a 256` at fetch time and re-verified
  by `analysis/01_anchors/scripts/verify_anchors.py` on every run of that node.
- **Licence**: **none declared** — the repository carries no licence file and GitHub reports
  no licence. The data's underlying sources (OpenDengue, ERA5-Land, OCHA COD-AB) carry their
  own terms. Redistribution is not established; raised with the human before release.
- **Known discrepancies**: the schema's `row_count` (2575) counts target-present rows rather
  than rows (2808); the schema names `LAO_ADM1.geojson` while the file present is
  `chap_LAO_admin1_monthly.geojson`; 233 rows have an empty `disease_cases` cell. All three
  are recorded in `analysis/01_anchors/results/anchor_discrepancies.tsv` and are not patched.
- **Agency**: `human-pointed` (the human named this directory); `agent-retrieved` (commit,
  checksums, schema contents).
