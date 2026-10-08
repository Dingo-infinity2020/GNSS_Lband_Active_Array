from __future__ import print_function
import ast, hashlib, json, re, sys
from pathlib import Path
ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
FREEZE=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_CIN_PAD_CLEARANCE_MANIFEST_V01.json"
MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_CIN_PAD_CLEARANCE_FORMAL_BUILD_MANIFEST_V01.json"
RUN=ROOT/"scripts"/"run_m7b_cin_pad_clearance_build_only_v01.py"
PKT=ROOT/"scripts"/"make_m7b_cin_pad_clearance_build_packet_v01.py"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_FORMAL_BUILD_PREP_V01"/"STATIC_AUDIT.json"
def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def run_solver_calls(p):
 tree=ast.parse(p.read_text(encoding="utf-8")); n=0
 for x in ast.walk(tree):
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=="run_solver": n+=1
 return n
freeze=json.loads(FREEZE.read_text(encoding="utf-8")); m=json.loads(MAN.read_text(encoding="utf-8"))
macro=ROOT/m["execution"]["macro"]; t=macro.read_text(encoding="utf-8")
inv=Path(m["parent"]["inventory_contract"]); j=json.loads(inv.read_text(encoding="utf-8"))
immutable_keys=("candidate","title","geometry","scientific_change","target_mechanism","primary_prediction","falsification","pre_registered_success_gate","comparison_authority")
checks={
 "candidate_m7b":m["candidate"]=="M7B",
 "stage_exact":m["stage"]=="R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_CIN_PAD_CLEARANCE_BUILD_ONLY",
 "freeze_hash":m["freeze_authority"]["candidate_manifest_sha256"]==sha(FREEZE),
 "science_freeze_exact":all(m[k]==freeze[k] for k in immutable_keys),
 "manifest_auth_false":m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},
 "parent_inventory_177":j["expected_final_shape_count"]==177 and len(j["expected_final_names"])==177,
 "parent_inventory_hash":sha(inv)==m["parent"]["inventory_contract_sha256"],
 "macro_hash":sha(macro)==m["execution"]["macro_sha256"],
 "macro_four_creates":t.count(".Create")==4,
 "macro_four_subtracts":t.count("Solid.Subtract")==4,
 "macro_only_background_targets":all("BackGround:LOCAL_BACK_GROUND" in x for x in re.findall(r'Solid\.Subtract "([^"]+)"',t)),
 "macro_no_port_solver_monitor":all(x not in t for x in ("Port.","DiscretePort","Solver.","run_solver","StartSolver","ChangeSolverType","Monitor.")),
 "runner_zero_run_solver":run_solver_calls(RUN)==0,
 "packet_zero_run_solver":run_solver_calls(PKT)==0,
 "runner_177_24_contract":'"shape_count_exact_177"' in RUN.read_text(encoding="utf-8") and '"ports_exact_24"' in RUN.read_text(encoding="utf-8"),
 "runner_m7b_volume_gate":'expected_loss=float(m["geometry"]["area_removed_per_branch_mm2"])*abs(float(m["geometry"]["tool_height_mm"]))' in RUN.read_text(encoding="utf-8"),
 "runner_m7b_human_review":"M7B CIN_PAD_PROJECTION_CLEARANCE Human Geometry Review" in RUN.read_text(encoding="utf-8"),
 "packet_id_m7b":'"packet_id":"GNSS-M7B-CIN-PAD-CLEARANCE-BUILD-V01"' in PKT.read_text(encoding="utf-8"),
 "packet_v02":'"schema_version":"runner-task-v0.2"' in PKT.read_text(encoding="utf-8"),
 "packet_fail_closed":"HOLD_M7B_LIVE_BUILD_GRANT" in PKT.read_text(encoding="utf-8")
}
status="PASS_M7B_FORMAL_BUILD_STATIC_CONTRACT" if all(checks.values()) else "HOLD_M7B_FORMAL_BUILD_STATIC_CONTRACT"
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({"status":status,"checks":checks,
 "runner_sha256":sha(RUN),"packet_generator_sha256":sha(PKT),"formal_manifest_sha256":sha(MAN),
 "freeze_manifest_sha256":sha(FREEZE),"expected_volume_loss_per_branch_mm3":0.077,
 "formal_build_invocations":0,"solver_invocations":0,
 "BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},indent=2)+"\n",encoding="utf-8")
print(status)
for k,v in checks.items():
 if not v: print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
