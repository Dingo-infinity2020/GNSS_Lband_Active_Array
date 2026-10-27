from __future__ import print_function
import argparse, hashlib, json, math, os, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

PARENT_SHA="3144672323cbd4123d6413e7d9ae8f4842b78707d3a71b641748c7250ca2a8f6"
KEEP=(
 "B0_Stalk:A_P_PRONG",
 "B0_Stalk:A_N_PRONG",
 "B0_MSL:A_P_MSL",
 "B0_MSL:A_N_MSL",
 "B1RT1_BackGround:A_P_GROUND_TAPER",
 "B1RT1_BackGround:A_N_GROUND_TAPER",
)

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
    if s is None or e is None or e<=s: raise RuntimeError("HOLD_T2F_R2_PORT_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def audit_vba(inv_path,param_path,status_path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(inv_path),
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+100",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      "  mat=Solid.GetMaterialNameForShape(nm)",
      '  Print #f, "SHAPE|" & nm & "|material=" & mat & "|volume=" & CStr(Solid.GetVolume(nm))',
      " End If",
      "Next i",
      "Close #f",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(param_path),
      'Print #f, "PARAM_COUNT=" & CStr(GetNumberOfParameters())',
      "For i=1 To GetNumberOfParameters()",
      ' Print #f, "PARAM|" & GetParameterName(i) & "|" & GetParameterSValue(i) & "|" & CStr(GetParameterNValue(i))',
      "Next i",
      "Close #f",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(status_path),
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "SOLVER_RUN=NO"',
      "Close #f",
      "On Error GoTo 0"
    ])

def parse_inv(path):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            _,nm,mat,vol=line.split("|",3)
            rows.append({"name":nm,"material":mat.split("=",1)[1],"volume":float(vol.split("=",1)[1])})
    return rows

