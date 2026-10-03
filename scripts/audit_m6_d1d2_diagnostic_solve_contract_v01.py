from __future__ import print_function
import ast, hashlib, json, re, sys
from pathlib import Path
ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1D2_DIAGNOSTIC_SOLVE_PREP_V01"/"STATIC_AUDIT.json"
files={
 "presolve":ROOT/"scripts"/"configure_m6_diagnostic_presolve_v01.py",
 "qualifier":ROOT/"scripts"/"qualify_m6_diagnostic_readonly_v01.py",
 "runner":ROOT/"scripts"/"run_m6_diagnostic_solve_v01.py",
 "packet":ROOT/"scripts"/"make_m6_diagnostic_solve_packet_v01.py"}
def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def run_calls(p):
 tree=ast.parse(p.read_text(encoding="utf-8")); calls=[]
 for x in ast.walk(tree):
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=="run_solver": calls.append(x)
 return tree,calls
checks={}; detail={}
for key in ("D1","D2"):
 man=ROOT/"execution"/("R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_%s_DIAGNOSTIC_SOLVE_MANIFEST_V01.json"%key)
 m=json.loads(man.read_text(encoding="utf-8")); cfg=ROOT/m["execution"]["config_macro"]; t=cfg.read_text(encoding="utf-8")
 checks[key+"_auth_false"]=m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
 checks[key+"_source_exists_hash"]=Path(m["source_build"]["path"]).exists() and sha(Path(m["source_build"]["path"]))==m["source_build"]["sha256"]
 checks[key+"_human_review_pass"]=m["source_build"]["human_review_status"].startswith("PASS_")
 checks[key+"_baseline_hash"]=sha(Path(m["response_contract"]["baseline_csv"]))==m["response_contract"]["baseline_sha256"]
 checks[key+"_six_port_delete_map"]=all(x in t for x in ('Port.Delete 12','Port.Delete 11','Port.Delete 10','Port.Delete 6','Port.Delete 5','Port.Delete 4','Port.Rename 7, 4','Port.Rename 8, 5','Port.Rename 9, 6'))
 checks[key+"_sources_exact"]=all(('.AddToExcitationList "%d", "1"'%p) in t for p in (1,2,4,5)) and all(('.AddToExcitationList "%d", "1"'%p) not in t for p in (3,6))
 checks[key+"_solver_fidelity"]=all(x in t for x in ('ChangeSolverType "HF Frequency Domain"','.OrderTet "Second"','.MaxPasses "16"','.MaxDeltaS "0.02"','.NumberOfDeltaSChecks "2"'))
 checks[key+"_three_hfield_monitors"]=t.count('.FieldType "Hfield"')==3 and all(('Frequency "%s"'%str(f)) in t for f in (1.2276,1.3384,1.57542))
 checks[key+"_no_solver_start_in_config"]=all(x not in t for x in ("run_solver","Solver.Start","StartSolver"))
 checks[key+"_thresholds_frozen"]=m["attribution_metrics"]["variant_classification"]["STRONG"].startswith("at least 2") and m["attribution_metrics"]["variant_classification"]["WEAK"].startswith("all 3")
 detail[key]={"manifest_sha256":sha(man),"config_sha256":sha(cfg),"source_sha256":m["source_build"]["sha256"]}
for k,p in files.items():
 tree,calls=run_calls(p)
 checks[k+"_compiles_ast"]=True
 checks[k+"_run_solver_count"]=(len(calls)==1 if k=="runner" else len(calls)==0)
 if k=="runner" and calls:
  call=calls[0]; in_loop=False
  for n in ast.walk(tree):
   if isinstance(n,(ast.For,ast.While)):
    for z in ast.walk(n):
     if z is call: in_loop=True
  checks["runner_run_solver_not_in_loop"]=not in_loop
checks["packet_v02"]='"schema_version":"runner-task-v0.2"' in files["packet"].read_text(encoding="utf-8")
checks["packet_live_solve_fail_closed"]="HOLD_M6_DIAG_LIVE_SOLVE_GRANT" in files["packet"].read_text(encoding="utf-8")
checks["presolve_named_inventory_no_index_scan"]="GetNameOfShapeFromIndex" not in files["presolve"].read_text(encoding="utf-8")
status="PASS_M6_D1D2_DIAGNOSTIC_SOLVE_STATIC_CONTRACT" if all(checks.values()) else "HOLD_M6_D1D2_DIAGNOSTIC_SOLVE_STATIC_CONTRACT"
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({"status":status,"checks":checks,"detail":detail,"formal_solver_invocations":0,"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},indent=2)+"\n",encoding="utf-8")
print(status)
for k,v in checks.items():
 if not v: print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
