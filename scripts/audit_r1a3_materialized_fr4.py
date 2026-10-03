#!/usr/bin/env python3
"""Static audit for R1A3 materialized FR4 build-only macro."""
from pathlib import Path
import sys

P=Path("source/cst/R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr")
if not P.exists():
    print("HOLD_R1A3_MACRO_MISSING")
    raise SystemExit(2)

t=P.read_text(encoding="utf-8")
exec_text="\n".join(line for line in t.splitlines() if not line.lstrip().startswith("'"))
fail=[]

for token in ("StartSolver","Solver.Start","Optimizer.","ParameterSweep","DiscretePort",
              "WaveguidePort","LumpedElement","Monitor.","QPL9547"):
    if token in exec_text:
        fail.append("forbidden:"+token)

required=(
    '.Name "FR4_COST_BASELINE"',
    'StoreParameter "fr4_er", 4.2',
    'StoreParameter "fr4_tand", 0.018',
    'StoreParameter "substrate_t", 1.00',
    'StoreParameter "copper_t", 0.035',
    '.Name "FR4_BOARD"',
    '.Name "TOP_COPPER"',
    'For p=0 To 1',
    'For i=0 To 11',
    '.Name "CENTER_CROSS_MASTER_N"',
    '.Name "RING_GAP_MASTER_N"',
    '.Angle "0.0", "0.0", "90.0"',
    '.Repetitions "3"',
    'Solid.Subtract "TopCopper:TOP_COPPER", toolName',
)
for x in required:
    if x not in t:
        fail.append("missing:"+x)

if t.count("With Transform") != 2:
    fail.append("transform_blocks_not_exactly_2")
if t.count('.Repetitions "3"') != 2:
    fail.append("rotation_repetitions_not_exactly_2")
if t.count('.Name "CENTER_CROSS_MASTER_N"') != 1:
    fail.append("center_cross_master_not_unique")
if t.count('.Name "RING_GAP_MASTER_N"') != 1:
    fail.append("ring_gap_master_not_unique")
if "TerminalReference" in exec_text or "TERMINAL_MASTER" in exec_text:
    fail.append("terminal_reference_solids_forbidden_in_r1a3")
if "FR4_BOARD" not in t or "TOP_COPPER" not in t:
    fail.append("physical_layers_missing")

if fail:
    print("HOLD_R1A3_STATIC_AUDIT")
    for x in fail:
        print("- "+x)
    raise SystemExit(3)

print("PASS_R1A3_STATIC_AUDIT")
print("THROUGH_SLOT_COORDINATES=12")
print("THROUGH_SLOT_LAYER_APPLICATIONS=2")
print("CENTER_CROSS_MASTER=1")
print("RING_GAP_MASTER=1")
print("ROTATION_COPY_BLOCKS=2")
print("ROTATION_ANGLE_DEG=90")
print("ROTATION_REPETITIONS=3")
print("PORTS=0")
print("SOLVER_RUN=NO")
