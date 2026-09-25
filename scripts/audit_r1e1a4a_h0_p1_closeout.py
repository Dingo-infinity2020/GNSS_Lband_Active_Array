#!/usr/bin/env python3
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
fail=[]
stage=json.loads((ROOT/"execution/stage_contract.json").read_text(encoding="utf-8"))
auth=stage["authorization"]
for k in ("BUILD_AUTHORIZED","SOLVE_AUTHORIZED","production_solve_authorized","cst251_authorized"):
    if auth.get(k) is not False: fail.append("authorization_not_closed:"+k)
ev=ROOT/"evidence/r1e1a4a_h0_p1_b0_nw_20260925_solve01"
for rel in ("FORMAL_STATUS.txt","FINAL_STATUS.txt","QUALIFICATION.md","readonly_summary.json","mixed_mode_2port_readonly.csv","physics_analysis.json"):
    if not (ev/rel).exists(): fail.append("missing_evidence:"+rel)
if (ev/"FINAL_STATUS.txt").exists() and (ev/"FINAL_STATUS.txt").read_text().strip()!="HOLD_R1E1A4A_H0_P1_GATE_R_RNF0":
    fail.append("wrong_final_status")
if (ev/"readonly_summary.json").exists():
    r=json.loads((ev/"readonly_summary.json").read_text())
    if not r["numerical_checks"]["pass"]: fail.append("numerical_not_pass")
    if not r["gate_r_mixed_mode"]["pass"]: fail.append("mixed_mode_not_pass")
shadow=ROOT/"circuit/qpl9547/analysis/R1E1A4A_H0_P1_B0_QPL9547_RECEIVER_SHADOW.json"
if not shadow.exists(): fail.append("missing_receiver_shadow")
else:
    s=json.loads(shadow.read_text())
    if s["r_nf0_both_branches_pass"] is not False: fail.append("r_nf0_not_fail")
if stage["scientific_freeze"].get("canonical_stage_status")!="HOLD_R1E1A4A_H0_P1_GATE_R_RNF0":
    fail.append("stage_status_mismatch")
if stage["scientific_freeze"].get("next_candidate")!="H1A_OFFSET_GROUND_G2P0":
    fail.append("next_candidate_mismatch")
plan=ROOT/"docs/R1E1A4A_H1_LOCAL_GROUND_REDESIGN_PLAN.md"
if not plan.exists(): fail.append("missing_h1_plan")
if fail:
    print("HOLD_R1E1A4A_H0_P1_CLOSEOUT_AUDIT")
    [print("- "+x) for x in fail]
    raise SystemExit(3)
print("PASS_R1E1A4A_H0_P1_CLOSEOUT_AUDIT")
print("NUMERICAL=PASS")
print("MIXED_MODE=PASS")
print("R_NF0=FAIL")
print("NEXT=H1A_OFFSET_GROUND_G2P0_DESIGN_ONLY")
print("BUILD_AUTHORIZED=NO")
print("SOLVE_AUTHORIZED=NO")
