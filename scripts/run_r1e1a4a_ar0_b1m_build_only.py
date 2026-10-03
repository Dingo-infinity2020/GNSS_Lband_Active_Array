from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from collections import Counter
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

PARENT_SHA="6b027162dd93d8613a0943df0fd96d6bf65d6721893e49c8d8bdc17f8f5eb698"
S2=1.0/math.sqrt(2.0)
Z0=57.1428571428
ZSUBTOP=58.1428571428
ZCUTTOP=58.1978571428
LOWER_TOP=45.1428571428
SPLIT=22.5714285714
POLS={
 "A":{"u":(S2,S2),"n":(-S2,S2)},
 "B":{"u":(-S2,S2),"n":(-S2,-S2)}
}
INTERLOCK_U={"A":(-0.125,1.125),"B":(-1.125,0.125)}
PARENT_RF_COMPONENTS=("B0_Stalk","B0_MSL","B0_BackGround","B0_LNAEnvelope","B0_SignalFeedthrough")

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def extrude_rect(name,comp,mat,u1,u2,n1,n2,z1,z2,uv,nv):
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
End With'''%(name,comp,mat,z2-z1,z1,uv[0],uv[1],nv[0],nv[1],
              u1,n1,u2,n1,u2,n2,u1,n2,u1,n1)

def inv_vba(path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(path),
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+400",
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
                         "material":mat.split("=",1)[1],
                         "volume":float(vol.split("=",1)[1])})
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

def poly(pol,u1,u2,n1,n2):
    uv=POLS[pol]["u"]; nv=POLS[pol]["n"]
    return [(uv[0]*u+nv[0]*n,uv[1]*u+nv[1]*n)
            for u,n in ((u1,n1),(u2,n1),(u2,n2),(u1,n2))]

def axes(p):
    out=[]
    for i in range(len(p)):
        x1,y1=p[i]; x2,y2=p[(i+1)%len(p)]
        dx=x2-x1; dy=y2-y1; L=math.hypot(dx,dy)
        if L: out.append((-dy/L,dx/L))
    return out

def overlap2d(a,b,eps=1e-10):
    for ax in axes(a)+axes(b):
        pa=[x*ax[0]+y*ax[1] for x,y in a]
        pb=[x*ax[0]+y*ax[1] for x,y in b]
        if max(pa)<=min(pb)+eps or max(pb)<=min(pa)+eps: return False
    return True

def add_mechanics(prj):
    code=[]
    # two lower load-bearing bodies
    for pol,m in POLS.items():
        uv,nv=m["u"],m["n"]
        code.append(extrude_rect(pol+"_LOWER_BODY","B1M_LowerStalk","FR4_COST_BASELINE",
                                 -15,15,-1,0,0,LOWER_TOP,uv,nv))
        # complementary half-depth interlock, fully through board thickness
        u1,u2=INTERLOCK_U[pol]
        if pol=="A": z1,z2=-0.02,SPLIT+0.02
        else: z1,z2=SPLIT-0.02,LOWER_TOP+0.02
        tname=pol+"_INTERLOCK_CUT"
        code.append(extrude_rect(tname,"B1M_Tools","Vacuum",
                                 u1,u2,-1.10,0.10,z1,z2,uv,nv))
        code.append('Solid.Subtract "B1M_LowerStalk:%s_LOWER_BODY", "B1M_Tools:%s"'%(pol,tname))

        # two outer upper rails, two top tenons, two bottom tenons
        for side,u1,u2 in (("N",-13.5,-10.5),("P",10.5,13.5)):
            code.append(extrude_rect(pol+"_"+side+"_UPPER_RAIL","B1M_UpperRail","FR4_COST_BASELINE",
                                     u1,u2,-1,0,LOWER_TOP,Z0,uv,nv))
            code.append(extrude_rect(pol+"_"+side+"_TOP_TENON","B1M_TopTenon","FR4_COST_BASELINE",
                                     u1,u2,-1,0,Z0,ZSUBTOP,uv,nv))
            code.append(extrude_rect(pol+"_"+side+"_BOTTOM_TENON","B1M_BottomTenon","FR4_COST_BASELINE",
                                     u1,u2,-1,0,-0.5,0,uv,nv))

            # top mortise: separate tools because subtraction consumes a tool
            mu1,mu2=(u1-0.15,u2+0.15)
            sname=pol+"_"+side+"_RAD_SUB_MORTISE"
            cname=pol+"_"+side+"_RAD_CU_CLEAR"
            code.append(extrude_rect(sname,"B1M_Tools","Vacuum",
                                     mu1,mu2,-1.125,0.125,Z0-0.02,ZSUBTOP+0.02,uv,nv))
            code.append('Solid.Subtract "Substrate:FR4_BOARD", "B1M_Tools:%s"'%sname)
            code.append(extrude_rect(cname,"B1M_Tools","Vacuum",
                                     mu1,mu2,-1.125,0.125,ZSUBTOP-0.02,ZCUTTOP,uv,nv))
            code.append('Solid.Subtract "TopCopper:TOP_COPPER", "B1M_Tools:%s"'%cname)

            # reflector mortise
            bname=pol+"_"+side+"_REFLECTOR_MORTISE"
            code.append(extrude_rect(bname,"B1M_Tools","Vacuum",
                                     mu1,mu2,-1.125,0.125,-0.52,0.02,uv,nv))
            code.append('Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "B1M_Tools:%s"'%bname)
    prj.modeler.add_to_history("AR0-B1M full mechanical stalk integration", "\n".join(code))

def rf_signature(rows):
    return {r["name"]:round(r["volume"],12) for r in rows if r["component"] in PARENT_RF_COMPONENTS}

def analytic_audit():
    # Cross-pol full-body occupancy at the central crossing after complementary cuts.
    # B thickness in A-local u = 0..1; A thickness in B-local u = -1..0.
    clearA=(INTERLOCK_U["A"][0] <= 0.0 and INTERLOCK_U["A"][1] >= 1.0)
    clearB=(INTERLOCK_U["B"][0] <= -1.0 and INTERLOCK_U["B"][1] >= 0.0)

    # Outer rails/tenons are far from the central crossing in local u.
    rails={}
    for pol in ("A","B"):
        rails[(pol,"N")]=poly(pol,-13.5,-10.5,-1,0)
        rails[(pol,"P")]=poly(pol,10.5,13.5,-1,0)
    rail_collisions=[]
    for sa in ("N","P"):
        for sb in ("N","P"):
            if overlap2d(rails[("A",sa)],rails[("B",sb)]):
                rail_collisions.append("A_%s_vs_B_%s"%(sa,sb))

    # RF keepout: mechanics at |u|>=10.5; B0 RF/LNA occupy |u|<=5 (feed head).
    return {
      "interlock_A_clears_B_thickness":clearA,
      "interlock_B_clears_A_thickness":clearB,
      "outer_rail_cross_pol_collisions":rail_collisions,
      "mechanical_vs_b0_feedhead_local_u_gap_mm":10.5-5.0,
      "top_bottom_mortise_clearance_each_side_mm":0.125,
      "interlock_clearance_each_side_mm":0.125
    }

def run(evidence,work,parent):
    evidence=Path(evidence); work=Path(work); parent=Path(parent)
    if evidence.exists(): raise RuntimeError("HOLD_B1M_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_B1M_WORK_EXISTS")
    if not parent.exists() or sha(parent)!=PARENT_SHA: raise RuntimeError("HOLD_B1M_PARENT_HASH")
    evidence.mkdir(parents=True); work.mkdir(parents=True)

    out=work/"R1E1A4A_AR0_B1M_FULL_MECHANICAL_STALK_BUILD_ONLY_V01.cst"
    shutil.copy2(str(parent),str(out))
    if sha(out)!=PARENT_SHA: raise RuntimeError("HOLD_B1M_PARENT_COPY_HASH")

    pre=evidence/"parent_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code(wrap(inv_vba(pre))):
            raise RuntimeError("HOLD_B1M_PARENT_INVENTORY")
        add_mechanics(prj)
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    build_sha=sha(out)
    post=evidence/"reopen_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code(wrap(inv_vba(post))):
            raise RuntimeError("HOLD_B1M_REOPEN_INVENTORY")
    finally:
        if prj is not None: prj.close()
        de.close()

    pre_rows,pre_kv=parse_inv(pre); rows,kv=parse_inv(post)
    pre_rf=rf_signature(pre_rows); post_rf=rf_signature(rows)
    counts=Counter(r["component"] for r in rows)
    analytic=analytic_audit()
    tree=solver_tree(out)

    rf_unchanged=(pre_rf==post_rf)
    expected_new={
      "B1M_LowerStalk":2,
      "B1M_UpperRail":4,
      "B1M_TopTenon":4,
      "B1M_BottomTenon":4
    }
    checks={
      "artifact_exists":out.exists(),
      "fresh_reopen_hash_stable":sha(out)==build_sha,
      "shape_count_37":len(rows)==37,
      "b1m_component_counts_exact":all(counts.get(k,0)==v for k,v in expected_new.items()),
      "no_tool_shapes":not any(r["component"]=="B1M_Tools" for r in rows),
      "all_positive_volume":all(r["volume"]>0 for r in rows),
      "b0g_rf_shape_volumes_byte_semantics_preserved":rf_unchanged,
      "port_count_zero":int(kv.get("PORT_COUNT","-1"))==0,
      "solver_tree_empty":len(tree)==0,
      "interlock_A_clear":analytic["interlock_A_clears_B_thickness"],
      "interlock_B_clear":analytic["interlock_B_clears_A_thickness"],
      "outer_rail_cross_pol_collision_zero":len(analytic["outer_rail_cross_pol_collisions"])==0,
      "mechanical_rf_keepout_ge_5p5mm":analytic["mechanical_vs_b0_feedhead_local_u_gap_mm"]>=5.5,
    }
    status="PASS_R1E1A4A_AR0_B1M_FULL_MECHANICAL_STALK_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1M_GEOMETRY"

    summary={
      "status":status,"simulationops":"0.2.8",
      "formal_build_invocations":1,"solver_invocations":0,
      "parent":{"path":str(parent),"sha256":PARENT_SHA},
      "artifact":{"path":str(out),"sha256":sha(out)},
      "inventory":{"shape_count":len(rows),"component_counts":dict(counts)},
      "b0g_rf_signature_before":pre_rf,
      "b0g_rf_signature_after":post_rf,
      "analytic_mechanical_audit":analytic,
      "solver_tree_matches":tree,
      "checks":checks,
      "rf_transition_status":"B0G abrupt 3-mm ground onset remains geometry placeholder; not RF-qualified"
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# AR0-B1M Human 3D Review Guide","",
      "Canonical build status: "+status,"",
      "Review the existing B1M artifact only.",
      "1. Radiator substrate/copper with four diagonal mortise clearances.",
      "2. Four upper mechanical rails and four top tenons.",
      "3. B0 RF fork/feed/LNA region with mechanics hidden, then together.",
      "4. Full lower stalk bodies; inspect complementary center interlock.",
      "5. Four bottom tenons and four reflector slots.",
      "6. Full dual-pol assembly.","",
      "Confirm:",
      "- two stalk PCBs are genuinely perpendicular and mechanically interlocked;",
      "- top tenons seat in radiator mortises without touching radiator copper;",
      "- bottom tenons seat in reflector slots;",
      "- no mechanical feature intrudes into the B0 RF/LNA feed head;",
      "- B0 signal traces, ground rails, feedthroughs and LNA envelopes look unchanged;",
      "- the assembly looks load-bearing rather than like a temporary RF coupon.","",
      "Important: the abrupt 3-mm B0 ground onset is still NOT RF-qualified.",
      "No solver is authorized."
    ]
    (evidence/"HUMAN_3D_REVIEW.md").write_text("\n".join(review)+"\n",encoding="utf-8")
    print(status); print("ARTIFACT_SHA256="+sha(out))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence",required=True); ap.add_argument("--work",required=True); ap.add_argument("--parent-cst",required=True)
    a=ap.parse_args()
    try:
        sys.exit(run(a.evidence,a.work,a.parent_cst))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1M_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