def parse_params(path):
    out={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.startswith("PARAM|"): continue
        p=line.split("|")
        if len(p)>=4:
            try: out[p[1]]=float(p[3])
            except Exception: pass
    return out

def port_count(path):
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("PORT_COUNT="): return int(line.split("=",1)[1])
    return None

def solver_tree(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return [x for x in p3.get_tree_items()
                if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+str(ex)]

def retained_signature(rows):
    return {r["name"]:(r["material"],round(r["volume"],12)) for r in rows if r["name"] in KEEP}

def delete_nonkeep_vba(parent_rows):
    lines=[]
    for r in parent_rows:
        if r["name"] not in KEEP:
            lines.append('Solid.Delete "%s"'%r["name"])
    return "\n".join(lines)

def expected_runtime():
    s2=1.0/math.sqrt(2.0); z0=57.1428571428; p1sig=0.035; outsig=0.0; outgnd=-1.0
    def xy(u,n): return (s2*(u-n),s2*(u+n))
    pp=xy(3.0,p1sig); pn=xy(-3.0,p1sig)
    op_s=xy(3.0,outsig); op_g=xy(3.0,outgnd)
    on_s=xy(-3.0,outsig); on_g=xy(-3.0,outgnd)
    return {
      "p1":pp,"p2":pn,
      "outp_sig":op_s,"outp_gnd":op_g,
      "outn_sig":on_s,"outn_gnd":on_g,
      "output_z":z0-10.0
    }

def close(a,b,tol=1e-9): return abs(a-b)<=tol

def run(repo,evidence,work,parent,macro):
    repo=Path(repo); evidence=Path(evidence); work=Path(work); parent=Path(parent); macro=Path(macro)
    if evidence.exists(): raise RuntimeError("HOLD_T2F_R2_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_T2F_R2_WORK_EXISTS")
    if not parent.exists() or sha(parent)!=PARENT_SHA: raise RuntimeError("HOLD_T2F_R2_PARENT_HASH")
    if not macro.exists(): raise RuntimeError("HOLD_T2F_R2_PORT_MACRO_MISSING")
    evidence.mkdir(parents=True); work.mkdir(parents=True)
    out=work/"R1E1A4A_AR0_B1R_T2F_R2_CANONICAL_TRANSITION_FIXTURE_V01.cst"
    shutil.copy2(str(parent),str(out))
    if sha(out)!=PARENT_SHA: raise RuntimeError("HOLD_T2F_R2_COPY_HASH")

    parent_inv=evidence/"parent_inventory.txt"
    build_inv=evidence/"build_inventory.txt"; build_par=evidence/"build_parameters.txt"; build_sta=evidence/"build_port_status.txt"
    reopen_inv=evidence/"reopen_inventory.txt"; reopen_par=evidence/"reopen_parameters.txt"; reopen_sta=evidence/"reopen_port_status.txt"

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code(wrap(audit_vba(parent_inv,evidence/"parent_parameters.txt",evidence/"parent_port_status.txt"))):
            raise RuntimeError("HOLD_T2F_R2_PARENT_AUDIT")
        parent_rows=parse_inv(parent_inv)
        sig0=retained_signature(parent_rows)
        if set(sig0)!=set(KEEP): raise RuntimeError("HOLD_T2F_R2_KEEP_SOLIDS_MISSING")
        prj.modeler.add_to_history("AR0-B1R-T2F-R2 extract canonical Pol-A transition",delete_nonkeep_vba(parent_rows))
        prj.modeler.add_to_history("AR0-B1R-T2F-R2 add three discrete ports",macro_body(macro))
        prj.save()
        if not prj.schematic.execute_vba_code(wrap(audit_vba(build_inv,build_par,build_sta))):
            raise RuntimeError("HOLD_T2F_R2_BUILD_AUDIT")
    finally:
        if prj is not None: prj.close()
        de.close()

    build_sha=sha(out)

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code(wrap(audit_vba(reopen_inv,reopen_par,reopen_sta))):
            raise RuntimeError("HOLD_T2F_R2_REOPEN_AUDIT")
    finally:
        if prj is not None: prj.close()
        de.close()

    parent_rows=parse_inv(parent_inv); build_rows=parse_inv(build_inv); reopen_rows=parse_inv(reopen_inv)
    sig_parent=retained_signature(parent_rows)
    sig_build=retained_signature(build_rows)
    sig_reopen=retained_signature(reopen_rows)
    bp=parse_params(build_par); rp=parse_params(reopen_par)
    exp=expected_runtime()

    runtime_names=(
      "t2f_r2_p1_x","t2f_r2_p1_y","t2f_r2_p2_x","t2f_r2_p2_y",
      "t2f_r2_outp_sig_x","t2f_r2_outp_sig_y","t2f_r2_outp_gnd_x","t2f_r2_outp_gnd_y",
      "t2f_r2_outn_sig_x","t2f_r2_outn_sig_y","t2f_r2_outn_gnd_x","t2f_r2_outn_gnd_y",
      "t2f_r2_output_z"
    )
    # CST 2022 may delay derived parameter t2f_r2_output_z until fresh reopen.
    immediate_required=tuple(k for k in runtime_names if k!="t2f_r2_output_z")
    runtime_present=all(k in bp and k in rp for k in immediate_required) and all(k in rp for k in runtime_names)
    runtime_equal=runtime_present and all(close(bp[k],rp[k]) for k in immediate_required)
    endpoint_ok=runtime_present and all([
      close(rp["t2f_r2_p1_x"],exp["p1"][0]), close(rp["t2f_r2_p1_y"],exp["p1"][1]),
      close(rp["t2f_r2_p2_x"],exp["p2"][0]), close(rp["t2f_r2_p2_y"],exp["p2"][1]),
      close(rp["t2f_r2_outp_sig_x"],exp["outp_sig"][0]), close(rp["t2f_r2_outp_sig_y"],exp["outp_sig"][1]),
      close(rp["t2f_r2_outp_gnd_x"],exp["outp_gnd"][0]), close(rp["t2f_r2_outp_gnd_y"],exp["outp_gnd"][1]),
      close(rp["t2f_r2_outn_sig_x"],exp["outn_sig"][0]), close(rp["t2f_r2_outn_sig_y"],exp["outn_sig"][1]),
      close(rp["t2f_r2_outn_gnd_x"],exp["outn_gnd"][0]), close(rp["t2f_r2_outn_gnd_y"],exp["outn_gnd"][1]),
      close(rp["t2f_r2_output_z"],exp["output_z"])
    ])

    tree=solver_tree(out)
    checks={
      "parent_hash_exact":sha(parent)==PARENT_SHA,
      "six_retained_solids_only_build":len(build_rows)==6 and set(r["name"] for r in build_rows)==set(KEEP),
      "six_retained_solids_only_reopen":len(reopen_rows)==6 and set(r["name"] for r in reopen_rows)==set(KEEP),
      "retained_signature_parent_build_equal":sig_parent==sig_build,
      "retained_signature_parent_reopen_equal":sig_parent==sig_reopen,
      "build_port_count_3":port_count(build_sta)==3,
      "reopen_port_count_3":port_count(reopen_sta)==3,
      "runtime_endpoint_params_present_with_output_z_reopen_authority":runtime_present,
      "runtime_endpoint_common_build_reopen_equal":runtime_equal,
      "runtime_endpoint_geometry_exact":endpoint_ok,
      "fresh_reopen_hash_stable":sha(out)==build_sha,
      "solver_tree_empty":len(tree)==0
    }
    status="PASS_R1E1A4A_AR0_B1R_T2F_R2_FIXTURE_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_T2F_R2_FIXTURE"

    summary={
      "status":status,"simulationops":"0.2.8",
      "formal_build_invocations":1,"solver_invocations":0,
      "parent":{"path":str(parent),"sha256":PARENT_SHA},
      "port_macro":{"path":str(macro),"sha256":sha(macro)},
      "artifact":{"path":str(out),"sha256":sha(out)},
      "retained_signature":sig_reopen,
      "port_counts":{"build":port_count(build_sta),"reopen":port_count(reopen_sta)},
      "runtime_endpoints":{k:rp.get(k) for k in runtime_names},
      "expected_endpoints":exp,
      "solver_tree_matches":tree,
      "checks":checks,
      "interpretation":"canonical Pol-A transition-only 3-port fixture; no radiator/mechanics/LNA/RF-tenon; no solve"
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# AR0-B1R-T2F-R2 Human Fixture Review","",
      "Canonical status: "+status,"",
      "This is an isolated transition coupon, not the product assembly.",
      "Retained geometry should be exactly two FR4 prongs, two front signal traces, and two backside T1 taper grounds.","",
      "Inspect:",
      "1. Top balanced input port spans +signal to -signal at v=0.",
      "2. Output Port 2 spans +signal to its local ground at v=10 mm.",
      "3. Output Port 3 mirrors Port 2 on the - branch.",
      "4. No radiator, reflector, tenon, solder proxy, LNA envelope or mechanical rail remains.",
      "5. Ground taper remains exactly the accepted T1 geometry.","",
      "No solver is authorized."
    ]
    (evidence/"HUMAN_FIXTURE_REVIEW.md").write_text("\n".join(review)+"\n",encoding="utf-8")
    print(status); print("ARTIFACT_SHA256="+sha(out)); print("REOPEN_PORT_COUNT="+str(port_count(reopen_sta)))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--parent-cst",required=True)
    ap.add_argument("--port-macro",required=True)
    a=ap.parse_args()
    try:
        sys.exit(run(a.repo,a.evidence,a.work,a.parent_cst,a.port_macro))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_T2F_R2_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
