#!/usr/bin/env python3
from pathlib import Path
import sys

p=Path("source/cst/R1A5R_SECOND_ORDER_SOLVER_CONFIG_V01.mcr")
t=p.read_text(encoding="utf-8")
exec_text="\n".join(x for x in t.splitlines() if not x.lstrip().startswith("'"))
fail=[]

for token in (
    "With Brick","With Extrude","With Material","With Transform","Solid.",
    "DiscretePort","WaveguidePort","LumpedElement",
    "Optimizer.","ParameterSweep","StartSolver","Solver.Start"
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
    'FDSolver.MeshAdaptionTet "False"',
    '.XminSpace "50"', '.XmaxSpace "50"',
    '.YminSpace "50"', '.YmaxSpace "50"',
    '.ZminSpace "50"', '.ZmaxSpace "50"',
)
for x in required:
    if x not in t:
        fail.append("missing:"+x)

if fail:
    print("HOLD_R1A5R_STATIC_AUDIT")
    for x in fail:
        print("- "+x)
    raise SystemExit(3)

print("PASS_R1A5R_STATIC_AUDIT")
print("PHYSICAL_CHANGES=0")
print("SOLVER=HF_FREQUENCY_DOMAIN")
print("MESH=TETRA_SECOND_ORDER")
print("CURVATURE_ORDER=3")
print("METHOD=GENERAL_PURPOSE")
print("ADAPTATION=OFF")
print("FREQ_GHZ=1.0..1.8")
