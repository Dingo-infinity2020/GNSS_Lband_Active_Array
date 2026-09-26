"""R1A5R second-order symmetry convergence solve on NW."""
import argparse, csv, hashlib, json, math, os, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

import cst.interface as ci
from cst.results import ProjectFile

BASE_SHA="4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364"
Z0=100.0
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

def audit_history(shape_path,port_path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1A5_SHAPE_INVENTORY"',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+10",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      '  Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm)) & "|area=" & CStr(Solid.GetArea(nm))',
      " End If","Next i","Close #f",
      "f=FreeFile", 'Open "%s" For Output As #f'%port_path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f","On Error GoTo 0"])

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def port_count(path):
    for x in open(path,encoding="utf-8").read().splitlines():
        if x.startswith("PORT_COUNT="):
            return int(x.split("=",1)[1])
    raise RuntimeError("port count missing")

def read_s(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    p3=pf.get_3d()
    tree=p3.get_tree_items()
    out={}
    for key,path in {
      "S11":r"1D Results\S-Parameters\S1,1",
      "S12":r"1D Results\S-Parameters\S1,2",
      "S21":r"1D Results\S-Parameters\S2,1",
      "S22":r"1D Results\S-Parameters\S2,2",
    }.items():
        if path not in tree:
            raise RuntimeError("missing result "+path)
        rows=p3.get_result_item(path).get_data()
        vals=[]
        for row in rows:
            vals.append((float(row[0]),complex(row[1])))
        out[key]=vals
    return out

def finite_complex(z):
    return math.isfinite(z.real) and math.isfinite(z.imag)

def db(z):
    return 20.0*math.log10(max(abs(z),1e-300))

def zin_from_s(s):
    den=1.0-s
    if abs(den)<1e-15:
        return complex(float("inf"),float("inf"))
    return Z0*(1.0+s)/den

def nearest(rows,f0):
    return min(rows,key=lambda r:abs(r[0]-f0))

def summarize(data):
    lens=[len(data[k]) for k in ("S11","S12","S21","S22")]
    if len(set(lens))!=1 or lens[0]==0:
        raise RuntimeError("unequal or empty S-parameter curves")
    n=lens[0]
    freqs=[x[0] for x in data["S11"]]
    for k in ("S12","S21","S22"):
        if any(abs(data[k][i][0]-freqs[i])>1e-12 for i in range(n)):
            raise RuntimeError("frequency grids differ")
    invalid=0
    rows=[]
    max_asym=0.0
    max_recip=0.0
    for i,f in enumerate(freqs):
        s11=data["S11"][i][1]; s12=data["S12"][i][1]
        s21=data["S21"][i][1]; s22=data["S22"][i][1]
        if not all(finite_complex(z) for z in (s11,s12,s21,s22)):
            invalid+=1
        d11=db(s11); d22=db(s22)
        max_asym=max(max_asym,abs(d11-d22))
        max_recip=max(max_recip,abs(s21-s12))
        z1=zin_from_s(s11); z2=zin_from_s(s22)
        rows.append((f,s11,s12,s21,s22,d11,db(s12),db(s21),d22,z1,z2))
    best1=min(rows,key=lambda r:r[5])
    best2=min(rows,key=lambda r:r[8])
    anchors={}
    for f0 in ANCHORS:
        r=min(rows,key=lambda r:abs(r[0]-f0))
        anchors[str(f0)]={
          "f_ghz":r[0],
          "s11_db":r[5],"s22_db":r[8],
          "s21_db":r[7],"s12_db":r[6],
          "zin1_ohm":[r[9].real,r[9].imag],
          "zin2_ohm":[r[10].real,r[10].imag],
          "s21_interpretation":"PORT_MODEL_LIMITED" if r[7] <= -50.0 else "QUALITATIVE_ONLY"
        }
    return rows,{
      "point_count":n,
      "invalid_complex_values":invalid,
      "max_abs_s11_s22_db_diff":max_asym,
      "max_complex_reciprocity_error":max_recip,
      "best_s11":{"f_ghz":best1[0],"db":best1[5]},
      "best_s22":{"f_ghz":best2[0],"db":best2[8]},
      "anchors":anchors,
    }

def write_csv(path,rows):
    with open(path,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow([
          "freq_ghz",
          "s11_re","s11_im","s11_db",
          "s12_re","s12_im","s12_db",
          "s21_re","s21_im","s21_db",
          "s22_re","s22_im","s22_db",
          "zin1_re_ohm","zin1_im_ohm",
          "zin2_re_ohm","zin2_im_ohm"
        ])
        for r in rows:
            fghz,s11,s12,s21,s22,d11,d12,d21,d22,z1,z2=r
            w.writerow([
              fghz,
              s11.real,s11.imag,d11,
              s12.real,s12.imag,d12,
              s21.real,s21.imag,d21,
              s22.real,s22.imag,d22,
              z1.real,z1.imag,z2.real,z2.imag
            ])

def capture_mesh_warnings(cstfile,outpath):
    stem=os.path.splitext(cstfile)[0]
    candidates=[
      os.path.join(stem,"Result","log.tet"),
      os.path.join(stem,"Result","meshrelated.info"),
    ]
    lines=[]
    for p in candidates:
        if not os.path.isfile(p):
            continue
        try:
            for line in open(p,encoding="utf-8",errors="ignore"):
                if "warning" in line.lower() or "error" in line.lower():
                    lines.append(os.path.basename(p)+"|"+line.rstrip())
        except Exception as e:
            lines.append("READ_ERROR|%s|%s"%(p,e))
    with open(outpath,"w",encoding="utf-8") as f:
        f.write("\n".join(lines)+("\n" if lines else "NO_WARNING_LINES_FOUND\n"))
    return lines

def run(repo,evidence,work,base_cst):
    if os.path.exists(evidence):
        raise RuntimeError("HOLD_R1A5_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work):
        raise RuntimeError("HOLD_R1A5_WORK_DIR_ALREADY_EXISTS")
    if not os.path.isfile(base_cst):
        raise RuntimeError("HOLD_R1A5_BASE_CST_MISSING")
    base_hash=sha(base_cst)
    if base_hash!=BASE_SHA:
        raise RuntimeError("HOLD_R1A5_BASE_HASH_MISMATCH:"+base_hash)
    os.makedirs(evidence)
    os.makedirs(work)
    cfg=os.path.join(repo,"source","cst","R1A5R_SECOND_ORDER_SOLVER_CONFIG_V01.mcr")
    dst=os.path.join(work,"R1A5R_SECOND_ORDER_V01.cst")
    shutil.copy2(base_cst,dst)
    copy_hash=sha(dst)
    if copy_hash!=BASE_SHA:
        raise RuntimeError("HOLD_R1A5_COPY_HASH_MISMATCH")
    pre_shape=os.path.join(evidence,"pre_solver_object_inventory.txt")
    pre_port=os.path.join(evidence,"pre_solver_port_status.txt")
    log=[
      "BASE_CST_SHA256="+base_hash,
      "PRE_CONFIG_COPY_SHA256="+copy_hash,
      "CONFIG_SHA256="+sha(cfg),
    ]
    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1A5 solver configuration",macro_body(cfg))
        prj.modeler.add_to_history("R1A5 pre-solver audit",audit_history(pre_shape,pre_port))
        prj.save()
        if port_count(pre_port)!=2:
            raise RuntimeError("HOLD_R1A5_PORT_COUNT_NOT_2")
        r1a4_shapes=shape_lines(os.path.join(repo,"evidence","r1a4_dc_nw_20260924_build01","build_object_inventory.txt"))
        if shape_lines(pre_shape)!=r1a4_shapes:
            raise RuntimeError("HOLD_R1A5_GEOMETRY_CHANGED_BEFORE_SOLVER")
        log.append("PRE_SOLVER_PROVENANCE_PASS")
        prj.modeler.run_solver()
        prj.save()
        log.append("SOLVER_COMPLETED")
    finally:
        if prj is not None: prj.close()
        de.close()

    data=read_s(dst)
    rows,metrics=summarize(data)
    write_csv(os.path.join(evidence,"sparameters_and_zin.csv"),rows)
    warnings=capture_mesh_warnings(dst,os.path.join(evidence,"solver_warnings.txt"))

    checks={
      "base_hash_match":base_hash==BASE_SHA,
      "pre_config_copy_hash_match":copy_hash==BASE_SHA,
      "port_count_2":port_count(pre_port)==2,
      "geometry_unchanged":shape_lines(pre_shape)==shape_lines(os.path.join(repo,"evidence","r1a4_dc_nw_20260924_build01","build_object_inventory.txt")),
      "all_curves_present":metrics["point_count"]>0,
      "no_nan_inf":metrics["invalid_complex_values"]==0,
      "reciprocity_pass":metrics["max_complex_reciprocity_error"]<=1e-3,
      "pol_symmetry_pass":metrics["max_abs_s11_s22_db_diff"]<=1.0,
    }
    checks["pass"]=all(checks.values())

    summary={
      "base_cst":base_cst,
      "base_cst_sha256":base_hash,
      "pre_config_copy_sha256":copy_hash,
      "config_sha256":sha(cfg),
      "r1a5_cst":dst,
      "r1a5_cst_sha256":sha(dst),
      "r1a5_cst_bytes":os.path.getsize(dst),
      "solver":"HF Frequency Domain",
      "mesh":"tetrahedral second order; curvature order 3; general purpose; adaptation off",
      "frequency_ghz":[1.0,1.8],
      "background_space_mm":50,
      "metrics":metrics,
      "checks":checks,
      "warning_line_count":len(warnings),
      "port_model_caveat":"Crossed discrete-edge ports add artificial coupling; isolation near/below -50 dB is port-model-limited.",
      "log":log,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f:
        json.dump(summary,f,indent=2)
    with open(os.path.join(evidence,"harness_log.txt"),"w") as f:
        f.write("\n".join(log)+"\n")
    status="PASS_R1A5R_SYMMETRY_CONVERGED" if checks["pass"] else "HOLD_R1A5R_DIAGNOSTIC_INTEGRITY"
    print(status)
    print("R1A5R_CST_PATH="+dst)
    print("R1A5R_CST_SHA256="+summary["r1a5_cst_sha256"])
    print("POINT_COUNT="+str(metrics["point_count"]))
    print("BEST_S11_DB=%.6f@%.6fGHz"%(metrics["best_s11"]["db"],metrics["best_s11"]["f_ghz"]))
    print("BEST_S22_DB=%.6f@%.6fGHz"%(metrics["best_s22"]["db"],metrics["best_s22"]["f_ghz"]))
    print("MAX_POL_ASYM_DB=%.9f"%metrics["max_abs_s11_s22_db_diff"])
    print("MAX_RECIP_ERR=%.12g"%metrics["max_complex_reciprocity_error"])
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--base-cst",required=True)
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work,a.base_cst)

