"""R1E0A periodic unit-cell configuration BUILD-ONLY harness."""
from __future__ import print_function
import argparse, hashlib, json, math, os, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci

BASE_SHA="74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce"

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

def audit_macro(shape_path,status_path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "Dim xmin As Double, xmax As Double, ymin As Double, ymax As Double, zmin As Double, zmax As Double",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1E0A_SHAPE_INVENTORY"',
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
      'Print #f, "STRUCTURE_ZMIN=" & CStr(zmin)',
      'Print #f, "STRUCTURE_ZMAX=" & CStr(zmax)',
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
        if "=" not in line: continue
        k,v=line.split("=",1)
        out[k.strip()]=v.strip()
    return out

def fval(d,k):
    return float(d[k])

def close(a,b,tol=1e-9):
    return abs(a-b)<=tol

def run(repo,evidence,work,base_cst):
    if os.path.exists(evidence):
        raise RuntimeError("HOLD_R1E0A_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work):
        raise RuntimeError("HOLD_R1E0A_WORK_DIR_ALREADY_EXISTS")
    if not os.path.isfile(base_cst):
        raise RuntimeError("HOLD_R1E0A_SOURCE_MISSING")
    base_sha=sha(base_cst)
    if base_sha!=BASE_SHA:
        raise RuntimeError("HOLD_R1E0A_SOURCE_HASH_MISMATCH:"+base_sha)

    os.makedirs(evidence)
    os.makedirs(work)
    cfg=os.path.join(repo,"source","cst","R1E0A_PERIODIC_BROADSIDE_BUILD_ONLY_V01.mcr")
    dst=os.path.join(work,"R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst")
    shutil.copy2(base_cst,dst)
    pre_sha=sha(dst)
    if pre_sha!=BASE_SHA:
        raise RuntimeError("HOLD_R1E0A_COPY_HASH_MISMATCH")

    build_shape=os.path.join(evidence,"build_object_inventory.txt")
    build_status=os.path.join(evidence,"build_periodic_status.txt")
    reopen_shape=os.path.join(evidence,"reopen_object_inventory.txt")
    reopen_status=os.path.join(evidence,"reopen_periodic_status.txt")

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E0A periodic broadside configuration",body(cfg))
        prj.save()
        prj.modeler.add_to_history("R1E0A build audit",audit_macro(build_shape,build_status))
    finally:
        if prj is not None: prj.close()
        de.close()

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E0A reopen audit",audit_macro(reopen_shape,reopen_status))
    finally:
        if prj is not None: prj.close()
        de.close()

    source_shapes=shape_lines(os.path.join(repo,"evidence","r1a5f_dc_nw_20260924_build01","A","reopen_object_inventory.txt"))
    bs=shape_lines(build_shape)
    rs=shape_lines(reopen_shape)
    st=parse_status(reopen_status)

    xspan=fval(st,"STRUCTURE_XMAX")-fval(st,"STRUCTURE_XMIN")
    yspan=fval(st,"STRUCTURE_YMAX")-fval(st,"STRUCTURE_YMIN")

    stem=os.path.splitext(dst)[0]
    output_exists=os.path.isfile(os.path.join(stem,"Result","output.txt"))

    checks={
      "source_hash_match":base_sha==BASE_SHA,
      "copy_hash_match":pre_sha==BASE_SHA,
      "geometry_unchanged_build":bs==source_shapes,
      "geometry_unchanged_reopen":rs==source_shapes,
      "port_count_1":int(st["PORT_COUNT"])==1,
      "x_boundaries_unit_cell":st["BOUNDARY_XMIN"].lower()=="unit cell" and st["BOUNDARY_XMAX"].lower()=="unit cell",
      "y_boundaries_unit_cell":st["BOUNDARY_YMIN"].lower()=="unit cell" and st["BOUNDARY_YMAX"].lower()=="unit cell",
      "z_boundaries_expanded_open":st["BOUNDARY_ZMIN"].lower()=="expanded open" and st["BOUNDARY_ZMAX"].lower()=="expanded open",
      "structure_query_ok":int(st["STRUCTURE_QUERY_ERR"])==0,
      "structure_x_span_94mm":close(xspan,94.0,1e-6),
      "structure_y_span_94mm":close(yspan,94.0,1e-6),
      "scan_query_ok":int(st["SCAN_QUERY_ERR"])==0,
      "scan_valid":st["SCAN_VALID"].lower()=="true",
      "theta_0":close(fval(st,"SCAN_THETA_DEG"),0.0,1e-9),
      "phi_45":close(fval(st,"SCAN_PHI_DEG"),45.0,1e-9),
      "direction_outward":int(st["SCAN_DIRECTION"])==1,
      "unitcell_angle_90":close(fval(st,"UNITCELL_ANGLE"),90.0,1e-9),
      "no_solver_output":not output_exists,
    }
    checks["pass"]=all(checks.values())

    summary={
      "source_cst":base_cst,
      "source_sha256":base_sha,
      "pre_config_copy_sha256":pre_sha,
      "config_sha256":sha(cfg),
      "r1e0a_cst":dst,
      "r1e0a_cst_sha256":sha(dst),
      "r1e0a_cst_bytes":os.path.getsize(dst),
      "reopen_status":st,
      "structure_span_mm":{"x":xspan,"y":yspan},
      "checks":checks,
      "solver_run":False,
    }
    with open(os.path.join(evidence,"harness_summary.json"),"w") as f:
        json.dump(summary,f,indent=2)

    status="PASS_R1E0A_PERIODIC_CONFIG_BUILD_ONLY" if checks["pass"] else "HOLD_R1E0A_PERIODIC_CONFIG_AUDIT"
    print(status)
    print("R1E0A_CST_PATH="+dst)
    print("R1E0A_CST_SHA256="+summary["r1e0a_cst_sha256"])
    print("XSPAN_MM=%.9f"%xspan)
    print("YSPAN_MM=%.9f"%yspan)
    print("SCAN="+json.dumps({"theta":st.get("SCAN_THETA_DEG"),"phi":st.get("SCAN_PHI_DEG"),"direction":st.get("SCAN_DIRECTION"),"valid":st.get("SCAN_VALID")}))
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--base-cst",required=True)
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work,a.base_cst)
