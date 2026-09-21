#!/usr/bin/env python3
"""Report, over every run collected so far, whether each route completes and how far its
scores move between runs.

Reads `results/history/<route>/*.csv` -- one `chap export-metrics` output per run, archived
by `scripts/rerun_routes.sh` -- and `results/run_ledger.tsv`, and writes:

  results/completion.tsv    per route: attempts, completions, how long a run takes
  results/score_spread.tsv  per route and metric: the runs, their range, and the spread

Movement between runs is expected and is not a fault (plan §2, §3). This script therefore
reports a spread and never a verdict about it: a route that varies is described by its
range rather than by one number. What it *does* judge is completion, because that is the
question the project asks of a route.

Nothing here compares route A's scores against route B's. They are different models, and
the plan rules that comparison out.
"""
from __future__ import annotations

import csv
import statistics
from pathlib import Path

NODE = Path(__file__).resolve().parent.parent
HISTORY = NODE / "results" / "history"
LEDGER = NODE / "results" / "run_ledger.tsv"
RESULTS = NODE / "results"

# The columns worth tracking. `chap export-metrics` writes a wide row of which most is
# derived from the same forecasts; these are the ones a reader would quote.
METRICS = ["mae", "rmse", "crps", "mape", "coverage_10_90", "coverage_25_75",
           "crps_norm", "ratio_above_truth", "sample_count"]


def read_runs(route: str) -> list[tuple[str, dict]]:
    runs = []
    directory = HISTORY / route
    if not directory.is_dir():
        return runs
    for path in sorted(directory.glob("*.csv")):
        with open(path, newline="") as fh:
            rows = list(csv.DictReader(fh))
        if rows:
            runs.append((path.name, rows[0]))
    return runs


def completion_rows():
    if not LEDGER.is_file():
        return []
    with open(LEDGER, newline="") as fh:
        ledger = list(csv.DictReader(fh, delimiter="\t"))
    out = []
    for route in sorted({r["route"] for r in ledger}):
        mine = [r for r in ledger if r["route"] == route]
        done = [r for r in mine if r["completed"] == "yes"]
        seconds = sorted(int(r["seconds"]) for r in mine)
        out.append((route, len(mine), len(done),
                    "yes" if done and len(done) == len(mine) else
                    ("partly" if done else "no"),
                    seconds[len(seconds) // 2] if seconds else "",
                    len(read_runs(route))))
    return out


def spread_rows():
    out = []
    for route in sorted(p.name for p in HISTORY.iterdir() if p.is_dir()):
        runs = read_runs(route)
        if not runs:
            continue
        for metric in METRICS:
            values = []
            for _, row in runs:
                raw = row.get(metric, "")
                try:
                    values.append(float(raw))
                except (TypeError, ValueError):
                    continue
            if not values:
                continue
            lo, hi = min(values), max(values)
            mean = statistics.fmean(values)
            # Spread as a percentage of the mean, which is the form the question "how much
            # does it move" is usually asked in. Undefined at a mean of zero, and said so
            # rather than shown as a zero that would read as stability.
            pct = f"{100 * (hi - lo) / mean:.2f}" if mean else "undefined (mean is 0)"
            out.append((route, metric, len(values), f"{lo:.6g}", f"{hi:.6g}",
                        f"{mean:.6g}", f"{hi - lo:.6g}", pct))
    return out


def write(path, header, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path.relative_to(NODE)} ({len(rows)} rows)")


def main():
    RESULTS.mkdir(exist_ok=True)
    write(RESULTS / "completion.tsv",
          ["route", "attempts", "completions", "completed_every_time",
           "median_seconds", "metric_files_collected"],
          completion_rows())
    write(RESULTS / "score_spread.tsv",
          ["route", "metric", "n_runs", "min", "max", "mean", "range", "range_pct_of_mean"],
          spread_rows())


if __name__ == "__main__":
    main()
