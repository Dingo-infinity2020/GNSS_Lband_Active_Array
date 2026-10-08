#!/usr/bin/env python3
"""Static audit for the R1A4 port-only CST macro."""
from pathlib import Path
import sys

p=Path("source/cst/R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.mcr")
if not p.exists():
    print("HOLD_R1A4_PORT_MACRO_MISSING")
    raise SystemExit(2)

t=p.read_text(encoding="utf-8")
exec_text="\n".join(x for x in t.splitlines() if not x.lstrip().startswith("'"))
fail=[]

for token in ("StartSolver","Solver.Start","FDSolver.Start","Optimizer.","ParameterSweep",
              "With Brick","With Extrude","With Material","With Transform",
              "Solid.","LumpedElement","WaveguidePort","Monitor."):
    if token in exec_text:
        fail.append("forbidden:"+token)

required=(
    'StoreParameter "port_ref_impedance", 100.0',
    'StoreParameter "port_terminal_xy", "terminal_r*port_s2"',
    'StoreParameter "port_terminal_z", "copper_top_z"',
    '.PortNumber "1"',
    '.PortNumber "2"',
    '.Type "SParameter"',
    '.Impedance "port_ref_impedance"',
    '.SetP1 "False", "port_terminal_xy", "port_terminal_xy", "port_terminal_z"',
    '.SetP2 "False", "-port_terminal_xy", "-port_terminal_xy", "port_terminal_z"',
    '.SetP1 "False", "-port_terminal_xy", "port_terminal_xy", "port_terminal_z"',
    '.SetP2 "False", "port_terminal_xy", "-port_terminal_xy", "port_terminal_z"',
)
for x in required:
    if x not in t:
        fail.append("missing:"+x)

if t.count("With DiscretePort") != 2:
    fail.append("discrete_port_blocks_not_2")
if t.count('.Type "SParameter"') != 2:
    fail.append("sparameter_type_count_not_2")
if t.count('.Create') != 2:
    fail.append("port_create_count_not_2")

if fail:
    print("HOLD_R1A4_STATIC_AUDIT")
    for x in fail:
        print("- "+x)
    raise SystemExit(3)

print("PASS_R1A4_STATIC_AUDIT")
print("PORT_ONLY_MACRO=YES")
print("DISCRETE_PORT_COUNT=2")
print("PORT_REFERENCE_OHM=100")
print("POL_A=NE_TO_SW")
print("POL_B=NW_TO_SE")
print("POL_B_RELATION=RZ_PLUS_90_OF_POL_A")
print("GEOMETRY_COMMANDS=0")
print("SOLVER_RUN=NO")
