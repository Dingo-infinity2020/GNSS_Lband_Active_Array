#!/usr/bin/env python3
"""Read-only qualification of the already solved R1E0B periodic CST."""
from __future__ import print_function
import argparse, csv, hashlib, json, math, os, re, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
from cst.results import ProjectFile

EXPECTED_SOLVED_SHA="339021e580efa6aae6dfcfa229e4194b4dcf0bbef854398d44a0efed65aac7ad"
PERIODIC_S11_PATH=r"1D Results\S-Parameters\S1(1),1(1)"
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

def zactive(s):
    den=1.0-s
    if abs(den)<1e-15:
        return complex(float("inf"),float("inf"))
    return Z0*(1.0+s)/den

def finite_complex(z):
    return math.isfinite(z.real) and math.isfinite(z.imag)

def read_periodic_s11(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    p3=pf.get_3d()
    tree=p3.get_tree_items()
    if PERIODIC_S11_PATH not in tree:
        raise RuntimeError("periodic S11 path missing: "+PERIODIC_S11_PATH)
    data=p3.get_result_item(PERIODIC_S11_PATH).get_data()
    return [(float(r[0]),complex(r[1])) for r in data], tree

def summarize(rows):
    vals=[]; invalid_s=0; invalid_z=0
    max_abs_s=(0.0,None)
    min_re_z=(float("inf"),None)
    max_re_z=(-float("inf"),None)
    max_abs_z=(0.0,None)
    min_s_db=(float("inf"),None)
    for f,s in rows:
        if not finite_complex(s): invalid_s+=1
        z=zactive(s)
        if not finite_complex(z): invalid_z+=1
        sd=db(s)
        if abs(s)>max_abs_s[0]: max_abs_s=(abs(s),f)
        if sd<min_s_db[0]: min_s_db=(sd,f)
        if finite_complex(z):
            if z.real<min_re_z[0]: min_re_z=(z.real,f)
            if z.real>max_re_z[0]: max_re_z=(z.real,f)
            if abs(z)>max_abs_z[0]: max_abs_z=(abs(z),f)
        vals.append((f,s,sd,z))
    anchors={}
    for f0 in ANCHORS:
        r=min(vals,key=lambda x:abs(x[0]-f0))
        anchors[str(f0)]={
          "f_ghz":r[0],
          "s11_db":r[2],
          "zactive_re_ohm":r[3].real,
          "zactive_im_ohm":r[3].imag,
        }
    return vals,{
      "point_count":len(vals),
      "invalid_s11_values":invalid_s,
      "invalid_zactive_values":invalid_z,
      "best_s11_db":{"db":min_s_db[0],"f_ghz":min_s_db[1]},
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
    rows=[]
    with open(path,newline="") as f:
        for r in csv.DictReader(f):
            rows.append((float(r["freq_ghz"]),complex(float(r["s11_re"]),float(r["s11_im"]))))
    return rows

def compare_isolated(periodic,isolated):
    maxd=(0.0,None); maxdb=(0.0,None); n=0
    for f,s in periodic:
        if not (SCI_LO<=f<=SCI_HI): continue
        _,si=min(isolated,key=lambda x:abs(x[0]-f))
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
    warnings=[x.strip() for x in text.splitlines() if "warning" in x.lower()]
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

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--artifact",required=True)
    a=ap.parse_args()

    artifact_sha=sha(a.artifact)
    st=parse_status(os.path.join(a.evidence,"pre_solver_periodic_status.txt"))
    md=metadata_checks(st)

    rows,tree=read_periodic_s11(a.artifact)
    vals,metrics=summarize(rows)
    write_csv(os.path.join(a.evidence,"active_s11_and_zactive.csv"),vals)

    isolated_path=os.path.join(a.repo,ISOLATED_REL)
    isolated=load_isolated(isolated_path)
    comparison=compare_isolated(rows,isolated)
    native=parse_native(a.artifact)

    tree_extract=[x for x in tree if ("S-Parameters" in x or "Reference Impedance" in x or "Power\\Excitation" in x)]
    with open(os.path.join(a.evidence,"periodic_result_tree_extract.txt"),"w",encoding="utf-8") as f:
        f.write("\n".join(tree_extract)+"\n")

    checks={
      "artifact_sha_match":artifact_sha==EXPECTED_SOLVED_SHA,
      "periodic_metadata_pass":all(md.values()),
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
      "mode":"READ_ONLY_RESULT_RECOVERY",
      "formal_solver_rerun":False,
      "original_formal_status":"HOLD_R1E0B_RESULT_PATH_QUALIFICATION",
      "hold_classification":"PERIODIC_RESULT_PATH_NAMING_MISMATCH",
      "artifact":a.artifact,
      "artifact_sha256":artifact_sha,
      "artifact_bytes":os.path.getsize(a.artifact),
      "periodic_s11_path":PERIODIC_S11_PATH,
      "periodic_metadata":st,
      "periodic_metadata_checks":md,
      "metrics":metrics,
      "comparison_vs_isolated_context":comparison,
      "native_adaptation":native,
      "checks":checks,
    }
    with open(os.path.join(a.evidence,"recovery_summary.json"),"w") as f:
        json.dump(summary,f,indent=2)
    with open(os.path.join(a.evidence,"native_adaptation.json"),"w") as f:
        json.dump(native,f,indent=2)

    if checks["pass"]:
        print("PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE_READONLY_RECOVERY")
    else:
        print("HOLD_R1E0B_READONLY_RESULT_RECOVERY")
    print("S11_PATH="+PERIODIC_S11_PATH)
    print("POINT_COUNT="+str(metrics["point_count"]))
    print("BEST_S11_DB=%.9f@%.9fGHz"%(metrics["best_s11_db"]["db"],metrics["best_s11_db"]["f_ghz"]))
    print("MIN_RE_ZACTIVE_OHM=%.9f"%metrics["min_re_zactive"]["ohm"])
    print("MAX_RE_ZACTIVE_OHM=%.9f"%metrics["max_re_zactive"]["ohm"])
    print("MAX_ABS_ZACTIVE_OHM=%.9f"%metrics["max_abs_zactive"]["ohm"])
    print("MAX_D_VS_ISOLATED=%.9f"%comparison["max_complex_delta"])
    print("WARNING_COUNT="+str(len(native["warning_lines"])))
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    main()
