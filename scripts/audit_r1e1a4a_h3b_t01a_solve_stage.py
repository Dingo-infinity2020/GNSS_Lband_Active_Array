#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
port=ROOT/"source/cst/R1E1A4A_H3B_T01A_PORTS_V01.mcr"
solver=ROOT/"source/cst/R1E1A4A_H3B_T01A_SOLVER_CONFIG_V01.mcr"
freeze=ROOT/"docs/R1E1A4A_H3B_T01A_PASSIVE_SOLVE_FREEZE_V01.md"
stage=ROOT/"execution/stage_contract.json"
fail=[]
for p in (port,solver,freeze,stage):
    if not p.exists(): fail.append("missing:"+str(p))
pt=port.read_text(encoding="utf-8") if port.exists() else ""
st=solver.read_text(encoding="utf-8") if solver.exists() else ""
checks={
 "two_discrete_ports":pt.count("With DiscretePort")==2,
 "port1_rp1":'.SetP1 "False", "0.0", "12.0", "-0.035"' in pt and '.SetP2 "False", "0.0", "12.0", "1.035"' in pt,
 "port2_rp2":'.SetP1 "False", "0.0", "0.535", "-12.0"' in pt and '.SetP2 "False", "0.0", "-0.535", "-12.0"' in pt,
 "ports_50ohm":'StoreParameter "h3b_t01a_port_z0", 50.0' in pt,
 "port_macro_no_geometry":not re.search(r'\b(Brick|Cylinder|Extrude|Polygon|Solid\.(Add|Subtract|Insert|Intersect))\b',pt),
 "freq_1_2":'Solver.FrequencyRange "1.0", "2.0"' in st,
 "all_open":all(f'.{a} "{b}"' in st for a in ("Xmin","Xmax","Ymin","Ymax","Zmin","Zmax") for b in ["open"] if True),
 "fd_solver":'ChangeSolverType "HF Frequency Domain"' in st,
 "second_order":'FDSolver.OrderTet "Second"' in st,
 "adaptive":'FDSolver.MeshAdaptionTet "True"' in st and '.MinPasses "3"' in st and '.MaxPasses "8"' in st and '.MaxDeltaS "0.02"' in st,
 "solver_macro_no_geometry":not re.search(r'\b(Brick|Cylinder|Extrude|Polygon|Solid\.(Add|Subtract|Insert|Intersect))\b',st),
 "no_start_in_macros":"run_solver" not in pt+st and "Solver.Start" not in pt+st and "FDSolver.Start" not in pt+st,
}
# Fix all_open independently to avoid nested-comprehension ambiguity.
checks["all_open"]=all(f'.{a} "open"' in st for a in ("Xmin","Xmax","Ymin","Ymax","Zmin","Zmax"))
for k,v in checks.items():
    if not v: fail.append("check_failed:"+k)
sc=json.loads(stage.read_text(encoding="utf-8")) if stage.exists() else {}
auth=sc.get("authorization",{})
if auth.get("SOLVE_AUTHORIZED") is not True: fail.append("SOLVE_AUTHORIZED_not_true")
if auth.get("BUILD_AUTHORIZED") is not False: fail.append("BUILD_AUTHORIZED_not_false")
if sc.get("scientific_freeze",{}).get("geometry_changes_allowed") is not False: fail.append("geometry_changes_allowed_not_false")
if fail:
    print("HOLD_R1E1A4A_H3B_T01A_SOLVE_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H3B_T01A_SOLVE_STATIC_AUDIT")
for k in sorted(checks): print(k+"=PASS")
print("SOLVE_AUTHORIZED=YES_ONE_T01A")
print("GEOMETRY_CHANGES=NO")
