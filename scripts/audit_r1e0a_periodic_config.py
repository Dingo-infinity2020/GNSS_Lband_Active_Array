#!/usr/bin/env python3
from pathlib import Path

p=Path("source/cst/R1E0A_PERIODIC_BROADSIDE_BUILD_ONLY_V01.mcr")
t=p.read_text(encoding="utf-8")
exec_text="\n".join(x for x in t.splitlines() if not x.lstrip().startswith("'"))
fail=[]

for token in (
    "With Brick","With Extrude","With Material","With Transform","Solid.",
    "DiscretePort","WaveguidePort","FloquetPort","LumpedElement",
    "Optimizer.","ParameterSweep","StartSolver","Solver.Start","FDSolver.Start"
):
    if token in exec_text:
        fail.append("forbidden:"+token)

required=(
    'StoreParameter "R1E0_pitch_nominal_mm", 94.0',
    'StoreParameter "R1E0_scan_theta_deg", 0.0',
    'StoreParameter "R1E0_scan_phi_deg", 45.0',
    'ChangeSolverType "HF Frequency Domain"',
    '.Xmin "unit cell"', '.Xmax "unit cell"',
    '.Ymin "unit cell"', '.Ymax "unit cell"',
    '.Zmin "expanded open"', '.Zmax "expanded open"',
    '.OpenAddSpaceFactor "0.5"',
    '.PeriodicUseConstantAngles "False"',
    '.SetPeriodicBoundaryAngles "R1E0_scan_theta_deg", "R1E0_scan_phi_deg"',
    '.SetPeriodicBoundaryAnglesDirection "outward"',
    '.UnitCellFitToBoundingBox "True"',
    '.UnitCellAngle "90.0"',
)
for x in required:
    if x not in t:
        fail.append("missing:"+x)

if fail:
    print("HOLD_R1E0A_STATIC_AUDIT")
    for x in fail:
        print("- "+x)
    raise SystemExit(3)

print("PASS_R1E0A_STATIC_AUDIT")
print("GEOMETRY_CHANGES=0")
print("PORT_CHANGES=0")
print("FLOQUET_PORTS=0")
print("SOLVER_START_COMMANDS=0")
print("X_Y_BOUNDARY=UNIT_CELL")
print("Z_BOUNDARY=EXPANDED_OPEN")
print("PITCH_MODE=FIT_TO_94MM_STRUCTURE_BBOX")
print("THETA_DEG=0")
print("PHI_DEG=45")
print("DIRECTION=OUTWARD")
