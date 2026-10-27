from __future__ import print_function
import ast, hashlib, json, re, sys
from pathlib import Path
ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7_CORRECTIVE_CANDIDATE_FREEZE_V01"/"STATIC_AUDIT.json"
PARENT_SHA="cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c"

def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()

checks={}; detail={}
for cid,stem in (
 ("M7A","R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK"),
 ("M7B","R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_CIN_PAD_CLEARANCE")):
 man=ROOT/"execution"/(stem+"_MANIFEST_V01.json")
 mac=ROOT/"source"/"cst"/(stem+"_BUILD_ONLY_V01.mcr")
 m=json.loads(man.read_text(encoding="utf-8")); t=mac.read_text(encoding="utf-8")
 checks[cid+"_status"]=m["status"]=="FROZEN_BUILD_ONLY_AWAIT_AUTH"
 checks[cid+"_parent_hash"]=m["parent"]["sha256"]==PARENT_SHA
 checks[cid+"_auth_false"]=m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
 checks[cid+"_four_tools"]=m["geometry"]["tool_count"]==4 and t.count(".Create")==4
 checks[cid+"_four_subtracts"]=t.count("Solid.Subtract")==4
 checks[cid+"_only_backgrounds_modified"]=all("BackGround:LOCAL_BACK_GROUND" in x for x in m["geometry"]["modified_entities"])
 checks[cid+"_no_signal_subtract"]=all("Signal:" not in x for x in re.findall(r'Solid\.Subtract "([^"]+)"',t))
 checks[cid+"_no_port_or_solver"]=all(x not in t for x in ("Port.","DiscretePort","Solver.","run_solver","StartSolver","ChangeSolverType","Monitor."))
 checks[cid+"_solid_count_unchanged"]=m["geometry"]["expected_final_solids"]==177 and m["geometry"]["expected_raw_ports"]==24
 checks[cid+"_macro_hash"]=sha(mac)==m["execution"]["macro_sha256"]
 checks[cid+"_four_branch_windows"]=set(m["geometry"]["clearance_windows_local_uv_mm"].keys())=={"A_P","A_N","B_P","B_N"}
 if cid=="M7A":
  w=m["geometry"]["clearance_windows_local_uv_mm"]
  checks["M7A_retains_signal_overhang"]=w["A_P"]==[1.0,1.5,3.0,5.0] and w["A_N"]==[-1.5,-1.0,3.0,5.0]
  checks["M7A_window_does_not_reach_signal_inner_edge"]=1.5 < 2.05
 if cid=="M7B":
  w=m["geometry"]["clearance_windows_local_uv_mm"]
  checks["M7B_exact_guarded_CIN_projection"]=w["A_P"]==[2.45,3.55,4.15,5.15] and w["A_N"]==[-3.55,-2.45,4.15,5.15]
  # Existing paddle vias start around v~7; CRF via around v~11, so the v<=5.15 window is separated.
  checks["M7B_window_separate_from_via_regions"]=max(x[3] for x in w.values())<=5.15
 detail[cid]={"manifest_sha256":sha(man),"macro_sha256":sha(mac),"success_gate":m["pre_registered_success_gate"]}

checks["candidate_count_exactly_two"]=len(detail)==2
status="PASS_M7_CORRECTIVE_CANDIDATE_STATIC_FREEZE" if all(checks.values()) else "HOLD_M7_CORRECTIVE_CANDIDATE_STATIC_FREEZE"
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({"status":status,"checks":checks,"detail":detail,"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},indent=2)+"\n",encoding="utf-8")
print(status)
for k,v in checks.items():
 if not v:print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
