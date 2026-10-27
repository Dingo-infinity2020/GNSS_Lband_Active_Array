#!/usr/bin/env python3
"""Static audit for R0 V0.2 slotted-plate BUILD-ONLY CST macro."""

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

REQUIRED_MARKERS = (
    'StoreParameter "board_span"',
    'StoreParameter "outer_slot_frame_span"',
    'StoreParameter "center_solid_span"',
    'StoreParameter "slot_width"',
    '.Name "GROUND_REFERENCE"',
    '.Name "ANTENNA_PLATE"',
    'Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_N"',
    'Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_S"',
    'Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_E"',
    'Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_W"',
    'Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_N"',
    'Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_S"',
    'Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_E"',
    'Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_W"',
)

REJECTED_V01_MARKERS = (
    '.Name "PETAL_N"',
    '.Name "PETAL_E"',
    '.Name "PETAL_S"',
    '.Name "PETAL_W"',
    '.Name "RING_N"',
    '.Name "RING_S"',
    '.Name "RING_E"',
    '.Name "RING_W"',
    'center_opening',
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "macro",
        nargs="?",
        default="source/cst/R0_CHARTS_SLOTTED_PLATE_BUILD_ONLY_V02.mcr",
    )
    args = ap.parse_args()
    path = Path(args.macro)

    if not path.exists():
        print("HOLD_R0_V02_MACRO_MISSING")
        return 2

    text = path.read_text(encoding="utf-8")
    failures: list[str] = []

    for token in FORBIDDEN:
        if token in text:
            failures.append(f"forbidden_token:{token}")

    for token in REQUIRED_MARKERS:
        if token not in text:
            failures.append(f"missing_marker:{token}")

    for token in REJECTED_V01_MARKERS:
        if token in text:
            failures.append(f"rejected_v01_topology_present:{token}")

    if text.count('Solid.Subtract "Radiator:ANTENNA_PLATE"') != 8:
        failures.append("expected_exactly_8_slot_subtractions")

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

    # Keep structure macro ASCII-only for CST history portability.
    non_ascii = sorted({ch for ch in text if ord(ch) > 127})
    if non_ascii:
        failures.append("non_ascii_present:" + repr(non_ascii))

    if failures:
        print("HOLD_R0_V02_STATIC_AUDIT")
        for item in failures:
            print(f"- {item}")
        return 3

    print("PASS_R0_V02_STATIC_AUDIT")
    print("EXPECTED_FINAL_SOLIDS=2")
    print("EXPECTED_SLOT_SUBTRACTIONS=8")
    print("EXPECTED_PORTS=0")
    print("CENTER_THROUGH_HOLE=NO")
    print("SOLVER_RUN=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
