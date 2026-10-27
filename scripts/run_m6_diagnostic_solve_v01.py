from __future__ import print_function
import argparse, json, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from configure_m6_diagnostic_presolve_v01 import configure
from qualify_m6_diagnostic_readonly_v01 import qualify

PREFIX="SIMOPS_EVENT "
def emit(phase,state,boundary,message=""):
    o={"schema_version":"simops-project-event-v0.1","event":"PHASE","phase":phase,"state":state,"production_boundary":boundary}
    if message: o["message"]=message
    print(PREFIX+json.dumps(o,separators=(",",":")),flush=True)

def main(manifest,out,evidence):
    manifest=Path(manifest); out=Path(out); evidence=Path(evidence)
    emit("presolve_config","START","NOT_OBSERVED")
    cfg=configure(manifest,out,evidence)
    emit("presolve_config","PASS","NOT_OBSERVED")

    (evidence/"solver_invocation.json").write_text(json.dumps({
      "formal_solver_invocations":1,"automatic_retries":0,"retry_authorized":False,
      "configured_sha256":cfg["configured_sha256"],"source_sha256":cfg["source_sha256"]},indent=2)+"\n",encoding="utf-8")

    emit("solver_run","START","OBSERVED")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        p.modeler.run_solver()
        p.save()
    finally:
        if p is not None: p.close()
        de.close()
    emit("solver_run","PASS","OBSERVED")

    emit("qualification","START","OBSERVED")
    rc=qualify(manifest,out,evidence)
    emit("qualification","PASS" if rc==0 else "HOLD","OBSERVED")
    emit("complete","PASS" if rc==0 else "HOLD","OBSERVED")
    return rc

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--variant-manifest",required=True); ap.add_argument("--out",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.variant_manifest,a.out,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_M6_DIAGNOSTIC_SOLVE_EXECUTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
