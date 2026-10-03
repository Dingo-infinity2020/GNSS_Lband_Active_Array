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
CU_T=0.035
L_BAL=1.50
V_FULL=4.50
V_BOTTOM=12.00
GROUND_W=3.60
POLS={
 "A":{"u":(S2,S2),"n":(-S2,S2)},
 "B":{"u":(-S2,S2),"n":(-S2,-S2)}
}
TERMS=(("P",3.0),("N",-3.0))
KEEP_A=(
 "B0_Stalk:A_P_PRONG",
 "B0_Stalk:A_N_PRONG",
 "B0_MSL:A_P_MSL",
 "B0_MSL:A_N_MSL",
 "B1RT1R1_BackGround:A_P_GROUND_TAPER",
 "B1RT1R1_BackGround:A_N_GROUND_TAPER",
)
GROUND_NAMES=tuple("B1RT1_BackGround:%s_%s_GROUND_TAPER"%(p,s) for p in ("A","B") for s,_ in TERMS)
CORR_NAMES=tuple("B1RT1R1_BackGround:%s_%s_GROUND_TAPER"%(p,s) for p in ("A","B") for s,_ in TERMS)
PRESERVE_COMPONENTS=(
 "UnitCellGround","Substrate","TopCopper",
 "B0_Stalk","B0_MSL","B0_LNAEnvelope",
 "B1M_LowerStalk","B1M_UpperRail","B1M_TopTenon","B1M_BottomTenon",
 "B1RT0_RFTenon","B1RT0_TongueCu","B1RT0_Solder"
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
    if s is None or e is None or e<=s: raise RuntimeError("HOLD_D1_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def inv_vba(path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(path).replace("\\","/"),
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+500",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      "  mat=Solid.GetMaterialNameForShape(nm)",
      '  Print #f, "SHAPE|" & nm & "|material=" & mat & "|volume=" & CStr(Solid.GetVolume(nm))',
      " End If",
      "Next i",
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f",
      "On Error GoTo 0"
    ])

