from __future__ import print_function
import argparse, csv, hashlib, json, math, cmath, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SHA_A="5aa3dd603607a70f7ac190c746e25af550f6cfcb81a9b1bb45846d9c776b6bcd"
SHA_B="93d97b06bc2a739f84f88454a7efa76b27731e7bbdb2714214118a3ec0bafb35"

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
    if s is None or e is None or e<=s: raise RuntimeError("SOLVER_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def port_status(path):
    return "\n".join(["Dim f As Integer","f=FreeFile",
      'Open "%s" For Output As #f'%str(path).replace("\\","/"),
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',"Close #f"])

def parse_port_count(path):
    for l in Path(path).read_text(encoding="utf-8").splitlines():
        if l.startswith("PORT_COUNT="): return int(l.split("=",1)[1])
    return None

def tree(cst):
    return ProjectFile(str(cst),allow_interactive=True).get_3d().get_tree_items()

def solver_paths(items):
    return [x for x in items if ("S-Parameters" in x or "Convergence" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def copy_native(dst,evidence):
    result=dst.with_suffix("")/"Result"
    for n in ("output.txt","Model.log","log.tet"):
        p=result/n
        if p.exists(): shutil.copy2(str(p),str(evidence/("native_"+n.replace(".","_"))))

def native_flags(evidence):
    txt=""
    for n in ("native_output_txt","native_Model_log","native_log_tet"):
        p=evidence/n
        if p.exists(): txt+="\n"+p.read_text(encoding="utf-8",errors="ignore")
    return {
      "bad_conductor_warning":"not connected to any good conductor" in txt.lower(),
      "mesh_corruption":"mesh near the lumped element" in txt.lower(),
      "large_reflection_warning":"input reflection seems to be large" in txt.lower()
    }

def choose_run(p3,paths):
    common=None
    allids={}
    for path in paths:
        ids=list(p3.get_run_ids(path,False))
        allids[path]=ids
        common=set(ids) if common is None else common.intersection(ids)
    if not common: raise RuntimeError("NO_COMMON_VALID_RUN_ID:"+json.dumps(allids))
    # highest run id avoids stale/deleted run-0 artifacts observed in prior stages.
    return max(common),allids

def read_s(cst,nport):
    pf=ProjectFile(str(cst),allow_interactive=True); p3=pf.get_3d(); items=p3.get_tree_items()
    paths=[r"1D Results\S-Parameters\S%d,%d"%(i,j) for i in range(1,nport+1) for j in range(1,nport+1)]
    for p in paths:
        if p not in items: raise RuntimeError("MISSING:"+p)
    rid,allids=choose_run(p3,paths)
    data={}
    for i in range(1,nport+1):
        for j in range(1,nport+1):
            p=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            data["S%d%d"%(i,j)]=[(float(r[0]),complex(r[1])) for r in p3.get_result_item(p,rid).get_data()]
    conv=r"1D Results\Convergence\S-Parameters\All S-Parameters"
    if conv not in items: raise RuntimeError("MISSING_CONVERGENCE_PATH")
    cids=list(p3.get_run_ids(conv,False))
    crid=rid if rid in cids else max(cids)
    seq=[{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)}
         for r in p3.get_result_item(conv,crid).get_data()]
    return data,items,{"selected_run_id":rid,"sparameter_run_ids":allids,"convergence_run_ids":cids,
                       "convergence_selected_run_id":crid,"delta_sequence":seq}

def db(z): return 20*math.log10(max(abs(z),1e-300))
def wrapdeg(x):
    while x>180: x-=360
    while x<=-180: x+=360
    return x
def zin100(s): return 100.0*(1+s)/(1-s) if abs(1-s)>1e-15 else complex(float("inf"),float("inf"))

def ref_samples(rows):
    out={}
    for name,f0 in (("L5",1.17645),("L2",1.22760),("L1",1.57542)):
        out[name]=min(rows,key=lambda r:abs(r["f_GHz"]-f0))
    return out

def metrics_a(data,runmeta):
    rows=[]
    freqs=[r[0] for r in data["S11"]]
    for k,f in enumerate(freqs):
        s11=data["S11"][k][1]; s21=data["S21"][k][1]; s12=data["S12"][k][1]; s22=data["S22"][k][1]
        rr=abs(s11)**2; tt=abs(s21)**2; closure=rr+tt
        eta=tt/max(1-rr,1e-15); loss=-10*math.log10(max(eta,1e-300))
        z=zin100(s11)
        rows.append({"f_GHz":f,"S11_dB":db(s11),"S22_dB":db(s22),"S21_dB":db(s21),"S12_dB":db(s12),
                     "reciprocity_abs_dB":abs(db(s21)-db(s12)),"power_closure":closure,
                     "mismatch_normalized_eta":eta,"normalized_excess_loss_dB":loss,
                     "Zin_real_ohm":z.real,"Zin_imag_ohm":z.imag})
    core=[r for r in rows if 1.15<=r["f_GHz"]<=1.65]
    c={"worst_S11_dB":max(r["S11_dB"] for r in core),"worst_S22_dB":max(r["S22_dB"] for r in core),
       "min_S21_dB":min(r["S21_dB"] for r in core),"worst_reciprocity_abs_dB":max(r["reciprocity_abs_dB"] for r in core),
       "worst_normalized_excess_loss_dB":max(r["normalized_excess_loss_dB"] for r in core),
       "min_power_closure":min(r["power_closure"] for r in core),"max_power_closure":max(r["power_closure"] for r in core),
       "Zin_real_range_ohm":[min(r["Zin_real_ohm"] for r in core),max(r["Zin_real_ohm"] for r in core)],
       "Zin_imag_range_ohm":[min(r["Zin_imag_ohm"] for r in core),max(r["Zin_imag_ohm"] for r in core)]}
    seq=runmeta["delta_sequence"]; numerical=len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02
    diag={"return_acceptable":c["worst_S11_dB"]<=-10 and c["worst_S22_dB"]<=-10,
          "loss_acceptable":c["worst_normalized_excess_loss_dB"]<=0.5,
          "passivity_closure_reasonable":c["max_power_closure"]<=1.02,
          "strong_return_concern":max(c["worst_S11_dB"],c["worst_S22_dB"])>-3,
          "loss_concern":c["worst_normalized_excess_loss_dB"]>1.0}
    verdict="ACCEPTABLE" if diag["return_acceptable"] and diag["loss_acceptable"] else ("STRONG_CONCERN" if diag["strong_return_concern"] or diag["loss_concern"] else "NEEDS_OPTIMIZATION")
    return rows,{"decision_band_GHz":[1.15,1.65],"core":c,"reference_samples":ref_samples(rows),
                 "adaptive":runmeta,"numerical_pass":numerical,"final_two_delta_s":[seq[-2]["delta_s"],seq[-1]["delta_s"]] if len(seq)>=2 else None,
                 "scientific_verdict":verdict,"diagnostics":diag}

def metrics_b(data,runmeta):
    rows=[]; freqs=[r[0] for r in data["S11"]]
    for k,f in enumerate(freqs):
        s11=data["S11"][k][1]; a=data["S21"][k][1]; b=data["S31"][k][1]
        ma=max(abs(a),1e-300); mb=max(abs(b),1e-300)
        amp=abs(20*math.log10(ma/mb))
        ph=abs(wrapdeg((math.degrees(cmath.phase(a))-math.degrees(cmath.phase(b)))-180))
        d=(a-b)/math.sqrt(2); c=(a+b)/math.sqrt(2)
        cmr=20*math.log10(max(abs(c),1e-300)/max(abs(d),1e-300))
        rr=abs(s11)**2; tt=abs(a)**2+abs(b)**2; closure=rr+tt
        eta=tt/max(1-rr,1e-15); loss=-10*math.log10(max(eta,1e-300)); z=zin100(s11)
        rows.append({"f_GHz":f,"S11_dB":db(s11),"S21_dB":db(a),"S31_dB":db(b),
                     "amp_imbalance_dB":amp,"phase_error_deg":ph,"CMR_dB":cmr,
                     "power_closure":closure,"normalized_excess_loss_dB":loss,
                     "Zin_real_ohm":z.real,"Zin_imag_ohm":z.imag})
    core=[r for r in rows if 1.15<=r["f_GHz"]<=1.65]
    c={"worst_S11_dB":max(r["S11_dB"] for r in core),
       "worst_amp_imbalance_dB":max(r["amp_imbalance_dB"] for r in core),
       "worst_phase_error_deg":max(r["phase_error_deg"] for r in core),
       "worst_CMR_dB":max(r["CMR_dB"] for r in core),
       "worst_normalized_excess_loss_dB":max(r["normalized_excess_loss_dB"] for r in core),
       "min_power_closure":min(r["power_closure"] for r in core),"max_power_closure":max(r["power_closure"] for r in core),
       "Zin_real_range_ohm":[min(r["Zin_real_ohm"] for r in core),max(r["Zin_real_ohm"] for r in core)],
       "Zin_imag_range_ohm":[min(r["Zin_imag_ohm"] for r in core),max(r["Zin_imag_ohm"] for r in core)]}
    seq=runmeta["delta_sequence"]; numerical=len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02
    diag={"return_acceptable":c["worst_S11_dB"]<=-10,"amp_acceptable":c["worst_amp_imbalance_dB"]<=0.5,
          "phase_acceptable":c["worst_phase_error_deg"]<=10,"cmr_acceptable":c["worst_CMR_dB"]<=-15,
          "loss_acceptable":c["worst_normalized_excess_loss_dB"]<=0.5,
          "passivity_closure_reasonable":c["max_power_closure"]<=1.02,
          "strong_return_concern":c["worst_S11_dB"]>-3,"loss_concern":c["worst_normalized_excess_loss_dB"]>1}
    verdict="ACCEPTABLE" if all(diag[k] for k in ("return_acceptable","amp_acceptable","phase_acceptable","cmr_acceptable","loss_acceptable")) else ("STRONG_CONCERN" if diag["strong_return_concern"] or diag["loss_concern"] or not diag["passivity_closure_reasonable"] else "NEEDS_OPTIMIZATION")
    return rows,{"decision_band_GHz":[1.15,1.65],"core":c,"reference_samples":ref_samples(rows),
                 "adaptive":runmeta,"numerical_pass":numerical,"final_two_delta_s":[seq[-2]["delta_s"],seq[-1]["delta_s"]] if len(seq)>=2 else None,
                 "scientific_verdict":verdict,"diagnostics":diag}

def solve_branch(tag,source,expected_sha,nport,work,evidence,solver_macro):
    source=Path(source); work=Path(work); evidence=Path(evidence); evidence.mkdir(parents=True); work.mkdir(parents=True)
    if sha(source)!=expected_sha: raise RuntimeError(tag+"_SOURCE_HASH")
    dst=work/("R1E1A4A_AR0_B1R_R3_D1R1%s_SOLVED_V01.cst"%tag)
    if dst.exists(): raise RuntimeError(tag+"_DST_EXISTS")
    shutil.copy2(str(source),str(dst))
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(dst)); p.modeler.add_to_history("R3-D1R1%s solver configuration"%tag,macro_body(solver_macro)); p.save()
    finally:
        if p is not None: p.close()
        de.close()
    configured_sha=sha(dst)
    ps=evidence/"presolve_status.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(dst))
        if not p.schematic.execute_vba_code(wrap(port_status(ps))): raise RuntimeError(tag+"_PORT_AUDIT")
    finally:
        if p is not None: p.close()
        de.close()
    pre={"source_sha_exact":sha(source)==expected_sha,"port_count":parse_port_count(ps),
         "port_count_expected":nport,"empty_result_tree":len(solver_paths(tree(dst)))==0}
    (evidence/"presolve_summary.json").write_text(json.dumps(pre,indent=2)+"\n",encoding="utf-8")
    if pre["port_count"]!=nport or not pre["empty_result_tree"]: raise RuntimeError(tag+"_PRESOLVE_GATE")
    (evidence/"solver_invocation.json").write_text(json.dumps({"formal_solver_invocations":1,"retry_authorized":False,"host":"NW","configured_sha256":configured_sha},indent=2)+"\n",encoding="utf-8")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(dst)); p.modeler.run_solver(); p.save()
    finally:
        if p is not None: p.close()
        de.close()
    copy_native(dst,evidence)
    flags=native_flags(evidence)
    data,items,runmeta=read_s(dst,nport)
    rows,metrics=(metrics_a(data,runmeta) if nport==2 else metrics_b(data,runmeta))
    csvname=evidence/("metrics_%s.csv"%tag)
    with csvname.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    qualified=metrics["numerical_pass"] and metrics["diagnostics"]["passivity_closure_reasonable"] and not flags["bad_conductor_warning"] and not flags["mesh_corruption"]
    status="PASS_R1E1A4A_AR0_B1R_R3_D1R1%s_CHARACTERIZED"%tag if qualified else "HOLD_R1E1A4A_AR0_B1R_R3_D1R1%s_QUALIFICATION"%tag
    out={"status":status,"formal_solver_invocations":1,"automatic_retries":0,"source_sha256":expected_sha,
         "configured_sha256":configured_sha,"solved_sha256":sha(dst),"solved_cst":str(dst),
         "native_flags":flags,"metrics":metrics,"scientific_verdict":metrics["scientific_verdict"]}
    (evidence/"summary.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    return out

def main(a,b,solver,workroot,evroot):
    workroot=Path(workroot); evroot=Path(evroot)
    if workroot.exists(): raise RuntimeError("WORKROOT_EXISTS")
    if evroot.exists(): raise RuntimeError("EVROOT_EXISTS")
    workroot.mkdir(parents=True); evroot.mkdir(parents=True)
    results={}
    for tag,src,h,n in (("A",a,SHA_A,2),("B",b,SHA_B,3)):
        try:
            results[tag]=solve_branch(tag,src,h,n,workroot/tag,evroot/tag,Path(solver))
        except Exception as ex:
            ed=evroot/tag; ed.mkdir(parents=True,exist_ok=True)
            (ed/"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
            (ed/"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R3_D1R1%s_EXECUTION\n"%tag,encoding="utf-8")
            results[tag]={"status":"HOLD_R1E1A4A_AR0_B1R_R3_D1R1%s_EXECUTION"%tag,"error":str(ex)}
    both=all(results[x]["status"].startswith("PASS_") for x in ("A","B"))
    status="PASS_R1E1A4A_AR0_B1R_R3_D1R1_DIAGNOSTIC_SOLVES" if both else "HOLD_R1E1A4A_AR0_B1R_R3_D1R1_DIAGNOSTIC_SOLVES_PARTIAL"
    (evroot/"summary.json").write_text(json.dumps({"status":status,"branches":results},indent=2)+"\n",encoding="utf-8")
    (evroot/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status); print(json.dumps(results,indent=2))
    return 0 if both else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-a",required=True); ap.add_argument("--source-b",required=True); ap.add_argument("--solver-macro",required=True)
    ap.add_argument("--work-root",required=True); ap.add_argument("--evidence-root",required=True)
    x=ap.parse_args()
    try: sys.exit(main(x.source_a,x.source_b,x.solver_macro,x.work_root,x.evidence_root))
    except Exception:
        Path(x.evidence_root).mkdir(parents=True,exist_ok=True)
        Path(x.evidence_root,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
