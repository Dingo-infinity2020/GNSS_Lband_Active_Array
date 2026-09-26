#!/usr/bin/env python3
"""Static SimulationOps audit for R1A1 CHARTS scaled-aperture build-only macro."""

from __future__ import annotations
import argparse
from pathlib import Path

FORBIDDEN = (
    "StartSolver", "Solver.Start", "Optimizer.", "ParameterSweep", "Sweep.",
    "AdaptiveMesh", "DiscretePort", "WaveguidePort", "LumpedElement", "Monitor.",
    "QPL9547", "LNA", "Rogers_4350B", "FR-4", "FR4",
)

REQUIRED = (
    'StoreParameter "scale_factor", 0.285714285714',
    'StoreParameter "src_board_span", 247.5',
    'StoreParameter "src_outer_slot_frame_span", 227.5',
    'StoreParameter "src_height_ground", 200.0',
    'StoreParameter "unit_cell_pitch_nominal", 94.0',
    '.Name "UNITCELL_GROUND_REFERENCE"',
    '.Name "ANTENNA_PLATE"',
)

OUTER = (
    "CUT_OUTER_N_L","CUT_OUTER_N_R","CUT_OUTER_S_L","CUT_OUTER_S_R",
    "CUT_OUTER_W_D","CUT_OUTER_W_U","CUT_OUTER_E_D","CUT_OUTER_E_U",
)
INNER = ("CUT_INNER_N","CUT_INNER_S","CUT_INNER_E","CUT_INNER_W")

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("macro", nargs="?", default="source/cst/R1A1_CHARTS_SCALED_APERTURE_BUILD_ONLY_V01.mcr")
    args=ap.parse_args()
    p=Path(args.macro)
    if not p.exists():
        print("HOLD_R1A1_MACRO_MISSING"); return 2
    t=p.read_text(encoding="utf-8")
    executable="\n".join(line for line in t.splitlines() if not line.lstrip().startswith("'"))
    failures=[]
    for x in FORBIDDEN:
        if x in executable: failures.append(f"forbidden_token:{x}")
    for x in REQUIRED:
        if x not in t: failures.append(f"missing_marker:{x}")
    for n in OUTER+INNER:
        if f'.Name "{n}"' not in t: failures.append(f"missing_slot:{n}")
    nsub=t.count('Solid.Subtract "Radiator:ANTENNA_PLATE"')
    if nsub != 12: failures.append(f"slot_subtractions={nsub},expected=12")
    if "Sub Main()" not in t or "End Sub" not in t: failures.append("missing_flat_main")
    helpers=[line.strip() for line in t.splitlines()
             if line.strip().lower().startswith(("sub ","function "))
             and line.strip().lower()!="sub main()"]
    if helpers: failures.append("helper_procedure_present:"+",".join(helpers))
    non_ascii=sorted({ch for ch in t if ord(ch)>127})
    if non_ascii: failures.append("non_ascii_present:"+repr(non_ascii))
    if failures:
        print("HOLD_R1A1_MACRO_STATIC_AUDIT")
        for f in failures: print("- "+f)
        return 3
    print("PASS_R1A1_MACRO_STATIC_AUDIT")
    print("EXPECTED_FINAL_SOLIDS=2")
    print("EXPECTED_OUTER_SLOT_SEGMENTS=8")
    print("EXPECTED_INNER_SLOT_SEGMENTS=4")
    print("EXPECTED_SLOT_SUBTRACTIONS=12")
    print("EXPECTED_PORTS=0")
    print("SOLVER_RUN=NO")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
