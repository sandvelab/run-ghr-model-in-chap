#!/usr/bin/env python3
"""Write the values behind each of this route's CHAP evaluation figures, beside the figure.

CHAP draws the figures; this does not redraw them. For each run -- the one made by hand during
discovery (`manual_run/`) and the one made by the route script (`route_run/`) -- the numbers
the figure is drawn from are read out of the figure's own inline Vega-Lite specification, so
that the table and the picture cannot drift apart. Same extractor as iteration 2's route A.
"""
from pathlib import Path
import sys

NODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(NODE.parents[2] / "AI-internal" / "useful-scripts"))
from vega_values import extract  # noqa: E402

if __name__ == "__main__":
    for run in ("manual_run", "route_run"):
        html = NODE / "results" / run / "evaluation_plot.html"
        out = NODE / "results" / run / "evaluation_plot.tsv"
        n = extract(html, out)
        print(f"{out.relative_to(NODE)}: {n} plotted rows, from {html.name}")
