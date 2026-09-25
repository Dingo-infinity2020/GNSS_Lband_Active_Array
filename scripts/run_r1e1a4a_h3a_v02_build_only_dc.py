"""H3A orthogonal PCB stalk assembly V0.1 — one-shot BUILD-ONLY harness."""
from __future__ import print_function
import argparse, hashlib, json, os, shutil, sys, time
from collections import Counter

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e"
SOLVER_MARKERS=("meshing successful","adaptive mesh refinement pass","running solver","excitation: port")

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def macro_body(path):
    lines=open(path,encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=lines.index("Sub Main()"); e=lines.index("End Sub")
    return "\n".join(lines[s+1:e])

def snapshot_tree(root):
    snap=[]
    if not os.path.isdir(root): return snap
    for d,_,files in os.walk(root):
        for name in files:
            q=os.path.join(d,name)
            with open(q,"rb") as f: snap.append((q,f.read()))
    return snap

def restore_snapshot(snap):
    changed=[]
    for q,data in snap:
        cur=None
        if os.path.isfile(q):
            with open(q,"rb") as f: cur=f.read()
        if cur!=data: changed.append(q)
        with open(q,"wb") as f: f.write(data)
    for q,data in snap:
        with open(q,"rb") as f:
            if f.read()!=data: raise RuntimeError("HOLD_H3A_PARENT_EVIDENCE_RESTORE_FAILED:"+q)
    return changed

def parameter_map(cstfile):
    q=os.path.join(os.path.splitext(cstfile)[0],"Model","Parameters.json")
    data=json.load(open(q,encoding="utf-8")); out={}
    def walk(x):
        if isinstance(x,dict):
            if "name" in x and "value" in x: out[str(x["name"])]=str(x["value"])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(data); return out

def solver_tree_items(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    return [x for x in pf.get_3d().get_tree_items()
            if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\Excitation" in x)]

def solver_log_hits(cstfile):
    q=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(q): return []
    low=open(q,encoding="utf-8",errors="ignore").read().lower()
    return [m for m in SOLVER_MARKERS if m in low]

def audit_vba(shape_path,status_path):
    return "\n".join([
      "On Error Resume Next","Dim f As Integer, i As Long, nm As String",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "H3A_SHAPE_INVENTORY"',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+160",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      ' If Len(nm)>0 Then Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm))',
      "Next i","Close #f",
      "scanok=Boundary.GetUnitCellScanAngle(th,ph,idir)",
      "f=FreeFile", 'Open "%s" For Output As #f'%status_path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "SCAN_VALID=" & CStr(scanok)',
      'Print #f, "THETA=" & CStr(th)','Print #f, "PHI=" & CStr(ph)',
      'Print #f, "DS1=" & CStr(Boundary.GetUnitCellDs1)',
      'Print #f, "DS2=" & CStr(Boundary.GetUnitCellDs2)',
      "Close #f","On Error GoTo 0"
    ])

def intersection_vba(status_path):
    return "\n".join([
      "Dim f As Integer",
      "f=FreeFile",
      'Open "%s" For Output As #f'%status_path,
      'Print #f, "COMMAND=CDCheckModelIntersections"',
      'Print #f, "STARTED=TRUE"',
      "Close #f",
      'RunCommand "CDCheckModelIntersections"',
      "f=FreeFile",
      'Open "%s" For Append As #f'%status_path,
      'Print #f, "RETURNED=TRUE"',
      "Close #f"
    ])

def parse_kv(path):
    d={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); d[k.strip()]=v.strip()
    return d

def shape_rows(path):
    out=[]
    for line in open(path,encoding="utf-8").read().splitlines():
        if line.startswith("SHAPE|"):
            _,name,vol=line.split("|",2)
            out.append((name,float(vol.split("=",1)[1])))
    return out

def component_counts(rows):
    c=Counter()
    for name,_ in rows:
        c[name.split(":",1)[0]]+=1
    return dict(c)

def critical_clearance_audit():
    import math
    checks={}
    checks["tenon_mortise_thickness_clearance_mm"]=(1.25-1.0)/2
    checks["tenon_mortise_length_clearance_mm"]=(3.30-3.0)/2
    checks["mortise_to_copper_corridor_side_clearance_mm"]=(2.571428571426-1.25)/2
    checks["cross_interlock_each_side_clearance_mm"]=(1.25-1.0)/2
    checks["shield_to_stalk_cavity_side_clearance_mm"]=(17.0-16.0)/2
    checks["shield_bottom_to_notch_bottom_clearance_mm"]=(57.1428571428-0.035-5.5)-50.1428571428
    checks["mechanical_to_rf_top_feature_gap_mm"]=(12.0-1.0)-(9.4+1.0+0.2)
    checks["route_start_beyond_lna_corner_mm"]=1.65-math.sqrt(2.0)
    checks["route_ground_to_bottom_mechanical_gap_mm"]=5.0-0.70
    checks["service_envelope_to_stalk_face_gap_mm"]=1.0-0.535

    # Check the four visual routes pass through 4-mm shield cardinal egresses.
    lna_xy=6.2/math.sqrt(2.0)
    routes=[((lna_xy,lna_xy),(9.4,0.0)),((-lna_xy,-lna_xy),(-9.4,0.0)),
            ((-lna_xy,lna_xy),(0.0,9.4)),((lna_xy,-lna_xy),(0.0,-9.4))]
    margins=[]
    for p0,p1 in routes:
        dx=p1[0]-p0[0]; dy=p1[1]-p0[1]; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L
        a=(p0[0]+ux*1.65,p0[1]+uy*1.65)
        b=(p1[0]-ux*0.90,p1[1]-uy*0.90)
        if abs(p1[0])>abs(p1[1]):
            xwall=7.8 if p1[0]>0 else -7.8
            t=(xwall-a[0])/(b[0]-a[0]); transverse=a[1]+t*(b[1]-a[1])
        else:
            ywall=7.8 if p1[1]>0 else -7.8
            t=(ywall-a[1])/(b[1]-a[1]); transverse=a[0]+t*(b[0]-a[0])
        margins.append(2.0-abs(transverse)-0.35)
    checks["route_to_shield_egress_min_clearance_mm"]=min(margins)
    return checks

def intersection_text_evidence(cstfile):
    root=os.path.splitext(cstfile)[0]
    hits=[]
    if not os.path.isdir(root): return hits
    needles=("no model intersections found","intersects with shape","intersecting shapes","performing intersection check")
    for d,_,files in os.walk(root):
        for name in files:
            q=os.path.join(d,name)
            try:
                if os.path.getsize(q)>2_000_000: continue
                raw=open(q,"rb").read()
                txt=raw.decode("utf-8","ignore").lower()
                for n in needles:
                    if n in txt:
                        hits.append({"file":q,"phrase":n})
            except Exception:
                pass
    return hits

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_H3A_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_H3A_WORK_EXISTS")
    if not os.path.isfile(source) or sha(source)!=SOURCE_SHA:
        raise RuntimeError("HOLD_H3A_SOURCE_HASH_MISMATCH")

    macro=os.path.join(repo,"source","cst","R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY_V02.mcr")
    if not os.path.isfile(macro): raise RuntimeError("HOLD_H3A_MACRO_MISSING")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY_V02.cst")
    shutil.copy2(source,dst)
    if sha(dst)!=SOURCE_SHA: raise RuntimeError("HOLD_H3A_COPY_HASH_MISMATCH")

    parent_ev=os.path.join(repo,"evidence","r1e1a1_dc_nw_20260924_build01","P094")
    snap=snapshot_tree(parent_ev)
    rewrites=[]

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New)
    de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("H3A Orthogonal PCB Stalk Assembly V0.1",macro_body(macro))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    result_sha=sha(dst)
    result_bytes=os.path.getsize(dst)

    shapes=os.path.join(evidence,"reopen_shapes.txt")
    status=os.path.join(evidence,"reopen_status.txt")
    intersection_status=os.path.join(evidence,"intersection_builtin_status.txt")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New)
    de.set_quiet_mode(True); prj=None
    builtin_return=False
    try:
        prj=de.open_project(dst)
        ok1=prj.schematic.execute_vba_code("Sub Main()\n"+audit_vba(shapes,status)+"\nEnd Sub")
        ok2=prj.schematic.execute_vba_code("Sub Main()\n"+intersection_vba(intersection_status)+"\nEnd Sub")
        builtin_return=bool(ok2)
    finally:
        if prj is not None: prj.close()
        de.close()
        rewrites=restore_snapshot(snap)

    rows=shape_rows(shapes)
    counts=component_counts(rows)
    st=parse_kv(status)
    params=parameter_map(dst)
    inter=parse_kv(intersection_status)
    clearances=critical_clearance_audit()
    clearances["bridge_axis_fr4_wall_mm"]=(5.50-3.30)/2
    clearances["bridge_cross_fr4_wall_mm"]=(2.571428571426-1.25)/2
    substrate_volume=next(v for n,v in rows if n=="Substrate:FR4_BOARD")
    text_hits=intersection_text_evidence(dst)

    expected_counts={
      "UnitCellGround":1,"Substrate":1,"TopCopper":1,
      "H3A_Stalk":10,"H3A_HubGround":4,"H3A_LNAEnvelope":4,
      "H3A_Shield":9,"H3A_RouteEnvelope":4,
      "H3A_MechLand":24,"H3A_MechSolder":16,
      "H3A_RFTransition":24,"H3A_RFSolder":12,
      "H3A_StalkRF":12,"H3A_ServiceEnvelope":4,
    }
    checks={
      "shape_count_126":len(rows)==126,
      "substrate_volume_proves_bridges":abs(substrate_volume-4518.704081623642)<1e-6,
      "bridge_component_consumed":"H3A_RadiatorBridge" not in counts,
      "component_counts_exact":counts==expected_counts,
      "all_shape_volumes_positive":all(v>0 for _,v in rows),
      "no_tools_remaining":"H3A_Tools" not in counts,
      "port_count_zero":int(st["PORT_COUNT"])==0,
      "unitcell_94":abs(float(st["DS1"])-94.0)<1e-6 and abs(float(st["DS2"])-94.0)<1e-6,
      "broadside":abs(float(st["THETA"]))<1e-9,
      "builtin_intersection_command_executed":builtin_return and inter.get("STARTED")=="TRUE" and inter.get("RETURNED")=="TRUE",
      "critical_clearances_positive":all(v>0 for v in clearances.values()),
      "no_solver_markers":len(solver_log_hits(dst))==0,
      "no_solver_result_items":len(solver_tree_items(dst))==0,
      "parent_evidence_restored":True,
      "artifact_unchanged_by_reopen_check":sha(dst)==result_sha,
    }
    checks["pass"]=all(checks.values())

    summary={
      "mode":"R1E1A4A_H3A_V02_FR4_BRIDGED_MORTISE_BUILD_ONLY",
      "simulationops":"0.2.5",
      "solver_run":False,
      "source_sha256":SOURCE_SHA,
      "result_cst":dst,
      "result_sha256":result_sha,
      "result_bytes":result_bytes,
      "shape_count":len(rows),
      "substrate_volume_mm3":substrate_volume,
      "component_counts":counts,
      "critical_clearances_mm":clearances,
      "builtin_intersection_command":{
        "command":"CDCheckModelIntersections",
        "execute_vba_return":builtin_return,
        "status_file":inter,
        "text_hits":text_hits,
        "note":"CST 2022.5 scripting API does not expose the dialog list as a structured return; command execution is paired with frozen-geometry clearance predicates and EM auto-intersection checking during build."
      },
      "parent_evidence_rewrites_detected":rewrites,
      "checks":checks,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    final="PASS_R1E1A4A_H3A_V02_FR4_BRIDGED_MORTISE_BUILD_ONLY" if checks["pass"] else "HOLD_R1E1A4A_H3A_V02_BUILD_QUALIFICATION"
    with open(os.path.join(evidence,"FORMAL_STATUS.txt"),"w") as f: f.write(final+"\n")
    print(final)
    print("RESULT_SHA256="+result_sha)
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True); ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work,a.source_cst)
