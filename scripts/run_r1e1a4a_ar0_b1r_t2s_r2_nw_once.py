from __future__ import print_function
import argparse, csv, hashlib, json, math, cmath, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="ae3bc705fea01e3a8f1c4a52458f447726843ba32a22d247c085c62b8bb83a7b"

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,l in enumerate(lines):
        if l.strip()=="Sub Main()": s=i
        elif l.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("HOLD_T2S_R2_SOLVER_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

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

def tree(cst):
    pf=ProjectFile(str(cst),allow_interactive=True)
    return pf.get_3d().get_tree_items()

def solver_tree_paths(items):
    return [x for x in items if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def read_s_and_adaptive(cst):
    pf=ProjectFile(str(cst),allow_interactive=True)
    p3=pf.get_3d(); items=p3.get_tree_items()
    data={}
    for i in (1,2,3):
        for j in (1,2,3):
            item=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            if item not in items:
                raise RuntimeError("HOLD_T2S_R2_MISSING_RESULT:"+item)
            data["S%d%d"%(i,j)]=[(float(r[0]),complex(r[1])) for r in p3.get_result_item(item).get_data()]
    delta_paths=[x for x in items if "Adaptive Meshing" in x and x.endswith(r"Delta\All S-Parameters")]
    mesh_paths=[x for x in items if "Adaptive Meshing" in x and x.endswith(r"Meshcells")]
    seq=[]; mesh=[]
    if delta_paths:
        seq=[{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)}
             for r in p3.get_result_item(delta_paths[-1]).get_data()]
    if mesh_paths:
        mesh=[{"pass":int(round(float(r[0]))),"cells":int(round(float(complex(r[1]).real)))}
              for r in p3.get_result_item(mesh_paths[-1]).get_data()]
    adaptive={"delta_path":delta_paths[-1] if delta_paths else None,
              "mesh_path":mesh_paths[-1] if mesh_paths else None,
              "delta_sequence":seq,"meshcells":mesh}
    return data,items,adaptive

def wrap_deg(x):
    while x>180: x-=360
    while x<=-180: x+=360
    return x

def calc(data):
    rows=[]
    for k,f in enumerate([r[0] for r in data["S11"]]):
        s11=data["S11"][k][1]; a=data["S21"][k][1]; b=data["S31"][k][1]
        ma=max(abs(a),1e-300); mb=max(abs(b),1e-300)
        amp=abs(20*math.log10(ma/mb))
        ph=abs(wrap_deg((math.degrees(cmath.phase(a))-math.degrees(cmath.phase(b)))-180.0))
        d=(a-b)/math.sqrt(2.0); c=(a+b)/math.sqrt(2.0)
        cmr=20*math.log10(max(abs(c),1e-300)/max(abs(d),1e-300))
        rr=abs(s11)**2; tt=abs(a)**2+abs(b)**2; pp=rr+tt
        eta=tt/max(1-rr,1e-15); loss=-10*math.log10(max(eta,1e-300))
        rows.append({"f_GHz":f,
          "S11_dB":20*math.log10(max(abs(s11),1e-300)),
          "S21_dB":20*math.log10(ma),"S31_dB":20*math.log10(mb),
          "S21_phase_deg":math.degrees(cmath.phase(a)),"S31_phase_deg":math.degrees(cmath.phase(b)),
          "amp_imbalance_dB":amp,"phase_error_deg":ph,"CMR_dB":cmr,
          "power_closure":pp,"transmitted_power":tt,
          "mismatch_normalized_eta":eta,"normalized_excess_loss_dB":loss})
    return rows

def summarize(rows,adaptive):
    lo,hi=1.15,1.65
    core_rows=[r for r in rows if lo<=r["f_GHz"]<=hi]
    if not core_rows: raise RuntimeError("HOLD_T2S_R2_NO_DECISION_BAND_SAMPLES")
    samples={}
    for name,f0 in (("L5",1.17645),("L2",1.22760),("L1",1.57542)):
        samples[name]=min(rows,key=lambda q:abs(q["f_GHz"]-f0))
    core={
      "worst_S11_dB":max(r["S11_dB"] for r in core_rows),
      "worst_amp_imbalance_dB":max(r["amp_imbalance_dB"] for r in core_rows),
      "worst_phase_error_deg":max(r["phase_error_deg"] for r in core_rows),
      "worst_CMR_dB":max(r["CMR_dB"] for r in core_rows),
      "worst_normalized_excess_loss_dB":max(r["normalized_excess_loss_dB"] for r in core_rows),
      "min_power_closure":min(r["power_closure"] for r in core_rows),
      "max_power_closure":max(r["power_closure"] for r in core_rows)
    }
    diag={
      "return_preferred":core["worst_S11_dB"]<=-15,
      "return_acceptable":core["worst_S11_dB"]<=-10,
      "amp_preferred":core["worst_amp_imbalance_dB"]<=0.25,
      "amp_acceptable":core["worst_amp_imbalance_dB"]<=0.50,
      "phase_preferred":core["worst_phase_error_deg"]<=5,
      "phase_acceptable":core["worst_phase_error_deg"]<=10,
      "cmr_preferred":core["worst_CMR_dB"]<=-20,
      "cmr_acceptable":core["worst_CMR_dB"]<=-15,
      "loss_preferred":core["worst_normalized_excess_loss_dB"]<=0.20,
      "loss_acceptable":core["worst_normalized_excess_loss_dB"]<=0.50,
      "strong_return_concern":core["worst_S11_dB"]>-3,
      "loss_concern":core["worst_normalized_excess_loss_dB"]>1.0,
      "passivity_closure_reasonable":core["max_power_closure"]<=1.02
    }
    if all(diag[k] for k in ("return_preferred","amp_preferred","phase_preferred","cmr_preferred","loss_preferred")):
        verdict="PREFERRED"
    elif all(diag[k] for k in ("return_acceptable","amp_acceptable","phase_acceptable","cmr_acceptable","loss_acceptable")):
        verdict="ACCEPTABLE"
    elif diag["strong_return_concern"] or diag["loss_concern"] or not diag["passivity_closure_reasonable"]:
        verdict="STRONG_CONCERN"
    else:
        verdict="NEEDS_OPTIMIZATION"
    seq=adaptive["delta_sequence"]
    numerical=(len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02)
    return {"decision_band_GHz":[lo,hi],"reference_samples":samples,"core":core,
            "diagnostics":diag,"scientific_verdict":verdict,
            "adaptive":adaptive,"numerical_pass":numerical,
            "passes_executed":adaptive["meshcells"][-1]["pass"] if adaptive["meshcells"] else (seq[-1]["pass"] if seq else None),
            "final_two_delta_s":[seq[-2]["delta_s"],seq[-1]["delta_s"]] if len(seq)>=2 else None}

def copy_native_logs(dst,evidence):
    root=dst.with_suffix("")
    result=root/"Result"
    for name in ("output.txt","Model.log","log.tet"):
        p=result/name
        if p.exists():
            shutil.copy2(str(p),str(evidence/("native_"+name.replace(".","_"))))

def run(repo,evidence,work,source,solver_macro):
    repo=Path(repo); evidence=Path(evidence); work=Path(work); source=Path(source); solver_macro=Path(solver_macro)
    if evidence.exists(): raise RuntimeError("HOLD_T2S_R2_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_T2S_R2_WORK_EXISTS")
    if not source.exists() or sha(source)!=SOURCE_SHA: raise RuntimeError("HOLD_T2S_R2_SOURCE_HASH")
    evidence.mkdir(parents=True); work.mkdir(parents=True)
    dst=work/"R1E1A4A_AR0_B1R_T2S_R2_NW_SOLVED_V01.cst"
    shutil.copy2(str(source),str(dst))
    if sha(dst)!=SOURCE_SHA: raise RuntimeError("HOLD_T2S_R2_COPY_HASH")

    # Apply the frozen solver configuration; no geometry or port edits.
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(dst))
        prj.modeler.add_to_history("AR0-B1R-T2S-R2 solver configuration",macro_body(solver_macro))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    configured_sha=sha(dst)
    ps=evidence/"presolve_status.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(dst))
        if not prj.schematic.execute_vba_code(wrap(status_vba(ps))):
            raise RuntimeError("HOLD_T2S_R2_PRESOLVE_STATUS")
    finally:
        if prj is not None: prj.close()
        de.close()

    t0=tree(dst)
    prechecks={
      "source_hash_exact":sha(source)==SOURCE_SHA,
      "configured_hash_stable":sha(dst)==configured_sha,
      "port_count_3":parse_port_count(ps)==3,
      "result_tree_empty_before_solve":len(solver_tree_paths(t0))==0
    }
    (evidence/"presolve_summary.json").write_text(json.dumps(prechecks,indent=2)+"\n",encoding="utf-8")
    if not all(prechecks.values()): raise RuntimeError("HOLD_T2S_R2_PRESOLVE_GATE")

    (evidence/"solver_invocation.json").write_text(json.dumps({
      "formal_solver_invocations":1,"host":"NW","retry_authorized":False,
      "source_fixture_sha256":SOURCE_SHA,"configured_sha256":configured_sha
    },indent=2)+"\n",encoding="utf-8")

    # Exactly one formal solver invocation.
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(dst))
        prj.modeler.run_solver()
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    copy_native_logs(dst,evidence)
    solved_sha=sha(dst)

    try:
        data,items,adaptive=read_s_and_adaptive(dst)
        rows=calc(data)
        metrics=summarize(rows,adaptive)
        with (evidence/"t2s_r2_metrics.csv").open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        (evidence/"t2s_r2_metrics_summary.json").write_text(json.dumps(metrics,indent=2)+"\n",encoding="utf-8")
        characterized=bool(metrics["numerical_pass"] and metrics["diagnostics"]["passivity_closure_reasonable"])
        status="PASS_R1E1A4A_AR0_B1R_T2S_R2_NW_BASELINE_CHARACTERIZED" if characterized else "HOLD_R1E1A4A_AR0_B1R_T2S_R2_QUALIFICATION"
        summary={"status":status,"simulationops":"0.2.8","formal_solver_invocations":1,"automatic_retries":0,
                 "source_fixture_sha256":SOURCE_SHA,"configured_sha256":configured_sha,"solved_sha256":solved_sha,
                 "solved_cst":str(dst),"sparameters_produced":True,"metrics":metrics,
                 "scientific_verdict":metrics["scientific_verdict"]}
    except Exception as ex:
        status="HOLD_R1E1A4A_AR0_B1R_T2S_R2_NO_VALID_RESULTS"
        summary={"status":status,"simulationops":"0.2.8","formal_solver_invocations":1,"automatic_retries":0,
                 "source_fixture_sha256":SOURCE_SHA,"configured_sha256":configured_sha,"solved_sha256":solved_sha,
                 "solved_cst":str(dst),"sparameters_produced":False,"result_error":str(ex)}
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status); print("SOLVED_SHA256="+solved_sha); print(json.dumps(summary,indent=2))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True); ap.add_argument("--source-cst",required=True)
    ap.add_argument("--solver-macro",required=True)
    a=ap.parse_args()
    try:
        sys.exit(run(a.repo,a.evidence,a.work,a.source_cst,a.solver_macro))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_T2S_R2_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
