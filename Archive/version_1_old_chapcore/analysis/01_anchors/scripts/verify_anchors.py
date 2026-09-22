#!/usr/bin/env python3
"""Verify and characterise the three project anchors.

Reads only from Archive/ (read-only) and writes three files to results/:

  anchor_manifest.tsv        one row per anchored artefact: what it is, how it is pinned,
                             its digest where it has one, and whether the digest still holds
  lao_characterisation.tsv   the development data described in numbers, so that a later
                             batch can tell whether the data it is handed is this data
  anchor_discrepancies.tsv   places where an anchor's own documentation disagrees with the
                             artefact, recorded rather than patched (plan §3)

Nothing here judges the anchors; it records them. A non-zero exit means a digest failed,
which is a stop-and-report condition.
"""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

NODE = Path(__file__).resolve().parent.parent
ARCHIVE = NODE.parent.parent / "Archive"
RESULTS = NODE / "results"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_field(path, key):
    for line in Path(path).read_text().splitlines():
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip()
    return ""


def write_tsv(path, header, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def verify_data_digests():
    """Re-check every file listed in the archived sha256sums.txt."""
    rows, failures = [], []
    sums = ARCHIVE / "data-lao" / "sha256sums.txt"
    for line in sums.read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        target = ARCHIVE / "data-lao" / name.strip()
        actual = sha256(target)
        ok = actual == digest
        if not ok:
            failures.append(name.strip())
        rows.append(("data", f"Archive/data-lao/{name.strip()}",
                     "sha256 in Archive/data-lao/sha256sums.txt", actual,
                     "holds" if ok else "FAILED"))
    return rows, failures


def model_rows():
    rows = []
    for anchor, dirname in (("model-route-a", "model-route-a"),
                            ("model-route-b", "model-route-b")):
        meta = ARCHIVE / dirname / "git-metadata.txt"
        repo = ARCHIVE / dirname / "repo"
        licences = sorted(p.name for p in repo.iterdir()
                          if p.is_file() and p.name.lower().split(".")[0]
                          in ("license", "licence", "copying"))
        rows.append((anchor, f"Archive/{dirname}/repo",
                     "git commit " + read_field(meta, "commit"),
                     read_field(meta, "remote"),
                     "licence file: " + (", ".join(licences) if licences else "NONE")))
    return rows


def platform_rows():
    meta = ARCHIVE / "platform-chap" / "install-metadata.txt"
    freeze = ARCHIVE / "platform-chap" / "chap-tool-freeze.txt"
    version = ""
    for line in meta.read_text().splitlines():
        if line.startswith("chap --version:"):
            version = line.split(":", 1)[1].strip()
    n = len([x for x in freeze.read_text().splitlines() if x.strip()])
    return [("platform", "Archive/platform-chap/",
             f"chap-core {version}, installed as a uv tool",
             f"{n} packages pinned in chap-tool-freeze.txt",
             "digest not applicable: captured state of an external install")]


def characterise_lao():
    csv_path = ARCHIVE / "data-lao" / "chap_LAO_admin1_monthly.csv"
    with open(csv_path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    cols = list(rows[0])
    locations = sorted({r["location"] for r in rows})
    periods = sorted({r["time_period"] for r in rows})
    cases = [int(r["disease_cases"]) for r in rows if r["disease_cases"] != ""]
    per_loc = Counter(r["location"] for r in rows)

    out = [
        ("columns", ",".join(cols)),
        ("n_rows", len(rows)),
        ("n_locations", len(locations)),
        ("locations", ",".join(locations)),
        ("n_time_periods", len(periods)),
        ("time_period_first", periods[0]),
        ("time_period_last", periods[-1]),
        ("rows_per_location_min", min(per_loc.values())),
        ("rows_per_location_max", max(per_loc.values())),
        ("target_column", "disease_cases"),
        ("target_n_present", len(cases)),
        ("target_n_missing", len(rows) - len(cases)),
        ("target_min", min(cases)),
        ("target_max", max(cases)),
        ("target_mean", round(sum(cases) / len(cases), 4)),
        ("target_n_zero", sum(1 for c in cases if c == 0)),
    ]
    for col in cols:
        out.append((f"empty_cells__{col}", sum(1 for r in rows if r[col] == "")))
    return out, len(rows), len(cases)


def discrepancies(n_rows, n_present):
    schema = json.loads((ARCHIVE / "data-lao"
                         / "chap_LAO_admin1_monthly_schema.json").read_text())
    ds = schema["dataset"]
    found = []
    if ds["row_count"] != n_rows:
        found.append((
            "data", "dataset.row_count",
            f"schema says {ds['row_count']}; the CSV has {n_rows} rows",
            f"the difference is {n_rows - ds['row_count']}, which equals the number of rows "
            f"with an empty disease_cases cell ({n_rows - n_present}); the schema count "
            "appears to be of target-present rows, not of rows",
            "recorded, not patched (plan §3)"))
    declared = ds.get("admin_geojson_file", "")
    present = [p.name for p in (ARCHIVE / "data-lao").glob("*.geojson")]
    if declared and declared not in present:
        found.append((
            "data", "dataset.admin_geojson_file",
            f"schema names {declared}; the directory holds {', '.join(present)}",
            "the boundary file was renamed upstream for CHAP compatibility and the schema "
            "was not updated with it",
            "recorded, not patched (plan §3)"))
    if n_rows - n_present:
        found.append((
            "data", "disease_cases completeness",
            f"{n_rows - n_present} of {n_rows} rows have no target value",
            "how a route handles missing target values is the route's business and is part "
            "of what is observed, so nothing is imputed or dropped here",
            "recorded, not patched (plan §3)"))
    if not any(p.name.lower().startswith("licen")
               for p in (ARCHIVE / "model-route-b" / "repo").iterdir() if p.is_file()):
        found.append((
            "model-route-b", "licence",
            "the repository carries no licence file and GitHub reports no licence",
            "with no licence, redistribution of the archived copy is not established; "
            "this blocks release, not analysis",
            "raised with the human before release (plan §4, data governance)"))
    return found


def main():
    RESULTS.mkdir(exist_ok=True)
    data_rows, failures = verify_data_digests()
    manifest = platform_rows() + model_rows() + data_rows
    write_tsv(RESULTS / "anchor_manifest.tsv",
              ["anchor", "path", "pinned_by", "detail", "integrity"], manifest)

    lao, n_rows, n_present = characterise_lao()
    write_tsv(RESULTS / "lao_characterisation.tsv", ["property", "value"], lao)

    disc = discrepancies(n_rows, n_present)
    write_tsv(RESULTS / "anchor_discrepancies.tsv",
              ["anchor", "where", "discrepancy", "reading", "disposition"], disc)

    print(f"anchors in manifest: {len(manifest)}")
    print(f"lao properties recorded: {len(lao)}")
    print(f"discrepancies recorded: {len(disc)}")
    if failures:
        print("DIGEST FAILURE: " + ", ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
