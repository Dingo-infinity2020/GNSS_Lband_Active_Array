"""R1E1A4A H0/P1 mixed-mode reference-plane BUILD-ONLY harness.

Copies the immutable bare P094 source, replaces the one differential port with
two 50-ohm single-ended P1 ports referenced to one H0 local-ground island,
fresh-reopens, audits, and never calls a solver.
"""
from __future__ import print_function
import argparse, hashlib, json, os, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
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
            p=os.path.join(d,name)
            with open(p,"rb") as f: snap.append((p,f.read()))
    return snap

def restore_snapshot(snap):
    changed=[]
    for path,data in snap:
        current=None
        if os.path.isfile(path):
            with open(path,"rb") as f: current=f.read()
        if current!=data: changed.append(path)
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,"wb") as f: f.write(data)
    for path,data in snap:
        with open(path,"rb") as f:
            if f.read()!=data:
                raise RuntimeError("HOLD_R1E1A4A_PARENT_EVIDENCE_RESTORE_FAILED:"+path)
    return changed

def parameter_map(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Model","Parameters.json")
    data=json.load(open(p,encoding="utf-8")); out={}
    def walk(x):
        if isinstance(x,dict):
            if "name" in x and "value" in x: out[str(x["name"])]=str(x["value"])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(data); return out

def result_tree_solver_items(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    items=pf.get_3d().get_tree_items()
    return [x for x in items if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def log_solver_hits(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(p): return []
    low=open(p,encoding="utf-8",errors="ignore").read().lower()
    return [m for m in SOLVER_MARKERS if m in low]

def parse_status(path):
    out={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k.strip()]=v.strip()
    return out

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def audit_vba(shape_path,status_path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "Dim stype As String, imp As Double, cur As Double, vol As Double",
      "Dim vimp As Double, rad As Double, mon As Boolean, pok As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double",
      "Dim cok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1E1A4A_H0_P1_SHAPE_INVENTORY"',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+20",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      ' If Len(nm)>0 Then Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm))',
      "Next i","Close #f",
      "scanok = Boundary.GetUnitCellScanAngle(th, ph, idir)",
      "f=FreeFile", 'Open "%s" For Output As #f'%status_path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "SCAN_VALID=" & CStr(scanok)',
      'Print #f, "SCAN_THETA_DEG=" & CStr(th)',
      'Print #f, "SCAN_PHI_DEG=" & CStr(ph)',
      'Print #f, "UNITCELL_DS1=" & CStr(Boundary.GetUnitCellDs1)',
      'Print #f, "UNITCELL_DS2=" & CStr(Boundary.GetUnitCellDs2)',
      "For i=1 To 2",
      " stype="": imp=0: cur=0: vol=0: vimp=0: rad=0: mon=False",
      " pok=DiscretePort.GetProperties(i,stype,imp,cur,vol,vimp,rad,mon)",
      " x0=0: y0=0: z0=0: x1=0: y1=0: z1=0",
      " cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "P" & CStr(i) & "_PROP_OK=" & CStr(pok)',
      ' Print #f, "P" & CStr(i) & "_TYPE=" & stype',
      ' Print #f, "P" & CStr(i) & "_IMPEDANCE=" & CStr(imp)',
      ' Print #f, "P" & CStr(i) & "_COORD_OK=" & CStr(cok)',
      ' Print #f, "P" & CStr(i) & "_P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0)',
      ' Print #f, "P" & CStr(i) & "_P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i","Close #f","On Error GoTo 0"
    ])

def parse_xyz(s):
    a=[float(x.strip()) for x in s.split(",")]
    if len(a)!=3: raise ValueError(s)
    return tuple(a)

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_R1E1A4A_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_R1E1A4A_WORK_EXISTS")
    if not os.path.isfile(source): raise RuntimeError("HOLD_R1E1A4A_SOURCE_MISSING")
    if sha(source)!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A4A_SOURCE_HASH_MISMATCH")

    macro=os.path.join(repo,"source","cst","R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_V01.mcr")
    if not os.path.isfile(macro): raise RuntimeError("HOLD_R1E1A4A_MACRO_MISSING")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_V01.cst")
    shutil.copy2(source,dst)
    if sha(dst)!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A4A_COPY_HASH_MISMATCH")

    parent_ev=os.path.join(repo,"evidence","r1e1a1_dc_nw_20260924_build01","P094")
    parent_snap=snapshot_tree(parent_ev)
    rewrites=[]
    bs=os.path.join(evidence,"build_shapes.txt"); bt=os.path.join(evidence,"build_status.txt")
    rs=os.path.join(evidence,"reopen_shapes.txt"); rt=os.path.join(evidence,"reopen_status.txt")

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E1A4A H0 P1 mixed-mode reference plane",macro_body(macro))
        prj.modeler.add_to_history("R1E1A4A build audit",audit_vba(bs,bt))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.schematic.execute_vba_code("Sub Main()\n"+audit_vba(rs,rt)+"\nEnd Sub")
    finally:
        if prj is not None: prj.close()
        de.close()
        rewrites=restore_snapshot(parent_snap)

    bsh=shape_lines(bs); rsh=shape_lines(rs); st=parse_status(rt); params=parameter_map(dst)
    p1a=parse_xyz(st["P1_P1"]); p1ag=parse_xyz(st["P1_P2"])
    p1b=parse_xyz(st["P2_P1"]); p1bg=parse_xyz(st["P2_P2"])
    xy=float(params["r1e1a4a_port_xy"])
    ztop=float(params["r1e1a4a_port_top_z"]); zg=float(params["r1e1a4a_ground_top_z"])
    expected_names={
      "GroundReference:UNITCELL_GROUND_REFERENCE",
      "Substrate:FR4_BOARD",
      "TopCopper:TOP_COPPER",
      "ActiveHub:H0_LOCAL_GROUND",
    }
    names=set(x.split("|",2)[1] for x in rsh)
    ground_line=[x for x in rsh if x.startswith("SHAPE|ActiveHub:H0_LOCAL_GROUND|")]
    ground_volume=float(ground_line[0].split("volume=",1)[1]) if ground_line else -1.0
    checks={
      "shape_count_4_build":len(bsh)==4,
      "shape_count_4_reopen":len(rsh)==4,
      "build_reopen_shapes_identical":bsh==rsh,
      "shape_names_exact":names==expected_names,
      "h0_ground_volume_3p5_mm3":abs(ground_volume-3.5)<1e-6,
      "port_count_2":int(st["PORT_COUNT"])==2,
      "p1_type_sparameter":st["P1_TYPE"].lower()=="sparameter" and st["P2_TYPE"].lower()=="sparameter",
      "p1_impedance_50":abs(float(st["P1_IMPEDANCE"])-50.0)<1e-9 and abs(float(st["P2_IMPEDANCE"])-50.0)<1e-9,
      "p1_coords_ok":st["P1_PROP_OK"].lower()=="true" and st["P1_COORD_OK"].lower()=="true" and st["P2_PROP_OK"].lower()=="true" and st["P2_COORD_OK"].lower()=="true",
      "p1a_terminal_exact":max(abs(p1a[i]-v) for i,v in enumerate((xy,xy,ztop)))<1e-8,
      "p1a_ground_exact":max(abs(p1ag[i]-v) for i,v in enumerate((xy,xy,zg)))<1e-8,
      "p1b_terminal_exact":max(abs(p1b[i]-v) for i,v in enumerate((-xy,-xy,ztop)))<1e-8,
      "p1b_ground_exact":max(abs(p1bg[i]-v) for i,v in enumerate((-xy,-xy,zg)))<1e-8,
      "p1_opposite_symmetry":abs(p1a[0]+p1b[0])<1e-8 and abs(p1a[1]+p1b[1])<1e-8,
      "unitcell_94":abs(float(st["UNITCELL_DS1"])-94.0)<1e-6 and abs(float(st["UNITCELL_DS2"])-94.0)<1e-6,
      "broadside":abs(float(st["SCAN_THETA_DEG"]))<1e-9,
      "h0_half_5":abs(float(params["r1e1a4a_h0_ground_half"])-5.0)<1e-9,
      "no_solver_markers":len(log_solver_hits(dst))==0,
      "no_solver_result_items":len(result_tree_solver_items(dst))==0,
      "parent_evidence_restored":True,
    }
    checks["pass"]=all(checks.values())
    summary={
      "mode":"R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY",
      "solver_run":False,
      "source_sha256":SOURCE_SHA,
      "result_cst":dst,
      "result_sha256":sha(dst),
      "result_bytes":os.path.getsize(dst),
      "parent_evidence_rewrites_detected":rewrites,
      "parameters":{k:params.get(k) for k in (
        "r1e1a4a_h0_ground_half","r1e1a4a_p1_ref_ohm","r1e1a4a_port_xy",
        "r1e1a4a_port_top_z","r1e1a4a_ground_top_z","r1e1a4a_ground_bottom_z")},
      "checks":checks,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    print("PASS_R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY" if checks["pass"] else "HOLD_R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY")
    print("RESULT_SHA256="+summary["result_sha256"])
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work,a.source_cst)
