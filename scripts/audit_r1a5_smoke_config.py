#!/usr/bin/env python3
"""Static audit for R1A5 solver-only smoke configuration."""
from pathlib import Path
import sys

p=Path("source/cst/R1A5_SMOKE_SOLVER_CONFIG_V01.mcr")
if not p.exists():
    print("HOLD_R1A5_CONFIG_MISSING")
    raise SystemExit(2)

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
    '.Xmin "open"', '.Xmax "open"',
    '.Ymin "open"', '.Ymax "open"',
    '.Zmin "open"', '.Zmax "open"',
    '.XminSpace "50"', '.XmaxSpace "50"',
    '.YminSpace "50"', '.YmaxSpace "50"',
    '.ZminSpace "50"', '.ZmaxSpace "50"',
    'ChangeSolverType "HF Frequency Domain"',
    'FDSolver.OrderTet "First"',
    'FDSolver.MeshAdaptionTet "False"',
)
for x in required:
    if x not in t:
        fail.append("missing:"+x)

if fail:
    print("HOLD_R1A5_STATIC_AUDIT")
    for x in fail:
        print("- "+x)
    raise SystemExit(3)

print("PASS_R1A5_STATIC_AUDIT")
print("CONFIG_ONLY=YES")
print("GEOMETRY_COMMANDS=0")
print("PORT_COMMANDS=0")
print("SOLVER=HF_FREQUENCY_DOMAIN")
print("MESH=TETRA_FIRST_ORDER")
print("ADAPTATION=OFF")
print("FREQ_GHZ=1.0..1.8")
print("BACKGROUND_SPACE_MM=50")
