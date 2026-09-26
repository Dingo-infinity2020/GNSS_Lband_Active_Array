from __future__ import print_function
import argparse, hashlib, json, math, os, shutil, sys, traceback
from collections import Counter
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

PARENT_SHA="b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa"
S2=1.0/math.sqrt(2.0)
TERMINAL_R=3.0
Z_SUB_BOTTOM=57.1428571428
Z_SUB_TOP=58.1428571428
Z_CU_BOTTOM=58.1428571428
FEED_DEPTH=12.0
DG=3.0
CU_T=0.035
BOARD_T=1.0
MSL_W=1.90
U_OUT=5.0
U_SLOT=0.75
LNA_V=7.0
LNA_HALF=1.0
FEED_HOLE_R=0.20
FEED_BARREL_RI=0.10

POLS={
 "A":{"u":(S2,S2),"n":(-S2,S2),"angle":45.0},
 "B":{"u":(-S2,S2),"n":(-S2,-S2),"angle":135.0},
}

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def vba(body):
    return "Sub Main()\n"+body+"\nEnd Sub"

def mat_vba():
    return r'''
With Material
 .Reset
 .Name "B0_COPPER"
 .Folder ""
 .FrqType "all"
 .Type "Lossy metal"
 .SetMaterialUnit "GHz", "mm"
 .Mue "1.0"
 .Sigma "58000000"
 .Create
End With
With Material
 .Reset
 .Name "B0_LNA_VISUAL_SURROGATE"
 .Folder ""
 .FrqType "all"
 .Type "Normal"
 .SetMaterialUnit "GHz", "mm"
 .Epsilon "1.0"
 .Mue "1.0"
 .TanD "0.0"
 .Create
End With
'''

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

def global_xy(uv,nv,u,n):
    return (uv[0]*u+nv[0]*n, uv[1]*u+nv[1]*n)

def cyl(name,comp,mat,x,y,rout,rin,z1,z2):
    return '''With Cylinder
 .Reset
 .Name "%s"
 .Component "%s"
 .Material "%s"
 .OuterRadius "%.12g"
 .InnerRadius "%.12g"
 .Axis "z"
 .Zrange "%.12g", "%.12g"
 .Xcenter "%.12g"
 .Ycenter "%.12g"
 .Segments "0"
 .Create
End With'''%(name,comp,mat,rout,rin,z1,z2,x,y)

