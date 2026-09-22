#!/usr/bin/env python3
"""Verify the three anchors against the files on disk, and characterise the Lao dataset.

Nothing here trusts the plan. Every value written is read out of a file under `Archive/`:
the checksums from the data manifest, the model commits from each clone's git metadata, the
platform versions from the install metadata, and the dataset's shape from the CSV and the
CHAP schema beside it.

Writes three tab-separated files to `results/`:

  anchor_manifest.tsv       one row per anchor, with what it was checked against
  lao_characterisation.tsv  the dataset's shape, target and covariates, as read
  anchor_discrepancies.tsv  where the published data does not agree with itself

The discrepancies are recorded, never repaired: how each route copes with an inconsistent
schema and a gappy target is part of what this project measures.

Standard library only -- the pinned analysis environment declares no dependencies.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

TSV = dict(delimiter="\t", lineterminator="\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def field(text: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


# --------------------------------------------------------------------------- anchors

def check_data(archive: Path) -> tuple[list[list[str]], Path, Path]:
    """Re-verify every file named in the data manifest against its recorded digest."""
    d = archive / "data-lao"
    manifest = d / "sha256sums.txt"
    rows = []
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        recorded, name = line.split(maxsplit=1)
        f = d / name.strip()
        actual = sha256(f) if f.exists() else "MISSING"
        rows.append([
            "data", f"data-lao/{name.strip()}", "sha256", recorded,
            actual, "verified" if actual == recorded else "MISMATCH",
            f"{f.stat().st_size} bytes" if f.exists() else "",
        ])
    return rows, d / "chap_LAO_admin1_monthly.csv", d / "chap_LAO_admin1_monthly_schema.json"


def check_model(archive: Path, folder: str, route: str) -> list[list[str]]:
    """Confirm an archived model clone is present and report the commit it is pinned at."""
    meta = (archive / folder / "git-metadata.txt").read_text()
    repo = archive / folder / "repo"
    n_files = sum(1 for p in repo.rglob("*") if p.is_file()) if repo.is_dir() else 0
    return [[
        f"model-{route}", f"{folder}/repo", "commit",
        field(meta, "commit"), field(meta, "commit"),
        "present" if n_files else "MISSING",
        f"{field(meta, 'remote')}; {n_files} files; committed {field(meta, 'committed')}",
    ]]


def check_platform(archive: Path) -> list[list[str]]:
    """Read the pinned platform versions back out of the archived install metadata."""
    meta = (archive / "platform-chap" / "install-metadata.txt").read_text()
    freeze = (archive / "platform-chap" / "chap-tool-freeze.txt").read_text()
    pinned = {}
    for pkg in ("chap-core", "chapkit", "servicekit"):
        m = re.search(rf"^{re.escape(pkg)}==(.+)$", freeze, re.M)
        pinned[pkg] = m.group(1).strip() if m else "ABSENT"
    reported = field(meta, "chap --version")
    rows = [[
        "platform", "platform-chap/install-metadata.txt", "chap --version",
        pinned["chap-core"], reported,
        "verified" if reported == pinned["chap-core"] else "MISMATCH",
        f"{sum(1 for l in freeze.splitlines() if l.strip())} packages frozen",
    ]]
    for pkg in ("chapkit", "servicekit"):
        rows.append([
            "platform", "platform-chap/chap-tool-freeze.txt", f"{pkg} resolved",
            pinned[pkg], pinned[pkg],
            "present" if pinned[pkg] != "ABSENT" else "MISSING",
            "what a chapkit model service negotiates with; not determined by chap-core's version",
        ])
    return rows


# ------------------------------------------------------------------- characterisation

def characterise(csv_path: Path, schema_path: Path) -> tuple[list[list[str]], list[list[str]]]:
    schema = json.loads(schema_path.read_text())
    ds = schema["dataset"]
    fields = {f["name"]: f for f in schema["fields"]}

    with csv_path.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    header = list(rows[0].keys())

    units = sorted({r["location"] for r in rows})
    periods = sorted({r["time_period"] for r in rows})
    blank = Counter(c for r in rows for c in header if r[c].strip() == "")
    target = "disease_cases"
    empty_units = sorted(
        u for u in units
        if all(r[target].strip() == "" for r in rows if r["location"] == u)
    )
    covariates = [
        c for c in header
        if c not in ("time_period", "location", "location_name", target)
    ]

    out = [
        ["dataset_name", ds["name"], "schema"],
        ["country_iso3", ds["country_iso3"], "schema"],
        ["admin_level", str(ds["admin_level"]), "schema"],
        ["temporal_resolution", ds["temporal_resolution"], "schema"],
        ["target_column", target, f"schema field: {fields[target]['description']}"],
        ["target_unit", fields[target].get("unit") or "", "schema"],
        ["target_provider", fields[target]["source"]["provider"], "schema"],
        ["primary_key", "+".join(ds["primary_key"]), "schema"],
        ["csv_columns", "+".join(header), "csv header"],
        ["covariates", "+".join(covariates), "csv header minus key, name and target"],
        ["n_rows", str(len(rows)), "csv"],
        ["n_units", str(len(units)), "csv"],
        ["n_periods", str(len(periods)), "csv"],
        ["period_first", periods[0], "csv"],
        ["period_last", periods[-1], "csv"],
        ["schema_time_range", f"{ds['time_range']['start']}..{ds['time_range']['end']}", "schema"],
        ["n_rows_target_missing", str(blank[target]), "csv"],
        ["n_rows_target_present", str(len(rows) - blank[target]), "csv"],
        ["units_with_no_target_at_all", "+".join(empty_units) or "none", "csv"],
        ["n_units_with_target", str(len(units) - len(empty_units)), "csv"],
    ]
    for c in covariates:
        out.append([f"n_missing_{c}", str(blank[c]), "csv"])

    disc = []
    if ds["row_count"] != len(rows):
        disc.append([
            "schema_row_count", "schema.dataset.row_count", str(ds["row_count"]),
            str(len(rows)),
            f"the schema's count equals the {len(rows) - blank[target]} rows that have a target "
            f"value, not the {len(rows)} rows in the file",
        ])
    geo_named = ds["admin_geojson_file"]
    geo_actual = csv_path.with_suffix(".geojson").name
    if geo_named != geo_actual:
        disc.append([
            "geojson_filename", "schema.dataset.admin_geojson_file", geo_named, geo_actual,
            "the schema names a boundary file that is not the one shipped beside the CSV",
        ])
    if blank[target]:
        disc.append([
            "target_gaps", f"csv column {target}", "0 missing", f"{blank[target]} missing",
            f"{len(empty_units)} unit(s) have no target value at any period: "
            f"{'+'.join(empty_units) or 'none'}",
        ])
    return out, disc


# --------------------------------------------------------------------------------- main

def main() -> int:
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--archive", type=Path, default=here.parents[1] / "Archive")
    ap.add_argument("--out", type=Path, default=here / "results")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    manifest, csv_path, schema_path = check_data(a.archive)
    manifest += check_model(a.archive, "model-route-a", "route-a")
    manifest += check_model(a.archive, "model-route-b", "route-b")
    manifest += check_platform(a.archive)

    with (a.out / "anchor_manifest.tsv").open("w", newline="") as fh:
        w = csv.writer(fh, **TSV)
        w.writerow(["anchor", "path", "pinned_by", "recorded", "actual", "status", "note"])
        w.writerows(manifest)

    characterisation, discrepancies = characterise(csv_path, schema_path)
    with (a.out / "lao_characterisation.tsv").open("w", newline="") as fh:
        w = csv.writer(fh, **TSV)
        w.writerow(["property", "value", "read_from"])
        w.writerows(characterisation)
    with (a.out / "anchor_discrepancies.tsv").open("w", newline="") as fh:
        w = csv.writer(fh, **TSV)
        w.writerow(["discrepancy", "where", "declared", "actual", "note"])
        w.writerows(discrepancies)

    bad = [r for r in manifest if r[5] in ("MISMATCH", "MISSING")]
    for r in manifest:
        print(f"{r[5]:9s} {r[0]:15s} {r[1]}")
    print(f"\n{len(characterisation)} properties, {len(discrepancies)} discrepancies recorded")
    if bad:
        print(f"\n{len(bad)} anchor check(s) failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
