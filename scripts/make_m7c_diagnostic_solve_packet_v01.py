from __future__ import print_function
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--project-root",required=True);ap.add_argument("--manifest",required=True)
 ap.add_argument("--packet",required=True);ap.add_argument("--state-root",required=True);ap.add_argument("--result-packet",required=True);ap.add_argument("--cst-python",required=True)
 a=ap.parse_args();root=Path(a.project_root).resolve();mp=Path(a.manifest).resolve();m=json.loads(mp.read_text(encoding="utf-8"))
 cpath=root/"execution"/"stage_contract.json";c=json.loads(cpath.read_text(encoding="utf-8-sig"))
 runner=root/"scripts"/"run_m7c_diagnostic_solve_v01.py";launcher=root/"scripts"/"cst_bundled_python_launcher_v01.py"
 evalp=root/"scripts"/"evaluate_m7c_modal_restoration_readonly_v01.py";g=c.get("authorization",{}).get("active_grant")
 if subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip():raise SystemExit("HOLD_M7C_PROJECT_DIRTY")
 head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
 fail=[]
 if c["authorization"]["BUILD_AUTHORIZED"] is not False:fail.append("build_false")
 if c["authorization"]["SOLVE_AUTHORIZED"] is not True:fail.append("solve_live")
 if not isinstance(g,dict):fail.append("active_grant")
 if isinstance(g,dict):
  if g.get("kind")!="SOLVE":fail.append("grant_kind")
  if g.get("state")!="GRANTED":fail.append("grant_state")
  if g.get("stage")!=m["stage"]:fail.append("grant_stage")
  if g.get("entrypoint_sha256")!=sha(runner):fail.append("entrypoint_sha")
  if g.get("source_commit")!=c["project"]["source_commit"]:fail.append("source_commit")
 if c["execution"]["current_stage"]!=m["stage"]:fail.append("current_stage")
 if fail:raise SystemExit("HOLD_M7C_LIVE_SOLVE_GRANT:"+",".join(fail))
 target=Path(m["execution"]["target_root"]);artifact=target/m["execution"]["artifact_name"];evidence=target/"evidence"
 rel=lambda p:str(p.relative_to(root)).replace("\\","/")
 packet={"schema_version":"runner-task-v0.2","packet_id":"GNSS-M7C-DIAGNOSTIC-SOLVE-V01",
  "project":{"name":"GNSS_Lband_Active_Array","repository":"Dingo-infinity2020/GNSS_Lband_Active_Array","source_commit":c["project"]["source_commit"],"model_identity":m["stage"]},
  "stage":{"name":m["stage"],"kind":"SOLVE_LAUNCH","control_host_alias":"NW","working_directory":str(root),"stop_boundary":m["execution"]["stop_boundary"]},
  "transport":{"type":"local","ssh_alias":"","remote_shell":""},
  "preflight":{"fail_closed":True,"checks":[
   {"id":"git_clean","type":"git_clean","path":"."},{"id":"git_head","type":"git_head_equals","path":".","commit":head},
   {"id":"runner_hash","type":"file_sha256_equals","path":rel(runner),"sha256":sha(runner)},
   {"id":"evaluator_hash","type":"file_sha256_equals","path":rel(evalp),"sha256":sha(evalp)},
   {"id":"launcher_hash","type":"file_sha256_equals","path":rel(launcher),"sha256":sha(launcher)},
   {"id":"manifest_hash","type":"file_sha256_equals","path":rel(mp),"sha256":sha(mp)},
   {"id":"config_hash","type":"file_sha256_equals","path":m["execution"]["config_macro"],"sha256":m["execution"]["config_macro_sha256"]},
   {"id":"inventory_hash","type":"file_sha256_equals","path":m["execution"]["inventory_contract"],"sha256":m["execution"]["inventory_contract_sha256"]},
   {"id":"contract_hash","type":"file_sha256_equals","path":"execution/stage_contract.json","sha256":sha(cpath)},
   {"id":"source_hash","type":"file_sha256_equals","path":m["canonical_build"]["path"],"sha256":m["canonical_build"]["sha256"]},
   {"id":"full_e2c_hash","type":"file_sha256_equals","path":m["full_e2c_reference"]["response_csv"],"sha256":m["full_e2c_reference"]["response_csv_sha256"]},
   {"id":"target_absent","type":"path_absent","path":str(target)},{"id":"result_absent","type":"result_path_absent"},
   {"id":"cst_gui_absent","type":"process_absent","name":"CST DESIGN ENVIRONMENT_AMD64.exe","ignore_case":True},
   {"id":"cst_modeler_absent","type":"process_absent","name":"modeler_AMD64.exe","ignore_case":True}]},
  "entrypoint":{"argv":["python",rel(launcher),rel(runner),"--manifest",rel(mp),"--out",str(artifact),"--evidence",str(evidence)],
    "environment":{"CST_PYTHON_EXECUTABLE":str(Path(a.cst_python).resolve())},"timeout_seconds":9000},
  "authorization":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":True,"grant_snapshot":{"grant_id":g["grant_id"],"kind":g["kind"],"state":g["state"],"stage":g["stage"],"source_commit":g["source_commit"],"entrypoint_path":rel(runner),"entrypoint_sha256":sha(runner),"stage_contract_path":"execution/stage_contract.json","stage_contract_sha256":sha(cpath),"granted_at":g["granted_at"],"expires_at":g.get("expires_at"),"entrypoint_arg_index":2}},
  "dc_call_budget":{"target_calls":1,"polling_policy":"no_polling","remote_mcp_calls_target":3},
  "expected_outputs":[{"path":str(artifact),"required":True,"sha256":True},
   {"path":str(evidence/"solver_invocation.json"),"required":True,"sha256":True},
   {"path":str(evidence/"qualification"/"loaded_response_native.csv"),"required":True,"sha256":True},
   {"path":str(evidence/"modal"/"modal_evaluation.json"),"required":True,"sha256":True},
   {"path":str(evidence/"summary.json"),"required":True,"sha256":True},
   {"path":str(evidence/"FINAL_STATUS.txt"),"required":True,"sha256":True}],
  "result":{"state_root":str(Path(a.state_root).resolve()),"result_packet_path":str(Path(a.result_packet).resolve())}}
 p=Path(a.packet);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(packet,indent=2)+"\n",encoding="utf-8")
 print("PASS_M7C_SOLVE_PACKET_GENERATED");return 0
if __name__=="__main__":sys.exit(main())
