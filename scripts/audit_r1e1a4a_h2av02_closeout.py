#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
fail=[]
stage=json.loads((ROOT/"execution/stage_contract.json").read_text(encoding="utf-8"))
for k in ("BUILD_AUTHORIZED","SOLVE_AUTHORIZED","production_solve_authorized","lna_integration_authorized","cst251_authorized"):
    if stage["authorization"].get(k) is not False: fail.append("authorization_not_closed:"+k)
if stage["scientific_freeze"].get("h2a_v02_status")!="PASS_R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY":
    fail.append("wrong_h2av02_status")
if stage["scientific_freeze"].get("h2a_v02_artifact_sha256")!="4756a525c407bac9f6de1c42c9274b74825a45a6b3cae81e60f1e67e64494064":
    fail.append("wrong_hash")
if stage["scientific_freeze"].get("tube_bond_state")!="UNFROZEN_T0_T1_T2_DEFERRED":
    fail.append("tube_bond_state_not_deferred")
ev=ROOT/"evidence/r1e1a4a_h2av02_nw_20260925_build01"
for rel in ("FINAL_STATUS.txt","QUALIFICATION.md","summary.json","reopen_shapes.txt","reopen_status.txt"):
    if not (ev/rel).exists(): fail.append("missing:"+rel)
if (ev/"FINAL_STATUS.txt").exists() and (ev/"FINAL_STATUS.txt").read_text().strip()!="PASS_R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY":
    fail.append("final_status_mismatch")
if (ev/"summary.json").exists():
    s=json.loads((ev/"summary.json").read_text())
    if not s["checks"]["pass"]: fail.append("summary_not_pass")
    if s["solver_run"] is not False: fail.append("solver_run_not_false")
    if s.get("shape_count")!=56: fail.append("shape_count_not_56")
if not (ROOT/"docs/R1E1A4A_H2A_V02_3D_REVIEW_GUIDE.md").exists():
    fail.append("review_guide_missing")
if fail:
    print("HOLD_R1E1A4A_H2AV02_CLOSEOUT_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H2AV02_CLOSEOUT_AUDIT")
print("BUILD=PASS")
print("SOLVER=NOT_RUN")
print("TUBE_BOND=UNFROZEN")
print("NEXT=HUMAN_3D_REVIEW")
print("ALL_PERMISSIONS=CLOSED")
