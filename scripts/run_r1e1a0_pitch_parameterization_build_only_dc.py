"""R1E1A0 endpoint pitch-parameterization BUILD-ONLY harness.

DESIGN-READY ONLY. Execution requires a separately frozen BUILD authorization.
No solver API is called.
"""
from __future__ import print_function
import argparse, hashlib, json, math, os, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223"
ENDPOINTS=[("P088",88.0),("P100",100.0)]
SOLVER_MARKERS=(
  "meshing successful",
  "adaptive mesh refinement pass",
  "mesh adaptation sample",
  "excitation: port",
  "all broadband sweep convergence criteria",
  "running solver",
)

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def pitch_update_vba(pitch):
    return "\n".join([
      "Sub Main()",
      '    StoreParameter "unit_cell_pitch_nominal", "%g"'%pitch,
      "    RebuildForParametricChange",
      "End Sub",
    ])

def audit_vba(shape_path,status_path,label):
    return "\n".join([
      "Sub Main()",
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "Dim xmin As Double, xmax As Double, ymin As Double, ymax As Double, zmin As Double, zmax As Double",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1E1A0_%s_SHAPE_INVENTORY"'%label,
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+10",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      '  Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm)) & "|area=" & CStr(Solid.GetArea(nm))',
      " End If","Next i","Close #f",
      "Err.Clear",
      "Boundary.GetStructureBox xmin, xmax, ymin, ymax, zmin, zmax",
      "Dim structureErr As Long","structureErr=Err.Number","Err.Clear",
      "scanok = Boundary.GetUnitCellScanAngle(th, ph, idir)",
      "Dim scanErr As Long","scanErr=Err.Number","Err.Clear",
      "f=FreeFile", 'Open "%s" For Output As #f'%status_path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "BOUNDARY_XMIN=" & Boundary.GetXmin',
      'Print #f, "BOUNDARY_XMAX=" & Boundary.GetXmax',
      'Print #f, "BOUNDARY_YMIN=" & Boundary.GetYmin',
      'Print #f, "BOUNDARY_YMAX=" & Boundary.GetYmax',
      'Print #f, "BOUNDARY_ZMIN=" & Boundary.GetZmin',
      'Print #f, "BOUNDARY_ZMAX=" & Boundary.GetZmax',
      'Print #f, "STRUCTURE_QUERY_ERR=" & CStr(structureErr)',
      'Print #f, "STRUCTURE_XMIN=" & CStr(xmin)',
      'Print #f, "STRUCTURE_XMAX=" & CStr(xmax)',
      'Print #f, "STRUCTURE_YMIN=" & CStr(ymin)',
      'Print #f, "STRUCTURE_YMAX=" & CStr(ymax)',
      'Print #f, "SCAN_QUERY_ERR=" & CStr(scanErr)',
      'Print #f, "SCAN_VALID=" & CStr(scanok)',
      'Print #f, "SCAN_THETA_DEG=" & CStr(th)',
      'Print #f, "SCAN_PHI_DEG=" & CStr(ph)',
      'Print #f, "SCAN_DIRECTION=" & CStr(idir)',
      'Print #f, "UNITCELL_DS1=" & CStr(Boundary.GetUnitCellDs1)',
      'Print #f, "UNITCELL_DS2=" & CStr(Boundary.GetUnitCellDs2)',
      'Print #f, "UNITCELL_ANGLE=" & CStr(Boundary.GetUnitCellAngle)',
      "Close #f",
      "On Error GoTo 0",
      "End Sub",
    ])

def parse_status(path):
    out={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k.strip()]=v.strip()
    return out

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def nonground(lines):
    return [x for x in lines if "UnitCellGround:UNITCELL_GROUND_REFERENCE" not in x]

def ground_line(lines):
    xs=[x for x in lines if "UnitCellGround:UNITCELL_GROUND_REFERENCE" in x]
    if len(xs)!=1: raise RuntimeError("expected exactly one ground shape")
    return xs[0]

