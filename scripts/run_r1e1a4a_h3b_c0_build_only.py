from __future__ import print_function
import argparse, hashlib, json, os, shutil, sys, traceback
from collections import Counter, defaultdict
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="9e810560fc8fc759a88d4ac5fc39067863a1e078b6f01e6e343b004891201db5"
Z0=57.1428571428
REMOVE_COMPONENTS=("H3A_LNAEnvelope","H3A_RouteEnvelope","H3A_ServiceEnvelope",
                   "H3A_RFTransition","H3A_RFSolder","H3A_StalkRF")
COPPER_COMPONENTS=("UnitCellGround","TopCopper","H3A_HubGround","H3A_Shield","H3A_MechLand")
SOLDER_COMPONENTS=("H3A_MechSolder",)
SOLVER_MARKERS=("meshing successful","adaptive mesh refinement pass","running solver","excitation: port")
BRANCHES={
 "X_POS_NE":{"center":(9.4,0.0,Z0),"map":"XP","host":"H3A_Stalk:X_STALK_BODY"},
 "X_NEG_SW":{"center":(-9.4,0.0,Z0),"map":"XN","host":"H3A_Stalk:X_STALK_BODY"},
 "Y_POS_NW":{"center":(0.0,9.4,Z0),"map":"YP","host":"H3A_Stalk:Y_STALK_BODY"},
 "Y_NEG_SE":{"center":(0.0,-9.4,Z0),"map":"YN","host":"H3A_Stalk:Y_STALK_BODY"},
}

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def vba_wrap(body):
    return "Sub Main()\n"+body+"\nEnd Sub"

def inv_vba(path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
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
      "scanok=Boundary.GetUnitCellScanAngle(th,ph,idir)",
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "SCAN_VALID=" & CStr(scanok)',
      'Print #f, "THETA=" & CStr(th)',
      'Print #f, "PHI=" & CStr(ph)',
      'Print #f, "DS1=" & CStr(Boundary.GetUnitCellDs1)',
      'Print #f, "DS2=" & CStr(Boundary.GetUnitCellDs2)',
      "Close #f",
      "On Error GoTo 0"
    ])

def intersection_vba(path):
    return "\n".join([
      "Dim f As Integer",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(path),
      'Print #f, "COMMAND=CDCheckModelIntersections"',
      'Print #f, "STARTED=TRUE"',
      "Close #f",
      'RunCommand "CDCheckModelIntersections"',
      "f=FreeFile",
      'Open "%s" For Append As #f'%str(path),
      'Print #f, "RETURNED=TRUE"',
      "Close #f"
    ])

def pair_vba(path,new_names,parent_metal):
    lines=["Dim f As Integer","f=FreeFile",'Open "%s" For Output As #f'%str(path)]
    for a in new_names:
        for b in parent_metal:
            lines.append('If Solid.DoTheseGeometricallyIntersect("%s","%s") Then Print #f, "HIT|%s|%s"'%(a,b,a,b))
    lines += ["Close #f"]
    return "\n".join(lines)

def parse_inventory(p):
    rows=[]; status={}
    for line in Path(p).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            _,name,mat,vol=line.split("|",3)
            rows.append({"name":name,"component":name.split(":",1)[0],
                         "material":mat.split("=",1)[1],
                         "volume":float(vol.split("=",1)[1])})
        elif "=" in line:
            k,v=line.split("=",1); status[k]=v
    return rows,status

