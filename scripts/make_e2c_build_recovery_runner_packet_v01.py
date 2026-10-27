from __future__ import print_function
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

PARENT_SHA="fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e"
MODEL="R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_ONLY_V01"

def sha256(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def git_head(repo):
    return subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()

def write_json(path,obj):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=["qualification","capability","smoke","build"],required=True)
    ap.add_argument("--project-root",required=True)
    ap.add_argument("--output-packet",required=True)
    ap.add_argument("--state-root",required=True)
    ap.add_argument("--result-packet",required=True)
    ap.add_argument("--qualification-output")
    ap.add_argument("--smoke-root")
    ap.add_argument("--smoke-output")
    ap.add_argument("--target-root")
    ap.add_argument("--parent-cst")
    ap.add_argument("--cst-python",required=True)
    a=ap.parse_args()
    root=Path(a.project_root).resolve(); head=git_head(root)
    runner="scripts/run_r1e1a4a_ar0_b1r_r4_a0_e2c_dualpol_build_only_v01.py"
    adapter="scripts/e2c_simops_watchdog_adapter_v01.py"
    smoke="scripts/smoke_e2c_parent_inventory_v01.py"
    capability="scripts/smoke_e2c_cst_capability_v01.py"
    audit="scripts/audit_e2c_build_entrypoint_contract_v01.py"
    generator="scripts/make_e2c_build_recovery_runner_packet_v01.py"
    macro="source/cst/R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_ONLY_V01.mcr"
    inv="execution/R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_INVENTORY_V01.json"
    kernel="source/cst/R1E1A4A_AR0_B1R_R4_A0_E2C_16VIA_DRILL_KERNEL_REFERENCE_V01.mcr"
    files=[runner,adapter,smoke,capability,audit,generator,macro,inv,kernel]
    hashes={p:sha256(root/p) for p in files}
    common={"schema_version":"runner-task-v0.1",
      "project":{"name":"GNSS_Lband_Active_Array","repository":"Dingo-infinity2020/GNSS_Lband_Active_Array","source_commit":head,"model_identity":MODEL},
      "transport":{"type":"local","ssh_alias":"","remote_shell":""},
      "authorization":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},
      "preflight":{"fail_closed":True,"checks":[
        {"id":"git_clean","type":"git_clean","path":"."},
        {"id":"git_head","type":"git_head_equals","path":".","commit":head},
        *[{"id":Path(p).stem+"_hash","type":"file_sha256_equals","path":p,"sha256":hashes[p]} for p in files[:5]],
        {"id":"result_absent","type":"result_path_absent"}]},
      "dc_call_budget":{"target_calls":1,"polling_policy":"no_polling"}}
    cst=str(Path(a.cst_python).resolve())
    if a.mode=="qualification":
        if not a.qualification_output: raise SystemExit("qualification requires --qualification-output")
        qout=str(Path(a.qualification_output).resolve())
        budgets=json.dumps({"default":60,"between_phases":30},separators=(",",":"))
        code=("import subprocess,sys; "
              "rc0=subprocess.call([sys.executable,'-m','py_compile','"+runner+"','"+adapter+"','"+smoke+"','"+generator+"']); "
              "rc1=subprocess.call([sys.executable,'"+audit+"','--runner','"+runner+"','--out',r'"+qout+"']); "
              "rc2=subprocess.call([sys.executable,'"+adapter+"','--startup-timeout','60','--phase-budgets-json',r'"+budgets+"','--','"+runner+"','--help']); "
              "sys.exit(rc0 or rc1 or rc2)")
        packet=dict(common); packet.update({
          "packet_id":"GNSS-E2C-RECOVERY-QUAL-20260930-05",
          "stage":{"name":"E2C_RECOVERY_ENTRYPOINT_QUALIFICATION","kind":"READ_ONLY","control_host_alias":"NW","working_directory":str(root),"stop_boundary":"RETURN_AFTER_AST_AND_WATCHDOG_RUNTIME_QUALIFICATION"},
          "entrypoint":{"argv":["python","-c",code],"environment":{"CST_PYTHON_EXECUTABLE":cst},"timeout_seconds":180},
          "expected_outputs":[{"path":qout,"required":True,"sha256":True}],
          "result":{"state_root":str(Path(a.state_root).resolve()),"result_packet_path":str(Path(a.result_packet).resolve())}})
        write_json(a.output_packet,packet); return 0

    if not a.parent_cst: raise SystemExit("smoke/build requires --parent-cst")
    parent=Path(a.parent_cst).resolve()
    common["preflight"]["checks"].extend([
      {"id":"parent_exists","type":"path_exists","path":str(parent)},
      {"id":"parent_companion_exists","type":"path_exists","path":str(parent.with_suffix(""))},
      {"id":"parent_hash","type":"file_sha256_equals","path":str(parent),"sha256":PARENT_SHA}])

    if a.mode=="capability":
        if not a.smoke_root or not a.smoke_output: raise SystemExit("capability requires --smoke-root --smoke-output")
        sroot=Path(a.smoke_root).resolve(); sout=Path(a.smoke_output).resolve()
        budgets=json.dumps({"capability_copy":60,"capability_open":120,"capability_tree":120,
          "capability_targeted_vba":120,"capability_result_tree":120,"capability_complete":30,
          "between_phases":45,"default":120},separators=(",",":"))
        packet=dict(common); packet.update({
          "packet_id":"GNSS-E2C-CST-CAPABILITY-SMOKE-20260930-04",
          "stage":{"name":"E2C_CST_CAPABILITY_SMOKE","kind":"GENERIC_NONPRODUCTION","control_host_alias":"NW","working_directory":str(root),"stop_boundary":"NO_PRODUCTION_SOURCE_TEST_TREE_AND_SINGLE_TARGETED_VBA_ONLY"},
          "entrypoint":{"argv":["python",adapter,"--startup-timeout","60","--phase-budgets-json",budgets,"--",
             capability,"--runner",runner,"--parent-cst",str(parent),"--inventory-contract",str(root/inv),"--smoke-root",str(sroot),"--result",str(sout)],
             "environment":{"CST_PYTHON_EXECUTABLE":cst},"timeout_seconds":600},
          "preflight":common["preflight"],
          "expected_outputs":[{"path":str(sout),"required":True,"sha256":True}],
          "result":{"state_root":str(Path(a.state_root).resolve()),"result_packet_path":str(Path(a.result_packet).resolve())}})
        packet["preflight"]["checks"].append({"id":"smoke_root_absent","type":"path_absent","path":str(sroot)})
        write_json(a.output_packet,packet); return 0

    if a.mode=="smoke":
        if not a.smoke_root or not a.smoke_output: raise SystemExit("smoke requires --smoke-root --smoke-output")
        sroot=Path(a.smoke_root).resolve(); sout=Path(a.smoke_output).resolve()
        budgets=json.dumps({"smoke_copy":60,"smoke_parent_inventory":1200,"smoke_result_tree":120,
                             "smoke_complete":30,"between_phases":45,"default":120},separators=(",",":"))
        packet=dict(common); packet.update({
          "packet_id":"GNSS-E2C-PARENT-SMOKE-20260930-04",
          "stage":{"name":"E2C_PARENT_SIMULATOR_SMOKE","kind":"GENERIC_NONPRODUCTION","control_host_alias":"NW","working_directory":str(root),"stop_boundary":"NO_PRODUCTION_HISTORY_NO_SOLVER_RETURN_AFTER_PARENT_OPEN_INVENTORY_RESULTTREE_CLOSE"},
          "entrypoint":{"argv":["python",adapter,"--startup-timeout","60","--phase-budgets-json",budgets,"--",
             smoke,"--runner",runner,"--parent-cst",str(parent),"--inventory-contract",str(root/inv),"--smoke-root",str(sroot),"--result",str(sout)],
             "environment":{"CST_PYTHON_EXECUTABLE":cst},"timeout_seconds":1800},
          "preflight":common["preflight"],
          "expected_outputs":[{"path":str(sout),"required":True,"sha256":True}],
          "result":{"state_root":str(Path(a.state_root).resolve()),"result_packet_path":str(Path(a.result_packet).resolve())}})
        packet["preflight"]["checks"].append({"id":"smoke_root_absent","type":"path_absent","path":str(sroot)})
        write_json(a.output_packet,packet); return 0

    if not a.target_root or not a.qualification_output or not a.smoke_output:
        raise SystemExit("build requires --target-root --qualification-output --smoke-output")
    qev=Path(a.qualification_output).resolve(); sev=Path(a.smoke_output).resolve()
    qj=json.loads(qev.read_text(encoding="utf-8")); sj=json.loads(sev.read_text(encoding="utf-8"))
    if qj.get("status")!="PASS_E2C_BUILD_ENTRYPOINT_STATIC_CONTRACT":
        raise SystemExit("HOLD_BUILD_QUALIFICATION_NOT_PASS")
    if sj.get("status")!="PASS_E2C_PARENT_SIMULATOR_SMOKE":
        raise SystemExit("HOLD_BUILD_SMOKE_NOT_PASS")
    target=Path(a.target_root).resolve(); out=target/"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_COEXISTENCE_BUILD_ONLY_V01.cst"
    review=target/"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_HUMAN_REVIEW_COPY.cst"; evidence=target/"evidence"
    budgets=json.dumps({"parent_inventory":180,"kernel_reference":420,"production_open":120,
       "production_build":420,"fresh_reopen":300,"whole_model_intersection":180,
       "pairwise":240,"review_copy":180,"complete":30,"between_phases":60,"default":300},separators=(",",":"))
    packet=dict(common); packet.update({
      "packet_id":"GNSS-E2C-DUALPOL-BUILD-RECOVERY-20260930-06",
      "stage":{"name":"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_RECOVERY","kind":"BUILD_ONLY","control_host_alias":"NW","working_directory":str(root),"stop_boundary":"STOP_AFTER_177_24_16_29_AUDIT_AND_COMPLETE_HUMAN_REVIEW_COPY_NO_SOLVER"},
      "authorization":{"BUILD_AUTHORIZED":True,"SOLVE_AUTHORIZED":False},
      "entrypoint":{"argv":["python",adapter,"--startup-timeout","60","--phase-budgets-json",budgets,"--",runner,
        "--parent-cst",str(parent),"--macro",str(root/macro),"--kernel-reference-macro",str(root/kernel),
        "--inventory-contract",str(root/inv),"--out",str(out),"--review-copy",str(review),"--evidence",str(evidence)],
        "environment":{"CST_PYTHON_EXECUTABLE":cst},"timeout_seconds":7200},
      "preflight":common["preflight"],
      "expected_outputs":[
        {"path":str(out),"required":True,"sha256":True},{"path":str(review),"required":True,"sha256":True},
        {"path":str(evidence/"FINAL_STATUS.txt"),"required":True,"sha256":True},
        {"path":str(evidence/"summary.json"),"required":True,"sha256":True},
        {"path":str(evidence/"HUMAN_3D_REVIEW.md"),"required":True,"sha256":True}],
      "result":{"state_root":str(Path(a.state_root).resolve()),"result_packet_path":str(Path(a.result_packet).resolve())}})
    packet["preflight"]["checks"].extend([
      {"id":"macro_hash","type":"file_sha256_equals","path":macro,"sha256":hashes[macro]},
      {"id":"inventory_hash","type":"file_sha256_equals","path":inv,"sha256":hashes[inv]},
      {"id":"kernel_hash","type":"file_sha256_equals","path":kernel,"sha256":hashes[kernel]},
      {"id":"qualification_hash","type":"file_sha256_equals","path":str(qev),"sha256":sha256(qev)},
      {"id":"smoke_hash","type":"file_sha256_equals","path":str(sev),"sha256":sha256(sev)},
      {"id":"target_root_absent","type":"path_absent","path":str(target)}])
    write_json(a.output_packet,packet); return 0

if __name__=="__main__": sys.exit(main())
