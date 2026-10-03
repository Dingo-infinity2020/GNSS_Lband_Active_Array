#!/usr/bin/env python3
from pathlib import Path

p=Path("source/cst/R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr")
t=p.read_text(encoding="utf-8")
exec_text="\n".join(x for x in t.splitlines() if not x.lstrip().startswith("'"))
fail=[]

for token in (
    "With Boundary","Boundary.","SetPeriodicBoundaryAngles","UnitCell",
    "With Brick","With Extrude","With Material","With Transform","Solid.",
    "DiscretePort","WaveguidePort","FloquetPort","LumpedElement",
    "Optimizer.","ParameterSweep","StartSolver","Solver.Start","FDSolver.Start",
    "PostProcess1D"
):
    if token in exec_text:
        fail.append("forbidden:"+token)

required=(
    'Solver.FrequencyRange "1.0", "1.8"',
    'ChangeSolverType "HF Frequency Domain"',
    '.SetMeshType "Tet"',
    '.Set "CurvatureOrder", "3"',
    'FDSolver.OrderTet "Second"',
    'FDSolver.SetMethod "Tetrahedral", "General purpose"',
    '.SetType "HighFrequencyTet"',
    '.SetAdaptionStrategy "ExpertSystem"',
    '.MinPasses "3"',
    '.MaxPasses "8"',
    '.MaxDeltaS "0.02"',
    '.NumberOfDeltaSChecks "2"',
    '.SetLinearGrowthLimitation "40"',
    'FDSolver.MeshAdaptionTet "True"',
)
for x in required:
    if x not in t:
        fail.append("missing:"+x)

if fail:
    print("HOLD_R1E0C_B_SCAN_SOLVER_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)

print("PASS_R1E0C_B_SCAN_SOLVER_STATIC_AUDIT")
print("BOUNDARY_COMMANDS=0")
print("GEOMETRY_CHANGES=0")
print("PORT_CHANGES=0")
print("POSTPROCESS_YZ=0")
print("SOLVER_START_COMMANDS=0")
print("SOLVER=HF_FREQUENCY_DOMAIN")
print("MESH=TETRA_SECOND_ORDER_ADAPTIVE")
print("FREQ_GHZ=1.0..1.8")
