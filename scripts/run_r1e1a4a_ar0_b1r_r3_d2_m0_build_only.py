from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

PARENT_SHA="fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e"
S2=1.0/math.sqrt(2.0)
Z0=57.1428571428
CU_T=0.035
V_TOP=12.0
V_TAPER_END=13.0
V_RAIL_END=40.0
W_TOP=3.60
W_LOWER=3.20
BRIDGE_U=1.40
A_BRIDGE_V=(33.80,34.30)
B_BRIDGE_V=(34.85,35.35)
SPLIT=22.5714285714
A_SLOT_ZMAX=SPLIT+0.02
B_SLOT_ZMIN=SPLIT-0.02
POLS={
 "A":{"u":(S2,S2),"n":(-S2,S2),"height":-CU_T},
 "B":{"u":(-S2,S2),"n":(-S2,-S2),"height":CU_T}
}
TERMS=(("P",3.0),("N",-3.0))
D2_NAMES=tuple(
 ["D2M0_BackGround:%s_%s_LOWER_RAIL"%(p,s) for p in ("A","B") for s,_ in TERMS] +
 ["D2M0_BackGround:A_COMMON_BRIDGE","D2M0_BackGround:B_COMMON_BRIDGE"]
)
FIXTURE_KEEP=(
 "B0_Stalk:A_P_PRONG","B0_Stalk:A_N_PRONG",
 "B0_MSL:A_P_MSL","B0_MSL:A_N_MSL",
 "B1RT1R1_BackGround:A_P_GROUND_TAPER","B1RT1R1_BackGround:A_N_GROUND_TAPER",
 "B1M_LowerStalk:A_LOWER_BODY",
 "D2M0_BackGround:A_P_LOWER_RAIL","D2M0_BackGround:A_N_LOWER_RAIL",
 "D2M0_BackGround:A_COMMON_BRIDGE",
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
    if s is None or e is None or e<=s: raise RuntimeError("HOLD_D2M0_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def inv_vba(path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(path).replace("\\","/"),
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
                if ("S-Parameters" in x or "Convergence" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+str(ex)]

def signature(rows,exclude_component=None):
    return {r["name"]:(r["material"],round(r["volume"],12))
            for r in rows if r["component"]!=exclude_component}

def extrude_uz_polygon(name,comp,mat,pol,points):
    uv=POLS[pol]["u"]; nv=POLS[pol]["n"]; height=POLS[pol]["height"]
    # Same handedness-aware backside rule proven in T1R1.
    x0,y0=-nv[0],-nv[1]
    lines=[
      "With Extrude",' .Reset',' .Name "%s"'%name,' .Component "%s"'%comp,
      ' .Material "%s"'%mat,' .Mode "Pointlist"',' .Height "%.12g"'%height,
      ' .Twist "0.0"',' .Taper "0.0"',
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

def z_from_v(v): return Z0-v

def lower_rail_points(uc):
    t1=uc-W_TOP/2.0; t2=uc+W_TOP/2.0
    l1=uc-W_LOWER/2.0; l2=uc+W_LOWER/2.0
    z12=z_from_v(V_TOP); z13=z_from_v(V_TAPER_END); zend=z_from_v(V_RAIL_END)
    return [(t1,z12),(t2,z12),(l2,z13),(l2,zend),(l1,zend),(l1,z13)]

def bridge_points(v1,v2):
    z1=z_from_v(v1); z2=z_from_v(v2)
    zlo=min(z1,z2); zhi=max(z1,z2)
    return [(-BRIDGE_U,zlo),(BRIDGE_U,zlo),(BRIDGE_U,zhi),(-BRIDGE_U,zhi)]

def add_d2(prj):
    code=[]
    for pol in ("A","B"):
        for side,uc in TERMS:
            code.append(extrude_uz_polygon("%s_%s_LOWER_RAIL"%(pol,side),
                                           "D2M0_BackGround","B0_COPPER",
                                           pol,lower_rail_points(uc)))
    code.append(extrude_uz_polygon("A_COMMON_BRIDGE","D2M0_BackGround","B0_COPPER","A",bridge_points(*A_BRIDGE_V)))
    code.append(extrude_uz_polygon("B_COMMON_BRIDGE","D2M0_BackGround","B0_COPPER","B",bridge_points(*B_BRIDGE_V)))
    prj.modeler.add_to_history("AR0-B1R-R3-D2-M0 supported lower-stalk ground merge","\n".join(code))

def run_vba_project(path,body,save=False):
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(path))
        ok=p.schematic.execute_vba_code(wrap(body))
        if save: p.save()
        return ok
    finally:
        if p is not None: p.close()
        de.close()

def destructive_overlap_audit(source,work,evidence,target_mode):
    tmp=work/("D2M0_%s_overlap_probe.cst"%target_mode)
    if tmp.exists(): tmp.unlink()
    shutil.copy2(str(source),str(tmp))
    out=evidence/("D2M0_%s_overlap.txt"%target_mode)
    pairs=[]
    for pol in ("A","B"):
        own="B1M_LowerStalk:%s_LOWER_BODY"%pol
        opp="B1M_LowerStalk:%s_LOWER_BODY"%("B" if pol=="A" else "A")
        for side,_ in TERMS:
            g="D2M0_BackGround:%s_%s_LOWER_RAIL"%(pol,side)
            pairs.append((pol+"_"+side,g,own if target_mode=="own_fr4" else opp))
        g="D2M0_BackGround:%s_COMMON_BRIDGE"%pol
        pairs.append((pol+"_BRIDGE",g,own if target_mode=="own_fr4" else opp))
    lines=["Dim f As Integer","f=FreeFile",'Open "%s" For Output As #f'%str(out).replace("\\","/")]
    for tag,g,t in pairs:
        lines += [
          'Solid.Intersect "%s", "%s"'%(g,t),
          "On Error Resume Next",
          'Print #f, "%s_AFTER=" & CStr(Solid.GetVolume("%s"))'%(tag,g),
          "If Err.Number <> 0 Then",
          " Err.Clear",
          ' Print #f, "%s_INTERSECTION=0"'%tag,
          "End If",
          "On Error GoTo 0"
        ]
    lines += ["Close #f"]
    try: run_vba_project(tmp,"\n".join(lines),False)
    except Exception: pass
    txt=out.read_text(encoding="utf-8") if out.exists() else ""
    flags={tag:("%s_INTERSECTION=0"%tag) in txt for tag,_,__ in pairs}
    return flags,txt

def delete_nonkeep(rows,keep):
    return "\n".join('Solid.Delete "%s"'%r["name"] for r in rows if r["name"] not in keep)

def analytic():
    a_slot_end_v=Z0-A_SLOT_ZMAX
    b_slot_end_v=Z0-B_SLOT_ZMIN
    return {
      "lower_rail_width_mm":W_LOWER,
      "lower_rail_inner_edges_mm":[-1.40,1.40],
      "closest_slot_edges_mm":[-1.125,1.125],
      "minimum_planar_rail_to_slot_clearance_mm":1.40-1.125,
      "A_bridge_v_mm":list(A_BRIDGE_V),
      "B_bridge_v_mm":list(B_BRIDGE_V),
      "A_slot_boundary_v_mm":a_slot_end_v,
      "B_slot_boundary_v_mm":b_slot_end_v,
      "A_bridge_to_slot_clearance_mm":a_slot_end_v-A_BRIDGE_V[1],
      "B_bridge_to_slot_clearance_mm":B_BRIDGE_V[0]-b_slot_end_v,
      "bridge_width_u_mm":2*BRIDGE_U,
      "bridge_length_v_mm":A_BRIDGE_V[1]-A_BRIDGE_V[0],
      "rail_expected_volume_mm3":(((W_TOP+W_LOWER)/2.0)*(V_TAPER_END-V_TOP)+W_LOWER*(V_RAIL_END-V_TAPER_END))*CU_T,
      "bridge_expected_volume_mm3":(2*BRIDGE_U)*(A_BRIDGE_V[1]-A_BRIDGE_V[0])*CU_T,
      "ground_to_reflector_min_z_mm":z_from_v(V_RAIL_END),
      "no_via":True
    }

def build_canonical(parent,out,evidence):
    shutil.copy2(str(parent),str(out))
    pre=evidence/"canonical_parent_inventory.txt"
    post=evidence/"canonical_reopen_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inv_vba(pre))): raise RuntimeError("HOLD_D2M0_PARENT_INV")
        add_d2(p); p.save()
    finally:
        if p is not None: p.close()
        de.close()
    build_sha=sha(out)
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inv_vba(post))): raise RuntimeError("HOLD_D2M0_REOPEN_INV")
    finally:
        if p is not None: p.close()
        de.close()
    return build_sha,parse_inv(pre),parse_inv(post)

