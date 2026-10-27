#!/usr/bin/env python3
"""Static audit for R0 V0.3 12-slot BUILD-ONLY CST macro."""

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

REQUIRED = (
    'StoreParameter "board_span"',
    'StoreParameter "outer_slot_frame_span"',
    'StoreParameter "outer_slot_width"',
    'StoreParameter "outer_mid_bridge"',
    'StoreParameter "outer_slot_segment_length"',
    'StoreParameter "inner_slot_width"',
    'StoreParameter "inner_center_clear_span"',
    'StoreParameter "inner_slot_length"',
    'StoreParameter "fig40_unresolved"',
    '.Name "GROUND_REFERENCE"',
    '.Name "ANTENNA_PLATE"',
    '.Name "CUT_OUTER_N_L"',
    '.Name "CUT_OUTER_N_R"',
    '.Name "CUT_OUTER_S_L"',
    '.Name "CUT_OUTER_S_R"',
    '.Name "CUT_OUTER_W_D"',
    '.Name "CUT_OUTER_W_U"',
    '.Name "CUT_OUTER_E_D"',
    '.Name "CUT_OUTER_E_U"',
    '.Name "CUT_INNER_N"',
    '.Name "CUT_INNER_S"',
    '.Name "CUT_INNER_E"',
    '.Name "CUT_INNER_W"',
)

REJECTED = (
    '.Name "PETAL_N"',
    '.Name "RING_N"',
    'center_opening',
    'center_solid_span',
    'candidate_swap',
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "macro",
        nargs="?",
        default="source/cst/R0_CHARTS_12SLOT_BUILD_ONLY_V03.mcr",
    )
    args = ap.parse_args()
    path = Path(args.macro)

    if not path.exists():
        print("HOLD_R0_V03_MACRO_MISSING")
        return 2

    text = path.read_text(encoding="utf-8")
    failures: list[str] = []

    for token in FORBIDDEN:
        if token in text:
            failures.append(f"forbidden_token:{token}")

    for token in REQUIRED:
        if token not in text:
            failures.append(f"missing_marker:{token}")

    for token in REJECTED:
        if token in text:
            failures.append(f"rejected_topology_present:{token}")

    n_sub = text.count('Solid.Subtract "Radiator:ANTENNA_PLATE"')
    if n_sub != 12:
        failures.append(f"slot_subtractions={n_sub},expected=12")

    outer_names = text.count('.Name "CUT_OUTER_')
    inner_names = text.count('.Name "CUT_INNER_')
    if outer_names != 8:
        failures.append(f"outer_slot_cutters={outer_names},expected=8")
    if inner_names != 4:
        failures.append(f"inner_slot_cutters={inner_names},expected=4")

    if "Sub Main()" not in text or "End Sub" not in text:
        failures.append("missing_flat_main")

    helper_lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip().lower().startswith(("sub ", "function "))
        and line.strip().lower() != "sub main()"
    ]
    if helper_lines:
        failures.append("helper_procedure_present:" + ",".join(helper_lines))

    non_ascii = sorted({ch for ch in text if ord(ch) > 127})
    if non_ascii:
        failures.append("non_ascii_present:" + repr(non_ascii))

    if failures:
        print("HOLD_R0_V03_STATIC_AUDIT")
        for item in failures:
            print(f"- {item}")
        return 3

    print("PASS_R0_V03_STATIC_AUDIT")
    print("EXPECTED_FINAL_SOLIDS=2")
    print("EXPECTED_OUTER_SLOT_SEGMENTS=8")
    print("EXPECTED_INNER_SLOT_SEGMENTS=4")
    print("EXPECTED_SLOT_SUBTRACTIONS=12")
    print("EXPECTED_PORTS=0")
    print("CENTER_THROUGH_HOLE=NO")
    print("FIG40_SEMANTICS=UNRESOLVED")
    print("SOLVER_RUN=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
