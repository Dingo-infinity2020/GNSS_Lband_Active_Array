from __future__ import print_function
import argparse, hashlib, json, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="f0184b638b5af6c5c752804fd5570a5e4178e52bc6bdd62e31e72c281c03de90"

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,l in enumerate(lines):
        if l.strip()=="Sub Main()": s=i
        elif l.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("HOLD_T2S_SOLVER_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def status_vba(path):
    return "\n".join([
      "Dim f As Integer","f=FreeFile",
      'Open "%s" For Output As #f'%str(path),
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "SOLVER_RUN=NO"',
      "Close #f"
    ])

def parse_status(path):
    out={}
    for l in Path(path).read_text(encoding="utf-8").splitlines():
        if "=" in l:
            k,v=l.split("=",1); out[k]=v
    return out

def solver_tree(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return [x for x in p3.get_tree_items() if "S-Parameters" in x or "Adaptive Meshing" in x]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+str(ex)]

def run(source,solver_macro,out,evidence):
    source=Path(source); solver_macro=Path(solver_macro); out=Path(out); evidence=Path(evidence)
    if evidence.exists(): raise RuntimeError("HOLD_T2S_PREP_EVIDENCE_EXISTS")
    if out.exists(): raise RuntimeError("HOLD_T2S_CONFIGURED_COPY_EXISTS")
    if not source.exists() or sha(source)!=SOURCE_SHA: raise RuntimeError("HOLD_T2S_SOURCE_HASH")
    evidence.mkdir(parents=True)
    out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(str(source),str(out))
    if sha(out)!=SOURCE_SHA: raise RuntimeError("HOLD_T2S_COPY_HASH")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        prj.modeler.add_to_history("AR0-B1R-T2S solver configuration",body(solver_macro))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    configured=sha(out)
    ps=evidence/"presolve_status.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code("Sub Main()\n"+status_vba(ps)+"\nEnd Sub"):
            raise RuntimeError("HOLD_T2S_PRESOLVE_STATUS")
    finally:
        if prj is not None: prj.close()
        de.close()

    st=parse_status(ps)
    tree=solver_tree(out)
    checks={
      "source_hash_exact":sha(source)==SOURCE_SHA,
      "configured_copy_exists":out.exists(),
      "configured_hash_stable_after_reopen":sha(out)==configured,
      "port_count_3":int(st.get("PORT_COUNT","-1"))==3,
      "solver_run_no":st.get("SOLVER_RUN")=="NO",
      "result_tree_empty_before_solve":len(tree)==0
    }
    status="PASS_R1E1A4A_AR0_B1R_T2S_PRESOLVE_CONFIG" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_T2S_PRESOLVE"
    summary={"status":status,"source_sha256":SOURCE_SHA,"configured_sha256":configured,"configured_path":str(out),"checks":checks}
    (evidence/"presolve_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"PRESOLVE_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status); print("CONFIGURED_SHA256="+configured)
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-cst",required=True); ap.add_argument("--solver-macro",required=True)
    ap.add_argument("--output-cst",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(run(a.source_cst,a.solver_macro,a.output_cst,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
