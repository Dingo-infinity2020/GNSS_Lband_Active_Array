"""R1E0B broadside periodic active-impedance smoke harness."""
from __future__ import print_function
import argparse, csv, hashlib, json, math, os, re, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223"
ISOLATED_REL=os.path.join("evidence","r1a5fq_dc_nw_20260924_equiv01","A","s11_and_zin.csv")
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

def audit_history(shape_path,status_path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "Dim xmin As Double, xmax As Double, ymin As Double, ymax As Double, zmin As Double, zmax As Double",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1E0B_SHAPE_INVENTORY"',
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

def metadata_checks(st):
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
      "theta_0":close(float(st["SCAN_THETA_DEG"]),0.0),
      "phi_45":close(float(st["SCAN_PHI_DEG"]),45.0),
      "direction_outward":int(st["SCAN_DIRECTION"])==1,
      "unitcell_ds1_94":close(float(st["UNITCELL_DS1"]),94.0,1e-6),
      "unitcell_ds2_94":close(float(st["UNITCELL_DS2"]),94.0,1e-6),
      "unitcell_angle_90":close(float(st["UNITCELL_ANGLE"]),90.0),
    }

def db(z):
    return 20.0*math.log10(max(abs(z),1e-300))

def zin(s):
    den=1.0-s
    if abs(den)<1e-15:
        return complex(float("inf"),float("inf"))
    return Z0*(1.0+s)/den
