# data-lao

The data anchor: the DHIS2 harmonised climate–health dataset for Laos, admin-1 monthly,
pinned at commit `af362d5` of `dhis2/climate-health-data`.

- `chap_LAO_admin1_monthly.csv` — the panel: 2808 rows, 18 admin units, 1998-01 to 2010-12.
  Target `disease_cases`; covariates `rainfall`, `mean_temperature`,
  `mean_relative_humidity`; plus `population` and `location_name`.
- `chap_LAO_admin1_monthly.geojson` — admin-1 boundaries (~8 MB).
- `chap_LAO_admin1_monthly_schema.json` — the dataset's own field and provenance schema.
- `sha256sums.txt` — written at fetch, re-verified on every run of `analysis/01_anchors`.
- `provenance.md` — source, pin, licence position and the three recorded discrepancies
  between the schema and the files.

Data files carry no `(IS_SHADOW)` marker: inserting a line would edit them and break their
checksums. **No licence is declared upstream**; redistribution is raised before release.
