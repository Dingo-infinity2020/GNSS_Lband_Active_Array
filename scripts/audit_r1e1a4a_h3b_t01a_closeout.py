#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
fail=[]
stage=json.loads((ROOT/"execution/stage_contract.json").read_text(encoding="utf-8"))
for k in ("BUILD_AUTHORIZED","SOLVE_AUTHORIZED","production_solve_authorized","lna_integration_authorized","cst251_authorized"):
    if stage["authorization"].get(k) is not False:
        fail.append("authorization_not_closed:"+k)
sf=stage["scientific_freeze"]
if sf.get("numerical_qualification_status")!="HOLD_R1E1A4A_H3B_T01A_ADAPTIVE_MAXPASS8_NOT_CONVERGED":
    fail.append("wrong_numerical_status")
if sf.get("adaptive_passes")!=8:
    fail.append("wrong_pass_count")
if sf.get("pass8_delta_s",0)<=sf.get("max_delta_s_required",0):
    fail.append("pass8_delta_not_above_threshold")
if sf.get("provisional_results_science_qualified") is not False:
    fail.append("provisional_results_should_not_be_qualified")
ev=ROOT/"evidence/r1e1a4a_h3b_t01a_nw_20260925_solve01"
for rel in ("FINAL_STATUS.txt","FORMAL_STATUS.txt","summary.json","sparams.csv","native_adaptation.json","NUMERICAL_QUALIFICATION_ADDENDUM.md"):
    if not (ev/rel).exists(): fail.append("missing:"+rel)
if (ev/"FINAL_STATUS.txt").exists():
    if (ev/"FINAL_STATUS.txt").read_text().strip()!="HOLD_R1E1A4A_H3B_T01A_ADAPTIVE_MAXPASS8_NOT_CONVERGED":
        fail.append("final_status_mismatch")
if (ev/"native_adaptation.json").exists():
    n=json.loads((ev/"native_adaptation.json").read_text())
    if n.get("numerical_convergence_pass") is not False: fail.append("native_should_fail")
    if n.get("max_passes_reached") is not True: fail.append("maxpass_not_recorded")
    if n.get("last_two_below_threshold") is not False: fail.append("last_two_wrong")
if fail:
    print("HOLD_R1E1A4A_H3B_T01A_CLOSEOUT_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H3B_T01A_CLOSEOUT_AUDIT")
print("SOLVER_EXECUTION=PASS")
print("NUMERICAL_QUALIFICATION=HOLD_MAXPASS8_NOT_CONVERGED")
print("PROVISIONAL_SPARAMS=NOT_SCIENCE_QUALIFIED")
print("NEXT=NUMERICAL_RECOVERY_AWAIT_AUTH")
print("ALL_PERMISSIONS=CLOSED")
