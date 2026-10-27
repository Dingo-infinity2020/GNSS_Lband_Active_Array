#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
run=ROOT/"scripts/run_r1e1a4a_h0_p1_broadside_solve_dc.py"
cfg=ROOT/"source/cst/R1E1A4A_H0_P1_BROADSIDE_SOLVER_CONFIG_V01.mcr"
ref=ROOT/"source/cst/R1E1A3R1_SUPPORT_SOLVER_CONFIG_V02.mcr"
contract=ROOT/"docs/R1E1A4A_H0_P1_BROADSIDE_SOLVE_CONTRACT_DRAFT.md"
stage=ROOT/"execution/stage_contract.json"
fail=[]
for p in (run,cfg,ref,contract,stage):
    if not p.exists(): fail.append("missing:"+str(p))
rt=run.read_text(encoding="utf-8") if run.exists() else ""
ct=contract.read_text(encoding="utf-8") if contract.exists() else ""
def effective(text):
    return "\n".join(x.rstrip() for x in text.splitlines()
                     if x.strip() and not x.lstrip().startswith("'"))
if cfg.exists() and ref.exists() and effective(cfg.read_text(encoding="utf-8"))!=effective(ref.read_text(encoding="utf-8")):
    fail.append("solver_config_not_identical_to_qualified_maxpasses12")
for token in (
    'SOURCE_SHA="d1ebb6f4a6e8b48f3484cc5459790dd5c9bbd29482832c491076c84f783b3deb"',
    'prj.modeler.run_solver()',
    'S1,1','S1,2','S2,1','S2,2',
    'sdd=(s11-s12-s21+s22)/2.0',
    'sdc=(s11+s12-s21-s22)/2.0',
    'scd=(s11-s12+s21-s22)/2.0',
    'scc=(s11+s12+s21+s22)/2.0',
    'Zbranch1' if False else 'zb1=z[0][0]-z[0][1]',
    'zb2=z[1][1]-z[1][0]',
    'max_sdc_db',
    'max_scd_db',
    'branch_symmetry_pass',
    'snapshot_tree',
    'restore_snapshot',
):
    if token not in rt: fail.append("harness_missing:"+token)
contract_tokens=(
    "one formal broadside invocation",
    "sdd = (s11-s12-s21+s22)/2",
    "zbranch1 = z11-z12",
    "no silent retry or pass-count increase",
)
ctl=ct.lower()
for token in contract_tokens:
    if token not in ctl: fail.append("contract_missing:"+token)
sc=json.loads(stage.read_text(encoding="utf-8")) if stage.exists() else {}
a=sc.get("authorization",{})
if a.get("BUILD_AUTHORIZED") is not False: fail.append("BUILD_AUTHORIZED_not_false")
if a.get("SOLVE_AUTHORIZED") is not True: fail.append("SOLVE_AUTHORIZED_not_true")
if a.get("production_solve_authorized") is not True: fail.append("production_solve_authorized_not_true")
if a.get("cst251_authorized") is not False: fail.append("cst251_authorized_not_false")
if fail:
    print("HOLD_R1E1A4A_BROADSIDE_SOLVE_STATIC_AUDIT")
    [print("- "+x) for x in fail]
    raise SystemExit(3)
print("PASS_R1E1A4A_BROADSIDE_SOLVE_STATIC_AUDIT")
print("SOURCE_HASH=LOCKED")
print("SOLVER_CONFIG=QUALIFIED_MAXPASSES12_IDENTICAL")
print("MIXED_MODE_FORMULAS=FROZEN")
print("BUILD_AUTHORIZED=NO")
print("SOLVE_AUTHORIZED=YES_ONE_BROADSIDE")
