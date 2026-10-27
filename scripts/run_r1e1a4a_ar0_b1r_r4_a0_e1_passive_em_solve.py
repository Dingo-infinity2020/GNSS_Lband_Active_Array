from __future__ import print_function
import argparse, csv, hashlib, json, math, cmath, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

EXPECTED_SOURCE_SHA256="aee6bc30085c002b6063de80f110096f6b62911bf897007d133b309e5a962b36"
SOLVER_HISTORY_LABEL="R4-A0-E1 passive EM solver config V01"

EXPECTED_PORTS={
1:(0.0,4.650,0.0,0.0,4.650,-1.0,50.0),
2:(0.0,6.085,0.0,0.0,6.085,-1.0,50.0),
3:(0.0,7.915,0.0,0.0,7.915,-1.0,50.0),
4:(0.0,9.350,0.0,0.0,9.350,-1.0,50.0),
5:(1.45,9.800,0.0,1.45,9.800,-1.0,50.0),
6:(-0.50,6.085,0.0,-0.50,6.085,-1.0,50.0),
}

GNSS_REFS={"L5":1.17645,"L2":1.22760,"L1":1.57542}

# These are interpretation sentinels, not solve PASS/FAIL gates.
COUPLING_SENTINELS={
"device_bypass_P_IN_to_P_OUT":(3,2),
"end_to_end_bypass_E_UP_to_E_DN":(4,1),
"cross_gap_CIN_parasitic":(2,1),
"cross_gap_COUT_parasitic":(4,3),
"cross_gap_L1_parasitic":(5,3),
"VBIAS_to_E_UP":(6,1),
"VBIAS_to_P_IN":(6,2),
"VBIAS_to_P_OUT":(6,3),
"VBIAS_to_E_DN":(6,4),
"VBIAS_to_B_VDD":(6,5),
}

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,line in enumerate(lines):
        if line.strip()=="Sub Main()": s=i
        elif line.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("HOLD_E1S0_SOLVER_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def wrap(body):
    return "Sub Main()\n"+body+"\nEnd Sub"

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    srcdir=src.with_suffix(""); dstdir=dst.with_suffix("")
    if not srcdir.exists():
        raise RuntimeError("HOLD_E1S0_SOURCE_COMPANION_MISSING:"+str(srcdir))
    if dstdir.exists():
        shutil.rmtree(str(dstdir),ignore_errors=True)
    shutil.copytree(str(srcdir),str(dstdir))

def port_audit_vba(path):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Integer, stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",'Open "%s" For Output As #f'%p,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "For i=1 To 6",
      " Err.Clear",
      " pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P|" & CStr(i) & "|PROP_OK=" & CStr(pok) & "|ERR=" & CStr(Err.Number) & "|TYPE=" & stype & "|ZREF=" & CStr(zref)',
      " Err.Clear",
      " cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "C|" & CStr(i) & "|COORD_OK=" & CStr(cok) & "|ERR=" & CStr(Err.Number) & "|P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0) & "|P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i","Close #f","On Error GoTo 0"])

def parse_ports(path):
    out={"count":None,"properties":{},"coordinates":{}}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("PORT_COUNT="):
            out["count"]=int(line.split("=",1)[1])
        elif line.startswith("P|"):
            parts=line.split("|"); idx=int(parts[1]); d={}
            for x in parts[2:]:
                k,v=x.split("=",1); d[k]=v
            out["properties"][idx]=d
        elif line.startswith("C|"):
            parts=line.split("|"); idx=int(parts[1]); d={}
            for x in parts[2:]:
                k,v=x.split("=",1); d[k]=v
            out["coordinates"][idx]=d
    return out

def parse_xyz(s):
    return tuple(float(x) for x in s.split(","))

