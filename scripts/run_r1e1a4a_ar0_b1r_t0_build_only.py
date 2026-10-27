from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from collections import Counter
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

PARENT_SHA="6b2e3edc230b54eef54bdd427e8585a9fee1f0ef0235c747aa1b0ef6571b1dbe"
S2=1.0/math.sqrt(2.0)
Z0=57.1428571428
ZSUBTOP=58.1428571428
ZCUTTOP=58.1978571428
ZTENON=58.7428571428
CU_T=0.035
TENON_W=2.20
MORTISE_W=2.50
MSL_W=1.90
POLS={
 "A":{"u":(S2,S2),"n":(-S2,S2)},
 "B":{"u":(-S2,S2),"n":(-S2,-S2)}
}
TERMS=(("P",3.0),("N",-3.0))
PRESERVE_COMPONENTS=(
 "UnitCellGround",
 "B0_Stalk","B0_MSL","B0_BackGround","B0_LNAEnvelope",
 "B1M_LowerStalk","B1M_UpperRail","B1M_TopTenon","B1M_BottomTenon"
)

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

def poly(pol,uc,w,n1,n2):
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

def signature(rows,components):
    return {r["name"]:round(r["volume"],12) for r in rows if r["component"] in components}

def comp_volume(rows,component):
    return sum(r["volume"] for r in rows if r["component"]==component)

def build(prj):
    code=[r'''
With Material
 .Reset
 .Name "B1RT0_SOLDER_PROXY"
 .Folder ""
 .FrqType "all"
 .Type "Lossy metal"
 .SetMaterialUnit "GHz", "mm"
 .Mue "1.0"
 .Sigma "7000000"
 .Create
End With
''']
    # Remove old signal PTH solids explicitly. CST VBA Solid.Delete is deterministic and supported.
    for pol in ("A","B"):
        for side,uc in TERMS:
            code.append('Solid.Delete "B0_SignalFeedthrough:%s_%s_SIG_FEEDTHROUGH"'%(pol,side))

    for pol,m in POLS.items():
        uv,nv=m["u"],m["n"]
        for side,uc in TERMS:
            tag=pol+"_"+side
            # Enlarge the old tiny feedthrough hole into an RF-tenon mortise in substrate.
            mt=tag+"_RF_MORTISE_SUB"
            code.append(extrude_rect(mt,"B1RT0_Tools","Vacuum",
                                     uc-MORTISE_W/2,uc+MORTISE_W/2,-1.125,0.125,
                                     Z0-0.02,ZSUBTOP+0.02,uv,nv))
            code.append('Solid.Subtract "Substrate:FR4_BOARD", "B1RT0_Tools:%s"'%mt)
            # Matching clearance through top copper so FR4/copper tongue can protrude.
            ct=tag+"_RF_MORTISE_CU"
            code.append(extrude_rect(ct,"B1RT0_Tools","Vacuum",
                                     uc-MORTISE_W/2,uc+MORTISE_W/2,-1.125,0.125,
                                     ZSUBTOP-0.02,ZCUTTOP,uv,nv))
            code.append('Solid.Subtract "TopCopper:TOP_COPPER", "B1RT0_Tools:%s"'%ct)

            # Signal-only FR4 tenon.
            code.append(extrude_rect(tag+"_RF_TENON","B1RT0_RFTenon","FR4_COST_BASELINE",
                                     uc-TENON_W/2,uc+TENON_W/2,-1.0,0.0,
                                     Z0,ZTENON,uv,nv))
            # Existing 1.90-mm MSL continues up the front face of the tenon.
            code.append(extrude_rect(tag+"_RF_TONGUE_CU","B1RT0_TongueCu","B0_COPPER",
                                     uc-MSL_W/2,uc+MSL_W/2,0.0,CU_T,
                                     Z0,ZTENON,uv,nv))
            # Small solder proxy bridges outward from tongue edge to outward radiator-mortise edge.
            if side=="P":
                su1,su2=uc+MSL_W/2,uc+MORTISE_W/2
            else:
                su1,su2=uc-MORTISE_W/2,uc-MSL_W/2
            code.append(extrude_rect(tag+"_SOLDER_BRIDGE","B1RT0_Solder","B1RT0_SOLDER_PROXY",
                                     su1,su2,CU_T,0.125,
                                     ZSUBTOP,ZSUBTOP+0.285,uv,nv))
    prj.modeler.add_to_history("AR0-B1R-T0 replace signal PTH with solderable RF tenons", "\n".join(code))

def analytic():
    tenons={}; mortises={}
    for pol in ("A","B"):
        for side,uc in TERMS:
            tenons[(pol,side)]=poly(pol,uc,TENON_W,-1,0)
            mortises[(pol,side)]=poly(pol,uc,MORTISE_W,-1.125,0.125)
    tenon_hits=[]; mortise_hits=[]
    for sa,ua in TERMS:
        for sb,ub in TERMS:
            if overlap2d(tenons[("A",sa)],tenons[("B",sb)]):
                tenon_hits.append("A_%s/B_%s"%(sa,sb))
            if overlap2d(mortises[("A",sa)],mortises[("B",sb)]):
                mortise_hits.append("A_%s/B_%s"%(sa,sb))
    return {
      "cross_pol_tenon_collisions":tenon_hits,
      "cross_pol_mortise_collisions":mortise_hits,
      "tenon_to_outer_mechanical_keepout_gap_mm":10.5-(3.0+TENON_W/2),
      "ground_to_radiator_gap_mm":3.0,
      "tenon_width_mm":TENON_W,
      "mortise_width_mm":MORTISE_W,
      "stalk_thickness_mm":1.0,
      "tenon_protrusion_above_top_copper_mm":ZTENON-(ZSUBTOP+0.035)
    }