def solver_tree(cst):
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
    return [x for x in p3.get_tree_items() if
            ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def solver_log_hits(cst):
    q=Path(os.path.splitext(str(cst))[0])/"Result"/"output.txt"
    if not q.exists(): return []
    low=q.read_text(encoding="utf-8",errors="ignore").lower()
    return [x for x in SOLVER_MARKERS if x in low]

def material_vba():
    return r'''
With Material
 .Reset
 .Name "H3B_COPPER"
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
 .Name "H3B_SOLDER_PROXY"
 .Folder ""
 .FrqType "all"
 .Type "Lossy metal"
 .SetMaterialUnit "GHz", "mm"
 .Mue "1.0"
 .Sigma "7000000"
 .Create
End With
'''

def map_pt(kind,x,y,z):
    if kind=="XP": return (9.4+x, y, Z0+z)
    if kind=="XN": return (-9.4+x, -y, Z0+z)
    if kind=="YP": return (-y, 9.4+x, Z0+z)
    if kind=="YN": return (y, -9.4+x, Z0+z)
    raise ValueError(kind)

def box_global(kind,xr,yr,zr):
    pts=[map_pt(kind,x,y,z) for x in xr for y in yr for z in zr]
    return ((min(p[0] for p in pts),max(p[0] for p in pts)),
            (min(p[1] for p in pts),max(p[1] for p in pts)),
            (min(p[2] for p in pts),max(p[2] for p in pts)))

def brick(name,comp,mat,b):
    xr,yr,zr=b
    return '''With Brick
 .Reset
 .Name "%s"
 .Component "%s"
 .Material "%s"
 .Xrange "%.12g", "%.12g"
 .Yrange "%.12g", "%.12g"
 .Zrange "%.12g", "%.12g"
 .Create
End With'''%(name,comp,mat,xr[0],xr[1],yr[0],yr[1],zr[0],zr[1])

def cyl(name,comp,mat,outer,inner,axis,rng,c1,c2):
    if axis=="z":
        coords='.Zrange "%.12g", "%.12g"\n .Xcenter "%.12g"\n .Ycenter "%.12g"'%(rng[0],rng[1],c1,c2)
    elif axis=="y":
        coords='.Yrange "%.12g", "%.12g"\n .Xcenter "%.12g"\n .Zcenter "%.12g"'%(rng[0],rng[1],c1,c2)
    elif axis=="x":
        coords='.Xrange "%.12g", "%.12g"\n .Ycenter "%.12g"\n .Zcenter "%.12g"'%(rng[0],rng[1],c1,c2)
    else:
        raise ValueError(axis)
    return '''With Cylinder
 .Reset
 .Name "%s"
 .Component "%s"
 .Material "%s"
 .OuterRadius "%.12g"
 .InnerRadius "%.12g"
 .Axis "%s"
 %s
 .Segments "0"
 .Create
End With'''%(name,comp,mat,outer,inner,axis,coords)

def mapped_cylinder(kind,name,comp,mat,outer,inner,local_axis,lo,hi,x,y,z):
    p0=map_pt(kind,x,y,z)
    if local_axis=="z":
        p1=map_pt(kind,x,y,hi); p2=map_pt(kind,x,y,lo)
    elif local_axis=="y":
        p1=map_pt(kind,x,hi,z); p2=map_pt(kind,x,lo,z)
    else:
        raise ValueError(local_axis)
    dif=[abs(p1[i]-p2[i]) for i in range(3)]
    gi=dif.index(max(dif))
    axis=("x","y","z")[gi]
    rng=(min(p1[gi],p2[gi]),max(p1[gi],p2[gi]))
    if axis=="z": c1,c2=p0[0],p0[1]
    elif axis=="y": c1,c2=p0[0],p0[2]
    else: c1,c2=p0[1],p0[2]
    return cyl(name,comp,mat,outer,inner,axis,rng,c1,c2)

def branch_vba(branch,meta):
    k=meta["map"]; pref=branch
    L="H3B_T01Line"; BG="H3B_T01BackGround"; T="H3B_T01Transition"
    E="H3B_T01EdgeCap"; S="H3B_T01Solder"; V="H3B_T01Via"; Tools="H3B_Tools"
    out=[]
    # uniform controlled-line slices to the 3-mm handoff
    for suffix,xr in (("SIG",(-.75,.75)),("GND_L",(-3.35,-1.15)),("GND_R",(1.15,3.35))):
        out.append(brick(pref+"_H_"+suffix,L,"H3B_COPPER",box_global(k,xr,(1.8,3.0),(-.035,0))))
        out.append(brick(pref+"_V_"+suffix,L,"H3B_COPPER",box_global(k,xr,(.5,.535),(-3.0,-1.5))))
    out.append(brick(pref+"_H_BACK",BG,"H3B_COPPER",box_global(k,(-4,4),(1.8,3.0),(1,1.035))))
    out.append(brick(pref+"_V_BACK",BG,"H3B_COPPER",box_global(k,(-4,4),(-.535,-.5),(-3.0,-1.5))))
    # frozen local transition
    pads=(("SIG",(-1,1)),("GND_L",(-3.7,-1.3)),("GND_R",(1.3,3.7)))
    for suffix,xr in pads:
        out.append(brick(pref+"_H_PAD_"+suffix,T,"H3B_COPPER",box_global(k,xr,(.5,1.8),(-.035,0))))
        out.append(brick(pref+"_V_PAD_"+suffix,T,"H3B_COPPER",box_global(k,xr,(.5,.535),(-1.5,-.035))))
        out.append(brick(pref+"_EDGE_"+suffix,E,"H3B_COPPER",box_global(k,xr,(-.5,.5),(-.035,0))))
        out.append(brick(pref+"_SOLDER_"+suffix,S,"H3B_SOLDER_PROXY",box_global(k,xr,(.535,1.0),(-.45,-.035))))
    # first frozen via station only
    for side,x in (("L",-2.3),("R",2.3)):
        hhole=pref+"_H_VIAHOLE_"+side
        out.append(mapped_cylinder(k,hhole,Tools,"Vacuum",.2,0,"z",-0.02,1.02,x,3.0,0))
        out.append('Solid.Subtract "Substrate:FR4_BOARD", "%s:%s"'%(Tools,hhole))
        out.append(mapped_cylinder(k,pref+"_H_VIA_"+side,V,"H3B_COPPER",.2,.15,"z",0,1,x,3.0,0))
        vhole=pref+"_V_VIAHOLE_"+side
        out.append(mapped_cylinder(k,vhole,Tools,"Vacuum",.2,0,"y",-0.52,.52,x,0,-3.0))
        out.append('Solid.Subtract "%s", "%s:%s"'%(meta["host"],Tools,vhole))
        out.append(mapped_cylinder(k,pref+"_V_VIA_"+side,V,"H3B_COPPER",.2,.15,"y",-0.5,.5,x,0,-3.0))
    return "\n".join(out)

def strip_and_physicalize(prj,inventory_path):
    ok=prj.schematic.execute_vba_code(vba_wrap(inv_vba(inventory_path)))
    if not ok: raise RuntimeError("HOLD_C0_SOURCE_INVENTORY_FAILED")
    rows,_=parse_inventory(inventory_path)
    changes=[material_vba()]
    for c in REMOVE_COMPONENTS:
        changes.append('On Error Resume Next\nComponent.Delete "%s"\nOn Error GoTo 0'%c)
    for r in rows:
        c=r["component"]; n=r["name"]
        if c in COPPER_COMPONENTS:
            changes.append('Solid.ChangeMaterial "%s", "H3B_COPPER"'%n)
        elif c in SOLDER_COMPONENTS:
            changes.append('Solid.ChangeMaterial "%s", "H3B_SOLDER_PROXY"'%n)
    prj.modeler.add_to_history("H3B-C0 strip placeholders and physicalize", "\n".join(changes))

def audit_one(cst,evidence,label,expected_count,require_t01):
    inv=evidence/(label+"_reopen_inventory.txt")
    ist=evidence/(label+"_intersection_status.txt")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(cst))
        ok1=prj.schematic.execute_vba_code(vba_wrap(inv_vba(inv)))
        ok2=prj.schematic.execute_vba_code(vba_wrap(intersection_vba(ist)))
    finally:
        if prj is not None: prj.close()
        de.close()
    rows,st=parse_inventory(inv)
    counts=Counter(r["component"] for r in rows)
    mats=Counter(r["material"] for r in rows)
    names=[r["name"] for r in rows]
    forbidden=[n for n in names if n.split(":",1)[0] in REMOVE_COMPONENTS]
    tools=[n for n in names if n.startswith("H3B_Tools:")]
    branch_counts={}
    c4_ok=True
    if require_t01:
        volsets=[]
        for b in BRANCHES:
            rr=[r for r in rows if r["name"].split(":",1)[-1].startswith(b+"_")]
            branch_counts[b]=len(rr)
            volsets.append(sorted(round(r["volume"],10) for r in rr))
        c4_ok=(len(set(tuple(v) for v in volsets))==1 and all(x==24 for x in branch_counts.values()))
    checks={
      "shape_count_exact":len(rows)==expected_count,
      "all_volumes_positive":all(r["volume"]>0 for r in rows),
      "forbidden_components_absent":not forbidden,
      "no_tools_remaining":not tools,
      "port_count_zero":int(st.get("PORT_COUNT","-1"))==0,
      "unitcell_94":abs(float(st.get("DS1","0"))-94)<1e-6 and abs(float(st.get("DS2","0"))-94)<1e-6,
      "broadside":abs(float(st.get("THETA","999")))<1e-9,
      "no_solver_tree":len(solver_tree(cst))==0,
      "no_solver_markers":len(solver_log_hits(cst))==0,
      "intersection_command_returned":Path(ist).exists() and "RETURNED=TRUE" in Path(ist).read_text(encoding="utf-8"),
      "c4_branch_volume_equivalence":c4_ok,
    }
    return rows,counts,mats,branch_counts,checks

