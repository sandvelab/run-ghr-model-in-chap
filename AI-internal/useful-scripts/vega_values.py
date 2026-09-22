#!/usr/bin/env python3
"""Extract the values behind a Vega-Lite figure into a tab-separated file.

CHAP writes its evaluation plot as a self-contained HTML page with the Vega-Lite
specification inline, and the specification carries the plotted rows in its `datasets`
block. Rule 7 asks that every figure keep the values behind it beside it; this reads them
out of the figure itself, so the file and the picture cannot disagree.

One implementation, used by both routes, so neither exports its figure's numbers by its own
slightly different route. Standard library only.

    from vega_values import extract
    n = extract(Path("eval.html"), Path("eval.tsv"))
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

SPEC = re.compile(r"var spec = (\{.*?\});\s*\n", re.S)


def read_spec(html_path: Path) -> dict:
    m = SPEC.search(html_path.read_text(encoding="utf-8"))
    if not m:
        raise ValueError(f"{html_path}: no inline Vega-Lite spec found")
    return json.loads(m.group(1))


def extract(html_path: Path, out_path: Path) -> int:
    """Write every row of every dataset in the figure. Returns the number of rows."""
    spec = read_spec(html_path)
    datasets = spec.get("datasets") or {}
    if not datasets:
        raise ValueError(f"{html_path}: the spec carries no datasets block")

    rows: list[dict] = []
    for name, data in datasets.items():
        if not isinstance(data, list):
            continue
        for r in data:
            if isinstance(r, dict):
                rows.append({"dataset": name, **r})
    if not rows:
        raise ValueError(f"{html_path}: the datasets block holds no rows")

    columns: list[str] = []
    for r in rows:                       # union of keys, in first-seen order
        for k in r:
            if k not in columns:
                columns.append(k)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, delimiter="\t",
                           lineterminator="\n", restval="")
        w.writeheader()
        w.writerows(rows)
    return len(rows)
