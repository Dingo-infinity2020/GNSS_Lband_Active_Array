#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ref=ROOT/"source/cst/R1E1A3R1_SUPPORT_SOLVER_CONFIG_V02.mcr"
new=ROOT/"source/cst/R1E1A4A_H0_P1_BROADSIDE_SOLVER_CONFIG_V01.mcr"
fail=[]
for p in (ref,new):
    if not p.exists(): fail.append("missing:"+str(p))
def effective(text):
    return "\n".join(x.rstrip() for x in text.splitlines()
                     if x.strip() and not x.lstrip().startswith("'"))
if not fail:
    a=effective(ref.read_text(encoding="utf-8"))
    b=effective(new.read_text(encoding="utf-8"))
    if a!=b: fail.append("solver_config_not_numerically_identical")
    for token in ("Brick","Cylinder","Material","DiscretePort","Boundary.","Monitor","Port.Delete","Optimizer"):
        if token in new.read_text(encoding="utf-8"):
            fail.append("forbidden_token:"+token)
if fail:
    print("HOLD_R1E1A4A_BROADSIDE_SOLVE_SOURCE_AUDIT")
    [print("- "+x) for x in fail]
    raise SystemExit(3)
print("PASS_R1E1A4A_BROADSIDE_SOLVE_SOURCE_AUDIT")
print("NUMERICAL_CONFIG=IDENTICAL_TO_QUALIFIED_MAXPASSES12_BASELINE")
print("SOLVE_AUTHORIZED=NO")
