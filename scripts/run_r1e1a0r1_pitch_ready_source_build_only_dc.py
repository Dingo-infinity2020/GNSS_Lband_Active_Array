"""R1E1A0-R1 pitch-ready canonical periodic source BUILD-ONLY harness.

Builds one fresh 94-mm Pol-A periodic source from deterministic derived macros.
No solver is started. Execution requires a separate BUILD authorization.
"""
from __future__ import print_function
import argparse, hashlib, json, math, os, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

HIST_GEOM_SHA="1e5bb3188c5d19146b673ec54372d0c35ae572abc775512529f71db71cfad5be"
HIST_PORT_SHA="f2b4555413005596f5fa8ceefacc64b7cadbba2cce1c430f0c9c713a6f7aead9"
HIST_PERIODIC_SHA="eaa9c714978c76381424747307d635397084078ddbf235103d54c3b51275f7ff"
DERIVED_GEOM_SHA="6f54dc6b7e73160f48a974e214fa481773f0d342a80bdb1242d0316fa39be6b7"
DERIVED_PERIODIC_SHA="b96469c62337f1dab9cb71a0bcdb7a7666e8ec558ee4f937c565d75a66e0de54"
R1A3_ARTIFACT_SHA="b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa"
R1A5F_POLA_ARTIFACT_SHA="74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce"
R1E0A_ARTIFACT_SHA="48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223"