def build_fixture(canonical,out,evidence,port_macro):
    shutil.copy2(str(canonical),str(out))
    pre=evidence/"fixture_parent_inventory.txt"
    post=evidence/"fixture_reopen_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inv_vba(pre))): raise RuntimeError("HOLD_D2M0_FIX_PARENT_INV")
        rows,_=parse_inv(pre)
        p.modeler.add_to_history("D2-M0A exact Pol-A supported-merge fixture",delete_nonkeep(rows,FIXTURE_KEEP))
        p.modeler.add_to_history("D2-M0A inherited corrected 100/50/50 ports",macro_body(port_macro))
        p.save()
    finally:
        if p is not None: p.close()
        de.close()
    build_sha=sha(out)
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inv_vba(post))): raise RuntimeError("HOLD_D2M0_FIX_REOPEN_INV")
    finally:
        if p is not None: p.close()
        de.close()
    return build_sha,parse_inv(pre),parse_inv(post),solver_tree(out)

def main(parent,work,evidence,port_macro):
    parent=Path(parent); work=Path(work); evidence=Path(evidence); port_macro=Path(port_macro)
    if evidence.exists(): raise RuntimeError("HOLD_D2M0_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_D2M0_WORK_EXISTS")
    if not parent.exists() or sha(parent)!=PARENT_SHA: raise RuntimeError("HOLD_D2M0_PARENT_HASH")
    if not port_macro.exists(): raise RuntimeError("HOLD_D2M0_PORT_MACRO")
    evidence.mkdir(parents=True); work.mkdir(parents=True)

    canonical=work/"R1E1A4A_AR0_B1R_R3_D2_M0_MANUFACTURABLE_GROUND_MERGE_BUILD_ONLY_V01.cst"
    csha,(pre_rows,prekv),(post_rows,postkv)=build_canonical(parent,canonical,evidence)
    an=analytic()
    new=[r for r in post_rows if r["component"]=="D2M0_BackGround"]
    rails=[r for r in new if r["name"].endswith("_LOWER_RAIL")]
    bridges=[r for r in new if r["name"].endswith("_COMMON_BRIDGE")]
    pre_sig=signature(pre_rows,"D2M0_BackGround"); post_sig=signature(post_rows,"D2M0_BackGround")
    own_flags,_=destructive_overlap_audit(canonical,work,evidence,"own_fr4")
    opp_flags,_=destructive_overlap_audit(canonical,work,evidence,"opposite_stalk")

    fixture=work/"R1E1A4A_AR0_B1R_R3_D2_M0A_RF_FIXTURE_BUILD_ONLY_V01.cst"
    fsha,(fpre,fprekv),(fpost,fpostkv),ftree=build_fixture(canonical,fixture,evidence,port_macro)

    rail_vol=an["rail_expected_volume_mm3"]; bridge_vol=an["bridge_expected_volume_mm3"]
    checks={
      "parent_hash_exact":sha(parent)==PARENT_SHA,
      "canonical_hash_stable":sha(canonical)==csha,
      "parent_geometry_preserved":pre_sig==post_sig,
      "new_d2_shape_count_6":len(new)==6,
      "new_lower_rail_count_4":len(rails)==4,
      "new_bridge_count_2":len(bridges)==2,
      "lower_rail_volumes_exact":len(rails)==4 and max(abs(r["volume"]-rail_vol) for r in rails)<1e-8,
      "bridge_volumes_exact":len(bridges)==2 and max(abs(r["volume"]-bridge_vol) for r in bridges)<1e-8,
      "all_new_copper_positive":all(r["volume"]>0 for r in new),
      "own_fr4_overlap_zero_all":all(own_flags.values()),
      "opposite_stalk_overlap_zero_all":all(opp_flags.values()),
      "rail_to_slot_clearance_ge_0p25mm":an["minimum_planar_rail_to_slot_clearance_mm"]>=0.25,
      "A_bridge_supported_clearance_ge_0p25mm":an["A_bridge_to_slot_clearance_mm"]>=0.25,
      "B_bridge_supported_clearance_ge_0p25mm":an["B_bridge_to_slot_clearance_mm"]>=0.25,
      "ground_stops_above_reflector":an["ground_to_reflector_min_z_mm"]>0,
      "canonical_port_count_zero":int(postkv.get("PORT_COUNT","-1"))==0,
      "canonical_result_tree_empty":len(solver_tree(canonical))==0,
      "fixture_hash_stable":sha(fixture)==fsha,
      "fixture_shape_count_10":len(fpost)==10,
      "fixture_exact_keep_names":set(r["name"] for r in fpost)==set(FIXTURE_KEEP),
      "fixture_port_count_3":int(fpostkv.get("PORT_COUNT","-1"))==3,
      "fixture_result_tree_empty":len(ftree)==0
    }
    status="PASS_R1E1A4A_AR0_B1R_R3_D2_M0_MANUFACTURABLE_GROUND_MERGE_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_R3_D2_M0_BUILD"
    summary={
      "status":status,"simulationops":"0.2.8","formal_build_products":2,"solver_invocations":0,
      "parent":{"path":str(parent),"sha256":PARENT_SHA},
      "canonical":{"path":str(canonical),"sha256":sha(canonical),"shape_count":len(post_rows)},
      "fixture_A":{"path":str(fixture),"sha256":sha(fixture),"shape_count":len(fpost),"port_count":int(fpostkv.get("PORT_COUNT","-1"))},
      "analytic":an,
      "own_fr4_overlap_zero":own_flags,
      "opposite_stalk_overlap_zero":opp_flags,
      "new_copper_volumes_mm3":{r["name"]:r["volume"] for r in new},
      "checks":checks
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    (evidence/"HUMAN_3D_REVIEW.md").write_text(
      "# D2-M0 Manufacturable Ground-Merge Review\n\n"
      "Status: "+status+"\n\n"
      "Inspect full dual-pol canonical artifact.\n"
      "1. Highlight D2M0_BackGround only.\n"
      "2. At v=12..13 mm verify each 3.60-mm T1R1 rail narrows smoothly to 3.20 mm.\n"
      "3. Inspect A bridge at v=33.80..34.30 mm: it must sit on intact FR4 above the A half-lap slot.\n"
      "4. Inspect B bridge at v=34.85..35.35 mm: it must sit on intact FR4 below the B half-lap slot.\n"
      "5. Show the orthogonal stalk together: no D2 copper may enter the other PCB.\n"
      "6. Verify feed/LNA head, radiator tenons and reflector tenons are unchanged.\n\n"
      "This stage contains no via and no solver result.\n",encoding="utf-8")
    print(status)
    print("CANONICAL_SHA256="+sha(canonical))
    print("FIXTURE_A_SHA256="+sha(fixture))
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
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R3_D2_M0_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