def run(evidence,work,parent):
    evidence=Path(evidence); work=Path(work); parent=Path(parent)
    if evidence.exists(): raise RuntimeError("HOLD_B1RT0_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_B1RT0_WORK_EXISTS")
    if not parent.exists() or sha(parent)!=PARENT_SHA: raise RuntimeError("HOLD_B1RT0_PARENT_HASH")
    evidence.mkdir(parents=True); work.mkdir(parents=True)
    out=work/"R1E1A4A_AR0_B1R_T0_RF_TENON_BUILD_ONLY_V01.cst"
    shutil.copy2(str(parent),str(out))
    if sha(out)!=PARENT_SHA: raise RuntimeError("HOLD_B1RT0_PARENT_COPY_HASH")

    pre=evidence/"parent_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not prj.schematic.execute_vba_code(wrap(inv_vba(pre))):
            raise RuntimeError("HOLD_B1RT0_PARENT_INVENTORY")
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
            raise RuntimeError("HOLD_B1RT0_REOPEN_INVENTORY")
    finally:
        if prj is not None: prj.close()
        de.close()

    pre_rows,prekv=parse_inv(pre); rows,kv=parse_inv(post)
    pre_sig=signature(pre_rows,PRESERVE_COMPONENTS)
    post_sig=signature(rows,PRESERVE_COMPONENTS)
    counts=Counter(r["component"] for r in rows)
    an=analytic()
    tree=solver_tree(out)
    checks={
      "artifact_exists":out.exists(),
      "fresh_reopen_hash_stable":sha(out)==build_sha,
      "shape_count_45":len(rows)==45,
      "preserved_b1m_and_nonfeedthrough_b0_volumes":pre_sig==post_sig,
      "old_signal_feedthrough_count_zero":counts.get("B0_SignalFeedthrough",0)==0,
      "rf_tenon_count_4":counts.get("B1RT0_RFTenon",0)==4,
      "tongue_copper_count_4":counts.get("B1RT0_TongueCu",0)==4,
      "solder_proxy_count_4":counts.get("B1RT0_Solder",0)==4,
      "no_tool_shapes":counts.get("B1RT0_Tools",0)==0,
      "all_positive_volume":all(r["volume"]>0 for r in rows),
      "substrate_volume_decreased":comp_volume(rows,"Substrate")<comp_volume(pre_rows,"Substrate"),
      "top_copper_volume_decreased":comp_volume(rows,"TopCopper")<comp_volume(pre_rows,"TopCopper"),
      "cross_pol_tenon_collision_zero":len(an["cross_pol_tenon_collisions"])==0,
      "cross_pol_mortise_collision_zero":len(an["cross_pol_mortise_collisions"])==0,
      "rf_to_mechanical_keepout_positive":an["tenon_to_outer_mechanical_keepout_gap_mm"]>0,
      "port_count_zero":int(kv.get("PORT_COUNT","-1"))==0,
      "solver_tree_empty":len(tree)==0
    }
    status="PASS_R1E1A4A_AR0_B1R_T0_RF_TENON_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_T0_GEOMETRY"
    summary={
      "status":status,"simulationops":"0.2.8",
      "formal_build_invocations":1,"solver_invocations":0,
      "parent":{"path":str(parent),"sha256":PARENT_SHA},
      "artifact":{"path":str(out),"sha256":sha(out)},
      "inventory":{"shape_count":len(rows),"component_counts":dict(counts)},
      "preserved_signature_before":pre_sig,
      "preserved_signature_after":post_sig,
      "analytic_interface_audit":an,
      "checks":checks,
      "stalk_thickness_status":"1.00 mm retained; 0.80 mm deferred",
      "rf_status":"manufacturable interface geometry only; no impedance qualification"
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# AR0-B1R-T0 Human 3D Review Guide","",
      "Canonical status: "+status,"",
      "Inspect:",
      "1. Hide ground/mechanics; show the four RF tenons and radiator mortises.",
      "2. Show stalk MSL + RF tongue copper; verify continuous visual alignment.",
      "3. Show radiator top copper; inspect the outward solder edge for each terminal.",
      "4. Show solder proxies; verify + terminals bridge outward +u and - terminals outward -u.",
      "5. Show B1M mechanical tenons/interlock to confirm they are unchanged and separated.",
      "6. Show backside ground to confirm no ground climbs onto RF tenons/radiator.","",
      "Questions:",
      "- can a real soldering iron/reflow joint reach the exposed RF tongue?",
      "- is ~0.565 mm exposed tongue height sensible for assembly?",
      "- is the 2.20-mm RF tenon mechanically plausible without dominating the feed gap?",
      "- does the 1.00-mm stalk still look acceptable, or should 0.80 mm be a later sensitivity case?","",
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
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_T0_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
