#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
port=(ROOT/"source/cst/R1E1A4A_H3B_T01A_PORTS_V01.mcr").read_text()
solver=(ROOT/"source/cst/R1E1A4A_H3B_T01A_SOLVER_CONFIG_MAXPASS16_V01.mcr").read_text()
stage=json.loads((ROOT/"execution/stage_contract.json").read_text())
fail=[]
checks={
 "two_ports":port.count("With DiscretePort")==2,
 "ports_50":'StoreParameter "h3b_t01a_port_z0", 50.0' in port,
 "maxpass16":'.MaxPasses "16"' in solver,
 "mindelta_frozen":'.MinPasses "3"' in solver and '.MaxDeltaS "0.02"' in solver and '.NumberOfDeltaSChecks "2"' in solver,
 "freq_frozen":'Solver.FrequencyRange "1.0", "2.0"' in solver,
 "second_order":'FDSolver.OrderTet "Second"' in solver,
 "no_geometry":not re.search(r'\b(Brick|Cylinder|Extrude|Polygon|Solid\.(Add|Subtract|Insert|Intersect))\b',port+solver),
 "no_start_in_macros":"Solver.Start" not in port+solver and "FDSolver.Start" not in port+solver
}
for k,v in checks.items():
    if not v: fail.append(k)
a=stage["authorization"]
if a.get("SOLVE_AUTHORIZED") is not True: fail.append("solve_not_authorized")
if a.get("BUILD_AUTHORIZED") is not False: fail.append("build_not_closed")
if stage["scientific_freeze"].get("geometry_changes_allowed") is not False: fail.append("geometry_not_frozen")
if fail:
    print("HOLD_R1E1A4A_H3B_T01A_RECOVERY_STATIC_AUDIT")
    print("\n".join("- "+x for x in fail)); raise SystemExit(3)
print("PASS_R1E1A4A_H3B_T01A_RECOVERY_STATIC_AUDIT")
for k in sorted(checks): print(k+"=PASS")
