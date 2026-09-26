#!/usr/bin/env python3
from pathlib import Path
import sys

p=Path("source/cst/R1A5M_ADAPTIVE_SECOND_ORDER_CONFIG_V01.mcr")
if not p.exists():
    print("HOLD_R1A5M_CONFIG_MISSING")
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
    'ChangeSolverType "HF Frequency Domain"',
    '.SetMeshType "Tet"',
    '.Set "CurvatureOrder", "3"',
    'FDSolver.OrderTet "Second"',
    'FDSolver.SetMethod "Tetrahedral", "General purpose"',
    '.SetType "HighFrequencyTet"',
    '.SetAdaptionStrategy "ExpertSystem"',
    '.MinPasses "3"',
    '.MaxPasses "6"',
    '.MaxDeltaS "0.02"',
    '.NumberOfDeltaSChecks "2"',
    '.SetLinearGrowthLimitation "40"',
    'FDSolver.MeshAdaptionTet "True"',
    '.XminSpace "50"', '.XmaxSpace "50"',
    '.YminSpace "50"', '.YmaxSpace "50"',
    '.ZminSpace "50"', '.ZmaxSpace "50"',
)
for x in required:
    if x not in t:
        fail.append("missing:"+x)

if fail:
    print("HOLD_R1A5M_STATIC_AUDIT")
    for x in fail:
        print("- "+x)
    raise SystemExit(3)

print("PASS_R1A5M_STATIC_AUDIT")
print("PHYSICAL_CHANGES=0")
print("SOLVER=HF_FREQUENCY_DOMAIN")
print("MESH=TETRA_SECOND_ORDER_ADAPTIVE")
print("CURVATURE_ORDER=3")
print("METHOD=GENERAL_PURPOSE")
print("ADAPTATION=ON")
print("MIN_PASSES=3")
print("MAX_PASSES=6")
print("MAX_DELTA_S=0.02")
print("DELTA_S_CHECKS=2")
print("FREQ_GHZ=1.0..1.8")
