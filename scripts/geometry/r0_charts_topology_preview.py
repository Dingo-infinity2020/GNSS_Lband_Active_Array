#!/usr/bin/env python3
"""Generate a schematic R0 CHARTS topology preview.

This is NOT an electromagnetic model.
It exists only to review reconstruction semantics before CST geometry work.

The preview represents:
- a square active envelope divided into four petals,
- a central square opening,
- a surrounding square passive ring.

Diagonal white gaps are visualization-only placeholders for inter-petal
separation. All values come from parameters.csv or documented topology
placeholders.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_manifest(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {row["parameter"]: row for row in rows}


def number(rows: dict[str, dict[str, str]], name: str) -> float:
    return float(rows[name]["value"])


def svg_for(candidate: str, petal_span: float, ring_span: float,
            center: float, slit: float, ring_width: float) -> str:
    margin = 40.0
    extent = max(petal_span, ring_span) / 2.0 + margin
    size = 900
    scale = size / (2.0 * extent)

    def sx(x: float) -> float:
        return size / 2.0 + x * scale

    def sy(y: float) -> float:
        return size / 2.0 - y * scale

    p = petal_span / 2.0
    c = center / 2.0
    r = ring_span / 2.0

    petals = {
        "N": [(-c, c), (c, c), (p, p), (-p, p)],
        "E": [(c, -c), (p, -p), (p, p), (c, c)],
        "S": [(-p, -p), (p, -p), (c, -c), (-c, -c)],
        "W": [(-p, -p), (-c, -c), (-c, c), (-p, p)],
    }

    def pts(poly):
        return " ".join(f"{sx(x):.2f},{sy(y):.2f}" for x, y in poly)

    outer_x = sx(-r)
    outer_y = sy(r)
    outer_w = 2 * r * scale
    ring_px = max(1.0, ring_width * scale)
    slit_px = max(1.0, slit * scale)

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="960" viewBox="0 0 900 960">',
        '<rect width="900" height="960" fill="white"/>',
        f'<text x="30" y="36" font-family="monospace" font-size="22">R0 TOPOLOGY PREVIEW — Candidate {candidate}</text>',
        '<text x="30" y="66" font-family="monospace" font-size="15">SCHEMATIC ONLY — NOT A CST/EM MODEL</text>',
        '<g transform="translate(0,60)">',
        f'<rect x="{outer_x:.2f}" y="{outer_y:.2f}" width="{outer_w:.2f}" height="{outer_w:.2f}" fill="none" stroke="goldenrod" stroke-width="{ring_px:.2f}"/>',
    ]
    for name, poly in petals.items():
        parts.append(
            f'<polygon points="{pts(poly)}" fill="#d8e6c1" stroke="#688b4e" stroke-width="2"/>'
        )

    # Visualization-only diagonal separation.
    parts += [
        f'<line x1="{sx(-p):.2f}" y1="{sy(-p):.2f}" x2="{sx(-c):.2f}" y2="{sy(-c):.2f}" stroke="white" stroke-width="{slit_px:.2f}"/>',
        f'<line x1="{sx(c):.2f}" y1="{sy(c):.2f}" x2="{sx(p):.2f}" y2="{sy(p):.2f}" stroke="white" stroke-width="{slit_px:.2f}"/>',
        f'<line x1="{sx(-p):.2f}" y1="{sy(p):.2f}" x2="{sx(-c):.2f}" y2="{sy(c):.2f}" stroke="white" stroke-width="{slit_px:.2f}"/>',
        f'<line x1="{sx(c):.2f}" y1="{sy(-c):.2f}" x2="{sx(p):.2f}" y2="{sy(-p):.2f}" stroke="white" stroke-width="{slit_px:.2f}"/>',
        f'<rect x="{sx(-c):.2f}" y="{sy(c):.2f}" width="{2*c*scale:.2f}" height="{2*c*scale:.2f}" fill="white" stroke="#444" stroke-width="1.5"/>',
        '</g>',
        f'<text x="30" y="890" font-family="monospace" font-size="16">petal_span={petal_span} mm   ring_span={ring_span} mm   center={center} mm</text>',
        f'<text x="30" y="920" font-family="monospace" font-size="14">slit={slit} mm and ring_width={ring_width} mm are topology placeholders only.</text>',
        '</svg>',
    ]
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--manifest",
        default="em/cst/R0_CHARTS_300_500/parameters.csv",
    )
    ap.add_argument("--candidate", choices=("A", "B"), default="A")
    ap.add_argument("--out", default="evidence")
    args = ap.parse_args()

    rows = read_manifest(Path(args.manifest))
    a = number(rows, "fig_label_227_5")
    b = number(rows, "fig_label_247_5")
    center = number(rows, "fig_label_center_40")
    slit = number(rows, "petal_slit")
    ring_width = number(rows, "ring_trace_width")

    if args.candidate == "A":
        petal_span, ring_span = a, b
    else:
        petal_span, ring_span = b, a

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    stem = f"R0_TOPOLOGY_CANDIDATE_{args.candidate}"
    (out / f"{stem}.svg").write_text(
        svg_for(args.candidate, petal_span, ring_span, center, slit, ring_width),
        encoding="utf-8",
    )
    payload = {
        "status": "SCHEMATIC_TOPOLOGY_ONLY",
        "candidate": args.candidate,
        "petal_span_mm": petal_span,
        "ring_span_mm": ring_span,
        "center_opening_mm": center,
        "petal_slit_placeholder_mm": slit,
        "ring_trace_width_placeholder_mm": ring_width,
        "warning": "Not an EM model; no solver interpretation permitted.",
    }
    (out / f"{stem}.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"PASS_R0_TOPOLOGY_PREVIEW_{args.candidate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
