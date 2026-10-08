from __future__ import print_function
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",required=True)
    ap.add_argument("--variant-manifest",required=True)
    ap.add_argument("--packet",required=True)
    ap.add_argument("--state-root",required=True)
    ap.add_argument("--result-packet",required=True)
    ap.add_argument("--cst-python",required=True)
    a=ap.parse_args()
    root=Path(a.project_root).resolve(); vm=Path(a.variant_manifest).resolve()
    m=json.loads(vm.read_text(encoding="utf-8"))
    contract=root/"execution"/"stage_contract.json"
    runner=root/"scripts"/"run_m7c_local_return_island_build_only_v01.py"
    launcher=root/"scripts"/"cst_bundled_python_launcher_v01.py"
    if subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip():
        raise SystemExit("HOLD_M7_PROJECT_DIRTY")
    head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    c=json.loads(contract.read_text(encoding="utf-8-sig")); g=c.get("authorization",{}).get("active_grant")
    failed=[]
    if c.get("authorization",{}).get("BUILD_AUTHORIZED") is not True: failed.append("build_live")
    if c.get("authorization",{}).get("SOLVE_AUTHORIZED") is not False: failed.append("solve_false")
    if not isinstance(g,dict): failed.append("active_grant")
    if isinstance(g,dict):
        if g.get("kind")!="BUILD": failed.append("grant_kind")
        if g.get("state")!="GRANTED": failed.append("grant_state")
        if g.get("stage")!=m["stage"]: failed.append("grant_stage")
        if g.get("entrypoint_sha256")!=sha(runner): failed.append("entrypoint_sha")
        if g.get("source_commit")!=c.get("project",{}).get("source_commit"): failed.append("source_commit")
    if c.get("execution",{}).get("current_stage")!=m["stage"]: failed.append("current_stage")
    if failed: raise SystemExit("HOLD_M7C_LIVE_BUILD_GRANT:"+",".join(failed))

    target=Path(m["execution"]["target_root"])
    artifact=target/m["execution"]["artifact_name"]; evidence=target/"evidence"
    rel=lambda p:str(p.relative_to(root)).replace("\\","/")
    cstpy=Path(a.cst_python).resolve()
    packet={
      "schema_version":"runner-task-v0.2",
      "packet_id":"GNSS-M7C-LOCAL-RETURN-ISLAND-BUILD-V01",
      "project":{"name":"GNSS_Lband_Active_Array","repository":"Dingo-infinity2020/GNSS_Lband_Active_Array",
                 "source_commit":c["project"]["source_commit"],"model_identity":m["stage"]},
      "stage":{"name":m["stage"],"kind":"BUILD_ONLY","control_host_alias":"NW",
               "working_directory":str(root),"stop_boundary":m["execution"]["build_stop"]},
      "transport":{"type":"local","ssh_alias":"","remote_shell":""},
      "preflight":{"fail_closed":True,"checks":[
        {"id":"git_clean","type":"git_clean","path":"."},
        {"id":"git_head","type":"git_head_equals","path":".","commit":head},
        {"id":"runner_hash","type":"file_sha256_equals","path":rel(runner),"sha256":sha(runner)},
        {"id":"launcher_hash","type":"file_sha256_equals","path":rel(launcher),"sha256":sha(launcher)},
        {"id":"manifest_hash","type":"file_sha256_equals","path":rel(vm),"sha256":sha(vm)},
        {"id":"macro_hash","type":"file_sha256_equals","path":m["execution"]["macro"],"sha256":m["execution"]["macro_sha256"]},
        {"id":"inventory_hash","type":"file_sha256_equals","path":rel(Path(m["parent"]["inventory_contract"])),"sha256":m["parent"]["inventory_contract_sha256"]},
        {"id":"stage_contract_hash","type":"file_sha256_equals","path":"execution/stage_contract.json","sha256":sha(contract)},
        {"id":"parent_hash","type":"file_sha256_equals","path":m["parent"]["path"],"sha256":m["parent"]["sha256"]},
        {"id":"target_absent","type":"path_absent","path":str(target)},
        {"id":"result_absent","type":"result_path_absent"},
        {"id":"cst_gui_absent","type":"process_absent","name":"CST DESIGN ENVIRONMENT_AMD64.exe","ignore_case":True},
        {"id":"cst_modeler_absent","type":"process_absent","name":"modeler_AMD64.exe","ignore_case":True}
      ]},
      "entrypoint":{"argv":["python",rel(launcher),rel(runner),"--variant-manifest",rel(vm),
                            "--out",str(artifact),"--evidence",str(evidence)],
                    "environment":{"CST_PYTHON_EXECUTABLE":str(cstpy)},"timeout_seconds":2400},
      "authorization":{"BUILD_AUTHORIZED":True,"SOLVE_AUTHORIZED":False,
        "grant_snapshot":{"grant_id":g["grant_id"],"kind":g["kind"],"state":g["state"],"stage":g["stage"],
          "source_commit":g["source_commit"],"entrypoint_path":rel(runner),"entrypoint_sha256":sha(runner),
          "stage_contract_path":"execution/stage_contract.json","stage_contract_sha256":sha(contract),
          "granted_at":g["granted_at"],"expires_at":g.get("expires_at"),"entrypoint_arg_index":2}},
      "dc_call_budget":{"target_calls":1,"polling_policy":"no_polling","remote_mcp_calls_target":3},
      "expected_outputs":[
        {"path":str(artifact),"required":True,"sha256":True},
        {"path":str(evidence/"FINAL_STATUS.txt"),"required":True,"sha256":True},
        {"path":str(evidence/"summary.json"),"required":True,"sha256":True},
        {"path":str(evidence/"HUMAN_3D_REVIEW.md"),"required":True,"sha256":True}],
      "result":{"state_root":str(Path(a.state_root).resolve()),"result_packet_path":str(Path(a.result_packet).resolve())}
    }
    p=Path(a.packet); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(packet,indent=2)+"\n",encoding="utf-8")
    print("PASS_M7C_BUILD_PACKET_GENERATED")
    return 0
if __name__=="__main__": sys.exit(main())