def ports_ok(data):
    if data["count"]!=6:
        return False
    tol=1e-9
    for i,e in EXPECTED_PORTS.items():
        p=data["properties"].get(i,{})
        c=data["coordinates"].get(i,{})
        if p.get("PROP_OK") not in ("True","TRUE","1","-1"): return False
        if c.get("COORD_OK") not in ("True","TRUE","1","-1"): return False
        if p.get("TYPE")!="SParameter": return False
        if abs(float(p.get("ZREF","nan"))-e[6])>tol: return False
        p1=parse_xyz(c["P1"]); p2=parse_xyz(c["P2"])
        if any(abs(a-b)>tol for a,b in zip(p1,e[:3])): return False
        if any(abs(a-b)>tol for a,b in zip(p2,e[3:6])): return False
    return True

def solver_paths(items):
    return [x for x in items if ("S-Parameters" in x or "Convergence" in x or
                                 "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def result_tree(cst):
    return ProjectFile(str(cst),allow_interactive=True).get_3d().get_tree_items()

def copy_native(dst,evidence):
    result=Path(dst).with_suffix("")/"Result"
    for n in ("output.txt","Model.log","log.tet"):
        p=result/n
        if p.exists():
            shutil.copy2(str(p),str(Path(evidence)/("native_"+n.replace(".","_"))))

def native_flags(evidence):
    txt=""
    for n in ("native_output_txt","native_Model_log","native_log_tet"):
        p=Path(evidence)/n
        if p.exists():
            txt+="\n"+p.read_text(encoding="utf-8",errors="ignore")
    lo=txt.lower()
    return {
      "fatal_error":("fatal error" in lo or "solver failed" in lo or "aborted due to" in lo),
      "mesh_corruption":("mesh near the lumped element" in lo or "corrupt mesh" in lo),
      "large_reflection_warning":"input reflection seems to be large" in lo,
      "disconnected_conductor_warning":"not connected to any good conductor" in lo,
    }

def choose_common_run(p3,paths):
    common=None; ids={}
    for path in paths:
        rids=list(p3.get_run_ids(path,False))
        ids[path]=rids
        common=set(rids) if common is None else common.intersection(rids)
    if not common:
        raise RuntimeError("HOLD_E1S0_NO_COMMON_SPARAM_RUN:"+json.dumps(ids))
    return max(common),ids

def read_network(cst):
    pf=ProjectFile(str(cst),allow_interactive=True)
    p3=pf.get_3d()
    items=p3.get_tree_items()
    paths=[r"1D Results\S-Parameters\S%d,%d"%(i,j) for j in range(1,7) for i in range(1,7)]
    for path in paths:
        if path not in items:
            raise RuntimeError("HOLD_E1S0_MISSING_SPARAM:"+path)
    rid,allids=choose_common_run(p3,paths)
    data={}
    reference_freqs=None
    for j in range(1,7):
        for i in range(1,7):
            path=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            vals=[(float(r[0]),complex(r[1])) for r in p3.get_result_item(path,rid).get_data()]
            freqs=[x[0] for x in vals]
            if reference_freqs is None:
                reference_freqs=freqs
            elif len(freqs)!=len(reference_freqs) or any(abs(a-b)>1e-9 for a,b in zip(freqs,reference_freqs)):
                raise RuntimeError("HOLD_E1S0_SPARAM_NATIVE_GRID_MISMATCH:"+path)
            data[(i,j)]=vals

    conv=r"1D Results\Convergence\S-Parameters\All S-Parameters"
    if conv not in items:
        raise RuntimeError("HOLD_E1S0_MISSING_CONVERGENCE_PATH")
    cids=list(p3.get_run_ids(conv,False))
    crid=rid if rid in cids else max(cids)
    seq=[{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)}
         for r in p3.get_result_item(conv,crid).get_data()]
    return data,{
      "selected_run_id":rid,
      "sparameter_run_ids":allids,
      "convergence_run_ids":cids,
      "convergence_selected_run_id":crid,
      "delta_sequence":seq,
      "native_frequency_count":len(reference_freqs),
      "native_frequency_min_ghz":min(reference_freqs),
      "native_frequency_max_ghz":max(reference_freqs),
    }

def db(z):
    return 20.0*math.log10(max(abs(z),1e-300))

def phase_deg(z):
    return math.degrees(cmath.phase(z))

def interpolate_complex(vals,f0):
    if f0<=vals[0][0]: return vals[0][1]
    if f0>=vals[-1][0]: return vals[-1][1]
    for k in range(1,len(vals)):
        f1=vals[k][0]
        if f1>=f0:
            fa,za=vals[k-1]; fb,zb=vals[k]
            if abs(fb-fa)<1e-15: return za
            a=(f0-fa)/(fb-fa)
            return za+a*(zb-za)
    return vals[-1][1]

def nearest_native(vals,f0):
    f,z=min(vals,key=lambda x:abs(x[0]-f0))
    return {"f_ghz":f,"offset_mhz":(f-f0)*1000.0,"real":z.real,"imag":z.imag,
            "db":db(z),"phase_deg":phase_deg(z)}

def write_native_csv(path,data):
    freqs=[x[0] for x in data[(1,1)]]
    header=["f_GHz"]
    for j in range(1,7):
        for i in range(1,7):
            p="S%d%d"%(i,j)
            header += [p+"_real",p+"_imag",p+"_dB",p+"_phase_deg"]
    with open(str(path),"w",newline="") as f:
        w=csv.writer(f); w.writerow(header)
        for k,fr in enumerate(freqs):
            row=[fr]
            for j in range(1,7):
                for i in range(1,7):
                    z=data[(i,j)][k][1]
                    row += [z.real,z.imag,db(z),phase_deg(z)]
            w.writerow(row)

def characterize(data,runmeta):
    freqs=[x[0] for x in data[(1,1)]]
    full_indices=list(range(len(freqs)))
    core_indices=[k for k,f in enumerate(freqs) if 1.15-1e-12<=f<=1.65+1e-12]
    if not core_indices:
        raise RuntimeError("HOLD_E1S0_NO_NATIVE_CORE_SAMPLES")

    recip=[]
    column_power=[]
    for k in full_indices:
        for i in range(1,7):
            for j in range(i+1,7):
                recip.append({"f_ghz":freqs[k],"i":i,"j":j,
                              "abs_complex":abs(data[(i,j)][k][1]-data[(j,i)][k][1])})
        for j in range(1,7):
            ps=sum(abs(data[(i,j)][k][1])**2 for i in range(1,7))
            column_power.append({"f_ghz":freqs[k],"excitation_port":j,"sum_abs_s_sq":ps})

    max_recip=max(recip,key=lambda x:x["abs_complex"])
    max_power=max(column_power,key=lambda x:x["sum_abs_s_sq"])
    min_power=min(column_power,key=lambda x:x["sum_abs_s_sq"])

    coupling={}
    for label,(i,j) in COUPLING_SENTINELS.items():
        core=[(freqs[k],data[(i,j)][k][1]) for k in core_indices]
        peak=max(core,key=lambda x:abs(x[1]))
        peak_db=db(peak[1])
        coupling[label]={
          "ports":[i,j],
          "max_core_db":peak_db,
          "frequency_ghz":peak[0],
          "review_gt_minus20db":peak_db>-20.0,
          "severe_gt_minus10db":peak_db>-10.0,
        }

    exact={}
    for name,f0 in GNSS_REFS.items():
        exact[name]={"target_ghz":f0,"interpolation":"linear_complex"}
        for label,(i,j) in COUPLING_SENTINELS.items():
            z=interpolate_complex(data[(i,j)],f0)
            exact[name][label]={"real":z.real,"imag":z.imag,"db":db(z),"phase_deg":phase_deg(z)}
        exact[name]["nearest_native_S11"]=nearest_native(data[(1,1)],f0)

    seq=runmeta["delta_sequence"]
    numerical=(len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02)
    reciprocity_ok=max_recip["abs_complex"]<=0.02
    passivity_ok=max_power["sum_abs_s_sq"]<=1.02

    return {
      "decision_band_ghz":[1.15,1.65],
      "modeled_band_ghz":[1.0,1.8],
      "numerical_convergence":{
        "pass":numerical,
        "criterion":"final two adaptive DeltaS <= 0.02",
        "final_two_delta_s":[seq[-2]["delta_s"],seq[-1]["delta_s"]] if len(seq)>=2 else None,
        "passes_executed":seq[-1]["pass"] if seq else None,
      },
      "reciprocity":{
        "pass":reciprocity_ok,
        "criterion":"max native-grid |Sij-Sji| <= 0.02 over full modeled band",
        "max_abs_complex":max_recip,
      },
      "passivity":{
        "pass":passivity_ok,
        "criterion":"max native-grid sum_i |Sij|^2 <= 1.02 over full modeled band",
        "max_column_power":max_power,
        "min_column_power":min_power,
        "interpretation":"deficit includes conductor/dielectric loss plus radiation/open-boundary power; it is not pure insertion loss",
      },
      "coupling_sentinels":coupling,
      "gnss_reference_samples":exact,
      "reference_frequency_rule":"PASS/HOLD gates use native solver samples; L5/L2/L1 reporting uses linear complex interpolation and records a nearest-native audit sample.",
    }

def main(source,solver_macro,out,evidence):
    source=Path(source); solver_macro=Path(solver_macro); out=Path(out); evidence=Path(evidence)
    if not source.exists():
        raise RuntimeError("HOLD_E1S0_SOURCE_MISSING")
    if sha(source)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E1S0_SOURCE_HASH:"+sha(source))
    if not source.with_suffix("").exists():
        raise RuntimeError("HOLD_E1S0_SOURCE_COMPANION_MISSING")
    if out.exists() or out.with_suffix("").exists():
        raise RuntimeError("HOLD_E1S0_DEST_EXISTS")
    if evidence.exists():
        raise RuntimeError("HOLD_E1S0_EVIDENCE_EXISTS")
    evidence.mkdir(parents=True)

    source_sha_before=sha(source)
    copy_project(source,out)
    if sha(out)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E1S0_COPY_HASH_BEFORE_CONFIG")

    # Configure the disposable solve copy only, through persistent History List.
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        p.modeler.add_to_history(SOLVER_HISTORY_LABEL,macro_body(solver_macro))
        p.save()
    finally:
        if p is not None: p.close()
        de.close()

    configured_sha=sha(out)
    presolve_ports=evidence/"presolve_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        ok=bool(p.schematic.execute_vba_code(wrap(port_audit_vba(presolve_ports))))
        if not ok:
            raise RuntimeError("HOLD_E1S0_PRESOLVE_PORT_AUDIT")
    finally:
        if p is not None: p.close()
        de.close()

    pdata=parse_ports(presolve_ports)
    hist=out.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=hist.read_text(encoding="utf-8",errors="replace") if hist.exists() else ""
    pre_tree=solver_paths(result_tree(out))
    presolve={
      "source_sha256":source_sha_before,
      "source_hash_still_exact":sha(source)==EXPECTED_SOURCE_SHA256,
      "configured_sha256":configured_sha,
      "six_ports_exact":ports_ok(pdata),
      "solver_history_persistent":SOLVER_HISTORY_LABEL in htext,
      "preexisting_solver_result_paths":pre_tree,
      "result_tree_empty_before_solve":len(pre_tree)==0,
    }
    (evidence/"presolve_summary.json").write_text(json.dumps(presolve,indent=2)+"\n",encoding="utf-8")
    if not (presolve["source_hash_still_exact"] and presolve["six_ports_exact"] and
            presolve["solver_history_persistent"] and presolve["result_tree_empty_before_solve"]):
        raise RuntimeError("HOLD_E1S0_PRESOLVE_GATE")

    # Exactly one formal solver invocation. No automatic retry.
    (evidence/"solver_invocation.json").write_text(json.dumps({
      "formal_solver_invocations":1,
      "automatic_retries":0,
      "retry_authorized":False,
      "configured_sha256":configured_sha,
      "source_sha256":EXPECTED_SOURCE_SHA256,
    },indent=2)+"\n",encoding="utf-8")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        p.modeler.run_solver()
        p.save()
    finally:
        if p is not None: p.close()
        de.close()

    solved_sha=sha(out)
    copy_native(out,evidence)
    flags=native_flags(evidence)
    data,runmeta=read_network(out)
    write_native_csv(evidence/"s_matrix_native.csv",data)
    metrics=characterize(data,runmeta)

    hard_checks={
      "source_artifact_unchanged":sha(source)==EXPECTED_SOURCE_SHA256,
      "full_6x6_network_extracted":len(data)==36,
      "numerical_convergence":metrics["numerical_convergence"]["pass"],
      "reciprocity":metrics["reciprocity"]["pass"],
      "passivity":metrics["passivity"]["pass"],
      "no_fatal_native_solver_error":not flags["fatal_error"],
      "no_mesh_corruption":not flags["mesh_corruption"],
    }
    hard_pass=all(hard_checks.values())

    review_flags={
      "any_unintended_coupling_gt_minus20db":any(
        v["review_gt_minus20db"] for k,v in metrics["coupling_sentinels"].items()
        if k not in ("cross_gap_CIN_parasitic","cross_gap_COUT_parasitic","cross_gap_L1_parasitic")
      ),
      "any_unintended_coupling_gt_minus10db":any(
        v["severe_gt_minus10db"] for k,v in metrics["coupling_sentinels"].items()
        if k not in ("cross_gap_CIN_parasitic","cross_gap_COUT_parasitic","cross_gap_L1_parasitic")
      ),
      "large_reflection_warning":flags["large_reflection_warning"],
      "disconnected_conductor_warning":flags["disconnected_conductor_warning"],
    }

    if hard_pass:
        disposition="PASS_CHARACTERIZED_WITH_COUPLING_REVIEW" if review_flags["any_unintended_coupling_gt_minus20db"] else "PASS_CHARACTERIZED_NETWORK_CLEAN_SENTINELS"
        status="PASS_R1E1A4A_AR0_B1R_R4_A0_E1_PASSIVE_EM_CHARACTERIZED"
    else:
        disposition="HOLD_NUMERICAL_OR_NETWORK_INTEGRITY"
        status="HOLD_R1E1A4A_AR0_B1R_R4_A0_E1_PASSIVE_EM_QUALIFICATION"

    summary={
      "status":status,
      "disposition":disposition,
      "simulationops":"0.2.10",
      "formal_solver_invocations":1,
      "automatic_retries":0,
      "source_artifact_sha256":EXPECTED_SOURCE_SHA256,
      "configured_copy_sha256":configured_sha,
      "solved_artifact_sha256":solved_sha,
      "solved_cst":str(out),
      "port_count":6,
      "frequency_ghz":[1.0,1.8],
      "decision_band_ghz":[1.15,1.65],
      "runmeta":runmeta,
      "native_flags":flags,
      "hard_checks":hard_checks,
      "review_flags":review_flags,
      "metrics":metrics,
      "interpretation_boundary":[
        "This is a six-port passive EM block with circuit-domain gaps intentionally open.",
        "S11/S22/etc. are diagnostic 50-ohm multiport quantities, not product input-match authority.",
        "E_UP-to-E_DN is not an insertion-loss path because C_IN/QPL9547/C_OUT/L1 are not inserted in this EM model.",
        "Cross-gap couplings are parasitic baselines for later circuit co-simulation.",
        "No geometry optimization is authorized by this solve."
      ]
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status)
    print("DISPOSITION="+disposition)
    print("SOLVED_SHA256="+solved_sha)
    print(json.dumps({"hard_checks":hard_checks,"review_flags":review_flags,
                      "numerical":metrics["numerical_convergence"],
                      "reciprocity":metrics["reciprocity"],
                      "passivity":metrics["passivity"],
                      "coupling_sentinels":metrics["coupling_sentinels"]},indent=2))
    return 0 if hard_pass else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-cst",required=True)
    ap.add_argument("--solver-macro",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.source_cst,a.solver_macro,a.out,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R4_A0_E1_PASSIVE_EM_EXECUTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
