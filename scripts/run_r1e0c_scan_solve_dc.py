"""R1E0C-B one-state periodic scan solve harness."""
from __future__ import print_function
import argparse, csv, hashlib, json, math, os, re, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

import cst.interface as ci
from cst.results import ProjectFile

REGISTRY={
  "C30P45":{"theta":30.0,"phi":45.0,"sha":"e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2"},
  "C45P45":{"theta":45.0,"phi":45.0,"sha":"ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed"},
  "C60P45":{"theta":60.0,"phi":45.0,"sha":"94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01"},
  "C60P135":{"theta":60.0,"phi":135.0,"sha":"c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1"},
}
PERIODIC_S11_PATH=r"1D Results\S-Parameters\S1(1),1(1)"
BROAD_REL=os.path.join("evidence","r1e0b_dc_nw_20260924_smoke01","active_s11_and_zactive.csv")
Z0=100.0
SCI_LO=1.15
SCI_HI=1.65
ANCHORS=[1.17645,1.22760,1.27875,1.40000,1.56110,1.57542,1.60200]

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""):
            h.update(c)
    return h.hexdigest()

def macro_body(path):
    lines=open(path,"r",encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=e=None
    for i,l in enumerate(lines):
        if l.strip()=="Sub Main()": s=i
        elif l.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("macro markers not found")
    return "\n".join(lines[s+1:e])

def audit_history(shape_path,status_path,label):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "Dim xmin As Double, xmax As Double, ymin As Double, ymax As Double, zmin As Double, zmax As Double",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1E0C_B_%s_SHAPE_INVENTORY"'%label,
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
      "Close #f","On Error GoTo 0"
    ])

def parse_status(path):
    out={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k.strip()]=v.strip()
    return out

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def boolish(v):
    return v.strip().lower() in ("true","1","-1")

def close(a,b,tol=1e-9):
    return abs(a-b)<=tol

def metadata_checks(st,theta,phi):
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

def db(z):
    return 20.0*math.log10(max(abs(z),1e-300))

def zactive(s):
    den=1.0-s
    if abs(den)<1e-15:
        return complex(float("inf"),float("inf"))
    return Z0*(1.0+s)/den

def finite_complex(z):
    return math.isfinite(z.real) and math.isfinite(z.imag)

