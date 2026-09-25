#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
fail=[]
stage=json.loads((ROOT/"execution/stage_contract.json").read_text(encoding="utf-8"))
for k in ("BUILD_AUTHORIZED","SOLVE_AUTHORIZED","production_solve_authorized","lna_integration_authorized","cst251_authorized"):
    if stage["authorization"].get(k) is not False: fail.append("authorization_not_closed:"+k)
if stage["scientific_freeze"].get("h2a_status")!="PASS_R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY":
    fail.append("wrong_h2a_status")
if stage["scientific_freeze"].get("h2a_artifact_sha256")!="b8f9161d7530b194fec1f35cc69f3cb5c770fb9daaba8eaeb519fbf064da644b":
    fail.append("wrong_hash")
ev=ROOT/"evidence/r1e1a4a_h2a_nw_20260925_build01"
for rel in ("FINAL_STATUS.txt","QUALIFICATION.md","summary.json","reopen_shapes.txt","reopen_status.txt"):
    if not (ev/rel).exists(): fail.append("missing:"+rel)
if (ev/"FINAL_STATUS.txt").exists() and (ev/"FINAL_STATUS.txt").read_text().strip()!="PASS_R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY":
    fail.append("final_status_mismatch")
if (ev/"summary.json").exists():
    s=json.loads((ev/"summary.json").read_text())
    if not s["checks"]["pass"]: fail.append("summary_not_pass")
    if s["solver_run"] is not False: fail.append("solver_run_not_false")
if not (ROOT/"docs/R1E1A4A_H2A_3D_REVIEW_GUIDE.md").exists(): fail.append("review_guide_missing")
if fail:
    print("HOLD_R1E1A4A_H2A_CLOSEOUT_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H2A_CLOSEOUT_AUDIT")
print("BUILD=PASS")
print("SOLVER=NOT_RUN")
print("NEXT=HUMAN_3D_REVIEW")
print("ALL_PERMISSIONS=CLOSED")
