from __future__ import print_function
import argparse, hashlib, json, os, shutil, subprocess, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="ab8a61cc781880ba938b729f44862d1d79f36dbb959288fc57ede5e61b4d2858"

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def status_vba(path):
    return "\n".join([
      "Dim f As Integer","f=FreeFile",
      'Open "%s" For Output As #f'%str(path),
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f"
    ])

def parse_port_count(path):
    for l in Path(path).read_text(encoding="utf-8").splitlines():
        if l.startswith("PORT_COUNT="): return int(l.split("=",1)[1])
    return None

def result_tree(cst):
    pf=ProjectFile(str(cst),allow_interactive=True)
    p3=pf.get_3d()
    return p3.get_tree_items()

def solver_result_paths(tree):
    return [x for x in tree if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def run(repo,evidence,work,source):
    repo=Path(repo); evidence=Path(evidence); work=Path(work); source=Path(source)
    if evidence.exists(): raise RuntimeError("HOLD_T2S_NW_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_T2S_NW_WORK_EXISTS")
    if not source.exists() or sha(source)!=SOURCE_SHA: raise RuntimeError("HOLD_T2S_NW_SOURCE_HASH")
    evidence.mkdir(parents=True); work.mkdir(parents=True)
    dst=work/"R1E1A4A_AR0_B1R_T2S_NW_SOLVED_V01.cst"
    shutil.copy2(str(source),str(dst))
    if sha(dst)!=SOURCE_SHA: raise RuntimeError("HOLD_T2S_NW_COPY_HASH")

    pre=evidence/"presolve_status.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(dst))
        if not prj.schematic.execute_vba_code(wrap(status_vba(pre))):
            raise RuntimeError("HOLD_T2S_NW_PRESOLVE_STATUS_API")
    finally:
        if prj is not None: prj.close()
        de.close()

    tree0=result_tree(dst)
    prechecks={
      "source_hash_exact":sha(source)==SOURCE_SHA,
      "solve_copy_hash_exact":sha(dst)==SOURCE_SHA,
      "port_count_3":parse_port_count(pre)==3,
      "result_tree_empty_before_solve":len(solver_result_paths(tree0))==0
    }
    (evidence/"presolve_summary.json").write_text(json.dumps(prechecks,indent=2)+"\n",encoding="utf-8")
    if not all(prechecks.values()):
        raise RuntimeError("HOLD_T2S_NW_PRESOLVE_GATE")

    # Exactly one formal solver invocation.
    invocation={
      "formal_solver_invocations":1,
      "host":"NW",
      "method":"cst.interface open_project -> modeler.run_solver",
      "source_sha256":SOURCE_SHA
    }
    (evidence/"solver_invocation.json").write_text(json.dumps(invocation,indent=2)+"\n",encoding="utf-8")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(dst))
        prj.modeler.run_solver()
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    solved_sha=sha(dst)

    extractor=repo/"scripts"/"extract_r1e1a4a_ar0_b1r_t2s_results.py"
    p=subprocess.run([sys.executable,str(extractor),"--cst",str(dst),"--outdir",str(evidence)],
                     stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (evidence/"extractor_stdout.txt").write_text(p.stdout,encoding="utf-8")
    if p.returncode!=0:
        raise RuntimeError("HOLD_T2S_NW_RESULT_EXTRACTOR_RC_%d"%p.returncode)

    metrics=json.loads((evidence/"t2s_metrics_summary.json").read_text(encoding="utf-8"))
    numerical=bool(metrics.get("numerical_pass"))
    sparams=bool(metrics.get("sparameter_tree_present"))
    physical=bool(metrics.get("diagnostics",{}).get("passivity_closure_reasonable"))
    characterized=numerical and sparams and physical

    status="PASS_R1E1A4A_AR0_B1R_T2S_NW_BASELINE_CHARACTERIZED" if characterized else "HOLD_R1E1A4A_AR0_B1R_T2S_NW_QUALIFICATION"
    summary={
      "status":status,
      "simulationops":"0.2.8",
      "formal_solver_invocations_this_recovery":1,
      "earlier_cst251_formal_launches":1,
      "earlier_cst251_solver_kernel_starts":0,
      "source_configured_sha256":SOURCE_SHA,
      "solved_sha256":solved_sha,
      "solved_cst":str(dst),
      "port_count":3,
      "frequency_GHz":[1.0,1.8],
      "decision_band_GHz":[1.15,1.65],
      "metrics":metrics,
      "scientific_verdict":metrics.get("scientific_verdict")
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status)
    print("SOLVED_SHA256="+solved_sha)
    print(json.dumps(metrics,indent=2))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-cst",required=True)
    a=ap.parse_args()
    try:
        sys.exit(run(a.repo,a.evidence,a.work,a.source_cst))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_T2S_NW_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
