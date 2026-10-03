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
if sf.get("build_status")!="PASS_R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY":
    fail.append("wrong_build_status")
if sf.get("artifact_sha256")!="3d15d5bf36c0d6f60a4d46d48fa5197818559890e27e0950556a0f14e2309043":
    fail.append("wrong_hash")
if sf.get("shape_count")!=126 or sf.get("port_count")!=0 or sf.get("solver_run") is not False:
    fail.append("wrong_build_facts")
ev=ROOT/"evidence/r1e1a4a_h3a_nw_20260925_build01"
for rel in ("FINAL_STATUS.txt","FORMAL_STATUS.txt","QUALIFICATION.md","summary.json","reopen_shapes.txt","reopen_status.txt","intersection_builtin_status.txt"):
    if not (ev/rel).exists(): fail.append("missing:"+rel)
if (ev/"FINAL_STATUS.txt").exists() and (ev/"FINAL_STATUS.txt").read_text().strip()!="PASS_R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY":
    fail.append("final_status_mismatch")
if (ev/"summary.json").exists():
    s=json.loads((ev/"summary.json").read_text())
    if not s["checks"]["pass"]: fail.append("summary_not_pass")
    if s["solver_run"] is not False: fail.append("solver_run_not_false")
    if s.get("shape_count")!=126: fail.append("shape_count_not_126")
    if not s["checks"].get("builtin_intersection_command_executed"): fail.append("builtin_intersection_not_executed")
    if not s["checks"].get("critical_clearances_positive"): fail.append("clearance_gate_not_pass")
if not (ROOT/"docs/R1E1A4A_H3A_3D_REVIEW_GUIDE.md").exists(): fail.append("review_guide_missing")
if fail:
    print("HOLD_R1E1A4A_H3A_CLOSEOUT_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H3A_CLOSEOUT_AUDIT")
print("BUILD=PASS")
print("SOLVER=NOT_RUN")
print("INTERSECTION_GATE=EXECUTED")
print("NEXT=HUMAN_3D_REVIEW")
print("ALL_PERMISSIONS=CLOSED")
