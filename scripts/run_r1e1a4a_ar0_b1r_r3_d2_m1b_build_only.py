from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

PARENT_SHA="4ec39ab9965dd9ec6b416d801ded0ee6e56d910d2ffc2ba405cb9dec978cd91e"
S2=1.0/math.sqrt(2.0)
Z0=57.1428571428
KEEP=(
 "B0_Stalk:B_P_PRONG","B0_Stalk:B_N_PRONG",
 "B0_MSL:B_P_MSL","B0_MSL:B_N_MSL",
 "B1RT1R1_BackGround:B_P_GROUND_TAPER","B1RT1R1_BackGround:B_N_GROUND_TAPER",
 "B1M_LowerStalk:B_LOWER_BODY",
 "D2M0R1_BackGround:B_P_LOWER_RAIL","D2M0R1_BackGround:B_N_LOWER_RAIL",
 "D2M0R1_BackGround:B_COMMON_BRIDGE",
)

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,l in enumerate(lines):
        if l.strip()=="Sub Main()": s=i
        elif l.strip()=="End Sub": e=i
    if s is None or e is None or e<=s: raise RuntimeError("HOLD_D2M1B_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def audit_vba(inv_path,param_path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(inv_path).replace("\\","/"),
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+700",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      "  mat=Solid.GetMaterialNameForShape(nm)",
      '  Print #f, "SHAPE|" & nm & "|material=" & mat & "|volume=" & CStr(Solid.GetVolume(nm))',
      " End If",
      "Next i",
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(param_path).replace("\\","/"),
      'Print #f, "PARAM_COUNT=" & CStr(GetNumberOfParameters())',
      "For i=1 To GetNumberOfParameters()",
      ' Print #f, "PARAM|" & GetParameterName(i) & "|" & GetParameterSValue(i) & "|" & CStr(GetParameterNValue(i))',
      "Next i",
      "Close #f",
      "On Error GoTo 0"
    ])

def parse_inv(path):
    rows=[]; kv={}
    for l in Path(path).read_text(encoding="utf-8").splitlines():
        if l.startswith("SHAPE|"):
            _,nm,mat,vol=l.split("|",3)
            rows.append({"name":nm,"material":mat.split("=",1)[1],"volume":float(vol.split("=",1)[1])})
        elif "=" in l:
            k,v=l.split("=",1); kv[k]=v
    return rows,kv

def parse_params(path):
    out={}
    for l in Path(path).read_text(encoding="utf-8").splitlines():
        if l.startswith("PARAM|"):
            p=l.split("|")
            if len(p)>=4:
                try: out[p[1]]=float(p[3])
                except Exception: pass
    return out

