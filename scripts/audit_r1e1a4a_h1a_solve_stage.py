#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
run=ROOT/"scripts/run_r1e1a4a_h1a_broadside_solve_dc.py"
cfg=ROOT/"source/cst/R1E1A4A_H1A_BROADSIDE_SOLVER_CONFIG_V01.mcr"
ref=ROOT/"source/cst/R1E1A3R1_SUPPORT_SOLVER_CONFIG_V02.mcr"
stage=ROOT/"execution/stage_contract.json"
ev=ROOT/"evidence/r1e1a4a_h1a_nw_20260925_build01/FINAL_STATUS.txt"
fail=[]
for p in (run,cfg,ref,stage,ev):
    if not p.exists(): fail.append("missing:"+str(p))
def effective(text):
    return "\n".join(x.rstrip() for x in text.splitlines()
                     if x.strip() and not x.lstrip().startswith("'"))
if cfg.exists() and ref.exists() and effective(cfg.read_text(encoding="utf-8"))!=effective(ref.read_text(encoding="utf-8")):
    fail.append("solver_config_not_identical_to_qualified_maxpasses12")
rt=run.read_text(encoding="utf-8") if run.exists() else ""
for token in (
 'SOURCE_SHA="b903d678a7039105ad4d91bea2f82e9c1e5e9f8bbf5a5977360c85e34ced3b94"',
 "prj.modeler.run_solver()","read_2port","mixed_row","gate_r",
 "comparison_vs_h0","comparison_vs_p0","receiver_shadow",
 "snapshot_tree","restore_snapshot",
):
    if token not in rt: fail.append("harness_missing:"+token)
sc=json.loads(stage.read_text(encoding="utf-8")) if stage.exists() else {}
a=sc.get("authorization",{})
if a.get("BUILD_AUTHORIZED") is not False: fail.append("BUILD_AUTHORIZED_not_false")
if a.get("SOLVE_AUTHORIZED") is not True: fail.append("SOLVE_AUTHORIZED_not_true")
if a.get("production_solve_authorized") is not True: fail.append("production_solve_authorized_not_true")
if a.get("cst251_authorized") is not False: fail.append("cst251_authorized_not_false")
if ev.exists() and ev.read_text().strip()!="PASS_R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY_READONLY_RECOVERY":
    fail.append("canonical_build_not_pass")
if fail:
    print("HOLD_R1E1A4A_H1A_SOLVE_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H1A_SOLVE_STATIC_AUDIT")
print("SOURCE_HASH=LOCKED")
print("SOLVER_CONFIG=QUALIFIED_MAXPASSES12_IDENTICAL")
print("BUILD_CANONICAL=PASS")
print("SOLVE_AUTHORIZED=YES_ONE_H1A_BROADSIDE")
