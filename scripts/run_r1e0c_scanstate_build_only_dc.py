"""R1E0C-A four-state periodic scan metadata BUILD-ONLY harness."""
from __future__ import print_function
import argparse, hashlib, json, os, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci

SOURCE_SHA="48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223"
STATES=[
  ("C30P45",30.0,45.0),
  ("C45P45",45.0,45.0),
  ("C60P45",60.0,45.0),
  ("C60P135",60.0,135.0),
]

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""):
            h.update(c)
    return h.hexdigest()

def body(path):
    lines=open(path,"r",encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=e=None
    for i,l in enumerate(lines):
        if l.strip()=="Sub Main()": s=i
        elif l.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("macro markers not found")
    return "\n".join(lines[s+1:e])

def audit_macro(shape_path,status_path,label):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "Dim xmin As Double, xmax As Double, ymin As Double, ymax As Double, zmin As Double, zmax As Double",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1E0C_%s_SHAPE_INVENTORY"'%label,
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
      'Print #f, "SOLVER_RUN=NO"',
      "Close #f","On Error GoTo 0"
    ])

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def parse_status(path):
    out={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k.strip()]=v.strip()
    return out

def boolish(v):
    return v.strip().lower() in ("true","1","-1")

def close(a,b,tol=1e-9):
    return abs(a-b)<=tol

def check_status(st,theta,phi):
    xspan=float(st["STRUCTURE_XMAX"])-float(st["STRUCTURE_XMIN"])
    yspan=float(st["STRUCTURE_YMAX"])-float(st["STRUCTURE_YMIN"])
    return {
      "port_count_1":int(st["PORT_COUNT"])==1,
      "x_boundaries_unit_cell":st["BOUNDARY_XMIN"].lower()=="unit cell" and st["BOUNDARY_XMAX"].lower()=="unit cell",
      "y_boundaries_unit_cell":st["BOUNDARY_YMIN"].lower()=="unit cell" and st["BOUNDARY_YMAX"].lower()=="unit cell",
      "z_boundaries_expanded_open":st["BOUNDARY_ZMIN"].lower()=="expanded open" and st["BOUNDARY_ZMAX"].lower()=="expanded open",
      "structure_query_ok":int(st["STRUCTURE_QUERY_ERR"])==0,
      "xspan_94":close(xspan,94.0,1e-6),
      "yspan_94":close(yspan,94.0,1e-6),
      "scan_query_ok":int(st["SCAN_QUERY_ERR"])==0,
      "scan_valid":boolish(st["SCAN_VALID"]),
      "theta_match":close(float(st["SCAN_THETA_DEG"]),theta,1e-9),
      "phi_match":close(float(st["SCAN_PHI_DEG"]),phi,1e-9),
      "direction_outward":int(st["SCAN_DIRECTION"])==1,
      "unitcell_ds1_94":close(float(st["UNITCELL_DS1"]),94.0,1e-6),
      "unitcell_ds2_94":close(float(st["UNITCELL_DS2"]),94.0,1e-6),
      "unitcell_angle_90":close(float(st["UNITCELL_ANGLE"]),90.0,1e-9),
    }

def run_one(repo,evidence,work,source,state,theta,phi,source_shapes):
    edir=os.path.join(evidence,state)
    os.makedirs(edir)
    dst=os.path.join(work,"R1E0C_%s_SCANSTATE_BUILD_ONLY_V01.cst"%state)
    shutil.copy2(source,dst)
    pre_sha=sha(dst)
    if pre_sha!=SOURCE_SHA:
        raise RuntimeError("HOLD_R1E0C_%s_COPY_HASH_MISMATCH"%state)
    macro=os.path.join(repo,"source","cst","R1E0C_%s_SCANSTATE_BUILD_ONLY_V01.mcr"%state)

    bshape=os.path.join(edir,"build_object_inventory.txt")
    bstatus=os.path.join(edir,"build_periodic_status.txt")
    rshape=os.path.join(edir,"reopen_object_inventory.txt")
    rstatus=os.path.join(edir,"reopen_periodic_status.txt")

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E0C "+state+" scan metadata",body(macro))
        prj.save()
        prj.modeler.add_to_history("R1E0C "+state+" build audit",audit_macro(bshape,bstatus,state))
    finally:
        if prj is not None: prj.close()
        de.close()

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E0C "+state+" reopen audit",audit_macro(rshape,rstatus,state))
    finally:
        if prj is not None: prj.close()
        de.close()

    bs=shape_lines(bshape); rs=shape_lines(rshape)
    bst=parse_status(bstatus); rst=parse_status(rstatus)
    bc=check_status(bst,theta,phi); rc=check_status(rst,theta,phi)
    stem=os.path.splitext(dst)[0]
    output_exists=os.path.isfile(os.path.join(stem,"Result","output.txt"))
    checks={
      "pre_copy_hash_match":pre_sha==SOURCE_SHA,
      "build_geometry_unchanged":bs==source_shapes,
      "reopen_geometry_unchanged":rs==source_shapes,
      "build_status_pass":all(bc.values()),
      "reopen_status_pass":all(rc.values()),
      "build_reopen_status_identical":bst==rst,
      "no_solver_output":not output_exists,
    }
    checks["pass"]=all(checks.values())
    return {
      "state":state,"theta_deg":theta,"phi_deg":phi,
      "cst":dst,"cst_sha256":sha(dst),"cst_bytes":os.path.getsize(dst),
      "macro_sha256":sha(macro),
      "reopen_status":rst,"checks":checks,
    }

def run(repo,evidence,work,source):
    if os.path.exists(evidence):
        raise RuntimeError("HOLD_R1E0C_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work):
        raise RuntimeError("HOLD_R1E0C_WORK_DIR_ALREADY_EXISTS")
    if not os.path.isfile(source):
        raise RuntimeError("HOLD_R1E0C_SOURCE_MISSING")
    if sha(source)!=SOURCE_SHA:
        raise RuntimeError("HOLD_R1E0C_SOURCE_HASH_MISMATCH")

    # Preflight every generated macro before creating any execution directory.
    for state,theta,phi in STATES:
        macro=os.path.join(repo,"source","cst","R1E0C_%s_SCANSTATE_BUILD_ONLY_V01.mcr"%state)
        if not os.path.isfile(macro):
            raise RuntimeError("HOLD_R1E0C_MACRO_MISSING_"+state)

    os.makedirs(evidence); os.makedirs(work)
    source_shapes=shape_lines(os.path.join(repo,"evidence","r1e0a_dc_nw_20260924_build01","reopen_object_inventory.txt"))
    results=[]
    for state,theta,phi in STATES:
        results.append(run_one(repo,evidence,work,source,state,theta,phi,source_shapes))

    checks={
      "source_hash_match":sha(source)==SOURCE_SHA,
      "all_four_states_present":len(results)==4,
      "all_states_pass":all(r["checks"]["pass"] for r in results),
      "all_artifact_hashes_unique":len(set(r["cst_sha256"] for r in results))==4,
    }
    checks["pass"]=all(checks.values())
    summary={
      "source_cst":source,
      "source_sha256":SOURCE_SHA,
      "states":results,
      "checks":checks,
      "solver_run":False,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f:
        json.dump(summary,f,indent=2)

    status="PASS_R1E0C_SCANSTATE_BUILD_ONLY" if checks["pass"] else "HOLD_R1E0C_SCANSTATE_BUILD_ONLY"
    print(status)
    for r in results:
        print("%s_CST=%s"%(r["state"],r["cst"]))
        print("%s_SHA256=%s"%(r["state"],r["cst_sha256"]))
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-cst",required=True)
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work,a.source_cst)
