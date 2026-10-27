from __future__ import print_function
import argparse, csv, hashlib, json, math, cmath, shutil, sys, traceback
from collections import Counter
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

import cst.interface as ci
from cst.results import ProjectFile

EXPECTED_SOURCE_SHA256="78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804"
HISTORY_LABEL="R4-A0-E2A-S0L loaded source-side solve config V01"
S2=1.0/math.sqrt(2.0)
Z0=57.1428571428

PORT_LOCAL={
    1:(3.0,4.650,"A_E_UP","SOURCE"),
    2:(3.0,6.085,"A_P_IN","SOURCE_DEVICE_INPUT"),
    3:(3.0,7.915,"A_P_OUT_LOAD50","MATCHED_LOAD_ONLY"),
    4:(-3.0,4.650,"B_E_UP","SOURCE"),
    5:(-3.0,6.085,"B_P_IN","SOURCE_DEVICE_INPUT"),
    6:(-3.0,7.915,"B_P_OUT_LOAD50","MATCHED_LOAD_ONLY"),
}
SOURCE_PORTS=(1,2,4,5)
LOAD_ONLY_PORTS=(3,6)
SOURCE_SIDE=(1,2,4,5)
ALL_ROWS=(1,2,3,4,5,6)
GNSS_REFS={"L5":1.17645,"L2":1.22760,"L1":1.57542}

REQUIRED_HISTORY_TOKENS=(
    'Port.Delete 12','Port.Delete 11','Port.Delete 10',
    'Port.Delete 6','Port.Delete 5','Port.Delete 4',
    'Port.Rename 7, 4','Port.Rename 8, 5','Port.Rename 9, 6',
    '.Stimulation "List", "List"',
    '.ResetExcitationList',
    '.AddToExcitationList "1", "1"',
    '.AddToExcitationList "2", "1"',
    '.AddToExcitationList "4", "1"',
    '.AddToExcitationList "5", "1"',
)
FORBIDDEN_EXCITATION_TOKENS=(
    '.AddToExcitationList "3", "1"',
    '.AddToExcitationList "6", "1"',
    '.Stimulation "All", "All"',
)

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def wrap(body):
    return "Sub Main()\n"+body+"\nEnd Sub"

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,line in enumerate(lines):
        if line.strip()=="Sub Main()": s=i
        elif line.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("HOLD_E2A_S0L_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    srcdir=src.with_suffix(""); dstdir=dst.with_suffix("")
    if not srcdir.exists():
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_COMPANION_MISSING")
    if dstdir.exists():
        shutil.rmtree(str(dstdir),ignore_errors=True)
    shutil.copytree(str(srcdir),str(dstdir))

def inventory_vba(path):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",'Open "'+p+'" For Output As #f',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+1200",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      "  mat=Solid.GetMaterialNameForShape(nm)",
      '  Print #f, "SHAPE|" & nm & "|material=" & mat & "|volume=" & CStr(Solid.GetVolume(nm))',
      " End If","Next i",
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f","On Error GoTo 0"
    ])

def port_audit_vba(path):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Integer, stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",'Open "'+p+'" For Output As #f',
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "For i=1 To 6",
      " Err.Clear",
      " pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P|" & CStr(i) & "|PROP_OK=" & CStr(pok) & "|ERR=" & CStr(Err.Number) & "|TYPE=" & stype & "|ZREF=" & CStr(zref)',
      " Err.Clear",
      " cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "C|" & CStr(i) & "|COORD_OK=" & CStr(cok) & "|ERR=" & CStr(Err.Number) & "|P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0) & "|P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i","Close #f","On Error GoTo 0"
    ])