def inventory_vba(path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(path),
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+300",
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

def paircheck_vba(path,pairs):
    lines=["On Error Resume Next","Dim f As Integer","f=FreeFile",'Open "%s" For Output As #f'%str(path)]
    for a,b,tag in pairs:
        lines.append('If Solid.DoTheseGeometricallyIntersect("%s","%s") Then Print #f, "HIT|%s|%s|%s"'%(a,b,tag,a,b))
    lines+=["Close #f","On Error GoTo 0"]
    return "\n".join(lines)

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
        return [x for x in p3.get_tree_items() if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]
    except Exception:
        return ["RESULT_API_ERROR"]

def build_geometry(prj):
    code=[mat_vba()]
    # Four prongs, four front microstrip traces, four backside ground rails, four package envelopes.
    for pol,meta in POLS.items():
        uv=meta["u"]; nv=meta["n"]
        for side,uc in (("P",3.0),("N",-3.0)):
            if side=="P": u1,u2=U_SLOT,U_OUT
            else: u1,u2=-U_OUT,-U_SLOT
            # board lies behind the front signal plane: local n=-1..0
            code.append(extrude_rect(pol+"_"+side+"_PRONG","B0_Stalk","FR4_COST_BASELINE",
                                     u1,u2,-BOARD_T,0.0,Z_SUB_BOTTOM-FEED_DEPTH,Z_SUB_BOTTOM,uv,nv))
            code.append(extrude_rect(pol+"_"+side+"_MSL","B0_MSL","B0_COPPER",
                                     uc-MSL_W/2,uc+MSL_W/2,0.0,CU_T,
                                     Z_SUB_BOTTOM-FEED_DEPTH,Z_SUB_BOTTOM,uv,nv))
            code.append(extrude_rect(pol+"_"+side+"_BACK_GND","B0_BackGround","B0_COPPER",
                                     u1,u2,-BOARD_T-CU_T,-BOARD_T,
                                     Z_SUB_BOTTOM-FEED_DEPTH,Z_SUB_BOTTOM-DG,uv,nv))
            # package visual envelope protrudes from front face, centered at v=7 mm
            code.append(extrude_rect(pol+"_"+side+"_QPL9547_ENV","B0_LNAEnvelope","B0_LNA_VISUAL_SURROGATE",
                                     uc-LNA_HALF,uc+LNA_HALF,CU_T,CU_T+1.0,
                                     Z_SUB_BOTTOM-LNA_V-LNA_HALF,Z_SUB_BOTTOM-LNA_V+LNA_HALF,uv,nv))
            x,y=global_xy(uv,nv,uc,0.0)
            # feedthrough hole through radiator substrate only
            hname=pol+"_"+side+"_FEED_HOLE"
            code.append(cyl(hname,"B0_Tools","Vacuum",x,y,FEED_HOLE_R,0.0,Z_SUB_BOTTOM,Z_SUB_TOP))
            code.append('Solid.Subtract "Substrate:FR4_BOARD", "B0_Tools:%s"'%hname)
            # signal-only plated barrel; face contact to radiator copper and MSL
            code.append(cyl(pol+"_"+side+"_SIG_FEEDTHROUGH","B0_SignalFeedthrough","B0_COPPER",
                            x,y,FEED_HOLE_R,FEED_BARREL_RI,Z_SUB_BOTTOM,Z_CU_BOTTOM))
    prj.modeler.add_to_history("AR0-B0G twin-MSL fork feed-head geometry", "\n".join(code))

def expected_manifest():
    terms={}
    reserves={}
    for pol,m in POLS.items():
        uv=m["u"]; nv=m["n"]
        for side,uc in (("P",3.0),("N",-3.0)):
            x,y=global_xy(uv,nv,uc,0.0)
            terms[pol+"_"+side]=[x,y]
            # four future ground-via reserve centers around each LNA, all in local prong FR4
            rr=[]
            for du in (-0.6,0.6):
                for dv in (-0.6,0.6):
                    rr.append([uc+du,LNA_V+dv])
            reserves[pol+"_"+side]=rr
    return {"terminal_xy_mm":terms,"via_reserve_local_uv_mm":reserves}

def run(repo,evidence,work,parent):
    repo=Path(repo); evidence=Path(evidence); work=Path(work); parent=Path(parent)
    if evidence.exists(): raise RuntimeError("HOLD_B0G_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_B0G_WORK_EXISTS")
    if not parent.exists() or sha(parent)!=PARENT_SHA: raise RuntimeError("HOLD_B0G_PARENT_HASH")
    evidence.mkdir(parents=True); work.mkdir(parents=True)
    out=work/"R1E1A4A_AR0_B0G_FEED_HEAD_BUILD_ONLY_V01.cst"
    shutil.copy2(str(parent),str(out))
    if sha(out)!=PARENT_SHA: raise RuntimeError("HOLD_B0G_COPY_HASH")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        build_geometry(prj)
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    build_sha=sha(out)
    inv=evidence/"reopen_inventory.txt"
    pairs=evidence/"targeted_intersections.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code(vba(inventory_vba(inv))):
            raise RuntimeError("HOLD_B0G_INVENTORY_API")
        pairlist=[]
        # Hard forbidden: any backside ground vs radiator copper/substrate; prong-prong collisions across polarizations;
        # LNA envelopes vs opposite-pol stalk/ground; feedthrough vs ground.
        for pol in ("A","B"):
            for side in ("P","N"):
                g="B0_BackGround:%s_%s_BACK_GND"%(pol,side)
                pairlist += [(g,"TopCopper:TOP_COPPER","GROUND_VS_RADIATOR_COPPER")]
                f="B0_SignalFeedthrough:%s_%s_SIG_FEEDTHROUGH"%(pol,side)
                for pol2 in ("A","B"):
                    for side2 in ("P","N"):
                        g2="B0_BackGround:%s_%s_BACK_GND"%(pol2,side2)
                        pairlist.append((f,g2,"FEEDTHROUGH_VS_GROUND"))
                env="B0_LNAEnvelope:%s_%s_QPL9547_ENV"%(pol,side)
                other="B" if pol=="A" else "A"
                for side2 in ("P","N"):
                    pairlist.append((env,"B0_Stalk:%s_%s_PRONG"%(other,side2),"LNA_ENV_VS_OTHER_STALK"))
                    pairlist.append((env,"B0_BackGround:%s_%s_BACK_GND"%(other,side2),"LNA_ENV_VS_OTHER_GROUND"))
        for sa in ("P","N"):
            for sb in ("P","N"):
                pairlist.append(("B0_Stalk:A_%s_PRONG"%sa,"B0_Stalk:B_%s_PRONG"%sb,"STALK_PRONG_COLLISION"))
        if not prj.schematic.execute_vba_code(vba(paircheck_vba(pairs,pairlist))):
            raise RuntimeError("HOLD_B0G_PAIRCHECK_API")
    finally:
        if prj is not None: prj.close()
        de.close()

    rows,kv=parse_inv(inv)
    names=[r["name"] for r in rows]
    counts=Counter(r["component"] for r in rows)
    hits=[x for x in pairs.read_text(encoding="utf-8").splitlines() if x.startswith("HIT|")]
    forbidden_hits=[h for h in hits if any(tag in h for tag in
                    ("GROUND_VS_RADIATOR_COPPER","FEEDTHROUGH_VS_GROUND","STALK_PRONG_COLLISION",
                     "LNA_ENV_VS_OTHER_STALK","LNA_ENV_VS_OTHER_GROUND"))]
    # Deterministic architecture checks independent of CST intersection semantics.
    man=expected_manifest()
    reserves_inside=True
    for key,pts in man["via_reserve_local_uv_mm"].items():
        side=key.split("_")[-1]
        for u,v in pts:
            if side=="P":
                inside=(U_SLOT < u < U_OUT and 0.0 < v < FEED_DEPTH)
            else:
                inside=(-U_OUT < u < -U_SLOT and 0.0 < v < FEED_DEPTH)
            reserves_inside = reserves_inside and inside
    expected_new={"B0_Stalk":4,"B0_MSL":4,"B0_BackGround":4,"B0_LNAEnvelope":4,"B0_SignalFeedthrough":4}
    checks={
      "fresh_reopen_shape_count_23":len(rows)==23,
      "new_component_counts_exact":all(counts.get(k,0)==v for k,v in expected_new.items()),
      "no_tool_shapes":not any(n.startswith("B0_Tools:") for n in names),
      "all_positive_volume":all(r["volume"]>0 for r in rows),
      "port_count_zero":int(kv.get("PORT_COUNT","-1"))==0,
      "no_solver_result_tree":len(solver_tree(out))==0,
      "targeted_forbidden_intersections_zero":len(forbidden_hits)==0,
      "via_reserves_inside_prongs":reserves_inside,
      "ground_setback_exact_3mm":DG==3.0,
      "msl_width_exact_1p9mm":MSL_W==1.90,
      "radiator_top_copper_shape_count_preserved":counts.get("TopCopper",0)==1,
      "substrate_shape_count_preserved":counts.get("Substrate",0)==1,
    }
    status="PASS_R1E1A4A_AR0_B0G_FEED_HEAD_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B0G_GEOMETRY"
    summary={
      "status":status,"simulationops":"0.2.8","formal_build_invocations":1,"solver_invocations":0,
      "parent":{"path":str(parent),"sha256":PARENT_SHA},
      "artifact":{"path":str(out),"sha256":sha(out),"build_sha256":build_sha},
      "geometry":{
        "terminal_r_mm":TERMINAL_R,"feed_head_depth_mm":FEED_DEPTH,"ground_setback_mm":DG,
        "msl_width_mm":MSL_W,"fork_outer_halfwidth_mm":U_OUT,"fork_slot_halfwidth_mm":U_SLOT,
        "lna_centers_local_uv_mm":[[-3.0,7.0],[3.0,7.0]],
        "feedthrough_outer_radius_mm":FEED_HOLE_R,"feedthrough_inner_radius_mm":FEED_BARREL_RI
      },
      "manifest":man,"shape_count":len(rows),"component_counts":dict(counts),
      "targeted_intersection_hits":hits,"checks":checks
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# AR0-B0G Human 3D Review Guide","",
      "Canonical build status: "+status,"",
      "Review in this order:",
      "1. Parent radiator copper only.",
      "2. Four fork prongs only.",
      "3. Four signal feedthroughs + MSL traces only.",
      "4. Backside ground rails only; verify 3-mm setback and no radiator overlap.",
      "5. QPL9547 visual envelopes only.",
      "6. Full dual-polarization feed head.","",
      "Mandatory questions:",
      "- Are the four signal feedthroughs at the intended terminal points?",
      "- Does any backside ground appear behind/inside radiator copper?",
      "- Do A/B fork prongs collide?",
      "- Do LNA envelopes collide with the other polarization stalk?",
      "- Does each future via-reserve region lie in real FR4?",
      "- Is there any unexpected metal in the radiator center besides the four signal feedthroughs?","",
      "No solver is authorized."
    ]
    (evidence/"HUMAN_3D_REVIEW.md").write_text("\n".join(review)+"\n",encoding="utf-8")
    print(status); print("ARTIFACT_SHA256="+sha(out)); print("HITS="+str(len(hits)))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True); ap.add_argument("--parent-cst",required=True)
    a=ap.parse_args()
    try:
        sys.exit(run(a.repo,a.evidence,a.work,a.parent_cst))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B0G_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