def run(repo,evidence,work,source):
    repo=Path(repo); evidence=Path(evidence); work=Path(work); source=Path(source)
    if evidence.exists(): raise RuntimeError("HOLD_C0_EVIDENCE_EXISTS")
    if work.exists(): raise RuntimeError("HOLD_C0_WORK_EXISTS")
    if not source.exists() or sha(source)!=SOURCE_SHA: raise RuntimeError("HOLD_C0_PARENT_HASH")
    evidence.mkdir(parents=True); work.mkdir(parents=True)
    A=work/"R1E1A4A_H3B_C0_H3A_MECH_ONLY_PHYSICALIZED_BUILD_ONLY_V01.cst"
    B=work/"R1E1A4A_H3B_C0_COMPLETE_PASSIVE_V1_BUILD_ONLY_V01.cst"
    shutil.copy2(str(source),str(A))
    if sha(A)!=SOURCE_SHA: raise RuntimeError("HOLD_C0_PARENT_COPY_HASH")
    source_inv=evidence/"source_inventory.txt"

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(A))
        strip_and_physicalize(prj,source_inv)
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    A_pre=sha(A)
    Arows,Acounts,Amats,Abranches,Achecks=audit_one(A,evidence,"A",66,False)
    Achecks["reopen_hash_stable"]=sha(A)==A_pre
    Achecks["copper_count_39"]=Amats.get("H3B_COPPER",0)==39
    Achecks["solder_count_16"]=Amats.get("H3B_SOLDER_PROXY",0)==16
    if not all(Achecks.values()):
        summary={"status":"HOLD_R1E1A4A_H3B_C0_A_BUILD","A_checks":Achecks,
                 "A_counts":dict(Acounts),"A_materials":dict(Amats),"A_sha256":sha(A)}
        (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
        (evidence/"FINAL_STATUS.txt").write_text(summary["status"]+"\n")
        print(summary["status"]); return 3

    shutil.copy2(str(A),str(B))
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(B))
        code=[material_vba()]
        for b,m in BRANCHES.items(): code.append(branch_vba(b,m))
        prj.modeler.add_to_history("H3B-C0 four local T01-A integration slices", "\n".join(code))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    B_pre=sha(B)
    Brows,Bcounts,Bmats,Bbranches,Bchecks=audit_one(B,evidence,"B",162,True)
    Bchecks["reopen_hash_stable"]=sha(B)==B_pre
    Bchecks["copper_count_123"]=Bmats.get("H3B_COPPER",0)==123
    Bchecks["solder_count_28"]=Bmats.get("H3B_SOLDER_PROXY",0)==28

    # Targeted new-T01 versus pre-existing physical metal intersection sentinel.
    new_names=[r["name"] for r in Brows if r["component"].startswith("H3B_T01")]
    parent_metal=[r["name"] for r in Brows if r["component"] in
                  ("UnitCellGround","TopCopper","H3A_HubGround","H3A_Shield","H3A_MechLand","H3A_MechSolder")]
    pairlog=evidence/"B_new_vs_parent_metal_intersections.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(B))
        ok=prj.schematic.execute_vba_code(vba_wrap(pair_vba(pairlog,new_names,parent_metal)))
    finally:
        if prj is not None: prj.close()
        de.close()
    hits=[x for x in pairlog.read_text(encoding="utf-8").splitlines() if x.startswith("HIT|")] if pairlog.exists() else []
    Bchecks["targeted_intersection_query_returned"]=bool(ok)
    Bchecks["no_new_vs_parent_metal_intersection"]=len(hits)==0

    status="PASS_R1E1A4A_H3B_C0_COMPLETE_PASSIVE_BUILD_ONLY" if all(Bchecks.values()) else "HOLD_R1E1A4A_H3B_C0_GEOMETRY"
    summary={
      "status":status,"simulationops":"0.2.8","solver_run":False,
      "parent":{"path":str(source),"sha256":SOURCE_SHA},
      "A":{"path":str(A),"sha256":sha(A),"shape_count":len(Arows),"component_counts":dict(Acounts),
           "material_counts":dict(Amats),"checks":Achecks},
      "B":{"path":str(B),"sha256":sha(B),"shape_count":len(Brows),"component_counts":dict(Bcounts),
           "material_counts":dict(Bmats),"branch_shape_counts":Bbranches,"checks":Bchecks,
           "new_vs_parent_metal_intersection_hits":hits},
      "frozen_handoff_mm":3.0,
      "formal_build_invocations":1,
      "solve_invocations":0
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n")
    q=["# H3B-C0 Build Qualification","", "Canonical status: "+status+".","",
       "A: "+str(A),"A SHA256: "+sha(A),"",
       "B: "+str(B),"B SHA256: "+sha(B),"",
       "Solver invocations: 0.",""]
    if hits:
        q += ["Targeted new-T01 versus parent-metal intersections require review:"]+["- "+x for x in hits]
    else:
        q += ["No targeted new-T01 versus parent-metal intersection was reported by CST."]
    q += ["","Human 3D review remains mandatory before any I01 solve."]
    (evidence/"QUALIFICATION.md").write_text("\n".join(q)+"\n",encoding="utf-8")
    print(status)
    print("A_SHA256="+sha(A))
    print("B_SHA256="+sha(B))
    print("INTERSECTION_HITS="+str(len(hits)))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-cst",required=True)
    a=ap.parse_args()
    try:
        sys.exit(run(a.repo,a.evidence,a.work,a.source_cst))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_H3B_C0_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