def parse_inventory(path):
    rows=[]; kv={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            _,nm,mat,vol=line.split("|",3)
            rows.append({"name":nm,"component":nm.split(":",1)[0],
                         "material":mat.split("=",1)[1],
                         "volume":float(vol.split("=",1)[1])})
        elif "=" in line:
            k,v=line.split("=",1); kv[k]=v
    return rows,kv

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

def xyz(s): return tuple(float(x) for x in s.split(","))

def expected_port_xyz(i):
    u,v,_,_=PORT_LOCAL[i]
    z=Z0-v
    return (S2*u,S2*u,z),(S2*(u+1.0),S2*(u-1.0),z)

def ports_exact(data,tol=2e-8):
    if data["count"]!=6: return False
    for i in range(1,7):
        p=data["properties"].get(i,{})
        c=data["coordinates"].get(i,{})
        if p.get("PROP_OK") not in ("True","TRUE","1","-1"): return False
        if c.get("COORD_OK") not in ("True","TRUE","1","-1"): return False
        if p.get("TYPE")!="SParameter": return False
        if abs(float(p.get("ZREF","nan"))-50.0)>tol: return False
        a,b=expected_port_xyz(i)
        if any(abs(x-y)>tol for x,y in zip(xyz(c["P1"]),a)): return False
        if any(abs(x-y)>tol for x,y in zip(xyz(c["P2"]),b)): return False
    return True

def signature(rows):
    return {r["name"]:(r["material"],round(r["volume"],12)) for r in rows}

def result_tree(cst):
    return ProjectFile(str(cst),allow_interactive=True).get_3d().get_tree_items()

def solver_paths(items):
    return [x for x in items if ("S-Parameters" in x or "Convergence" in x or
                                 "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def history_exact(history):
    if HISTORY_LABEL not in history: return False
    if not all(t in history for t in REQUIRED_HISTORY_TOKENS): return False
    if any(t in history for t in FORBIDDEN_EXCITATION_TOKENS): return False
    for p in SOURCE_PORTS:
        if history.count('.AddToExcitationList "%d", "1"'%p)!=1: return False
    for p in LOAD_ONLY_PORTS:
        if '.AddToExcitationList "%d", "1"'%p in history: return False
    return True

def copy_native(dst,evidence):
    result=Path(dst).with_suffix("")/"Result"
    for n in ("output.txt","Model.log","log.tet"):
        p=result/n
        if p.exists():
            shutil.copy2(str(p),str(Path(evidence)/("native_"+n.replace(".","_"))))

def native_text(evidence):
    txt=""
    for n in ("native_output_txt","native_Model_log","native_log_tet"):
        p=Path(evidence)/n
        if p.exists():
            txt+="\n"+p.read_text(encoding="utf-8",errors="ignore")
    return txt

def native_flags(evidence):
    lo=native_text(evidence).lower()
    return {
      "fatal_error":("fatal error" in lo or "solver failed" in lo or "aborted due to" in lo),
      "mesh_corruption":("corrupt mesh" in lo or "mesh near the lumped element" in lo),
      "large_reflection_warning":"input reflection seems to be large" in lo,
      "disconnected_conductor_warning":"not connected to any good conductor" in lo,
    }

def native_delta_sequence(evidence):
    # CST native output lines may use either All S-Parameters or legacy DeltaS wording.
    txt=native_text(evidence)
    out=[]
    import re
    patterns=[
      r"All\s+S-Parameters\s*=\s*([0-9.+Ee-]+)",
      r"Maximum difference of S-parameters[^=]*=\s*([0-9.+Ee-]+)",
      r"DeltaS\s*=\s*([0-9.+Ee-]+)",
    ]
    seen=[]
    for pat in patterns:
        vals=re.findall(pat,txt,re.I)
        if vals:
            seen=[float(v) for v in vals]
            break
    for i,v in enumerate(seen,1):
        out.append({"ordinal":i,"delta_s":v})
    return out

def choose_common_run(p3,paths):
    common=None; ids={}
    for path in paths:
        rids=list(p3.get_run_ids(path,False)); ids[path]=rids
        common=set(rids) if common is None else common.intersection(rids)
    if not common:
        raise RuntimeError("HOLD_E2A_S0L_NO_COMMON_RESPONSE_RUN:"+json.dumps(ids))
    return max(common),ids

def required_paths():
    return [r"1D Results\S-Parameters\S%d,%d"%(i,j)
            for j in SOURCE_PORTS for i in ALL_ROWS]

def read_responses(cst):
    pf=ProjectFile(str(cst),allow_interactive=True)
    p3=pf.get_3d(); items=p3.get_tree_items()
    paths=required_paths()
    for path in paths:
        if path not in items:
            raise RuntimeError("HOLD_E2A_S0L_MISSING_RESPONSE:"+path)
    rid,allids=choose_common_run(p3,paths)
    data={}; reference_freqs=None
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            path=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            vals=[(float(r[0]),complex(r[1])) for r in p3.get_result_item(path,rid).get_data()]
            freqs=[x[0] for x in vals]
            if reference_freqs is None: reference_freqs=freqs
            elif len(freqs)!=len(reference_freqs) or any(abs(a-b)>1e-9 for a,b in zip(freqs,reference_freqs)):
                raise RuntimeError("HOLD_E2A_S0L_NATIVE_GRID_MISMATCH:"+path)
            data[(i,j)]=vals

    # Result-tree convergence is secondary evidence only.
    conv=r"1D Results\Convergence\S-Parameters\All S-Parameters"
    cmeta={"path_present":conv in items,"run_ids":[],"delta_sequence":[]}
    if conv in items:
        cids=list(p3.get_run_ids(conv,False)); cmeta["run_ids"]=cids
        crid=rid if rid in cids else max(cids)
        cmeta["selected_run_id"]=crid
        cmeta["delta_sequence"]=[
          {"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)}
          for r in p3.get_result_item(conv,crid).get_data()
        ]

    return data,{
      "selected_run_id":rid,
      "response_run_ids":allids,
      "native_frequency_count":len(reference_freqs),
      "native_frequency_min_ghz":min(reference_freqs),
      "native_frequency_max_ghz":max(reference_freqs),
      "result_tree_convergence":cmeta,
    }

def db(z): return 20.0*math.log10(max(abs(z),1e-300))
def phase_deg(z): return math.degrees(cmath.phase(z))

def interp(vals,f0):
    if f0<=vals[0][0]: return vals[0][1]
    if f0>=vals[-1][0]: return vals[-1][1]
    for k in range(1,len(vals)):
        if vals[k][0]>=f0:
            fa,za=vals[k-1]; fb,zb=vals[k]
            a=(f0-fa)/(fb-fa)
            return za+a*(zb-za)
    return vals[-1][1]

def characterize(data):
    freqs=[x[0] for x in data[(1,1)]]
    core=[k for k,f in enumerate(freqs) if 1.15-1e-12<=f<=1.65+1e-12]
    if not core: raise RuntimeError("HOLD_E2A_S0L_NO_CORE_SAMPLES")

    reciprocity=[]
    src=list(SOURCE_SIDE)
    for k,f in enumerate(freqs):
        for a in range(len(src)):
            for b in range(a+1,len(src)):
                i,j=src[a],src[b]
                reciprocity.append({"f_ghz":f,"i":i,"j":j,
                  "abs_complex":abs(data[(i,j)][k][1]-data[(j,i)][k][1])})
    max_recip=max(reciprocity,key=lambda x:x["abs_complex"])

    powers=[]
    for k,f in enumerate(freqs):
        for j in SOURCE_PORTS:
            p=sum(abs(data[(i,j)][k][1])**2 for i in ALL_ROWS)
            powers.append({"f_ghz":f,"source_port":j,"sum_abs_s_sq":p})
    max_power=max(powers,key=lambda x:x["sum_abs_s_sq"])
    min_power=min(powers,key=lambda x:x["sum_abs_s_sq"])

    # Same-branch C_IN-gap parasitic and cross-branch source coupling.
    sentinels={
      "A_CIN_GAP":(2,1),
      "B_CIN_GAP":(5,4),
      "A_TO_B_EUP":(4,1),
      "A_PIN_TO_B_PIN":(5,2),
      "A_EUP_TO_B_PIN":(5,1),
      "A_PIN_TO_B_EUP":(4,2),
      "A_SOURCE_TO_A_OUTLOAD":(3,1),
      "A_PIN_TO_A_OUTLOAD":(3,2),
      "B_SOURCE_TO_B_OUTLOAD":(6,4),
      "B_PIN_TO_B_OUTLOAD":(6,5),
      "A_SOURCE_TO_B_OUTLOAD":(6,1),
      "A_PIN_TO_B_OUTLOAD":(6,2),
      "B_SOURCE_TO_A_OUTLOAD":(3,4),
      "B_PIN_TO_A_OUTLOAD":(3,5),
    }
    sd={}
    for name,(i,j) in sentinels.items():
        pts=[(freqs[k],data[(i,j)][k][1]) for k in core]
        peak=max(pts,key=lambda x:abs(x[1]))
        val=db(peak[1])
        sd[name]={"ports":[i,j],"max_core_db":val,"frequency_ghz":peak[0],
                  "review_gt_minus20db":val>-20.0,
                  "severe_gt_minus10db":val>-10.0}

    refs={}
    for name,f0 in GNSS_REFS.items():
        refs[name]={"target_ghz":f0}
        for key,(i,j) in sentinels.items():
            z=interp(data[(i,j)],f0)
            refs[name][key]={"real":z.real,"imag":z.imag,"db":db(z),"phase_deg":phase_deg(z)}

    return {
      "source_side_reciprocity":{
        "max_abs_complex":max_recip,
        "pass":max_recip["abs_complex"]<=0.02
      },
      "loaded_power_closure":{
        "max_column_power":max_power,
        "min_column_power":min_power,
        "pass":max_power["sum_abs_s_sq"]<=1.02
      },
      "sentinels":sd,
      "gnss_reference_samples":refs,
    }

def write_csv(path,data):
    freqs=[x[0] for x in data[(1,1)]]
    header=["f_GHz"]
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            p="S%d%d"%(i,j)
            header += [p+"_real",p+"_imag",p+"_dB",p+"_phase_deg"]
    with open(str(path),"w",newline="") as f:
        w=csv.writer(f); w.writerow(header)
        for k,fr in enumerate(freqs):
            row=[fr]
            for j in SOURCE_PORTS:
                for i in ALL_ROWS:
                    z=data[(i,j)][k][1]
                    row += [z.real,z.imag,db(z),phase_deg(z)]
            w.writerow(row)

def main(source,config_macro,inventory_contract,out,evidence):
    source=Path(source); config_macro=Path(config_macro)
    inventory_contract=Path(inventory_contract); out=Path(out); evidence=Path(evidence)

    if not source.exists() or sha(source)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_SHA")
    if not source.with_suffix("").exists():
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_COMPANION")
    if not config_macro.exists() or not inventory_contract.exists():
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_FILES")
    if out.exists() or out.with_suffix("").exists():
        raise RuntimeError("HOLD_E2A_S0L_DEST_EXISTS")
    if evidence.exists():
        raise RuntimeError("HOLD_E2A_S0L_EVIDENCE_EXISTS")

    evidence.mkdir(parents=True)
    contract=json.loads(inventory_contract.read_text(encoding="utf-8"))
    expected_names=set(contract["expected_final_names"])
    expected_counts=contract["expected_final_component_counts"]

    source_sha_before=sha(source)
    copy_project(source,out)
    if sha(out)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E2A_S0L_COPY_SHA")

    # Before-configuration geometry audit.
    before_inv=evidence/"before_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inventory_vba(before_inv))):
            raise RuntimeError("HOLD_E2A_S0L_BEFORE_INVENTORY")
    finally:
        if p is not None: p.close()
        de.close()

    before_rows,before_kv=parse_inventory(before_inv)
    before_sig=signature(before_rows)
    if not (
      len(before_rows)==107 and
      set(r["name"] for r in before_rows)==expected_names and
      dict(Counter(r["component"] for r in before_rows))==expected_counts and
      int(before_kv.get("PORT_COUNT","-1"))==12 and
      len(solver_paths(result_tree(out)))==0
    ):
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_GATE")

    # Persistent solve-copy configuration.
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        p.modeler.add_to_history(HISTORY_LABEL,macro_body(config_macro))
        p.save()
    finally:
        if p is not None: p.close()
        de.close()

    configured_sha=sha(out)

    # Fresh-reopen presolve qualification.
    cinv=evidence/"configured_inventory.txt"; cports=evidence/"configured_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inventory_vba(cinv))):
            raise RuntimeError("HOLD_E2A_S0L_CONFIG_INVENTORY")
        if not p.schematic.execute_vba_code(wrap(port_audit_vba(cports))):
            raise RuntimeError("HOLD_E2A_S0L_PORT_AUDIT")
    finally:
        if p is not None: p.close()
        de.close()

    after_rows,after_kv=parse_inventory(cinv); pdata=parse_ports(cports)
    hpath=out.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=hpath.read_text(encoding="utf-8",errors="replace") if hpath.exists() else ""
    pre_tree=solver_paths(result_tree(out))
    presolve={
      "source_sha_exact_and_unchanged":sha(source)==EXPECTED_SOURCE_SHA256,
      "configured_shape_count_107":len(after_rows)==107,
      "exact_shape_name_set":set(r["name"] for r in after_rows)==expected_names,
      "component_counts_exact":dict(Counter(r["component"] for r in after_rows))==expected_counts,
      "geometry_material_volume_signature_unchanged":signature(after_rows)==before_sig,
      "six_ports_exact":ports_exact(pdata),
      "selected_excitation_history_exact":history_exact(htext),
      "result_tree_empty_before_solve":len(pre_tree)==0,
      "configured_hash_stable":sha(out)==configured_sha,
    }
    (evidence/"presolve_summary.json").write_text(json.dumps(presolve,indent=2)+"\n",encoding="utf-8")
    if not all(presolve.values()):
        raise RuntimeError("HOLD_E2A_S0L_PRESOLVE_GATE")

    # Exactly one formal solver invocation; no automatic retry.
    (evidence/"solver_invocation.json").write_text(json.dumps({
      "formal_solver_invocations":1,
      "automatic_retries":0,
      "retry_authorized":False,
      "source_excitation_set":list(SOURCE_PORTS),
      "matched_load_only_set":list(LOAD_ONLY_PORTS),
      "configured_sha256":configured_sha,
      "source_sha256":EXPECTED_SOURCE_SHA256
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
    native_seq=native_delta_sequence(evidence)

    data,runmeta=read_responses(out)
    write_csv(evidence/"loaded_response_native.csv",data)
    metrics=characterize(data)

    # Native convergence is authoritative. If native parser cannot establish the final two
    # DeltaS values, result semantics are HOLD rather than falling back silently.
    native_convergence=(
      len(native_seq)>=2 and
      native_seq[-2]["delta_s"]<=0.02 and
      native_seq[-1]["delta_s"]<=0.02
    )

    hard_checks={
      "source_artifact_unchanged":sha(source)==EXPECTED_SOURCE_SHA256,
      "required_24_responses_extracted":len(data)==24,
      "native_numerical_convergence":native_convergence,
      "source_side_reciprocity":metrics["source_side_reciprocity"]["pass"],
      "loaded_power_closure":metrics["loaded_power_closure"]["pass"],
      "no_fatal_solver_error":not flags["fatal_error"],
      "no_mesh_corruption":not flags["mesh_corruption"],
    }
    hard_pass=all(hard_checks.values())

    review_gt20=any(v["review_gt_minus20db"] for v in metrics["sentinels"].values())
    severe_gt10=any(v["severe_gt_minus10db"] for v in metrics["sentinels"].values())
    review_flags={
      "any_review_gt_minus20db":review_gt20,
      "any_severe_gt_minus10db":severe_gt10,
      "large_reflection_warning":flags["large_reflection_warning"],
      "disconnected_conductor_warning":flags["disconnected_conductor_warning"],
    }

    if hard_pass:
        disposition=("PASS_LOADED_SOURCE_WITH_REVIEW"
                     if review_gt20 else
                     "PASS_LOADED_SOURCE_CLEAN_SENTINELS")
        status="PASS_R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_CHARACTERIZED"
    else:
        disposition="HOLD_NUMERICAL_OR_LOADED_RESPONSE_INTEGRITY"
        status="HOLD_R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_QUALIFICATION"

    summary={
      "status":status,
      "disposition":disposition,
      "simulationops":"0.2.12",
      "formal_solver_invocations":1,
      "automatic_retries":0,
      "source_artifact_sha256":EXPECTED_SOURCE_SHA256,
      "configured_copy_sha256":configured_sha,
      "solved_artifact_sha256":solved_sha,
      "source_excitation_set":list(SOURCE_PORTS),
      "matched_load_only_set":list(LOAD_ONLY_PORTS),
      "response_contract":"24 complex traces = 6 response rows x 4 source excitations",
      "runmeta":runmeta,
      "native_delta_sequence":native_seq,
      "native_flags":flags,
      "hard_checks":hard_checks,
      "review_flags":review_flags,
      "metrics":metrics,
      "interpretation_boundary":[
        "P_OUT ports 3 and 6 are 50-ohm matched passive loads and are excluded from the selected excitation list.",
        "E_DN/VDD/VBIAS audit ports are removed only from the solve copy; their copper pads remain open.",
        "C_IN remains absent from CST, so final QPL9547 source impedance is not directly claimed.",
        "After qualified C_IN insertion, the derived device-input condition is labeled 50OHM_OUTPUT_LOADED_SOURCE_CONDITION.",
        "Full-network extraction remains deferred until arbitrary output/bias reconnection, reverse feedback, active stability or transistor co-simulation requires it."
      ]
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status)
    print("SOLVED_SHA256="+solved_sha)
    return 0 if hard_pass else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-cst",required=True)
    ap.add_argument("--config-macro",required=True)
    ap.add_argument("--inventory-contract",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.source_cst,a.config_macro,a.inventory_contract,a.out,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_EXECUTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
