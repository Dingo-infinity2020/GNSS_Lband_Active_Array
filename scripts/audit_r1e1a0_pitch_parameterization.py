#!/usr/bin/env python3
from pathlib import Path

SHA="48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223"
files={
 "harness":Path("scripts/run_r1e1a0_pitch_parameterization_build_only_dc.py"),
 "contract":Path("docs/R1E1A0_PITCH_PARAMETERIZATION_CONTRACT.md"),
 "runbook":Path("em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E1A0_PITCH_PARAMETERIZATION_BUILD_ONLY.md"),
 "plan":Path("docs/R1E1_PITCH_MATERIAL_TRADE_PLAN.md"),
}
fail=[]
texts={}
for k,p in files.items():
    if not p.exists(): fail.append("missing:"+str(p)); continue
    texts[k]=p.read_text(encoding="utf-8")

for k in ("harness","contract","runbook"):
    if k in texts and SHA not in texts[k]: fail.append(k+":source_sha_mismatch_or_missing")

h=texts.get("harness","")
for req in (
    'ENDPOINTS=[("P088",88.0),("P100",100.0)]',
    "prj.schematic.execute_vba_code(pitch_update_vba(pitch))",
    'StoreParameter "unit_cell_pitch_nominal", "%g"',
    "RebuildForParametricChange",
    "project.schematic.execute_vba_code" if False else "execute_vba_code",
    "no_pitch_history_warning",
    "no_solver_markers",
    "no_solver_result_items",
):
    if req not in h: fail.append("harness_missing:"+req)

for forbidden in (
    ".add_to_history(",
    "full_history_rebuild(",
    ".run_solver(",
    ".start_solver(",
    "Solver.Start",
    "FDSolver.Start",
    "Optimizer.",
    "ParameterSweep",
):
    if forbidden in h: fail.append("harness_forbidden:"+forbidden)

for token in ("With Brick",".Create","Solid.Subtract","Solid.Union","Material.Create","DiscretePort"):
    if token in h: fail.append("harness_geometry_or_port_mutation:"+token)

c=texts.get("contract","")
for req in ("RebuildForParametricChange","88 mm","100 mm","BUILD NOT AUTHORIZED","No solver"):
    if req not in c: fail.append("contract_missing:"+req)

r=texts.get("runbook","")
for req in ("RebuildForParametricChange","P088: 88.0 mm","P100: 100.0 mm","BUILD NOT AUTHORIZED","No solver"):
    if req not in r: fail.append("runbook_missing:"+req)

p=texts.get("plan","")
for req in ("88 mm","90 mm","92 mm","94 mm","96 mm","100 mm","RebuildForParametricChange"):
    if req not in p: fail.append("plan_missing:"+req)

if fail:
    print("HOLD_R1E1A0_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)

print("PASS_R1E1A0_STATIC_AUDIT")
print("SOURCE_SHA="+SHA)
print("ENDPOINTS=88,100")
print("PARAMETER_MUTATION=DIRECT_VBA_PARAMETER_LIST")
print("REBUILD=RebuildForParametricChange")
print("ADD_TO_HISTORY=0")
print("FULL_HISTORY_REBUILD=0")
print("GEOMETRY_COMMANDS=0")
print("PORT_CHANGES=0")
print("SOLVER_COMMANDS=0")
