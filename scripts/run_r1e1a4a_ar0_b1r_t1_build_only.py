from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from collections import Counter
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

PARENT_SHA="f4c51b603fc01e8c3cec095de0ca641a3a671dc1e2449a95a123af6a8b902bb9"
S2=1.0/math.sqrt(2.0)
Z0=57.1428571428
CU_T=0.035
L_BAL=1.50
L_TAPER=3.00
V_FULL=4.50
V_BOTTOM=12.00
GROUND_W=3.60
TRACE_W=1.90
BOARD_T=1.0
POLS={
 "A":{"u":(S2,S2),"n":(-S2,S2)},
 "B":{"u":(-S2,S2),"n":(-S2,-S2)}
}
TERMS=(("P",3.0),("N",-3.0))
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

def inv_vba(path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(path),
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

def signature(rows,components):
    return {r["name"]:round(r["volume"],12) for r in rows if r["component"] in components}

def poly_rect(pol,uc,w,n1,n2):
    uv=POLS[pol]["u"]; nv=POLS[pol]["n"]
    u1,u2=uc-w/2,uc+w/2
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

def extrude_uz_polygon(name,comp,mat,pol,points,height=CU_T):
    uv=POLS[pol]["u"]; nv=POLS[pol]["n"]
    # Base plane is stalk backside n=-1.0. U is local u, V is global z.
    # U x V = -n, so positive height extrudes outward to n=-1.035.
    x0,y0=-nv[0],-nv[1]
    lines=[
      "With Extrude",
      ' .Reset',
      ' .Name "%s"'%name,
      ' .Component "%s"'%comp,
      ' .Material "%s"'%mat,
      ' .Mode "Pointlist"',
      ' .Height "%.12g"'%height,
      ' .Twist "0.0"',
      ' .Taper "0.0"',
      ' .Origin "%.15g", "%.15g", "0.0"'%(x0,y0),
      ' .Uvector "%.15g", "%.15g", "0.0"'%(uv[0],uv[1]),
      ' .Vvector "0.0", "0.0", "1.0"'
    ]
    u0,z0=points[0]
    lines.append(' .Point "%.12g", "%.12g"'%(u0,z0))
    for u,z in points[1:]:
        lines.append(' .LineTo "%.12g", "%.12g"'%(u,z))
    lines.append(' .LineTo "%.12g", "%.12g"'%(u0,z0))
    lines += [" .Create","End With"]
    return "\n".join(lines)

def ground_points(uc):
    half=GROUND_W/2.0
    z_tip=Z0-L_BAL
    z_full=Z0-V_FULL
    z_bot=Z0-V_BOTTOM
    return [
      (uc,z_tip),
      (uc+half,z_full),
      (uc+half,z_bot),
      (uc-half,z_bot),
      (uc-half,z_full)
    ]

def build(prj):
    code=[]
    for pol in ("A","B"):
        for side,uc in TERMS:
            code.append('Solid.Delete "B0_BackGround:%s_%s_BACK_GND"'%(pol,side))
    for pol in ("A","B"):
        for side,uc in TERMS:
            tag=pol+"_"+side
            code.append(extrude_uz_polygon(
              tag+"_GROUND_TAPER","B1RT1_BackGround","B0_COPPER",
              pol,ground_points(uc),CU_T))
    prj.modeler.add_to_history("AR0-B1R-T1 symmetric backside ground acquisition", "\n".join(code))

def analytic():
    grounds={}
    prongs={}
    for pol in ("A","B"):
        for side,uc in TERMS:
            grounds[(pol,side)]=poly_rect(pol,uc,GROUND_W,-1.035,-1.0)
            if side=="P":
                # B0 prong local u=+1..+5 -> centered +3 width 4
                prongs[(pol,side)]=poly_rect(pol,3.0,4.0,-1.0,0.0)
            else:
                prongs[(pol,side)]=poly_rect(pol,-3.0,4.0,-1.0,0.0)
    gg=[]; gp=[]
    for sa,ua in TERMS:
        for sb,ub in TERMS:
            if overlap2d(grounds[("A",sa)],grounds[("B",sb)]):
                gg.append("A_%s/B_%s"%(sa,sb))
            if overlap2d(grounds[("A",sa)],prongs[("B",sb)]):
                gp.append("A_%s_ground/B_%s_prong"%(sa,sb))
            if overlap2d(grounds[("B",sb)],prongs[("A",sa)]):
                gp.append("B_%s_ground/A_%s_prong"%(sb,sa))
    area_mm2=0.5*GROUND_W*L_TAPER + GROUND_W*(V_BOTTOM-V_FULL)
    return {
      "ground_ground_crosspol_collisions":sorted(set(gg)),
      "ground_opposite_stalk_collisions":sorted(set(gp)),
      "balanced_throat_mm":L_BAL,
      "taper_length_mm":L_TAPER,
      "full_ground_start_v_mm":V_FULL,
      "ground_width_mm":GROUND_W,
      "prong_edge_margin_mm":(4.0-GROUND_W)/2.0,
      "ground_top_gap_to_radiator_mm":L_BAL,
      "expected_ground_planar_area_mm2":area_mm2,
      "expected_ground_volume_mm3":area_mm2*CU_T
    }

def run(evidence,work,parent):
    evidence=Path(evidence); work=Path(work); parent=Path(parent)
    if evidence.exists(): raise RuntimeError("HOLD_B1RT1_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_B1RT1_WORK_EXISTS")
    if not parent.exists() or sha(parent)!=PARENT_SHA:
        raise RuntimeError("HOLD_B1RT1_PARENT_HASH")
    evidence.mkdir(parents=True); work.mkdir(parents=True)

    out=work/"R1E1A4A_AR0_B1R_T1_GROUND_ACQUISITION_BUILD_ONLY_V01.cst"
    shutil.copy2(str(parent),str(out))
    if sha(out)!=PARENT_SHA: raise RuntimeError("HOLD_B1RT1_PARENT_COPY_HASH")

    pre=evidence/"parent_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code(wrap(inv_vba(pre))):
            raise RuntimeError("HOLD_B1RT1_PARENT_INVENTORY")
        build(prj)
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
            raise RuntimeError("HOLD_B1RT1_REOPEN_INVENTORY")
    finally:
        if prj is not None: prj.close()
        de.close()

    pre_rows,prekv=parse_inv(pre); rows,kv=parse_inv(post)
    pre_sig=signature(pre_rows,PRESERVE_COMPONENTS)
    post_sig=signature(rows,PRESERVE_COMPONENTS)
    counts=Counter(r["component"] for r in rows)
    an=analytic()
    tree=solver_tree(out)
    newg=[r for r in rows if r["component"]=="B1RT1_BackGround"]
    target_vol=an["expected_ground_volume_mm3"]
    vol_equal=(len(newg)==4 and max(abs(r["volume"]-target_vol) for r in newg)<1e-8)
    checks={
      "artifact_exists":out.exists(),
      "fresh_reopen_hash_stable":sha(out)==build_sha,
      "shape_count_45":len(rows)==45,
      "all_non_ground_parent_volumes_preserved":pre_sig==post_sig,
      "old_b0_background_count_zero":counts.get("B0_BackGround",0)==0,
      "new_t1_background_count_4":counts.get("B1RT1_BackGround",0)==4,
      "new_ground_volumes_exact_and_c4_equal":vol_equal,
      "all_positive_volume":all(r["volume"]>0 for r in rows),
      "ground_ground_crosspol_collision_zero":len(an["ground_ground_crosspol_collisions"])==0,
      "ground_opposite_stalk_collision_zero":len(an["ground_opposite_stalk_collisions"])==0,
      "balanced_throat_1p5mm":abs(an["balanced_throat_mm"]-1.5)<1e-12,
      "taper_length_3mm":abs(an["taper_length_mm"]-3.0)<1e-12,
      "full_ground_start_4p5mm":abs(an["full_ground_start_v_mm"]-4.5)<1e-12,
      "ground_width_3p6mm":abs(an["ground_width_mm"]-3.6)<1e-12,
      "ground_not_on_radiator":an["ground_top_gap_to_radiator_mm"]>=1.5,
      "port_count_zero":int(kv.get("PORT_COUNT","-1"))==0,
      "solver_tree_empty":len(tree)==0
    }
    status="PASS_R1E1A4A_AR0_B1R_T1_GROUND_ACQUISITION_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_T1_GEOMETRY"
    summary={
      "status":status,"simulationops":"0.2.8",
      "formal_build_invocations":1,"solver_invocations":0,
      "parent":{"path":str(parent),"sha256":PARENT_SHA},
      "artifact":{"path":str(out),"sha256":sha(out)},
      "inventory":{"shape_count":len(rows),"component_counts":dict(counts)},
      "preserved_signature_before":pre_sig,
      "preserved_signature_after":post_sig,
      "analytic_transition_audit":an,
      "new_ground_volumes_mm3":[r["volume"] for r in newg],
      "checks":checks,
      "rf_status":"first-cut transition geometry only; no impedance/mode-conversion qualification"
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# AR0-B1R-T1 Human 3D Review Guide","",
      "Canonical status: "+status,"",
      "Inspect:",
      "1. Hide all but signal traces and RF tenons: confirm no changes from T0.",
      "2. Show only T1 backside ground: confirm a groundless 1.5-mm throat at the top.",
      "3. Inspect each triangular flare from v=1.5 to 4.5 mm.",
      "4. Inspect the 3.60-mm full rail below v=4.5 mm.",
      "5. Show both polarizations together and inspect the central crossing for copper clearance.",
      "6. Show LNA envelopes and verify they sit below the fully-established-ground region.","",
      "Confirm visually:",
      "- no ground reaches the radiator/RF tenons;",
      "- + and - tapers are mirror copies;",
      "- Pol-A and Pol-B are rotational copies;",
      "- no backside copper crosses the orthogonal stalk;",
      "- the taper looks manufacturable as ordinary backside copper.","",
      "No solver is authorized."
    ]
    (evidence/"HUMAN_3D_REVIEW.md").write_text("\n".join(review)+"\n",encoding="utf-8")
    print(status); print("ARTIFACT_SHA256="+sha(out))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--parent-cst",required=True)
    a=ap.parse_args()
    try:
        sys.exit(run(a.evidence,a.work,a.parent_cst))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_T1_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