def volume_from_shape_line(line):
    for part in line.split("|"):
        if part.startswith("volume="): return float(part.split("=",1)[1])
    raise RuntimeError("volume missing")

def parameter_map(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Model","Parameters.json")
    data=json.load(open(p,encoding="utf-8"))
    out={}
    def walk(x):
        if isinstance(x,dict):
            if "name" in x and "value" in x: out[str(x["name"])]=str(x["value"])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(data)
    return out

def boolish(v):
    return v.strip().lower() in ("true","1","-1")

def close(a,b,tol=1e-7):
    return abs(a-b)<=tol

def status_checks(st,pitch):
    xspan=float(st["STRUCTURE_XMAX"])-float(st["STRUCTURE_XMIN"])
    yspan=float(st["STRUCTURE_YMAX"])-float(st["STRUCTURE_YMIN"])
    return {
      "port_count_1":int(st["PORT_COUNT"])==1,
      "x_boundaries_unit_cell":st["BOUNDARY_XMIN"].lower()=="unit cell" and st["BOUNDARY_XMAX"].lower()=="unit cell",
      "y_boundaries_unit_cell":st["BOUNDARY_YMIN"].lower()=="unit cell" and st["BOUNDARY_YMAX"].lower()=="unit cell",
      "z_boundaries_expanded_open":st["BOUNDARY_ZMIN"].lower()=="expanded open" and st["BOUNDARY_ZMAX"].lower()=="expanded open",
      "structure_query_ok":int(st["STRUCTURE_QUERY_ERR"])==0,
      "xspan_target":close(xspan,pitch,1e-6),
      "yspan_target":close(yspan,pitch,1e-6),
      "scan_query_ok":int(st["SCAN_QUERY_ERR"])==0,
      "scan_valid":boolish(st["SCAN_VALID"]),
      "theta_broadside":close(float(st["SCAN_THETA_DEG"]),0.0,1e-9),
      "phi_45":close(float(st["SCAN_PHI_DEG"]),45.0,1e-9),
      "direction_outward":int(st["SCAN_DIRECTION"])==1,
      "unitcell_ds1_target":close(float(st["UNITCELL_DS1"]),pitch,1e-6),
      "unitcell_ds2_target":close(float(st["UNITCELL_DS2"]),pitch,1e-6),
      "unitcell_angle_90":close(float(st["UNITCELL_ANGLE"]),90.0,1e-9),
    }

def log_checks(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(p):
        return {"solver_marker_hits":[],"pitch_history_warning_hits":[]}
    text=open(p,encoding="utf-8",errors="ignore").read()
    low=text.lower()
    solver=[m for m in SOLVER_MARKERS if m in low]
    warnings=[]
    for line in text.splitlines():
        l=line.lower()
        if "prevented attempt to change" in l and ("unit_cell_pitch_nominal" in l or "ground_reference_span" in l):
            warnings.append(line.strip())
    return {"solver_marker_hits":solver,"pitch_history_warning_hits":warnings}

def result_tree_solver_items(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    items=pf.get_3d().get_tree_items()
    return [x for x in items if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def run_one(repo,evidence,work,source,label,pitch,source_shapes):
    edir=os.path.join(evidence,label); os.makedirs(edir)
    dst=os.path.join(work,"R1E1A0_%s_PITCH_BUILD_ONLY_V01.cst"%label)
    shutil.copy2(source,dst)
    pre_sha=sha(dst)
    if pre_sha!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A0_%s_COPY_HASH_MISMATCH"%label)

    bshape=os.path.join(edir,"build_object_inventory.txt")
    bstatus=os.path.join(edir,"build_periodic_status.txt")
    rshape=os.path.join(edir,"reopen_object_inventory.txt")
    rstatus=os.path.join(edir,"reopen_periodic_status.txt")

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.schematic.execute_vba_code(pitch_update_vba(pitch))
        prj.save()
        prj.schematic.execute_vba_code(audit_vba(bshape,bstatus,label))
    finally:
        if prj is not None: prj.close()
        de.close()

    build_params=parameter_map(dst)

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.schematic.execute_vba_code(audit_vba(rshape,rstatus,label))
    finally:
        if prj is not None: prj.close()
        de.close()

    reopen_params=parameter_map(dst)
    bs=shape_lines(bshape); rs=shape_lines(rshape)
    bst=parse_status(bstatus); rst=parse_status(rstatus)
    bc=status_checks(bst,pitch); rc=status_checks(rst,pitch)
    logs=log_checks(dst)
    solver_items=result_tree_solver_items(dst)
    expected_ground_volume=pitch*pitch*0.5
    checks={
      "pre_copy_hash_match":pre_sha==SOURCE_SHA,
      "shape_count_3_build":len(bs)==3,
      "shape_count_3_reopen":len(rs)==3,
      "nonground_geometry_unchanged_build":nonground(bs)==nonground(source_shapes),
      "nonground_geometry_unchanged_reopen":nonground(rs)==nonground(source_shapes),
      "ground_volume_target_build":close(volume_from_shape_line(ground_line(bs)),expected_ground_volume,1e-5),
      "ground_volume_target_reopen":close(volume_from_shape_line(ground_line(rs)),expected_ground_volume,1e-5),
      "build_status_pass":all(bc.values()),
      "reopen_status_pass":all(rc.values()),
      "build_reopen_status_identical":bst==rst,
      "pitch_parameter_build":close(float(build_params["unit_cell_pitch_nominal"]),pitch,1e-9),
      "pitch_parameter_reopen":close(float(reopen_params["unit_cell_pitch_nominal"]),pitch,1e-9),
      "no_pitch_history_warning":len(logs["pitch_history_warning_hits"])==0,
      "no_solver_markers":len(logs["solver_marker_hits"])==0,
      "no_solver_result_items":len(solver_items)==0,
    }
    checks["pass"]=all(checks.values())
    return {
      "label":label,"pitch_mm":pitch,
      "cst":dst,"cst_sha256":sha(dst),"cst_bytes":os.path.getsize(dst),
      "build_status":bst,"reopen_status":rst,
      "build_pitch_parameter":build_params.get("unit_cell_pitch_nominal"),
      "reopen_pitch_parameter":reopen_params.get("unit_cell_pitch_nominal"),
      "log_evidence":logs,"solver_result_items":solver_items,
      "checks":checks,
    }

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_R1E1A0_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_R1E1A0_WORK_DIR_ALREADY_EXISTS")
    if not os.path.isfile(source): raise RuntimeError("HOLD_R1E1A0_SOURCE_MISSING")
    if sha(source)!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A0_SOURCE_HASH_MISMATCH")
    os.makedirs(evidence); os.makedirs(work)
    source_shapes=shape_lines(os.path.join(repo,"evidence","r1e0a_dc_nw_20260924_build01","reopen_object_inventory.txt"))
    results=[]
    for label,pitch in ENDPOINTS:
        results.append(run_one(repo,evidence,work,source,label,pitch,source_shapes))
    top={
      "source_hash_match":sha(source)==SOURCE_SHA,
      "endpoint_count_2":len(results)==2,
      "both_endpoints_pass":all(x["checks"]["pass"] for x in results),
      "artifact_hashes_unique":len(set(x["cst_sha256"] for x in results))==2,
    }
    top["pass"]=all(top.values())
    summary={"mode":"R1E1A0_PITCH_PARAMETERIZATION_BUILD_ONLY","solver_run":False,"endpoints":results,"checks":top}
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    print("PASS_R1E1A0_PITCH_PARAMETERIZATION_BUILD_ONLY" if top["pass"] else "HOLD_R1E1A0_PITCH_PARAMETERIZATION_BUILD_ONLY")
    for x in results:
        print(x["label"]+"_SHA256="+x["cst_sha256"])
        print(x["label"]+"_PASS="+str(x["checks"]["pass"]))
    print(json.dumps(top,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-cst",required=True)
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work,a.source_cst)
