"""R1A5FQ clean-feed isolated-equivalence solver qualification on NW."""
from __future__ import print_function
import argparse, csv, hashlib, json, math, os, re, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

import cst.interface as ci
from cst.results import ProjectFile

A_SHA="74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce"
B_SHA="11ca4ae06baa1d3f18376789c90717f28aee2b02480d7eba88d2f5155d51a1bf"
BASELINE_REL=os.path.join("evidence","r1a5m2_dc_nw_20260924_recovery01","sparameters_and_zin.csv")
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

def audit_history(shape_path,port_path,label):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1A5FQ_%s_SHAPE_INVENTORY"'%label,
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

def db(z):
    return 20.0*math.log10(max(abs(z),1e-300))

def finite_complex(z):
    return math.isfinite(z.real) and math.isfinite(z.imag)

def zin_from_s(s):
    den=1.0-s
    if abs(den)<1e-15:
        return complex(float("inf"),float("inf"))
    return Z0*(1.0+s)/den

def read_s11(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    p3=pf.get_3d()
    tree=p3.get_tree_items()
    path=r"1D Results\S-Parameters\S1,1"
    if path not in tree:
        raise RuntimeError("missing result "+path)
    rows=p3.get_result_item(path).get_data()
    out=[]
    for row in rows:
        f=float(row[0]); s=complex(row[1])
        out.append((f,s))
    return out

def load_baseline(path):
    rows=[]
    with open(path,newline="") as f:
        for r in csv.DictReader(f):
            rows.append({
              "f":float(r["freq_ghz"]),
              "S11":complex(float(r["s11_re"]),float(r["s11_im"])),
              "S22":complex(float(r["s22_re"]),float(r["s22_im"])),
            })
    if not rows:
        raise RuntimeError("baseline CSV empty")
    return rows

def summarize(rows):
    if not rows:
        raise RuntimeError("empty S11 curve")
    invalid=sum(0 if finite_complex(s) else 1 for _,s in rows)
    vals=[]
    for f,s in rows:
        z=zin_from_s(s)
        vals.append((f,s,db(s),z))
    best=min(vals,key=lambda r:r[2])
    anchors={}
    for f0 in ANCHORS:
        r=min(vals,key=lambda x:abs(x[0]-f0))
        anchors[str(f0)]={
          "f_ghz":r[0],
          "s11_db":r[2],
          "zin_ohm":[r[3].real,r[3].imag],
        }
    return vals,{
      "point_count":len(vals),
      "invalid_complex_values":invalid,
      "best_s11":{"f_ghz":best[0],"db":best[2]},
      "anchors":anchors,
    }

def write_csv(path,vals):
    with open(path,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["freq_ghz","s11_re","s11_im","s11_db","zin_re_ohm","zin_im_ohm"])
        for fghz,s,d,z in vals:
            w.writerow([fghz,s.real,s.imag,d,z.real,z.imag])

def parse_native(cstfile):
    stem=os.path.splitext(cstfile)[0]
    p=os.path.join(stem,"Result","output.txt")
    if not os.path.isfile(p):
        raise RuntimeError("output.txt missing")
    text=open(p,encoding="utf-8",errors="ignore").read()
    current_pass=None
    seq=[]
    for line in text.splitlines():
        m=re.search(r"Adaptive mesh refinement pass\s+(\d+)",line,re.I)
        if m:
            current_pass=int(m.group(1))
        m=re.search(r"All S-Parameters\s*=\s*([0-9eE+\-.]+)",line,re.I)
        if m and current_pass is not None:
            seq.append({"pass":current_pass,"delta_s":float(m.group(1))})
    desired=("desired accuracy limit is reached" in text.lower())
    maxpass=("maximum number of passes is reached" in text.lower())
    broadband=("all broadband sweep convergence criteria have been satisfied" in text.lower())
    errors=[x.strip() for x in text.splitlines() if "error" in x.lower()]
    last_two=(len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02)
    return {
      "delta_s_sequence":seq,
      "last_two_below_0p02":last_two,
      "desired_accuracy_termination":desired,
      "max_passes_reached":maxpass,
      "broadband_sweep_converged":broadband,
      "error_lines":errors,
    }

def capture_warnings(cstfile,outpath):
    stem=os.path.splitext(cstfile)[0]
    candidates=[
      os.path.join(stem,"Result","log.tet"),
      os.path.join(stem,"Result","meshrelated.info"),
      os.path.join(stem,"Result","output.txt"),
    ]
    lines=[]
    for p in candidates:
        if not os.path.isfile(p):
            continue
        for line in open(p,encoding="utf-8",errors="ignore"):
            if "warning" in line.lower() or "error" in line.lower():
                lines.append(os.path.basename(p)+"|"+line.rstrip())
    with open(outpath,"w",encoding="utf-8") as f:
        f.write("\n".join(lines)+("\n" if lines else "NO_WARNING_LINES_FOUND\n"))
    return lines

def run_model(repo,evidence,work,source_cst,expected_sha,label,expected_shape_file,cfg):
    edir=os.path.join(evidence,label)
    os.makedirs(edir)
    if sha(source_cst)!=expected_sha:
        raise RuntimeError("HOLD_R1A5FQ_%s_SOURCE_HASH_MISMATCH"%label)

    dst=os.path.join(work,"R1A5FQ_%s_EQUIVALENCE_V01.cst"%label)
    shutil.copy2(source_cst,dst)
    pre_sha=sha(dst)
    if pre_sha!=expected_sha:
        raise RuntimeError("HOLD_R1A5FQ_%s_COPY_HASH_MISMATCH"%label)

    pre_shape=os.path.join(edir,"pre_solver_object_inventory.txt")
    pre_port=os.path.join(edir,"pre_solver_port_status.txt")

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1A5FQ solver configuration",macro_body(cfg))
        prj.modeler.add_to_history("R1A5FQ "+label+" pre-solver audit",audit_history(pre_shape,pre_port,label))
        prj.save()
        if port_count(pre_port)!=1:
            raise RuntimeError("HOLD_R1A5FQ_%s_PORT_COUNT_NOT_1"%label)
        if shape_lines(pre_shape)!=shape_lines(expected_shape_file):
            raise RuntimeError("HOLD_R1A5FQ_%s_GEOMETRY_CHANGED"%label)
        prj.modeler.run_solver()
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    rows=read_s11(dst)
    vals,metrics=summarize(rows)
    write_csv(os.path.join(edir,"s11_and_zin.csv"),vals)
    native=parse_native(dst)
    with open(os.path.join(edir,"native_adaptation.json"),"w") as f:
        json.dump(native,f,indent=2)
    warnings=capture_warnings(dst,os.path.join(edir,"solver_warnings.txt"))

    native_pass=(
      native["last_two_below_0p02"]
      and native["desired_accuracy_termination"]
      and not native["max_passes_reached"]
      and native["broadband_sweep_converged"]
      and len(native["error_lines"])==0
    )
    return {
      "label":label,
      "source_cst":source_cst,
      "source_sha256":expected_sha,
      "pre_config_copy_sha256":pre_sha,
      "cst":dst,
      "cst_sha256":sha(dst),
      "cst_bytes":os.path.getsize(dst),
      "point_count":metrics["point_count"],
      "invalid_complex_values":metrics["invalid_complex_values"],
      "best_s11":metrics["best_s11"],
      "anchors":metrics["anchors"],
      "native":native,
      "native_pass":native_pass,
      "warning_line_count":len(warnings),
      "rows":rows,
    }

def compare_rows(clean,baseline,key):
    maxd=(0.0,None)
    maxdb=(0.0,None)
    count=0
    for f,s in clean:
        if not (SCI_LO <= f <= SCI_HI):
            continue
        b=min(baseline,key=lambda x:abs(x["f"]-f))
        ref=b[key]
        d=abs(s-ref)
        dd=abs(db(s)-db(ref))
        if d>maxd[0]: maxd=(d,f)
        if dd>maxdb[0]: maxdb=(dd,f)
        count+=1
    if count==0:
        raise RuntimeError("no science-band comparison samples")
    return {
      "sample_count":count,
      "max_complex_delta":maxd[0],
      "max_complex_delta_freq_ghz":maxd[1],
      "max_db_delta":maxdb[0],
      "max_db_delta_freq_ghz":maxdb[1],
    }

def compare_clean(a,b):
    maxd=(0.0,None)
    maxdb=(0.0,None)
    count=0
    for fa,sa in a:
        if not (SCI_LO <= fa <= SCI_HI):
            continue
        fb,sb=min(b,key=lambda x:abs(x[0]-fa))
        d=abs(sa-sb)
        dd=abs(db(sa)-db(sb))
        if d>maxd[0]: maxd=(d,fa)
        if dd>maxdb[0]: maxdb=(dd,fa)
        count+=1
    return {
      "sample_count":count,
      "max_complex_delta":maxd[0],
      "max_complex_delta_freq_ghz":maxd[1],
      "max_db_delta":maxdb[0],
      "max_db_delta_freq_ghz":maxdb[1],
    }

def run(repo,evidence,work,source_a,source_b):
    if os.path.exists(evidence):
        raise RuntimeError("HOLD_R1A5FQ_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work):
        raise RuntimeError("HOLD_R1A5FQ_WORK_DIR_ALREADY_EXISTS")
    for p in (source_a,source_b):
        if not os.path.isfile(p):
            raise RuntimeError("HOLD_R1A5FQ_SOURCE_MISSING:"+p)

    baseline_path=os.path.join(repo,BASELINE_REL)
    if not os.path.isfile(baseline_path):
        raise RuntimeError("HOLD_R1A5FQ_BASELINE_MISSING")
    baseline=load_baseline(baseline_path)

    cfg=os.path.join(repo,"source","cst","R1A5FQ_EQUIVALENCE_SOLVER_CONFIG_V01.mcr")
    os.makedirs(evidence)
    os.makedirs(work)

    shape_a=os.path.join(repo,"evidence","r1a5f_dc_nw_20260924_build01","A","reopen_object_inventory.txt")
    shape_b=os.path.join(repo,"evidence","r1a5f_dc_nw_20260924_build01","B","reopen_object_inventory.txt")

    A=run_model(repo,evidence,work,source_a,A_SHA,"A",shape_a,cfg)
    B=run_model(repo,evidence,work,source_b,B_SHA,"B",shape_b,cfg)

    comp_A=compare_rows(A["rows"],baseline,"S11")
    comp_B=compare_rows(B["rows"],baseline,"S22")
    comp_AB=compare_clean(A["rows"],B["rows"])

    checks={
      "A_source_hash_match":A["source_sha256"]==A_SHA,
      "B_source_hash_match":B["source_sha256"]==B_SHA,
      "A_native_converged":A["native_pass"],
      "B_native_converged":B["native_pass"],
      "A_curve_complete_finite":A["point_count"]>0 and A["invalid_complex_values"]==0,
      "B_curve_complete_finite":B["point_count"]>0 and B["invalid_complex_values"]==0,
      "A_vs_R1A5M2_S11_pass":comp_A["max_complex_delta"]<=0.03,
      "B_vs_R1A5M2_S22_pass":comp_B["max_complex_delta"]<=0.03,
      "A_vs_B_complex_pass":comp_AB["max_complex_delta"]<=0.02,
      "A_vs_B_db_pass":comp_AB["max_db_delta"]<=0.5,
    }
    checks["pass"]=all(checks.values())

    summary={
      "config_sha256":sha(cfg),
      "baseline_csv":baseline_path,
      "baseline_csv_sha256":sha(baseline_path),
      "science_band_ghz":[SCI_LO,SCI_HI],
      "A":{k:v for k,v in A.items() if k!="rows"},
      "B":{k:v for k,v in B.items() if k!="rows"},
      "comparisons":{
        "A_vs_R1A5M2_S11":comp_A,
        "B_vs_R1A5M2_S22":comp_B,
        "A_vs_B":comp_AB,
      },
      "checks":checks,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f:
        json.dump(summary,f,indent=2)

    status="PASS_R1A5FQ_CLEAN_FEED_EQUIVALENT" if checks["pass"] else "HOLD_R1A5FQ_NOT_EQUIVALENT"
    print(status)
    print("A_RESULT_CST="+A["cst"])
    print("A_RESULT_SHA256="+A["cst_sha256"])
    print("B_RESULT_CST="+B["cst"])
    print("B_RESULT_SHA256="+B["cst_sha256"])
    print("A_NATIVE="+json.dumps(A["native"]["delta_s_sequence"]))
    print("B_NATIVE="+json.dumps(B["native"]["delta_s_sequence"]))
    print("MAX_D_A_VS_BASE=%.9f"%comp_A["max_complex_delta"])
    print("MAX_D_B_VS_BASE=%.9f"%comp_B["max_complex_delta"])
    print("MAX_D_A_VS_B=%.9f"%comp_AB["max_complex_delta"])
    print("MAX_DB_A_VS_B=%.9f"%comp_AB["max_db_delta"])
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-a",required=True)
    ap.add_argument("--source-b",required=True)
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work,a.source_a,a.source_b)
