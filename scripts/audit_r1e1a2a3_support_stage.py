#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
b=ROOT/"scripts/run_r1e1a2_support_build_only_dc.py"
s=ROOT/"scripts/run_r1e1a3_support_solve_dc.py"
c=ROOT/"docs/R1E1A2A3_SUPPORT_SENSITIVITY_CONTRACT.md"
m=ROOT/"em/cst/R1_CHARTS_LBAND/materials_r1e1a2_support.csv"
fail=[]
for p in (b,s,c,m):
    if not p.exists(): fail.append("missing:"+str(p))
bt=b.read_text(encoding="utf-8") if b.exists() else ""
st=s.read_text(encoding="utf-8") if s.exists() else ""
ct=c.read_text(encoding="utf-8") if c.exists() else ""
for x in ("fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e","S1_BONDED_B0","S1_BONDED_C60P45","S1_BONDED_C60P135","S4_PEC_B0"):
    if x not in bt and x not in ct: fail.append("missing_freeze:"+x)
for x in ("run_solver(","Solver.Start","FDSolver.Start","start_solver("):
    if x in bt: fail.append("build_forbidden:"+x)
for x in ('comp["max_complex_delta_s11"]<=0.05','comp["max_abs_delta_zactive_ohm"]<=10.0'):
    if x not in st: fail.append("solve_gate_missing:"+x)
if "prj.modeler.run_solver()" not in st: fail.append("solve_invocation_missing")
if fail:
    print("HOLD_R1E1A2A3_STATIC_AUDIT")
    [print("- "+x) for x in fail]
    raise SystemExit(3)
print("PASS_R1E1A2A3_STATIC_AUDIT")
print("BUILD_MATRIX=4")
print("SOLVE_MATRIX=4_ONE_SHOT")
print("S1_GATE=DELTA_S11_0.05_AND_DELTA_Z_10OHM")