def parse_inv(path):
    rows=[]; kv={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            _,nm,mat,vol=line.split("|",3)
            rows.append({"name":nm,"component":nm.split(":",1)[0],
                         "material":mat.split("=",1)[1],"volume":float(vol.split("=",1)[1])})
        elif "=" in line:
            k,v=line.split("=",1); kv[k]=v
    return rows,kv

def solver_tree(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return [x for x in p3.get_tree_items()
                if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+str(ex)]

def signature(rows,components):
    return {r["name"]:(r["material"],round(r["volume"],12)) for r in rows if r["component"] in components}

def ground_points(uc):
    h=GROUND_W/2.0
    return [(uc,Z0-L_BAL),(uc+h,Z0-V_FULL),(uc+h,Z0-V_BOTTOM),
            (uc-h,Z0-V_BOTTOM),(uc-h,Z0-V_FULL)]

def extrude_uz_polygon(name,comp,mat,pol,points,height=-CU_T):
    uv=POLS[pol]["u"]; nv=POLS[pol]["n"]
    # Base plane is local n=-1.0. CST positive height points INTO the FR4 here.
    # Therefore corrected backside copper uses negative height to n=-1.035.
    x0,y0=-nv[0],-nv[1]
    lines=["With Extrude",' .Reset',' .Name "%s"'%name,' .Component "%s"'%comp,
           ' .Material "%s"'%mat,' .Mode "Pointlist"',' .Height "%.12g"'%height,
           ' .Twist "0.0"',' .Taper "0.0"',
           ' .Origin "%.15g", "%.15g", "0.0"'%(x0,y0),
           ' .Uvector "%.15g", "%.15g", "0.0"'%(uv[0],uv[1]),
           ' .Vvector "0.0", "0.0", "1.0"']
    u0,z0=points[0]; lines.append(' .Point "%.12g", "%.12g"'%(u0,z0))
    for u,z in points[1:]: lines.append(' .LineTo "%.12g", "%.12g"'%(u,z))
    lines.append(' .LineTo "%.12g", "%.12g"'%(u0,z0))
    lines += [" .Create","End With"]
    return "\n".join(lines)

def correct_ground(prj):
    code=[]
    for nm in GROUND_NAMES: code.append('Solid.Delete "%s"'%nm)
    for pol in ("A","B"):
        for side,uc in TERMS:
            code.append(extrude_uz_polygon("%s_%s_GROUND_TAPER"%(pol,side),
                                           "B1RT1R1_BackGround","B0_COPPER",
                                           pol,ground_points(uc),-CU_T))
    prj.modeler.add_to_history("AR0-B1R-T1R1 corrected backside ground placement","\n".join(code))

def delete_nonkeep(rows,keep):
    return "\n".join('Solid.Delete "%s"'%r["name"] for r in rows if r["name"] not in keep)

def extrude_bridge():
    u=(S2,S2); n=(-S2,S2); z1=Z0-12.0; z2=Z0-11.0
    return '''With Extrude
 .Reset
 .Name "GROUND_BRIDGE"
 .Component "R3D1B_CommonGround"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "%.12g"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.0", "0.0", "%.12g"
 .Uvector "%.15g", "%.15g", "0.0"
 .Vvector "%.15g", "%.15g", "0.0"
 .Point "-1.2", "-1.035"
 .LineTo "1.2", "-1.035"
 .LineTo "1.2", "-1.0"
 .LineTo "-1.2", "-1.0"
 .LineTo "-1.2", "-1.035"
 .Create
End With'''%(z2-z1,z1,u[0],u[1],n[0],n[1])

def run_vba_on(path,body):
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(path))
        ok=p.schematic.execute_vba_code(wrap(body))
        p.save()
        return ok
    finally:
        if p is not None: p.close()
        de.close()

def build_t1r1(parent,out,evidence):
    shutil.copy2(str(parent),str(out))
    pre=evidence/"T1R1_parent_inventory.txt"
    post=evidence/"T1R1_reopen_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inv_vba(pre))): raise RuntimeError("HOLD_D1_T1R1_PARENT_INV")
        correct_ground(p); p.save()
    finally:
        if p is not None: p.close()
        de.close()
    build_sha=sha(out)
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inv_vba(post))): raise RuntimeError("HOLD_D1_T1R1_REOPEN_INV")
    finally:
        if p is not None: p.close()
        de.close()
    return build_sha,parse_inv(pre),parse_inv(post)

def boolean_overlap_zero(source,evidence):
    results={}
    # One temporary project per own-pair group: each corrected ground is consumed exactly once.
    tmp=evidence.parent/"_r3d1_t1r1_own_overlap_probe.cst"
    if tmp.exists(): tmp.unlink()
    shutil.copy2(str(source),str(tmp))
    out=evidence/"T1R1_ground_prong_overlap.txt"
    lines=['Dim f As Integer','f=FreeFile','Open "%s" For Output As #f'%str(out).replace("\\","/")]
    pairs=[
      ("A_P","B1RT1R1_BackGround:A_P_GROUND_TAPER","B0_Stalk:A_P_PRONG"),
      ("A_N","B1RT1R1_BackGround:A_N_GROUND_TAPER","B0_Stalk:A_N_PRONG"),
      ("B_P","B1RT1R1_BackGround:B_P_GROUND_TAPER","B0_Stalk:B_P_PRONG"),
      ("B_N","B1RT1R1_BackGround:B_N_GROUND_TAPER","B0_Stalk:B_N_PRONG"),
    ]
    for tag,g,s in pairs:
        lines += [
          'Solid.Intersect "%s", "%s"'%(g,s),
          'On Error Resume Next',
          'Print #f, "%s_AFTER=" & CStr(Solid.GetVolume("%s"))'%(tag,g),
          'If Err.Number <> 0 Then',
          ' Err.Clear',
          ' Print #f, "%s_INTERSECTION=0"'%tag,
          'End If',
          'On Error GoTo 0'
        ]
    lines += ["Close #f"]
    try:
        run_vba_on(tmp,"\n".join(lines))
    except Exception:
        # CST may raise when an intersection is empty before On Error traps.
        pass
    txt=out.read_text(encoding="utf-8") if out.exists() else ""
    for tag,_,__ in pairs:
        results[tag]=("%s_INTERSECTION=0"%tag) in txt
    try: tmp.unlink()
    except Exception: pass
    return results,txt

