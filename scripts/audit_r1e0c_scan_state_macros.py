#!/usr/bin/env python3
from pathlib import Path
import importlib.util

gp=Path("scripts/generate_r1e0c_scan_state_macros.py")
spec=importlib.util.spec_from_file_location("r1e0cgen",str(gp))
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
expected=mod.expected()
fail=[]

for state,theta,phi in mod.STATES:
    p=Path("source/cst")/("R1E0C_%s_SCANSTATE_BUILD_ONLY_V01.mcr"%state)
    if not p.exists():
        fail.append("missing:"+str(p)); continue
    t=p.read_text(encoding="utf-8").replace("\r\n","\n")
    if t != expected[state].replace("\r\n","\n"):
        fail.append("generator_mismatch:"+state)
    exec_text="\n".join(x for x in t.splitlines() if not x.lstrip().startswith("'"))
    for token in (
      '.Xmin ','.Xmax ','.Ymin ','.Ymax ','.Zmin ','.Zmax ',
      'UnitCellFitToBoundingBox','UnitCellDs1','UnitCellDs2','UnitCellAngle',
      'With Brick','With Extrude','With Material','With Transform','Solid.',
      'DiscretePort','WaveguidePort','FloquetPort','LumpedElement',
      'ChangeSolverType','FDSolver.','MeshSettings','MeshAdaption3D',
      'Optimizer.','ParameterSweep','StartSolver','Solver.Start'
    ):
        if token in exec_text:
            fail.append(state+":forbidden:"+token)
    req=(
      'StoreParameter "R1E0_scan_theta_deg", %s'%theta,
      'StoreParameter "R1E0_scan_phi_deg", %s'%phi,
      '.SetPeriodicBoundaryAngles "R1E0_scan_theta_deg", "R1E0_scan_phi_deg"',
      '.SetPeriodicBoundaryAnglesDirection "outward"',
    )
    for x in req:
        if x not in t: fail.append(state+":missing:"+x)

if fail:
    print("HOLD_R1E0C_SCAN_MACRO_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)

print("PASS_R1E0C_SCAN_MACRO_STATIC_AUDIT")
print("STATE_COUNT=4")
print("C30P45=30,45")
print("C45P45=45,45")
print("C60P45=60,45")
print("C60P135=60,135")
print("BOUNDARY_TYPE_CHANGES=0")
print("GEOMETRY_CHANGES=0")
print("PORT_CHANGES=0")
print("SOLVER_COMMANDS=0")