def read_s11(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    p3=pf.get_3d()
    tree=p3.get_tree_items()
    if PERIODIC_S11_PATH not in tree:
        raise RuntimeError("missing periodic driven-port S11: "+PERIODIC_S11_PATH)
    data=p3.get_result_item(PERIODIC_S11_PATH).get_data()
    return [(float(r[0]),complex(r[1])) for r in data],tree

def summarize(rows):
    vals=[]
    invalid_s=0; invalid_z=0
    min_re=(float("inf"),None); max_re=(-float("inf"),None)
    min_im=(float("inf"),None); max_im=(-float("inf"),None)
    max_abs_z=(0.0,None); max_abs_s=(0.0,None)
    anchors={}
    for f,s in rows:
        if not finite_complex(s): invalid_s+=1
        z=zactive(s)
        if not finite_complex(z): invalid_z+=1
        vals.append((f,s,db(s),z))
        if SCI_LO<=f<=SCI_HI and finite_complex(z):
            if z.real<min_re[0]: min_re=(z.real,f)
            if z.real>max_re[0]: max_re=(z.real,f)
            if z.imag<min_im[0]: min_im=(z.imag,f)
            if z.imag>max_im[0]: max_im=(z.imag,f)
            if abs(z)>max_abs_z[0]: max_abs_z=(abs(z),f)
            if abs(s)>max_abs_s[0]: max_abs_s=(abs(s),f)
    for f0 in ANCHORS:
        r=min(vals,key=lambda x:abs(x[0]-f0))
        anchors[str(f0)]={"f_ghz":r[0],"s11_db":r[2],"zactive_re_ohm":r[3].real,"zactive_im_ohm":r[3].imag}
    return vals,{
      "point_count":len(vals),
      "invalid_s11_values":invalid_s,
      "invalid_zactive_values":invalid_z,
      "science_band_re_min":{"ohm":min_re[0],"f_ghz":min_re[1]},
      "science_band_re_max":{"ohm":max_re[0],"f_ghz":max_re[1]},
      "science_band_im_min":{"ohm":min_im[0],"f_ghz":min_im[1]},
      "science_band_im_max":{"ohm":max_im[0],"f_ghz":max_im[1]},
      "science_band_max_abs_z":{"ohm":max_abs_z[0],"f_ghz":max_abs_z[1]},
      "science_band_max_abs_s11":{"value":max_abs_s[0],"f_ghz":max_abs_s[1]},
      "anchors":anchors,
    }

def write_csv(path,vals):
    with open(path,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["freq_ghz","s11_re","s11_im","s11_db","zactive_re_ohm","zactive_im_ohm"])
        for f0,s,d,z in vals:
            w.writerow([f0,s.real,s.imag,d,z.real,z.imag])

def load_broadside(path):
    out=[]
    with open(path,newline="") as f:
        for r in csv.DictReader(f):
            f0=float(r["freq_ghz"])
            s=complex(float(r["s11_re"]),float(r["s11_im"]))
            z=complex(float(r["zactive_re_ohm"]),float(r["zactive_im_ohm"]))
            out.append((f0,s,z))
    return out

def compare_broadside(rows,broad):
    max_ds=(0.0,None)
    max_dz=(0.0,None)
    n=0
    for f,s in rows:
        if not (SCI_LO<=f<=SCI_HI): continue
        _,sb,zb=min(broad,key=lambda x:abs(x[0]-f))
        z=zactive(s)
        ds=abs(s-sb)
        dz=abs(z-zb)
        if ds>max_ds[0]: max_ds=(ds,f)
        if dz>max_dz[0]: max_dz=(dz,f)
        n+=1
    return {
      "sample_count":n,
      "max_complex_delta_s11":max_ds[0],
      "max_complex_delta_s11_freq_ghz":max_ds[1],
      "max_abs_delta_zactive_ohm":max_dz[0],
      "max_abs_delta_zactive_freq_ghz":max_dz[1],
    }

def parse_native(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(p): raise RuntimeError("output.txt missing after solve")
    text=open(p,encoding="utf-8",errors="ignore").read()
    current=None; seq=[]
    for line in text.splitlines():
        m=re.search(r"Adaptive mesh refinement pass\s+(\d+)",line,re.I)
        if m: current=int(m.group(1))
        m=re.search(r"All S-Parameters\s*=\s*([0-9eE+\-.]+)",line,re.I)
        if m and current is not None:
            seq.append({"pass":current,"delta_s":float(m.group(1))})
    warnings=[x.strip() for x in text.splitlines() if "warning" in x.lower() or "prevented attempt" in x.lower()]
    errors=[x.strip() for x in text.splitlines() if "error" in x.lower()]
    return {
      "delta_s_sequence":seq,
      "last_two_below_0p02":len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02,
      "desired_accuracy_termination":"desired accuracy limit is reached" in text.lower(),
      "max_passes_reached":"maximum number of passes is reached" in text.lower(),
      "broadband_sweep_converged":"all broadband sweep convergence criteria have been satisfied" in text.lower(),
      "warning_lines":warnings,
      "error_lines":errors,
    }

def physics_alerts(rows):
    sci=[(f,s,zactive(s)) for f,s in rows if SCI_LO<=f<=SCI_HI]
    max_abs_s=max((abs(s) for _,s,_ in sci),default=0.0)
    min_re=min((z.real for _,_,z in sci if finite_complex(z)),default=float("inf"))
    max_abs_z=max((abs(z) for _,_,z in sci if finite_complex(z)),default=0.0)
    return {
      "abs_s11_ge_0p90":max_abs_s>=0.90,
      "re_zactive_le_0":min_re<=0.0,
      "abs_zactive_ge_1000":max_abs_z>=1000.0,
      "max_abs_s11":max_abs_s,
      "min_re_zactive_ohm":min_re,
      "max_abs_zactive_ohm":max_abs_z,
    }

def run(repo,evidence,work,source_cst,state):
    if state not in REGISTRY:
        raise RuntimeError("unknown state: "+state)
    reg=REGISTRY[state]
    if os.path.exists(evidence): raise RuntimeError("HOLD_R1E0C_B_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_R1E0C_B_WORK_DIR_ALREADY_EXISTS")
    if not os.path.isfile(source_cst): raise RuntimeError("HOLD_R1E0C_B_SOURCE_MISSING")
    if sha(source_cst)!=reg["sha"]: raise RuntimeError("HOLD_R1E0C_B_SOURCE_HASH_MISMATCH")

    broad_path=os.path.join(repo,BROAD_REL)
    if not os.path.isfile(broad_path): raise RuntimeError("HOLD_R1E0C_B_BROADSIDE_CONTEXT_MISSING")
    cfg=os.path.join(repo,"source","cst","R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr")
    if not os.path.isfile(cfg): raise RuntimeError("HOLD_R1E0C_B_CONFIG_MISSING")

    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E0C_B_%s_SCAN_SMOKE_V01.cst"%state)
    shutil.copy2(source_cst,dst)
    if sha(dst)!=reg["sha"]: raise RuntimeError("HOLD_R1E0C_B_COPY_HASH_MISMATCH")

    source_shapes=shape_lines(os.path.join(repo,"evidence","r1e0c_dc_nw_20260924_recovery01",state,"reopen_object_inventory.txt"))
    pshape=os.path.join(evidence,"pre_solver_object_inventory.txt")
    pstatus=os.path.join(evidence,"pre_solver_periodic_status.txt")

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E0C-B solver configuration",macro_body(cfg))
        prj.modeler.add_to_history("R1E0C-B pre-solver audit",audit_history(pshape,pstatus,state))
        prj.save()
        if shape_lines(pshape)!=source_shapes:
            raise RuntimeError("HOLD_R1E0C_B_GEOMETRY_CHANGED_PRE_SOLVER")
        md=metadata_checks(parse_status(pstatus),reg["theta"],reg["phi"])
        if not all(md.values()):
            raise RuntimeError("HOLD_R1E0C_B_PERIODIC_METADATA_INVALID")
        prj.modeler.run_solver()
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    rows,tree=read_s11(dst)
    vals,metrics=summarize(rows)
    write_csv(os.path.join(evidence,"active_s11_and_zactive.csv"),vals)
    broad=load_broadside(broad_path)
    comparison=compare_broadside(rows,broad)
    native=parse_native(dst)
    alerts=physics_alerts(rows)

    checks={
      "source_hash_match":sha(source_cst)==reg["sha"],
      "periodic_s11_path_present":PERIODIC_S11_PATH in tree,
      "s11_nonempty":metrics["point_count"]>0,
      "s11_finite":metrics["invalid_s11_values"]==0,
      "zactive_finite":metrics["invalid_zactive_values"]==0,
      "native_last_two_delta_s_pass":native["last_two_below_0p02"],
      "native_desired_accuracy_termination":native["desired_accuracy_termination"],
      "native_not_maxpass_terminated":not native["max_passes_reached"],
      "broadband_sweep_converged":native["broadband_sweep_converged"],
      "native_no_error_lines":len(native["error_lines"])==0,
    }
    checks["pass"]=all(checks.values())
    summary={
      "state":state,"theta_deg":reg["theta"],"phi_deg":reg["phi"],
      "source_cst":source_cst,"source_sha256":reg["sha"],
      "config_sha256":sha(cfg),
      "broadside_context_sha256":sha(broad_path),
      "result_cst":dst,"result_cst_sha256":sha(dst),"result_cst_bytes":os.path.getsize(dst),
      "metrics":metrics,"comparison_vs_broadside":comparison,
      "native_adaptation":native,"physics_alerts":alerts,"checks":checks,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    with open(os.path.join(evidence,"native_adaptation.json"),"w") as f: json.dump(native,f,indent=2)

    status=("PASS_R1E0C_B_%s_SCAN_SOLVE"%state) if checks["pass"] else ("HOLD_R1E0C_B_%s_SCAN_SOLVE"%state)
    print(status)
    print("RESULT_CST="+dst)
    print("RESULT_SHA256="+summary["result_cst_sha256"])
    print("POINT_COUNT="+str(metrics["point_count"]))
    print("MAX_D_S11_VS_BROADSIDE=%.9f"%comparison["max_complex_delta_s11"])
    print("MAX_D_Z_VS_BROADSIDE_OHM=%.9f"%comparison["max_abs_delta_zactive_ohm"])
    print("PHYSICS_ALERTS="+json.dumps(alerts,sort_keys=True))
    print("NATIVE="+json.dumps(native["delta_s_sequence"]))
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-cst",required=True)
    ap.add_argument("--state",required=True,choices=sorted(REGISTRY))
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work,a.source_cst,a.state)
