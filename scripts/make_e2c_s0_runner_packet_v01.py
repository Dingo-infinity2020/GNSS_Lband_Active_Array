from __future__ import print_function
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

MODEL="R1E1A4A_AR0_B1R_R4_A0_E2C_R7"
STAGE="R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_SENTINEL"
SOURCE_SHA="cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c"

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def git_head(repo):
    return subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()

def git_clean(repo):
    return subprocess.check_output(["git","-C",str(repo),"status","--porcelain"],text=True).strip()==""

def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")

def live_solve_grant(contract,runner_sha):
    auth=contract.get("authorization",{})
    exe=contract.get("execution",{})
    project=contract.get("project",{})
    grant=auth.get("active_grant")
    checks={
      "semantics_current_live_only":auth.get("semantics")=="CURRENT_LIVE_ONLY",
      "build_not_live":auth.get("BUILD_AUTHORIZED") is False,
      "solve_live":auth.get("SOLVE_AUTHORIZED") is True,
      "active_grant_object":isinstance(grant,dict),
      "current_stage_matches":exe.get("current_stage")==STAGE,
    }
    if isinstance(grant,dict):
        checks.update({
          "grant_kind_solve":grant.get("kind")=="SOLVE",
          "grant_state_granted":grant.get("state")=="GRANTED",
          "grant_stage_matches":grant.get("stage")==STAGE,
          "grant_source_commit_matches_contract":grant.get("source_commit")==project.get("source_commit"),
          "grant_entrypoint_sha_matches":grant.get("entrypoint_sha256")==runner_sha,
        })
    return checks,grant

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=["qualification","solve"],required=True)
    ap.add_argument("--project-root",required=True)
    ap.add_argument("--output-packet",required=True)
    ap.add_argument("--state-root",required=True)
    ap.add_argument("--result-packet",required=True)
    ap.add_argument("--cst-python",required=True)
    ap.add_argument("--qualification-output",required=True)
    ap.add_argument("--target-root")
    a=ap.parse_args()

    root=Path(a.project_root).resolve()
    if not git_clean(root):
        raise SystemExit("HOLD_E2C_S0_PROJECT_DIRTY")
    head=git_head(root)

    rel={
      "runner":"scripts/run_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_coexistence_solve.py",
      "presolve":"scripts/configure_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_presolve.py",
      "qualifier":"scripts/qualify_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_readonly.py",
      "audit":"scripts/audit_e2c_s0_entrypoint_contract_v01.py",
      "generator":"scripts/make_e2c_s0_runner_packet_v01.py",
      "watchdog":"scripts/e2c_simops_watchdog_adapter_v01.py",
      "macro":"source/cst/R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_CONFIG_V01.mcr",
      "manifest":"execution/R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_SENTINEL_MANIFEST_V01.json",
      "inventory":"execution/R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_INVENTORY_V01.json",
      "contract":"execution/stage_contract.json",
    }
    paths={k:(root/v) for k,v in rel.items()}
    for k,p in paths.items():
        if not p.exists():
            raise SystemExit("HOLD_E2C_S0_MISSING_"+k.upper())
    hashes={k:sha(p) for k,p in paths.items()}

    manifest=json.loads(paths["manifest"].read_text(encoding="utf-8"))
    source=Path(manifest["canonical_build"]["path"])
    if not source.exists() or sha(source)!=SOURCE_SHA or not source.with_suffix("").exists():
        raise SystemExit("HOLD_E2C_S0_CANONICAL_SOURCE")
    for pol in ("PolA","PolB"):
        b=manifest["isolated_baselines"][pol]; p=Path(b["csv_path"])
        if not p.exists() or sha(p)!=b["csv_sha256"]:
            raise SystemExit("HOLD_E2C_S0_BASELINE_"+pol.upper())

    qout=Path(a.qualification_output).resolve()
    state_root=Path(a.state_root).resolve()
    result_packet=Path(a.result_packet).resolve()
    cstpython=Path(a.cst_python).resolve()
    if not cstpython.exists():
        raise SystemExit("HOLD_E2C_S0_CST_PYTHON_MISSING")

    common_checks=[
      {"id":"git_clean","type":"git_clean","path":"."},
      {"id":"git_head","type":"git_head_equals","path":".","commit":head},
      *[{"id":k+"_hash","type":"file_sha256_equals","path":rel[k],"sha256":hashes[k]}
        for k in ("runner","presolve","qualifier","audit","generator","watchdog","macro","manifest","inventory","contract")],
      {"id":"canonical_source_exists","type":"path_exists","path":str(source)},
      {"id":"canonical_companion_exists","type":"path_exists","path":str(source.with_suffix(""))},
      {"id":"canonical_source_hash","type":"file_sha256_equals","path":str(source),"sha256":SOURCE_SHA},
      {"id":"baseline_pola_hash","type":"file_sha256_equals",
       "path":manifest["isolated_baselines"]["PolA"]["csv_path"],
       "sha256":manifest["isolated_baselines"]["PolA"]["csv_sha256"]},
      {"id":"baseline_polb_hash","type":"file_sha256_equals",
       "path":manifest["isolated_baselines"]["PolB"]["csv_path"],
       "sha256":manifest["isolated_baselines"]["PolB"]["csv_sha256"]},
      {"id":"result_absent","type":"result_path_absent"},
    ]

    base={
      "schema_version":"runner-task-v0.2",
      "project":{"name":"GNSS_Lband_Active_Array",
                 "repository":"Dingo-infinity2020/GNSS_Lband_Active_Array",
                 "source_commit":head,"model_identity":MODEL},
      "transport":{"type":"local","ssh_alias":"","remote_shell":""},
      "preflight":{"fail_closed":True,"checks":common_checks},
      "dc_call_budget":{"target_calls":1,"polling_policy":"no_polling","remote_mcp_calls_target":3},
      "result":{"state_root":str(state_root),"result_packet_path":str(result_packet)},
    }

    if a.mode=="qualification":
        if qout.exists():
            raise SystemExit("HOLD_E2C_S0_QUALIFICATION_OUTPUT_EXISTS")
        packet=dict(base)
        packet.update({
          "packet_id":"GNSS-E2C-S0-ENTRYPOINT-QUAL-20261002-01",
          "stage":{"name":"E2C_S0_ENTRYPOINT_QUALIFICATION","kind":"READ_ONLY",
                   "control_host_alias":"NW","working_directory":str(root),
                   "stop_boundary":"RETURN_AFTER_STATIC_AST_HASH_BASELINE_AND_CST_RUNTIME_HELP_NO_DESIGNENV_NO_SOLVER"},
          "entrypoint":{"argv":["python",rel["audit"],"--project-root",str(root),
                                "--cst-python",str(cstpython),"--out",str(qout)],
                        "environment":{},"timeout_seconds":180},
          "authorization":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},
          "expected_outputs":[{"path":str(qout),"required":True,"sha256":True}],
        })
        write_json(a.output_packet,packet)
        return 0

    if not a.target_root:
        raise SystemExit("solve requires --target-root")
    if not qout.exists():
        raise SystemExit("HOLD_E2C_S0_QUALIFICATION_MISSING")
    q=json.loads(qout.read_text(encoding="utf-8"))
    if q.get("status")!="PASS_E2C_S0_ENTRYPOINT_STATIC_CONTRACT":
        raise SystemExit("HOLD_E2C_S0_QUALIFICATION_NOT_PASS")

    contract=json.loads(paths["contract"].read_text(encoding="utf-8-sig"))
    grant_checks,grant=live_solve_grant(contract,hashes["runner"])
    failed=[k for k,v in grant_checks.items() if not v]
    if failed:
        raise SystemExit("HOLD_E2C_S0_LIVE_SOLVE_GRANT:"+",".join(failed))
    stage_contract_sha=hashes["contract"]
    packet_source_commit=contract["project"]["source_commit"]

    target=Path(a.target_root).resolve()
    if target.exists():
        raise SystemExit("HOLD_E2C_S0_TARGET_EXISTS")
    solved=target/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_SOLVED_V01.cst"
    evidence=target/"evidence"

    budgets=json.dumps({
      "presolve_config":1500,
      "solver_run":7200,
      "qualification":900,
      "complete":30,
      "between_phases":60,
      "default":600
    },separators=(",",":"))

    packet=dict(base)
    packet["project"]=dict(packet["project"])
    packet["project"]["source_commit"]=packet_source_commit
    packet["preflight"]={"fail_closed":True,"checks":list(common_checks)+[
      {"id":"qualification_hash","type":"file_sha256_equals","path":str(qout),"sha256":sha(qout)},
      {"id":"target_root_absent","type":"path_absent","path":str(target)},
      {"id":"cst_gui_absent","type":"process_absent","name":"CST DESIGN ENVIRONMENT_AMD64.exe","ignore_case":True},
      {"id":"cst_modeler_absent","type":"process_absent","name":"modeler_AMD64.exe","ignore_case":True},
    ]}
    packet.update({
      "packet_id":"GNSS-E2C-S0-COEXISTENCE-SOLVE-20261002-01",
      "stage":{"name":STAGE,"kind":"SOLVE_LAUNCH",
               "control_host_alias":"NW","working_directory":str(root),
               "stop_boundary":"STOP_AFTER_ONE_12PORT_8SOURCE_SENTINEL_SOLVE_AND_READONLY_QUALIFICATION_NO_RETRY_NO_C1"},
      "entrypoint":{"argv":["python",rel["watchdog"],
                           "--startup-timeout","60",
                           "--phase-budgets-json",budgets,
                           "--",rel["runner"],
                           "--source-cst",str(source),
                           "--config-macro",str(paths["macro"]),
                           "--inventory-contract",str(paths["inventory"]),
                           "--sentinel-manifest",str(paths["manifest"]),
                           "--out",str(solved),
                           "--evidence",str(evidence)],
                    "environment":{"CST_PYTHON_EXECUTABLE":str(cstpython)},
                    "timeout_seconds":10800},
      "authorization":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":True,
        "grant_snapshot":{
          "grant_id":grant["grant_id"],
          "kind":grant["kind"],
          "state":grant["state"],
          "stage":grant["stage"],
          "source_commit":grant["source_commit"],
          "entrypoint_path":rel["runner"],
          "entrypoint_sha256":hashes["runner"],
          "stage_contract_path":rel["contract"],
          "stage_contract_sha256":stage_contract_sha,
          "granted_at":grant["granted_at"],
          "expires_at":grant.get("expires_at"),
          "entrypoint_arg_index":7
        }},
      "expected_outputs":[
        {"path":str(solved),"required":True,"sha256":True},
        {"path":str(evidence/"FINAL_STATUS.txt"),"required":True,"sha256":True},
        {"path":str(evidence/"summary.json"),"required":True,"sha256":True},
        {"path":str(evidence/"solver_invocation.json"),"required":True,"sha256":True},
        {"path":str(evidence/"qualification"/"qualification_summary.json"),"required":True,"sha256":True},
      ],
    })
    # The immutable packet is additionally bound to the exact stage-contract hash
    # containing the live grant. runner-task-v0.1 has no native grant_id field.
    write_json(a.output_packet,packet)
    return 0

if __name__=="__main__":
    sys.exit(main())
