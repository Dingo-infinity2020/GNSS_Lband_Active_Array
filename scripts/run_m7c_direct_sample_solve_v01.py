"""One-shot same-geometry direct-sample diagnostic. --help cannot import CST."""
from __future__ import print_function
import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path
from m7c_direct_sample_contract_v01 import require_ready,require_direct_config,sha

ROOT = Path(__file__).resolve().parents[1]


def emit(phase,state,boundary,message=""):
    event={"schema_version":"simops-project-event-v0.1","event":"PHASE",
           "phase":phase,"state":state,"production_boundary":boundary}
    if message:
        event["message"]=message
    print("SIMOPS_EVENT "+json.dumps(event,separators=(",",":")),flush=True)


def save(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")


def main(manifest_path,out,evidence):
    m=json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    out,evidence=Path(out),Path(evidence)
    before=require_ready(m,ROOT,out,evidence,fresh=True)
    import configure_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_presolve as presolve
    ci=presolve.ci
    import qualify_m7c_direct_sample_readonly_v01 as qualifier
    presolve.EXPECTED_SOURCE_SHA256=m["canonical_build"]["sha256"]
    presolve.HISTORY_LABEL="R4-A0-E2C-S0 M7C direct-sample presolve config V01"
    config=ROOT/m["execution"]["config_macro"]
    emit("presolve_config","START","NOT_OBSERVED")
    started=time.monotonic()
    rc=presolve.main(m["canonical_build"]["path"],config,ROOT/m["execution"]["inventory_contract"],
                     manifest_path,out,evidence/"presolve")
    if rc!=0 or time.monotonic()-started>m["phase_budgets_seconds"]["presolve_config"]:
        emit("presolve_config","HOLD","NOT_OBSERVED");return 9
    history=(out.with_suffix("")/"Model/3D/Model.mod").read_text(encoding="utf-8",errors="replace")
    position=history.find(presolve.HISTORY_LABEL)
    if position<0:
        raise RuntimeError("HOLD_M7C_DIRECT_CONFIG_HISTORY")
    require_direct_config(history[position:])
    emit("presolve_config","PASS","NOT_OBSERVED")
    invoc={"formal_solver_invocations":0,"automatic_retries":0,"solver_started":False,
           "source_sha256":m["canonical_build"]["sha256"],"python_pid":os.getpid(),
           "configured_copy_sha256":sha(out),"geometry_build_invocations":0}
    save(evidence/"solver_invocation.json",invoc)
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New)
    de.set_quiet_mode(True)
    project=None
    try:
        project=de.open_project(str(out))
        immediately_before=require_ready(m,ROOT,out,evidence,fresh=False)
        save(evidence/"storage_preflight.json",{"before_presolve":before,"before_solver":immediately_before})
        invoc.update(formal_solver_invocations=1,solver_started=True)
        save(evidence/"solver_invocation.json",invoc)
        emit("solver_run","START","OBSERVED")
        started=time.monotonic()
        project.modeler.run_solver()
        project.save()
        invoc["solver_elapsed_seconds"]=time.monotonic()-started
        invoc["solver_completed"]=True
        invoc["solved_artifact_sha256"]=sha(out)
        save(evidence/"solver_invocation.json",invoc)
        if invoc["solver_elapsed_seconds"]>m["phase_budgets_seconds"]["solver_run"]:
            raise RuntimeError("HOLD_M7C_DIRECT_SOLVER_PHASE_ELAPSED_BUDGET")
        emit("solver_run","PASS","OBSERVED")
    finally:
        if project is not None:
            project.close()
        de.close()
    emit("qualification","START","OBSERVED")
    started=time.monotonic()
    rc=qualifier.main(out,manifest_path,evidence/"qualification")
    if time.monotonic()-started>m["phase_budgets_seconds"]["qualification"]:
        raise RuntimeError("HOLD_M7C_DIRECT_QUALIFICATION_PHASE_ELAPSED_BUDGET")
    result=json.loads((evidence/"qualification/diagnostic_evaluation.json").read_text(encoding="utf-8"))
    status=result["status"]
    save(evidence/"summary.json",{"status":status,"diagnostic":result,"formal_solver_invocations":1,
        "automatic_retries":0,"solved_artifact_sha256":sha(out),"science_status":"HOLD_M7C_GUARD",
        "next_boundary":"STOP_DIRECT_SAMPLE_RESULT_REVIEW_NO_GEOMETRY_CHANGE_OR_NEW_SOLVE"})
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    emit("qualification","PASS" if rc==0 else "HOLD","OBSERVED",status)
    emit("complete","PASS" if rc==0 else "HOLD","OBSERVED",status)
    print(status)
    return rc


if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest",required=True);ap.add_argument("--out",required=True);ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.manifest,a.out,a.evidence))
    except Exception:
        ev=Path(a.evidence)
        boundary="NOT_OBSERVED"
        marker=ev/"solver_invocation.json"
        if marker.exists() and json.loads(marker.read_text(encoding="utf-8")).get("solver_started"):
            boundary="OBSERVED"
        if ev.exists():
            (ev/"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
            (ev/"FINAL_STATUS.txt").write_text("HOLD_M7C_DIRECT_EXECUTION\n",encoding="utf-8")
        emit("complete","HOLD",boundary,"HOLD_M7C_DIRECT_EXECUTION")
        traceback.print_exc();sys.exit(9)