def solver_tree(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return [x for x in p3.get_tree_items()
                if ("S-Parameters" in x or "Convergence" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+str(ex)]

def sig(rows):
    return {r["name"]:(r["material"],round(r["volume"],12)) for r in rows if r["name"] in KEEP}

def xy(u,n):
    return (-S2*(u+n), S2*(u-n))

def close(a,b,t=1e-9): return abs(a-b)<=t

def main(parent,outdir,evidence,macro):
    parent=Path(parent); outdir=Path(outdir); evidence=Path(evidence); macro=Path(macro)
    if not parent.exists() or sha(parent)!=PARENT_SHA: raise RuntimeError("HOLD_D2M1B_PARENT_HASH")
    if outdir.exists(): raise RuntimeError("HOLD_D2M1B_WORK_EXISTS")
    if evidence.exists(): raise RuntimeError("HOLD_D2M1B_EVIDENCE_EXISTS")
    if not macro.exists(): raise RuntimeError("HOLD_D2M1B_MACRO_MISSING")
    outdir.mkdir(parents=True); evidence.mkdir(parents=True)
    out=outdir/"R1E1A4A_AR0_B1R_R3_D2_M1B_RF_FIXTURE_BUILD_ONLY_V01.cst"
    shutil.copy2(str(parent),str(out))

    pinv=evidence/"parent_inventory.txt"; ppar=evidence/"parent_parameters.txt"
    rinv=evidence/"reopen_inventory.txt"; rpar=evidence/"reopen_parameters.txt"

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(audit_vba(pinv,ppar))): raise RuntimeError("HOLD_D2M1B_PARENT_AUDIT")
        rows,_=parse_inv(pinv)
        if set(sig(rows))!=set(KEEP): raise RuntimeError("HOLD_D2M1B_KEEP_MISSING")
        delete="\n".join('Solid.Delete "%s"'%r["name"] for r in rows if r["name"] not in KEEP)
        p.modeler.add_to_history("D2-M1B exact Pol-B supported-merge fixture",delete)
        p.modeler.add_to_history("D2-M1B rotated 100/50/50 ports",macro_body(macro))
        p.save()
    finally:
        if p is not None: p.close()
        de.close()
    build_sha=sha(out)

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(audit_vba(rinv,rpar))): raise RuntimeError("HOLD_D2M1B_REOPEN_AUDIT")
    finally:
        if p is not None: p.close()
        de.close()

    prows,pkv=parse_inv(pinv); rows,kv=parse_inv(rinv); pars=parse_params(rpar)
    p1p=xy(3.0,0.035); p1n=xy(-3.0,0.035)
    ops=xy(3.0,0.0); opg=xy(3.0,-1.0); ons=xy(-3.0,0.0); ong=xy(-3.0,-1.0)
    need=("r3d2m1b_p1_x","r3d2m1b_p1_y","r3d2m1b_p2_x","r3d2m1b_p2_y",
          "r3d2m1b_outp_sig_x","r3d2m1b_outp_sig_y","r3d2m1b_outp_gnd_x","r3d2m1b_outp_gnd_y",
          "r3d2m1b_outn_sig_x","r3d2m1b_outn_sig_y","r3d2m1b_outn_gnd_x","r3d2m1b_outn_gnd_y","r3d2m1b_output_z")
    endpoint=all(k in pars for k in need) and all([
      close(pars["r3d2m1b_p1_x"],p1p[0]),close(pars["r3d2m1b_p1_y"],p1p[1]),
      close(pars["r3d2m1b_p2_x"],p1n[0]),close(pars["r3d2m1b_p2_y"],p1n[1]),
      close(pars["r3d2m1b_outp_sig_x"],ops[0]),close(pars["r3d2m1b_outp_sig_y"],ops[1]),
      close(pars["r3d2m1b_outp_gnd_x"],opg[0]),close(pars["r3d2m1b_outp_gnd_y"],opg[1]),
      close(pars["r3d2m1b_outn_sig_x"],ons[0]),close(pars["r3d2m1b_outn_sig_y"],ons[1]),
      close(pars["r3d2m1b_outn_gnd_x"],ong[0]),close(pars["r3d2m1b_outn_gnd_y"],ong[1]),
      close(pars["r3d2m1b_output_z"],Z0-10.0)
    ])
    tree=solver_tree(out)
    checks={
      "parent_hash_exact":sha(parent)==PARENT_SHA,
      "shape_count_10":len(rows)==10,
      "exact_keep_names":set(r["name"] for r in rows)==set(KEEP),
      "retained_signature_exact":sig(prows)==sig(rows),
      "port_count_3":int(kv.get("PORT_COUNT","-1"))==3,
      "polB_endpoint_transform_exact":endpoint,
      "fresh_reopen_hash_stable":sha(out)==build_sha,
      "result_tree_empty":len(tree)==0
    }
    status="PASS_R1E1A4A_AR0_B1R_R3_D2_M1B_RF_FIXTURE_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_R3_D2_M1B_BUILD"
    summary={"status":status,"simulationops":"0.2.8","solver_invocations":0,
             "parent":{"path":str(parent),"sha256":PARENT_SHA},
             "artifact":{"path":str(out),"sha256":sha(out)},
             "shape_count":len(rows),"port_count":int(kv.get("PORT_COUNT","-1")),
             "checks":checks}
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status); print("FIXTURE_B_SHA256="+sha(out))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--parent-cst",required=True); ap.add_argument("--work",required=True)
    ap.add_argument("--evidence",required=True); ap.add_argument("--port-macro",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.parent_cst,a.work,a.evidence,a.port_macro))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R3_D2_M1B_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
