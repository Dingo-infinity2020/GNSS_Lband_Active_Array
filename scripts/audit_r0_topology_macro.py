#!/usr/bin/env python3
"""Static audit for the R0 CST topology BUILD-ONLY structure macro.

This audit does not execute CST and does not validate CST runtime syntax.
It only enforces the project contract before human/CST review.
"""

from __future__ import annotations

import argparse
from pathlib import Path

FORBIDDEN = (
    "StartSolver",
    ".Start",
    "Optimizer.",
    "ParameterSweep",
    "Sweep.",
    "AdaptiveMesh",
    "DiscretePort",
    "WaveguidePort",
    "LumpedElement",
    "Monitor.",
)

REQUIRED_OBJECT_NAMES = (
    "GROUND_REFERENCE",
    "PETAL_N",
    "PETAL_E",
    "PETAL_S",
    "PETAL_W",
    "RING_N",
    "RING_S",
    "RING_E",
    "RING_W",
)

REQUIRED_MARKERS = (
    'StoreParameter "candidate_swap"',
    'StoreParameter "fig227"',
    'StoreParameter "fig247"',
    'StoreParameter "center_opening"',
    'With Extrude',
    'With Brick',
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "macro",
        nargs="?",
        default="source/cst/R0_CHARTS_TOPOLOGY_BUILD_ONLY_V01.mcr",
    )
    args = ap.parse_args()
    path = Path(args.macro)

    if not path.exists():
        print("HOLD_R0_TOPOLOGY_MACRO_MISSING")
        return 2

    text = path.read_text(encoding="utf-8")
    failures: list[str] = []

    for token in FORBIDDEN:
        if token in text:
            failures.append(f"forbidden_token:{token}")

    for token in REQUIRED_MARKERS:
        if token not in text:
            failures.append(f"missing_marker:{token}")

    for name in REQUIRED_OBJECT_NAMES:
        marker = f'.Name "{name}"'
        if marker not in text:
            failures.append(f"missing_object:{name}")

    if "Sub Main()" not in text or "End Sub" not in text:
        failures.append("missing_flat_main")

    # No helper procedures/functions are allowed in replay-safe R0.
    helper_lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip().lower().startswith(("sub ", "function "))
        and line.strip().lower() != "sub main()"
    ]
    if helper_lines:
        failures.append("helper_procedure_present:" + ",".join(helper_lines))

    if failures:
        print("HOLD_R0_TOPOLOGY_MACRO_STATIC_AUDIT")
        for item in failures:
            print(f"- {item}")
        return 3

    print("PASS_R0_TOPOLOGY_MACRO_STATIC_AUDIT")
    print("EXPECTED_SOLIDS=9")
    print("EXPECTED_PORTS=0")
    print("SOLVER_RUN=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
