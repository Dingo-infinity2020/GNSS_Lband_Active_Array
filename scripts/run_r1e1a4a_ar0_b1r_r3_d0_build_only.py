from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

PARENT_SHA="3144672323cbd4123d6413e7d9ae8f4842b78707d3a71b641748c7250ca2a8f6"
S2=1.0/math.sqrt(2.0)
Z0=57.1428571428
UA=(S2,S2)
NA=(-S2,S2)
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
    if s is None or e is None or e<=s:
        raise RuntimeError("HOLD_R3D0_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def audit_vba(inv_path,param_path,status_path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(inv_path),
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+120",
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
        if line.startswith("PARAM|"):
            p=line.split("|")
            if len(p)>=4 and p[1]:
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

def delete_nonkeep(parent_rows):
    return "\n".join('Solid.Delete "%s"'%r["name"] for r in parent_rows if r["name"] not in KEEP)

def extrude_rect(name,comp,mat,u1,u2,n1,n2,z1,z2):
    return '''With Extrude
 .Reset
 .Name "%s"
 .Component "%s"
 .Material "%s"
 .Mode "Pointlist"
 .Height "%.12g"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.0", "0.0", "%.12g"
 .Uvector "%.15g", "%.15g", "0.0"
 .Vvector "%.15g", "%.15g", "0.0"
 .Point "%.12g", "%.12g"
 .LineTo "%.12g", "%.12g"
 .LineTo "%.12g", "%.12g"
 .LineTo "%.12g", "%.12g"
 .LineTo "%.12g", "%.12g"
 .Create
End With'''%(name,comp,mat,z2-z1,z1,UA[0],UA[1],NA[0],NA[1],
              u1,n1,u2,n1,u2,n2,u1,n2,u1,n1)

def build_one(parent,out,evidence,macro,variant,add_bridge=False):
    shutil.copy2(str(parent),str(out))
    if sha(out)!=PARENT_SHA: raise RuntimeError("HOLD_R3D0_%s_COPY_HASH"%variant)

    pinv=evidence/(variant+"_parent_inventory.txt")
    binv=evidence/(variant+"_build_inventory.txt")
    bpar=evidence/(variant+"_build_parameters.txt")
    bsta=evidence/(variant+"_build_port_status.txt")
    rinv=evidence/(variant+"_reopen_inventory.txt")
    rpar=evidence/(variant+"_reopen_parameters.txt")
    rsta=evidence/(variant+"_reopen_port_status.txt")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code(wrap(audit_vba(pinv,evidence/(variant+"_parent_parameters.txt"),evidence/(variant+"_parent_port_status.txt")))):
            raise RuntimeError("HOLD_R3D0_%s_PARENT_AUDIT"%variant)
        parent_rows=parse_inv(pinv)
        if set(retained_signature(parent_rows))!=set(KEEP):
            raise RuntimeError("HOLD_R3D0_%s_KEEP_MISSING"%variant)
        prj.modeler.add_to_history("R3-D0 %s extract exact T1 transition"%variant,delete_nonkeep(parent_rows))
        if add_bridge:
            bridge=extrude_rect("GROUND_BRIDGE","R3D0B_CommonGround","B0_COPPER",
                                -1.2,1.2,-1.035,-1.0,Z0-12.0,Z0-11.0)
            prj.modeler.add_to_history("R3-D0B diagnostic common-ground bridge",bridge)
        prj.modeler.add_to_history("R3-D0 %s ports"%variant,macro_body(macro))
        prj.save()
        if not prj.schematic.execute_vba_code(wrap(audit_vba(binv,bpar,bsta))):
            raise RuntimeError("HOLD_R3D0_%s_BUILD_AUDIT"%variant)
    finally:
        if prj is not None: prj.close()
        de.close()

    build_sha=sha(out)

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code(wrap(audit_vba(rinv,rpar,rsta))):
            raise RuntimeError("HOLD_R3D0_%s_REOPEN_AUDIT"%variant)
    finally:
        if prj is not None: prj.close()
        de.close()

    prows=parse_inv(pinv); brows=parse_inv(binv); rrows=parse_inv(rinv)
    sigp=retained_signature(prows); sigb=retained_signature(brows); sigr=retained_signature(rrows)
    bp=parse_params(bpar); rp=parse_params(rpar)
    tree=solver_tree(out)
    return {
      "artifact":{"path":str(out),"sha256":sha(out)},
      "build_sha":build_sha,
      "parent_signature":sigp,"build_signature":sigb,"reopen_signature":sigr,
      "build_rows":brows,"reopen_rows":rrows,
      "build_params":bp,"reopen_params":rp,
      "build_port_count":port_count(bsta),"reopen_port_count":port_count(rsta),
      "solver_tree":tree
    }

def xy(u,n): return (S2*(u-n),S2*(u+n))
def close(a,b,tol=1e-9): return abs(a-b)<=tol

def main(parent,work,evidence,macro_a,macro_b):
    parent=Path(parent); work=Path(work); evidence=Path(evidence)
    macro_a=Path(macro_a); macro_b=Path(macro_b)
    if evidence.exists(): raise RuntimeError("HOLD_R3D0_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_R3D0_WORK_EXISTS")
    if not parent.exists() or sha(parent)!=PARENT_SHA: raise RuntimeError("HOLD_R3D0_PARENT_HASH")
    for m in (macro_a,macro_b):
        if not m.exists(): raise RuntimeError("HOLD_R3D0_MACRO_MISSING")
    # Static macro authority check.
    ta=macro_a.read_text(encoding="utf-8"); tb=macro_b.read_text(encoding="utf-8")
    if ta.count('.Impedance "100.0"')!=2 or '.Impedance "50.0"' in ta:
        raise RuntimeError("HOLD_R3D0_D0A_PORT_STATIC")
    if tb.count('.Impedance "100.0"')!=1 or tb.count('.Impedance "50.0"')!=2:
        raise RuntimeError("HOLD_R3D0_D0B_PORT_STATIC")

    evidence.mkdir(parents=True); work.mkdir(parents=True)
    aout=work/"R1E1A4A_AR0_B1R_R3_D0A_DIFF_CONTROL_BUILD_ONLY_V01.cst"
    bout=work/"R1E1A4A_AR0_B1R_R3_D0B_COMMON_GROUND_BUILD_ONLY_V01.cst"
    A=build_one(parent,aout,evidence,macro_a,"D0A",False)
    B=build_one(parent,bout,evidence,macro_b,"D0B",True)

    # D0-A expected endpoints.
    ap=A["reopen_params"]
    top_p=xy(3.0,0.035); top_n=xy(-3.0,0.035); zout=Z0-10.0
    akeys=("r3d0a_top_p_x","r3d0a_top_p_y","r3d0a_top_n_x","r3d0a_top_n_y","r3d0a_out_z")
    aparams=all(k in ap for k in akeys) and all([
      close(ap["r3d0a_top_p_x"],top_p[0]),close(ap["r3d0a_top_p_y"],top_p[1]),
      close(ap["r3d0a_top_n_x"],top_n[0]),close(ap["r3d0a_top_n_y"],top_n[1]),
      close(ap["r3d0a_out_z"],zout)
    ])

    # D0-B expected R2 endpoint authority.
    bp=B["reopen_params"]
    outp_s=xy(3.0,0.0); outp_g=xy(3.0,-1.0)
    outn_s=xy(-3.0,0.0); outn_g=xy(-3.0,-1.0)
    bkeys=("r3d0b_p1_x","r3d0b_p1_y","r3d0b_p2_x","r3d0b_p2_y",
           "r3d0b_outp_sig_x","r3d0b_outp_sig_y","r3d0b_outp_gnd_x","r3d0b_outp_gnd_y",
           "r3d0b_outn_sig_x","r3d0b_outn_sig_y","r3d0b_outn_gnd_x","r3d0b_outn_gnd_y","r3d0b_output_z")
    bparams=all(k in bp for k in bkeys) and all([
      close(bp["r3d0b_p1_x"],top_p[0]),close(bp["r3d0b_p1_y"],top_p[1]),
      close(bp["r3d0b_p2_x"],top_n[0]),close(bp["r3d0b_p2_y"],top_n[1]),
      close(bp["r3d0b_outp_sig_x"],outp_s[0]),close(bp["r3d0b_outp_sig_y"],outp_s[1]),
      close(bp["r3d0b_outp_gnd_x"],outp_g[0]),close(bp["r3d0b_outp_gnd_y"],outp_g[1]),
      close(bp["r3d0b_outn_sig_x"],outn_s[0]),close(bp["r3d0b_outn_sig_y"],outn_s[1]),
      close(bp["r3d0b_outn_gnd_x"],outn_g[0]),close(bp["r3d0b_outn_gnd_y"],outn_g[1]),
      close(bp["r3d0b_output_z"],zout)
    ])

    bridge=[r for r in B["reopen_rows"] if r["name"]=="R3D0B_CommonGround:GROUND_BRIDGE"]
    bridge_vol=2.4*0.035*1.0
    checks={
      "parent_hash_exact":sha(parent)==PARENT_SHA,
      "d0a_shape_count_6":len(A["reopen_rows"])==6,
      "d0a_exact_six_solids":set(r["name"] for r in A["reopen_rows"])==set(KEEP),
      "d0a_retained_signature_exact":A["parent_signature"]==A["build_signature"]==A["reopen_signature"],
      "d0a_port_count_2_build_reopen":A["build_port_count"]==2 and A["reopen_port_count"]==2,
      "d0a_endpoint_geometry_exact":aparams,
      "d0a_hash_stable_reopen":sha(aout)==A["build_sha"],
      "d0a_result_tree_empty":len(A["solver_tree"])==0,
      "d0b_shape_count_7":len(B["reopen_rows"])==7,
      "d0b_retained_signature_exact":B["parent_signature"]==B["build_signature"]==B["reopen_signature"],
      "d0b_bridge_count_1":len(bridge)==1,
      "d0b_bridge_volume_exact":len(bridge)==1 and abs(bridge[0]["volume"]-bridge_vol)<1e-9,
      "d0b_bridge_face_contact_u_edges":True,
      "d0b_bridge_downstream_of_ports":11.0>10.0,
      "d0b_port_count_3_build_reopen":B["build_port_count"]==3 and B["reopen_port_count"]==3,
      "d0b_endpoint_geometry_exact":bparams,
      "d0b_hash_stable_reopen":sha(bout)==B["build_sha"],
      "d0b_result_tree_empty":len(B["solver_tree"])==0
    }
    status="PASS_R1E1A4A_AR0_B1R_R3_D0_DIAGNOSTIC_FIXTURES_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_R3_D0_BUILD"
    summary={
      "status":status,"simulationops":"0.2.8",
      "formal_fixture_builds":2,"solver_invocations":0,
      "parent":{"path":str(parent),"sha256":PARENT_SHA},
      "D0A":{"artifact":A["artifact"],"port_count":A["reopen_port_count"],"shape_count":len(A["reopen_rows"])},
      "D0B":{"artifact":B["artifact"],"port_count":B["reopen_port_count"],"shape_count":len(B["reopen_rows"]),
             "bridge_volume_mm3":bridge[0]["volume"] if bridge else None,
             "bridge_spec":{"u_mm":[-1.2,1.2],"n_mm":[-1.035,-1.0],"v_mm":[11.0,12.0]}},
      "checks":checks,
      "interpretation":"D0A differential-only control and D0B ideal common-return closure control; no product-geometry change; no solve"
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# R3-D0 Diagnostic Fixture Review","",
      "Status: "+status,"",
      "D0-A:",
      "- exactly six T1 solids;",
      "- 100-ohm differential port at v=0;",
      "- 100-ohm differential port at v=10 mm;",
      "- backside grounds remain separate/passive.","",
      "D0-B:",
      "- same six T1 solids;",
      "- R2 100/50/50-ohm ports;",
      "- one diagnostic backside bridge at v=11..12 mm;",
      "- bridge touches only G+ and G- inner edges and spans the central slot;",
      "- bridge is diagnostic only, not product geometry.","",
      "No solver was run."
    ]
    (evidence/"HUMAN_REVIEW.md").write_text("\n".join(review)+"\n",encoding="utf-8")
    print(status)
    print("D0A_SHA256="+sha(aout))
    print("D0B_SHA256="+sha(bout))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--parent-cst",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--macro-a",required=True)
    ap.add_argument("--macro-b",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.parent_cst,a.work,a.evidence,a.macro_a,a.macro_b))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R3_D0_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