def read_s11(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    p3=pf.get_3d()
    path=r"1D Results\S-Parameters\S1,1"
    if path not in p3.get_tree_items():
        raise RuntimeError("missing S1,1")
    return [(float(r[0]),complex(r[1])) for r in p3.get_result_item(path).get_data()]

def finite_complex(z):
    return math.isfinite(z.real) and math.isfinite(z.imag)

def summarize(rows):
    out=[]; invalid_s=0; invalid_z=0
    max_abs_s=(0.0,None)
    min_re_z=(float("inf"),None); max_re_z=(-float("inf"),None)
    max_abs_z=(0.0,None)
    for f,s in rows:
        if not finite_complex(s): invalid_s+=1
        z=zin(s)
        if not finite_complex(z): invalid_z+=1
        a=abs(s)
        if a>max_abs_s[0]: max_abs_s=(a,f)
        if finite_complex(z):
            if z.real<min_re_z[0]: min_re_z=(z.real,f)
            if z.real>max_re_z[0]: max_re_z=(z.real,f)
            if abs(z)>max_abs_z[0]: max_abs_z=(abs(z),f)
        out.append((f,s,db(s),z))
    anchors={}
    for f0 in ANCHORS:
        r=min(out,key=lambda x:abs(x[0]-f0))
        anchors[str(f0)]={
          "f_ghz":r[0],
          "s11_db":r[2],
          "z_active_ohm":[r[3].real,r[3].imag],
        }
    return out,{
      "point_count":len(out),
      "invalid_s11_values":invalid_s,
      "invalid_zactive_values":invalid_z,
      "max_abs_s11":{"value":max_abs_s[0],"f_ghz":max_abs_s[1]},
      "min_re_zactive":{"ohm":min_re_z[0],"f_ghz":min_re_z[1]},
      "max_re_zactive":{"ohm":max_re_z[0],"f_ghz":max_re_z[1]},
      "max_abs_zactive":{"ohm":max_abs_z[0],"f_ghz":max_abs_z[1]},
      "anchors":anchors,
    }

def write_csv(path,vals):
    with open(path,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["freq_ghz","s11_re","s11_im","s11_db","zactive_re_ohm","zactive_im_ohm"])
        for f0,s,d,z in vals:
            w.writerow([f0,s.real,s.imag,d,z.real,z.imag])

def load_isolated(path):
    out=[]
    with open(path,newline="") as f:
        for r in csv.DictReader(f):
            out.append((float(r["freq_ghz"]),complex(float(r["s11_re"]),float(r["s11_im"]))))
    return out

def compare_isolated(periodic,isolated):
    maxd=(0.0,None); maxdb=(0.0,None); n=0
    for f,s in periodic:
        if not (SCI_LO<=f<=SCI_HI): continue
        fi,si=min(isolated,key=lambda x:abs(x[0]-f))
        d=abs(s-si); dd=abs(db(s)-db(si))
        if d>maxd[0]: maxd=(d,f)
        if dd>maxdb[0]: maxdb=(dd,f)
        n+=1
    return {
      "sample_count":n,
      "max_complex_delta":maxd[0],
      "max_complex_delta_freq_ghz":maxd[1],
      "max_db_delta":maxdb[0],
      "max_db_delta_freq_ghz":maxdb[1],
    }

def parse_native(cstfile):
    stem=os.path.splitext(cstfile)[0]
    p=os.path.join(stem,"Result","output.txt")
    if not os.path.isfile(p):
        raise RuntimeError("output.txt missing")
    text=open(p,encoding="utf-8",errors="ignore").read()
    current=None; seq=[]
    for line in text.splitlines():
        m=re.search(r"Adaptive mesh refinement pass\s+(\d+)",line,re.I)
        if m: current=int(m.group(1))
        m=re.search(r"All S-Parameters\s*=\s*([0-9eE+\-.]+)",line,re.I)
        if m and current is not None:
            seq.append({"pass":current,"delta_s":float(m.group(1))})
    return {
      "delta_s_sequence":seq,
      "last_two_below_0p02":len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02,
      "desired_accuracy_termination":"desired accuracy limit is reached" in text.lower(),
      "max_passes_reached":"maximum number of passes is reached" in text.lower(),
      "broadband_sweep_converged":"all broadband sweep convergence criteria have been satisfied" in text.lower(),
      "error_lines":[x.strip() for x in text.splitlines() if "error" in x.lower()],
    }

def capture_warnings(cstfile,path):
    stem=os.path.splitext(cstfile)[0]
    lines=[]
    for p in [os.path.join(stem,"Result","log.tet"),os.path.join(stem,"Result","meshrelated.info"),os.path.join(stem,"Result","output.txt")]:
        if not os.path.isfile(p): continue
        for line in open(p,encoding="utf-8",errors="ignore"):
            if "warning" in line.lower() or "error" in line.lower():
                lines.append(os.path.basename(p)+"|"+line.rstrip())
    with open(path,"w",encoding="utf-8") as f:
        f.write("\n".join(lines)+("\n" if lines else "NO_WARNING_LINES_FOUND\n"))
    return lines
def run(repo,evidence,work,source_cst):
    if os.path.exists(evidence):
        raise RuntimeError("HOLD_R1E0B_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work):
        raise RuntimeError("HOLD_R1E0B_WORK_DIR_ALREADY_EXISTS")
    if not os.path.isfile(source_cst):
        raise RuntimeError("HOLD_R1E0B_SOURCE_MISSING")
    if sha(source_cst)!=SOURCE_SHA:
        raise RuntimeError("HOLD_R1E0B_SOURCE_HASH_MISMATCH")

    isolated_path=os.path.join(repo,ISOLATED_REL)
    if not os.path.isfile(isolated_path):
        raise RuntimeError("HOLD_R1E0B_ISOLATED_BASELINE_MISSING")

    os.makedirs(evidence); os.makedirs(work)
    cfg=os.path.join(repo,"source","cst","R1E0B_PERIODIC_BROADSIDE_SOLVER_CONFIG_V01.mcr")
    dst=os.path.join(work,"R1E0B_POLA_PERIODIC_BROADSIDE_SMOKE_V01.cst")
    shutil.copy2(source_cst,dst)
    pre_sha=sha(dst)
    if pre_sha!=SOURCE_SHA:
        raise RuntimeError("HOLD_R1E0B_COPY_HASH_MISMATCH")

    stem=os.path.splitext(dst)[0]
    if os.path.isfile(os.path.join(stem,"Result","output.txt")):
        raise RuntimeError("HOLD_R1E0B_PREEXISTING_SOLVER_OUTPUT")

    pre_shape=os.path.join(evidence,"pre_config_object_inventory.txt")
    pre_status=os.path.join(evidence,"pre_config_periodic_status.txt")
    post_shape=os.path.join(evidence,"pre_solver_object_inventory.txt")
    post_status=os.path.join(evidence,"pre_solver_periodic_status.txt")

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E0B pre-config audit",audit_history(pre_shape,pre_status))
        prj.modeler.add_to_history("R1E0B solver configuration",macro_body(cfg))
        prj.modeler.add_to_history("R1E0B pre-solver audit",audit_history(post_shape,post_status))
        prj.save()

        src_shapes=shape_lines(os.path.join(repo,"evidence","r1a5f_dc_nw_20260924_build01","A","reopen_object_inventory.txt"))
        if shape_lines(pre_shape)!=src_shapes or shape_lines(post_shape)!=src_shapes:
            raise RuntimeError("HOLD_R1E0B_GEOMETRY_CHANGED")
        pre_checks=metadata_checks(parse_status(pre_status))
        post_checks=metadata_checks(parse_status(post_status))
        if not all(pre_checks.values()) or not all(post_checks.values()):
            raise RuntimeError("HOLD_R1E0B_PERIODIC_METADATA_INVALID")

        prj.modeler.run_solver()
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    rows=read_s11(dst)
    vals,metrics=summarize(rows)
    write_csv(os.path.join(evidence,"active_s11_and_zactive.csv"),vals)
    isolated=load_isolated(isolated_path)
    comparison=compare_isolated(rows,isolated)
    native=parse_native(dst)
    warnings=capture_warnings(dst,os.path.join(evidence,"solver_warnings.txt"))
    with open(os.path.join(evidence,"native_adaptation.json"),"w") as f:
        json.dump(native,f,indent=2)

    checks={
      "source_hash_match":sha(source_cst)==SOURCE_SHA,
      "copy_hash_match":pre_sha==SOURCE_SHA,
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
      "source_cst":source_cst,
      "source_sha256":SOURCE_SHA,
      "pre_config_copy_sha256":pre_sha,
      "config_sha256":sha(cfg),
      "isolated_context_csv":isolated_path,
      "isolated_context_sha256":sha(isolated_path),
      "result_cst":dst,
      "result_cst_sha256":sha(dst),
      "result_cst_bytes":os.path.getsize(dst),
      "metrics":metrics,
      "comparison_vs_isolated":comparison,
      "native_adaptation":native,
      "warning_line_count":len(warnings),
      "checks":checks,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f:
        json.dump(summary,f,indent=2)

    status="PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE" if checks["pass"] else "HOLD_R1E0B_BROADSIDE_PERIODIC_SMOKE"
    print(status)
    print("RESULT_CST="+dst)
    print("RESULT_SHA256="+summary["result_cst_sha256"])
    print("POINT_COUNT="+str(metrics["point_count"]))
    print("MAX_ABS_S11=%.9f"%metrics["max_abs_s11"]["value"])
    print("MIN_RE_ZACTIVE_OHM=%.9f"%metrics["min_re_zactive"]["ohm"])
    print("MAX_ABS_ZACTIVE_OHM=%.9f"%metrics["max_abs_zactive"]["ohm"])
    print("MAX_D_VS_ISOLATED=%.9f"%comparison["max_complex_delta"])
    print("NATIVE="+json.dumps(native["delta_s_sequence"]))
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-cst",required=True)
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work,a.source_cst)
