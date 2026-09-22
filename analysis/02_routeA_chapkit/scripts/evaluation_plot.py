#!/usr/bin/env python3
"""Write the values behind this route's CHAP evaluation figure, beside the figure.

CHAP draws the figure; this does not redraw it. `results/eval/evaluation.html` is the figure
as CHAP wrote it and is the complete one -- every location, every split. The PNG beside it
is a viewport capture of that page, made by opening it in a browser, and exists because a
document has to embed an image rather than a live page.

What this script produces is the third thing Rule 7 asks for: the numbers the picture is
drawn from, read out of the figure's own inline Vega-Lite specification so that the table
and the picture cannot drift apart.
"""
from pathlib import Path
import sys

NODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(NODE.parents[1] / "AI-internal" / "useful-scripts"))
from vega_values import extract  # noqa: E402

HTML = NODE / "results" / "eval/evaluation.html"
OUT = NODE / "results" / "eval" / "evaluation_plot.tsv"

if __name__ == "__main__":
    n = extract(HTML, OUT)
    print(f"{OUT.relative_to(NODE)}: {n} plotted rows, from {HTML.name}")
