#!/usr/bin/env python3
"""Static audit for R1A5F split single-port generated macros."""
from __future__ import print_function
from pathlib import Path
import importlib.util
import math
import sys

gen_path=Path("scripts/generate_r1a5f_single_port_macros.py")
spec=importlib.util.spec_from_file_location("r1a5f_gen",str(gen_path))
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

files={
  "A":Path("source/cst/R1A5F_POLA_SINGLE_PORT_BUILD_ONLY_V01.mcr"),
  "B":Path("source/cst/R1A5F_POLB_SINGLE_PORT_BUILD_ONLY_V01.mcr"),
}
expected=mod.expected()
fail=[]

for key,p in files.items():
    if not p.exists():
        fail.append("missing:"+str(p))
        continue
    t=p.read_text(encoding="utf-8").replace("\r\n","\n")
    if t != expected[key].replace("\r\n","\n"):
        fail.append("not_generator_exact:"+str(p))
    exec_text="\n".join(x for x in t.splitlines() if not x.lstrip().startswith("'"))
    for token in (
      "With Brick","With Extrude","With Material","With Transform","Solid.",
      "WaveguidePort","LumpedElement","Optimizer.","ParameterSweep",
      "StartSolver","Solver.Start","FDSolver.Start","Monitor."
    ):
        if token in exec_text:
            fail.append(key+":forbidden:"+token)
    if t.count("With DiscretePort") != 1:
        fail.append(key+":discrete_port_block_count")
    if t.count('.PortNumber "1"') != 1:
        fail.append(key+":port_number_count")
    if t.count(".Create") != 1:
        fail.append(key+":create_count")

b1=mod.rot90(mod.A_P1)
b2=mod.rot90(mod.A_P2)
if b1 != (-1,+1) or b2 != (+1,-1):
    fail.append("rotation_math_failed")

if fail:
    print("HOLD_R1A5F_STATIC_AUDIT")
    for x in fail:
        print("- "+x)
    raise SystemExit(3)

print("PASS_R1A5F_STATIC_AUDIT")
print("GENERATOR_EXACT=YES")
print("MODEL_A=NE_TO_SW")
print("MODEL_B=NW_TO_SE")
print("MODEL_B_RELATION=RZ_PLUS_90_OF_A")
print("PORTS_PER_MODEL=1")
print("GEOMETRY_COMMANDS=0")
print("SOLVER_COMMANDS=0")
