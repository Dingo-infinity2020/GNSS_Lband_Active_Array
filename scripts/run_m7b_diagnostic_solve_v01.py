from __future__ import print_function
import argparse, json, sys, traceback
from pathlib import Path
LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
import configure_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_presolve as presolve
import qualify_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_readonly as qualifier
import evaluate_m7b_corrective_readonly_v01 as evaluator

def emit(phase,state,boundary,message=""):
    o={"schema_version":"simops-project-event-v0.1","event":"PHASE","phase":phase,"state":state,"production_boundary":boundary}
    if message:o["message"]=message
    print("SIMOPS_EVENT "+json.dumps(o,separators=(",",":")),flush=True)

def main(manifest_path,out,evidence):
    manifest_path=Path(manifest_path); out=Path(out); evidence=Path(evidence)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    source=Path(m["canonical_build"]["path"]); config=ROOT/m["execution"]["config_macro"]; inv=ROOT/m["execution"]["inventory_contract"]
    # Reuse the proven full-E2C 12-port presolve implementation, rebound only to the reviewed M7B source SHA.
    presolve.EXPECTED_SOURCE_SHA256=m["canonical_build"]["sha256"]
    presolve.HISTORY_LABEL="R4-A0-E2C-S0 M7B diagnostic presolve config V01"

    emit("presolve_config","START","NOT_OBSERVED")
    rc=presolve.main(source,config,inv,manifest_path,out,evidence/"presolve")
    if rc!=0:
        emit("presolve_config","HOLD","NOT_OBSERVED"); return 9
    emit("presolve_config","PASS","NOT_OBSERVED")
    evidence.mkdir(parents=True,exist_ok=True)
    invoc={"formal_solver_invocations":1,"automatic_retries":0,"retry_authorized":False,
           "solver_started":False,"source_sha256":m["canonical_build"]["sha256"]}
    (evidence/"solver_invocation.json").write_text(json.dumps(invoc,indent=2)+"\n",encoding="utf-8")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
      p=de.open_project(str(out))
      invoc["solver_started"]=True; (evidence/"solver_invocation.json").write_text(json.dumps(invoc,indent=2)+"\n",encoding="utf-8")
      emit("solver_run","START","OBSERVED")
      p.modeler.run_solver()
      p.save()
      emit("solver_run","PASS","OBSERVED")
    finally:
      if p is not None:p.close()
      de.close()

    invoc["solver_completed"]=True; invoc["solved_artifact_sha256"]=presolve.sha(out)
    (evidence/"solver_invocation.json").write_text(json.dumps(invoc,indent=2)+"\n",encoding="utf-8")
    emit("qualification","START","OBSERVED")
    qrc=qualifier.main(out,manifest_path,evidence/"qualification")
    qsum=evidence/"qualification"/"qualification_summary.json"
    if not qsum.exists():
      emit("qualification","HOLD","OBSERVED","missing numerical summary"); return 9
    emit("corrective_evaluation","START","OBSERVED")
    erc=evaluator.main(evidence/"qualification"/"loaded_response_native.csv",manifest_path,qsum,evidence/"corrective")
    final=(evidence/"corrective"/"FINAL_STATUS.txt").read_text(encoding="utf-8").strip()
    (evidence/"FINAL_STATUS.txt").write_text(final+"\n",encoding="utf-8")
    summary={"status":final,"formal_solver_invocations":1,"automatic_retries":0,
             "solved_artifact_sha256":presolve.sha(out),
             "numerical_qualification":str(qsum),
             "corrective_evaluation":str(evidence/"corrective"/"corrective_evaluation.json"),
             "next_boundary":"M7B_RESULT_REVIEW_NO_AUTOMATIC_NEXT_STAGE"}
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    emit("corrective_evaluation","PASS" if not final.startswith("HOLD_") else "HOLD","OBSERVED",final)
    emit("complete","PASS" if qrc==0 and erc==0 else "HOLD","OBSERVED",final)
    print(final); print("SOLVED_SHA256="+presolve.sha(out))
    return 0 if qrc==0 and erc==0 else 4

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--manifest",required=True); ap.add_argument("--out",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.manifest,a.out,a.evidence))
    except Exception:
      ev=Path(a.evidence); ev.mkdir(parents=True,exist_ok=True)
      marker=ev/"solver_invocation.json"; started=False
      if marker.exists():
        try:started=bool(json.loads(marker.read_text(encoding="utf-8")).get("solver_started"))
        except:started=True
      status="HOLD_M7B_POSTSOLVE_EXECUTION" if started else "HOLD_M7B_PRESOLVE_EXECUTION"
      (ev/"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
      (ev/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
      emit("complete","HOLD","OBSERVED" if started else "NOT_OBSERVED",status)
      traceback.print_exc(); sys.exit(9)
