from __future__ import print_function
import argparse, json, sys, traceback
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

import cst.interface as ci

import configure_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_presolve as presolve
import qualify_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_readonly as qualifier

EXPECTED_SOURCE_SHA256="cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c"

def _simops_emit(obj):
    print("SIMOPS_EVENT "+json.dumps(obj,separators=(",",":")),flush=True)

def simops_phase(phase,state,production_boundary,message=None):
    obj={"schema_version":"simops-project-event-v0.1","event":"PHASE",
         "phase":str(phase),"state":str(state),
         "production_boundary":str(production_boundary)}
    if message:
        obj["message"]=str(message)
    _simops_emit(obj)

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")

def main(source_cst,config_macro,inventory_contract,sentinel_manifest,out,evidence):
    source_cst=Path(source_cst); config_macro=Path(config_macro)
    inventory_contract=Path(inventory_contract); sentinel_manifest=Path(sentinel_manifest)
    out=Path(out); evidence=Path(evidence)

    if evidence.exists():
        raise RuntimeError("HOLD_E2C_S0_EVIDENCE_EXISTS")
    if out.exists() or out.with_suffix("").exists():
        raise RuntimeError("HOLD_E2C_S0_OUTPUT_EXISTS")
    if not source_cst.exists() or presolve.sha(source_cst)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E2C_S0_CANONICAL_SOURCE_SHA")

    # The presolve function makes the complete-project copy, applies only the
    # frozen solver-copy port/configuration history, fresh-reopens it, and
    # proves geometry/ports/excitation/result-tree state. It invokes no solver.
    presolve_ev=evidence/"presolve"
    simops_phase("presolve_config","START","NOT_OBSERVED",
                 "configure and qualify frozen 12-port solve copy")
    rc=presolve.main(source_cst,config_macro,inventory_contract,sentinel_manifest,out,presolve_ev)
    if rc!=0:
        simops_phase("presolve_config","HOLD","NOT_OBSERVED","presolve gate failed")
        raise RuntimeError("HOLD_E2C_S0_PRESOLVE_GATE")
    simops_phase("presolve_config","PASS","NOT_OBSERVED")

    configured_sha=presolve.sha(out)
    evidence.mkdir(parents=True,exist_ok=True)
    invocation={
      "formal_solver_invocations":1,
      "automatic_retries":0,
      "retry_authorized":False,
      "solver_started":False,
      "canonical_source_sha256":EXPECTED_SOURCE_SHA256,
      "configured_copy_sha256":configured_sha,
      "source_excitation_set":[1,2,4,5,7,8,10,11],
      "matched_load_only_set":[3,6,9,12],
      "required_complex_traces":96
    }
    write_json(evidence/"solver_invocation.json",invocation)

    # Exactly one formal solver invocation. No loop and no retry path.
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New)
    de.set_quiet_mode(True); p=None
    invocation["solver_started"]=True
    write_json(evidence/"solver_invocation.json",invocation)
    try:
        p=de.open_project(str(out))
        simops_phase("solver_run","START","OBSERVED",
                     "formal one-shot solver invocation boundary")
        p.modeler.run_solver()
        p.save()
        simops_phase("solver_run","PASS","OBSERVED")
    finally:
        if p is not None:
            p.close()
        de.close()

    invocation["solved_artifact_sha256"]=presolve.sha(out)
    invocation["solver_completed"]=True
    write_json(evidence/"solver_invocation.json",invocation)

    qual_ev=evidence/"qualification"
    simops_phase("qualification","START","OBSERVED",
                 "read-only 96-trace numerical and coexistence qualification")
    qrc=qualifier.main(out,sentinel_manifest,qual_ev)
    qsummary=json.loads((qual_ev/"qualification_summary.json").read_text(encoding="utf-8"))
    status=qsummary["status"]
    simops_phase("qualification",
                 "HOLD" if status.startswith("HOLD_") else "PASS",
                 "OBSERVED",status)

    summary={
      "status":status,
      "simulationops":"0.2.25",
      "formal_solver_invocations":1,
      "automatic_retries":0,
      "canonical_source_sha256":EXPECTED_SOURCE_SHA256,
      "configured_copy_sha256":configured_sha,
      "solved_artifact_sha256":presolve.sha(out),
      "presolve_summary":str(presolve_ev/"summary.json"),
      "qualification_summary":str(qual_ev/"qualification_summary.json"),
      "next_boundary":(
        "OFFLINE_MECHANISM_CLASSIFICATION_NO_RERUN"
        if status.startswith("REVIEW_") or status.startswith("HOLD_")
        else "E2C_SENTINEL_PASS_CLOSEOUT_NO_AUTOMATIC_C1"
      )
    }
    write_json(evidence/"summary.json",summary)
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status)
    print("SOLVED_SHA256="+presolve.sha(out))

    if qrc!=0 or status.startswith("HOLD_"):
        simops_phase("complete","HOLD","OBSERVED",status)
        return 4
    simops_phase("complete","PASS","OBSERVED",status)
    return 0

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-cst",required=True)
    ap.add_argument("--config-macro",required=True)
    ap.add_argument("--inventory-contract",required=True)
    ap.add_argument("--sentinel-manifest",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    solver_started=False
    try:
        sys.exit(main(a.source_cst,a.config_macro,a.inventory_contract,a.sentinel_manifest,a.out,a.evidence))
    except Exception:
        ev=Path(a.evidence); ev.mkdir(parents=True,exist_ok=True)
        marker=ev/"solver_invocation.json"
        if marker.exists():
            try:
                solver_started=bool(json.loads(marker.read_text(encoding="utf-8")).get("solver_started"))
            except Exception:
                solver_started=True
        status=("HOLD_E2C_S0_POSTSOLVE_EXECUTION" if solver_started
                else "HOLD_E2C_S0_PRESOLVE_EXECUTION")
        (ev/"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        (ev/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
        simops_phase("complete","HOLD","OBSERVED" if solver_started else "NOT_OBSERVED",status)
        traceback.print_exc()
        sys.exit(9)
