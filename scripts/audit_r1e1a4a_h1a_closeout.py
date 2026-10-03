#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
fail=[]
stage=json.loads((ROOT/"execution/stage_contract.json").read_text(encoding="utf-8"))
auth=stage["authorization"]
for k in ("BUILD_AUTHORIZED","SOLVE_AUTHORIZED","production_solve_authorized","cst251_authorized"):
    if auth.get(k) is not False:
        fail.append("authorization_not_closed:"+k)

ev=ROOT/"evidence/r1e1a4a_h1a_b0_nw_20260925_solve01"
for rel in ("FORMAL_STATUS.txt","FINAL_STATUS.txt","QUALIFICATION.md","summary.json","mixed_mode_2port.csv"):
    if not (ev/rel).exists(): fail.append("missing_evidence:"+rel)

if (ev/"FINAL_STATUS.txt").exists():
    if (ev/"FINAL_STATUS.txt").read_text().strip()!="HOLD_R1E1A4A_H1A_BROADSIDE_NUMERICAL_MAXPASSES":
        fail.append("wrong_final_status")

if (ev/"summary.json").exists():
    s=json.loads((ev/"summary.json").read_text())
    if s["numerical_checks"]["pass"] is not False: fail.append("numerical_should_fail")
    if s["native"]["maxpasses"] is not True: fail.append("maxpasses_not_true")
    if abs(s["native"]["delta_s_sequence"][-1]["delta_s"]-0.0213176)>1e-9:
        fail.append("unexpected_final_delta_s")
    if s["native"]["broadband_converged"] is not True:
        fail.append("broadband_not_converged")

sf=stage["scientific_freeze"]
if sf.get("h1a_solve_status")!="HOLD_R1E1A4A_H1A_BROADSIDE_NUMERICAL_MAXPASSES":
    fail.append("stage_h1a_status_mismatch")
if sf.get("next_stage")!="R1E1A4A_H1R_NUMERICAL_RECOVERY_DESIGN":
    fail.append("next_stage_mismatch")
if sf.get("sole_future_solver_change")!="MaxPasses_12_to_16":
    fail.append("recovery_change_mismatch")

for rel in ("docs/R1E1A4A_H1R_NUMERICAL_RECOVERY_PLAN.md",
            "docs/R1E1A4A_H1A_MODEL_VISUAL_GUIDE.md"):
    if not (ROOT/rel).exists(): fail.append("missing:"+rel)

if fail:
    print("HOLD_R1E1A4A_H1A_CLOSEOUT_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)

print("PASS_R1E1A4A_H1A_CLOSEOUT_AUDIT")
print("H1A_BUILD=PASS_CANONICAL")
print("H1A_SOLVE=HOLD_NUMERICAL_MAXPASSES")
print("FINAL_DELTA_S=0.0213176")
print("BROADBAND=PASS")
print("PROVISIONAL_PHYSICS=NONAUTHORITATIVE")
print("NEXT=H1R_NUMERICAL_RECOVERY_DESIGN_ONLY")
print("BUILD_AUTHORIZED=NO")
print("SOLVE_AUTHORIZED=NO")