SOLVER_MARKERS=(
  "meshing successful",
  "adaptive mesh refinement pass",
  "mesh adaptation sample",
  "excitation: port",
  "all broadband sweep convergence criteria",
  "running solver",
)
SWEEP_WARNING_PARAMS=(
  "unit_cell_pitch_nominal",
  "ground_reference_span",
  "r1e0_pitch_nominal_mm",
  "r1e0_scan_theta_deg",
  "r1e0_scan_phi_deg",
)

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def body(path):
    lines=open(path,encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=e=None
    for i,l in enumerate(lines):
        if l.strip()=="Sub Main()": s=i
        elif l.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("macro markers not found: "+path)
    return "\n".join(lines[s+1:e])

def audit_vba(shape_path,status_path,label):
    return "\n".join([
      "Sub Main()",
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "Dim xmin As Double, xmax As Double, ymin As Double, ymax As Double, zmin As Double, zmax As Double",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1E1A0R1_%s_SHAPE_INVENTORY"'%label,
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

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def parse_status(path):
    out={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k.strip()]=v.strip()
    return out

def parameter_records(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Model","Parameters.json")
    data=json.load(open(p,encoding="utf-8"))
    out={}
    def walk(x):
        if isinstance(x,dict):
            if "name" in x and "value" in x:
                out[str(x["name"])]=dict(x)
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(data)
    return out

def close(a,b,tol=1e-9):
    return abs(a-b)<=tol

def boolish(v):
    return v.strip().lower() in ("true","1","-1")

def status_checks(st):
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
      "theta_0":close(float(st["SCAN_THETA_DEG"]),0.0,1e-9),
      "phi_45":close(float(st["SCAN_PHI_DEG"]),45.0,1e-9),
      "direction_outward":int(st["SCAN_DIRECTION"])==1,
      "unitcell_ds1_94":close(float(st["UNITCELL_DS1"]),94.0,1e-6),
      "unitcell_ds2_94":close(float(st["UNITCELL_DS2"]),94.0,1e-6),
      "unitcell_angle_90":close(float(st["UNITCELL_ANGLE"]),90.0,1e-9),
    }

def param_checks(params):
    required=("unit_cell_pitch_nominal","ground_reference_span","R1E0_pitch_nominal_mm",
              "R1E0_scan_theta_deg","R1E0_scan_phi_deg","port_ref_impedance",
              "port_terminal_xy","port_terminal_z")
    if any(k not in params for k in required):
        return {"required_parameters_present":False}
    def val(k): return float(params[k]["value"])
    return {
      "required_parameters_present":True,
      "pitch_value_94":close(val("unit_cell_pitch_nominal"),94.0),
      "ground_value_94":close(val("ground_reference_span"),94.0),
      "ground_expr_tracks_pitch":params["ground_reference_span"].get("expr","").strip()=="unit_cell_pitch_nominal",
      "periodic_pitch_value_94":close(val("R1E0_pitch_nominal_mm"),94.0),
      "periodic_pitch_expr_tracks_pitch":params["R1E0_pitch_nominal_mm"].get("expr","").strip()=="unit_cell_pitch_nominal",
      "theta_value_0":close(val("R1E0_scan_theta_deg"),0.0),
      "phi_value_45":close(val("R1E0_scan_phi_deg"),45.0),
      "port_ref_100":close(val("port_ref_impedance"),100.0),
      "port_terminal_xy_frozen":close(val("port_terminal_xy"),2.12132034355964,1e-12),
      "port_terminal_z_frozen":close(val("port_terminal_z"),58.1778571428,1e-9),
    }

def log_evidence(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(p):
        return {"exists":False,"solver_marker_hits":[],"sweep_parameter_warning_hits":[]}
    text=open(p,encoding="utf-8",errors="ignore").read()
    low=text.lower()
    solver=[m for m in SOLVER_MARKERS if m in low]
    warnings=[]
    for line in text.splitlines():
        l=line.lower()
        if "prevented attempt to change" in l and any(k in l for k in SWEEP_WARNING_PARAMS):
            warnings.append(line.strip())
    return {"exists":True,"solver_marker_hits":solver,"sweep_parameter_warning_hits":warnings}

def solver_result_items(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    items=pf.get_3d().get_tree_items()
    return [x for x in items if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def run(repo,evidence,work):
    if os.path.exists(evidence): raise RuntimeError("HOLD_R1E1A0R1_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_R1E1A0R1_WORK_DIR_ALREADY_EXISTS")

    hist_geom=os.path.join(repo,"source","cst","R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr")
    hist_port=os.path.join(repo,"source","cst","R1A5F_POLA_SINGLE_PORT_BUILD_ONLY_V01.mcr")
    hist_periodic=os.path.join(repo,"source","cst","R1E0A_PERIODIC_BROADSIDE_BUILD_ONLY_V01.mcr")
    geom=os.path.join(repo,"source","cst","R1E1A0R1_PITCH_READY_R1A3_GEOMETRY_V01.mcr")
    periodic=os.path.join(repo,"source","cst","R1E1A0R1_PARAMETER_READY_PERIODIC_BROADSIDE_V01.mcr")

    frozen={
      hist_geom:HIST_GEOM_SHA, hist_port:HIST_PORT_SHA, hist_periodic:HIST_PERIODIC_SHA,
      geom:DERIVED_GEOM_SHA, periodic:DERIVED_PERIODIC_SHA,
    }
    for p,s in frozen.items():
        if not os.path.isfile(p) or sha(p)!=s:
            raise RuntimeError("HOLD_R1E1A0R1_HASH_MISMATCH:"+p)

    r1a3_cst=r"D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst"
    r1a5f_cst=r"D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst"
    r1e0a_cst=r"D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst"
    for p,s in ((r1a3_cst,R1A3_ARTIFACT_SHA),(r1a5f_cst,R1A5F_POLA_ARTIFACT_SHA),(r1e0a_cst,R1E0A_ARTIFACT_SHA)):
        if not os.path.isfile(p) or sha(p)!=s:
            raise RuntimeError("HOLD_R1E1A0R1_HISTORICAL_ARTIFACT_HASH_MISMATCH:"+p)

    os.makedirs(evidence); os.makedirs(work)
    cst=os.path.join(work,"R1E1A0R1_POLA_PERIODIC_PITCH_READY_94MM_V01.cst")
    build_shape=os.path.join(evidence,"build_object_inventory.txt")
    build_status=os.path.join(evidence,"build_periodic_status.txt")
    reopen_shape=os.path.join(evidence,"reopen_object_inventory.txt")
    reopen_status=os.path.join(evidence,"reopen_periodic_status.txt")

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.new_mws()
        prj.modeler.add_to_history("R1E1A0-R1 pitch-ready R1A3 geometry",body(geom))
        prj.modeler.add_to_history("R1E1A0-R1 frozen R1A5F Pol-A single port",body(hist_port))
        prj.modeler.add_to_history("R1E1A0-R1 parameter-ready periodic broadside",body(periodic))
        prj.save(cst)
        prj.schematic.execute_vba_code(audit_vba(build_shape,build_status,"BUILD"))
    finally:
        if prj is not None: prj.close()
        de.close()

    build_params=parameter_records(cst)

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(cst)
        prj.schematic.execute_vba_code(audit_vba(reopen_shape,reopen_status,"REOPEN"))
    finally:
        if prj is not None: prj.close()
        de.close()

    reopen_params=parameter_records(cst)
    hist_shapes=shape_lines(os.path.join(repo,"evidence","r1a3_dc_nw_20260924_build01","reopen_object_inventory.txt"))
    bs=shape_lines(build_shape); rs=shape_lines(reopen_shape)
    bst=parse_status(build_status); rst=parse_status(reopen_status)
    bsc=status_checks(bst); rsc=status_checks(rst)
    bpc=param_checks(build_params); rpc=param_checks(reopen_params)
    logs=log_evidence(cst)
    solver_items=solver_result_items(cst)

    checks={
      "shape_count_3_build":len(bs)==3,
      "shape_count_3_reopen":len(rs)==3,
      "geometry_equals_historical_r1a3_build":bs==hist_shapes,
      "geometry_equals_historical_r1a3_reopen":rs==hist_shapes,
      "build_reopen_geometry_identical":bs==rs,
      "build_periodic_status_pass":all(bsc.values()),
      "reopen_periodic_status_pass":all(rsc.values()),
      "build_reopen_status_identical":bst==rst,
      "build_parameter_readiness_pass":all(bpc.values()),
      "reopen_parameter_readiness_pass":all(rpc.values()),
      "no_sweep_parameter_history_warning":len(logs["sweep_parameter_warning_hits"])==0,
      "no_solver_markers":len(logs["solver_marker_hits"])==0,
      "no_solver_result_items":len(solver_items)==0,
    }
    checks["pass"]=all(checks.values())

    summary={
      "mode":"R1E1A0R1_PITCH_READY_CANONICAL_SOURCE_BUILD_ONLY",
      "cst":cst,"cst_sha256":sha(cst),"cst_bytes":os.path.getsize(cst),
      "derived_geometry_macro_sha256":sha(geom),
      "frozen_port_macro_sha256":sha(hist_port),
      "derived_periodic_macro_sha256":sha(periodic),
      "build_status":bst,"reopen_status":rst,
      "build_param_checks":bpc,"reopen_param_checks":rpc,
      "log_evidence":logs,"solver_result_items":solver_items,
      "checks":checks,"solver_run":False,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    status="PASS_R1E1A0R1_PITCH_READY_CANONICAL_SOURCE_BUILD_ONLY" if checks["pass"] else "HOLD_R1E1A0R1_PITCH_READY_CANONICAL_SOURCE_BUILD_ONLY"
    print(status)
    print("CST="+cst)
    print("CST_SHA256="+summary["cst_sha256"])
    print("CST_BYTES="+str(summary["cst_bytes"]))
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work)