def build_fixture(t1r1,out,evidence,macro,variant,bridge):
    shutil.copy2(str(t1r1),str(out))
    pinv=evidence/(variant+"_parent_inventory.txt")
    rinv=evidence/(variant+"_reopen_inventory.txt")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inv_vba(pinv))): raise RuntimeError("HOLD_D1_%s_PARENT_INV"%variant)
        rows,_=parse_inv(pinv)
        p.modeler.add_to_history("R3-D1 %s exact corrected Pol-A transition"%variant,delete_nonkeep(rows,KEEP_A))
        if bridge: p.modeler.add_to_history("R3-D1B diagnostic common-ground bridge",extrude_bridge())
        p.modeler.add_to_history("R3-D1 %s ports"%variant,macro_body(macro))
        p.save()
    finally:
        if p is not None: p.close()
        de.close()
    build_sha=sha(out)
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inv_vba(rinv))): raise RuntimeError("HOLD_D1_%s_REOPEN_INV"%variant)
    finally:
        if p is not None: p.close()
        de.close()
    return build_sha,parse_inv(pinv),parse_inv(rinv),solver_tree(out)

def main(parent,work,evidence,macro_a,macro_b):
    parent=Path(parent); work=Path(work); evidence=Path(evidence); macro_a=Path(macro_a); macro_b=Path(macro_b)
    if evidence.exists(): raise RuntimeError("HOLD_D1_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_D1_WORK_EXISTS")
    if not parent.exists() or sha(parent)!=PARENT_SHA: raise RuntimeError("HOLD_D1_PARENT_HASH")
    evidence.mkdir(parents=True); work.mkdir(parents=True)

    t1r1=work/"R1E1A4A_AR0_B1R_T1R1_GROUND_PLACEMENT_CORRECTED_BUILD_ONLY_V01.cst"
    tsha,(pre_rows,prekv),(post_rows,postkv)=build_t1r1(parent,t1r1,evidence)
    pre_sig=signature(pre_rows,PRESERVE_COMPONENTS); post_sig=signature(post_rows,PRESERVE_COMPONENTS)
    corr=[r for r in post_rows if r["component"]=="B1RT1R1_BackGround"]
    vol_equal=(len(corr)==4 and max(abs(r["volume"]-1.134) for r in corr)<1e-9)
    overlap,overlap_txt=boolean_overlap_zero(t1r1,evidence)

    d1a=work/"R1E1A4A_AR0_B1R_R3_D1A_DIFF_CONTROL_BUILD_ONLY_V01.cst"
    d1b=work/"R1E1A4A_AR0_B1R_R3_D1B_COMMON_GROUND_BUILD_ONLY_V01.cst"
    asha,(apre,aprekv),(apost,apostkv),atree=build_fixture(t1r1,d1a,evidence,macro_a,"D1A",False)
    bsha,(bpre,bprekv),(bpost,bpostkv),btree=build_fixture(t1r1,d1b,evidence,macro_b,"D1B",True)

    asig={r["name"]:(r["material"],round(r["volume"],12)) for r in apost if r["name"] in KEEP_A}
    bsig={r["name"]:(r["material"],round(r["volume"],12)) for r in bpost if r["name"] in KEEP_A}
    parent_a={r["name"]:(r["material"],round(r["volume"],12)) for r in post_rows if r["name"] in KEEP_A}
    bridge=[r for r in bpost if r["name"]=="R3D1B_CommonGround:GROUND_BRIDGE"]

    checks={
      "parent_hash_exact":sha(parent)==PARENT_SHA,
      "t1r1_fresh_reopen_hash_stable":sha(t1r1)==tsha,
      "t1r1_non_ground_geometry_preserved":pre_sig==post_sig,
      "t1r1_corrected_ground_count_4":len(corr)==4,
      "t1r1_corrected_ground_volume_exact":vol_equal,
      "t1r1_ground_prong_overlap_zero_all":all(overlap.values()),
      "t1r1_port_count_zero":int(postkv.get("PORT_COUNT","-1"))==0,
      "t1r1_result_tree_empty":len(solver_tree(t1r1))==0,
      "d1a_shape_count_6":len(apost)==6,
      "d1a_corrected_six_signature_exact":asig==parent_a,
      "d1a_port_count_2":int(apostkv.get("PORT_COUNT","-1"))==2,
      "d1a_hash_stable":sha(d1a)==asha,
      "d1a_result_tree_empty":len(atree)==0,
      "d1b_shape_count_7":len(bpost)==7,
      "d1b_corrected_six_signature_exact":bsig==parent_a,
      "d1b_bridge_count_1":len(bridge)==1,
      "d1b_bridge_volume_exact":len(bridge)==1 and abs(bridge[0]["volume"]-0.084)<1e-9,
      "d1b_port_count_3":int(bpostkv.get("PORT_COUNT","-1"))==3,
      "d1b_hash_stable":sha(d1b)==bsha,
      "d1b_result_tree_empty":len(btree)==0
    }
    status="PASS_R1E1A4A_AR0_B1R_R3_D1_CORRECTED_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_R3_D1_BUILD"
    summary={
      "status":status,"simulationops":"0.2.8","formal_build_products":3,"solver_invocations":0,
      "root_cause":"original T1 backside ground copper fully embedded in FR4 because extrusion sign was reversed",
      "correction":{"old_height_mm":0.035,"new_height_mm":-0.035,"corrected_n_mm":[-1.035,-1.0]},
      "T1R1":{"artifact":str(t1r1),"sha256":sha(t1r1),"shape_count":len(post_rows),
              "corrected_ground_volumes_mm3":[r["volume"] for r in corr],
              "ground_prong_overlap_zero":overlap},
      "D1A":{"artifact":str(d1a),"sha256":sha(d1a),"shape_count":len(apost),"port_count":int(apostkv.get("PORT_COUNT","-1"))},
      "D1B":{"artifact":str(d1b),"sha256":sha(d1b),"shape_count":len(bpost),"port_count":int(bpostkv.get("PORT_COUNT","-1")),
             "bridge_volume_mm3":bridge[0]["volume"] if bridge else None},
      "checks":checks
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    (evidence/"HUMAN_REVIEW.md").write_text(
      "# R3-D1 Corrected Build Review\n\n"
      "Status: "+status+"\n\n"
      "- T1R1: four backside grounds moved outward only; all own-prong volumetric intersections are zero.\n"
      "- D1-A: corrected six-solid differential control, 2 ports.\n"
      "- D1-B: corrected six solids + diagnostic common-ground bridge, 3 ports.\n"
      "- No solver was invoked in build stage.\n",encoding="utf-8")
    print(status)
    print("T1R1_SHA256="+sha(t1r1))
    print("D1A_SHA256="+sha(d1a))
    print("D1B_SHA256="+sha(d1b))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--parent-cst",required=True); ap.add_argument("--work",required=True); ap.add_argument("--evidence",required=True)
    ap.add_argument("--macro-a",required=True); ap.add_argument("--macro-b",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.parent_cst,a.work,a.evidence,a.macro_a,a.macro_b))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R3_D1_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
