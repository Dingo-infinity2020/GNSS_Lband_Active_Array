#!/usr/bin/env python3
"""Static audit for R1A2 exact-rotation feed-reference build-only macro."""

from pathlib import Path
import sys

P=Path("source/cst/R1A2_CHARTS_FEED_REFERENCE_BUILD_ONLY_V01.mcr")
if not P.exists():
    print("HOLD_R1A2_MACRO_MISSING"); raise SystemExit(2)

t=P.read_text(encoding="utf-8")
exec_text="\n".join(line for line in t.splitlines() if not line.lstrip().startswith("'"))
fail=[]

for token in ("StartSolver","Solver.Start","Optimizer.","ParameterSweep","DiscretePort",
              "WaveguidePort","LumpedElement","Monitor.","QPL9547"):
    if token in exec_text: fail.append("forbidden:"+token)

required=(
    '.Name "CENTER_GAP_MASTER_N"',
    '.Name "FeedGapReference:CENTER_GAP_MASTER_N"',
    '.Name "TERMINAL_MASTER_NE"',
    '.Name "TerminalReference:TERMINAL_MASTER_NE"',
    '.Angle "0.0", "0.0", "90.0"',
    '.Repetitions "3"',
    '.MultipleObjects "True"',
    'StoreParameter "feed_gap_center_width", 1.20',
    'StoreParameter "terminal_r", 3.00',
)
for x in required:
    if x not in t: fail.append("missing:"+x)

if t.count('With Transform') != 2:
    fail.append("transform_blocks_not_exactly_2")
if t.count('.Repetitions "3"') != 2:
    fail.append("rotation_copy_repetitions_not_exactly_2")
if t.count('.Name "CENTER_GAP_MASTER_N"') != 1:
    fail.append("gap_master_not_unique")
if t.count('.Name "TERMINAL_MASTER_NE"') != 1:
    fail.append("terminal_master_not_unique")

# Reference shapes must not be physically subtracted from the aperture in R1A2.
for x in ("FeedGapReference:", "TerminalReference:"):
    if ('Solid.Subtract "Radiator:ANTENNA_PLATE", "'+x) in t:
        fail.append("reference_geometry_subtracted:"+x)

if fail:
    print("HOLD_R1A2_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)

print("PASS_R1A2_STATIC_AUDIT")
print("MASTER_GAP_COUNT=1")
print("MASTER_TERMINAL_COUNT=1")
print("ROTATION_COPY_BLOCKS=2")
print("ROTATION_ANGLE_DEG=90")
print("ROTATION_REPETITIONS=3")
print("EXPECTED_FINAL_SOLIDS=10")
print("EXPECTED_PORTS=0")
print("SOLVER_RUN=NO")
