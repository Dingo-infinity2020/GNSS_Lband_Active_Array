"""R1E1A3 one-state support-sensitivity solve harness.
One formal invocation solves exactly one immutable R1E1A2 source.
"""
from __future__ import print_function
import argparse, csv, hashlib, json, math, os, re, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

PERIODIC_S11_PATH=r"1D Results\S-Parameters\S1(1),1(1)"
SCI_LO=1.15
SCI_HI=1.65
Z0=100.0
STATE_REF={
 "B0":("evidence/r1e0b_dc_nw_20260924_smoke01/active_s11_and_zactive.csv",0.0,45.0),
 "C60P45":("evidence/r1e0c_b_c60p45_dc_nw_20260924_solve01/active_s11_and_zactive.csv",60.0,45.0),
 "C60P135":("evidence/r1e0c_b_c60p135_dc_nw_20260924_solve01/active_s11_and_zactive.csv",60.0,135.0),
}

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def macro_body(path):
    lines=open(path,encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=lines.index("Sub Main()"); e=lines.index("End Sub")
    return "\n".join(lines[s+1:e])

def audit_vba(path):
    return "\n".join([
      "On Error Resume Next","Dim f As Integer","Dim th As Double, ph As Double, idir As Long, ok As Boolean",
      "ok=Boundary.GetUnitCellScanAngle(th,ph,idir)",
      "f=FreeFile", 'Open "%s" For Output As #f'%path,
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "THETA=" & CStr(th)', 'Print #f, "PHI=" & CStr(ph)',
      'Print #f, "DIRECTION=" & CStr(idir)',
      'Print #f, "DS1=" & CStr(Boundary.GetUnitCellDs1)',
      'Print #f, "DS2=" & CStr(Boundary.GetUnitCellDs2)',
      "Close #f","On Error GoTo 0"
    ])

def parse_kv(path):
    d={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); d[k.strip()]=v.strip()
    return d

def zactive(s):
    den=1.0-s
    if abs(den)<1e-15: return complex(float("inf"),float("inf"))
    return Z0*(1.0+s)/den

def read_s11(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    p3=pf.get_3d(); tree=p3.get_tree_items()
    if PERIODIC_S11_PATH not in tree:
        raise RuntimeError("missing periodic S11 result")
    data=p3.get_result_item(PERIODIC_S11_PATH).get_data()
    return [(float(x[0]),complex(x[1])) for x in data],tree

def load_ref(path):
    out=[]
    with open(path,newline="") as f:
        for r in csv.DictReader(f):
            out.append((float(r["freq_ghz"]),complex(float(r["s11_re"]),float(r["s11_im"])),
                        complex(float(r["zactive_re_ohm"]),float(r["zactive_im_ohm"]))))
    return out

def compare(rows,ref):
    dsmax=(0.0,None); dzmax=(0.0,None); sumds=0.0; sumdz=0.0; n=0
    for f,s in rows:
        if not (SCI_LO<=f<=SCI_HI): continue
        fr,sr,zr=min(ref,key=lambda x:abs(x[0]-f))
        z=zactive(s); ds=abs(s-sr); dz=abs(z-zr)
        if ds>dsmax[0]: dsmax=(ds,f)
        if dz>dzmax[0]: dzmax=(dz,f)
        sumds+=ds*ds; sumdz+=dz*dz; n+=1
    return {
      "sample_count":n,
      "max_complex_delta_s11":dsmax[0],"max_complex_delta_s11_freq_ghz":dsmax[1],
      "rms_complex_delta_s11":math.sqrt(sumds/max(n,1)),
      "max_abs_delta_zactive_ohm":dzmax[0],"max_abs_delta_zactive_freq_ghz":dzmax[1],
      "rms_abs_delta_zactive_ohm":math.sqrt(sumdz/max(n,1)),
    }

def parse_native(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(p): raise RuntimeError("output.txt missing")
    text=open(p,encoding="utf-8",errors="ignore").read()
    cur=None; seq=[]
    for line in text.splitlines():
        m=re.search(r"Adaptive mesh refinement pass\s+(\d+)",line,re.I)
        if m: cur=int(m.group(1))
        m=re.search(r"All S-Parameters\s*=\s*([0-9eE+\-.]+)",line,re.I)
        if m and cur is not None: seq.append({"pass":cur,"delta_s":float(m.group(1))})
    return {
      "delta_s_sequence":seq,
      "last_two_below_0p02":len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02,
      "desired_accuracy":"desired accuracy limit is reached" in text.lower(),
      "maxpasses":"maximum number of passes is reached" in text.lower(),
      "broadband_converged":"all broadband sweep convergence criteria have been satisfied" in text.lower(),
      "errors":[x.strip() for x in text.splitlines() if "error" in x.lower()],
    }

def alerts(rows):
    sci=[(f,s,zactive(s)) for f,s in rows if SCI_LO<=f<=SCI_HI]
    maxs=max((abs(s) for _,s,_ in sci),default=0.0)
    minre=min((z.real for _,_,z in sci if math.isfinite(z.real)),default=float("inf"))
    maxz=max((abs(z) for _,_,z in sci if math.isfinite(z.real) and math.isfinite(z.imag)),default=0.0)
    return {"abs_s11_ge_0p90":maxs>=0.90,"re_zactive_le_0":minre<=0.0,
            "abs_zactive_ge_1000":maxz>=1000.0,"max_abs_s11":maxs,
            "min_re_zactive_ohm":minre,"max_abs_zactive_ohm":maxz}

def write_csv(path,rows):
    with open(path,"w",newline="") as f:
        w=csv.writer(f); w.writerow(["freq_ghz","s11_re","s11_im","s11_db","zactive_re_ohm","zactive_im_ohm"])
        for fr,s in rows:
            z=zactive(s); w.writerow([fr,s.real,s.imag,20*math.log10(max(abs(s),1e-300)),z.real,z.imag])

def run(repo,evidence,work,source_cst,source_sha,variant,state):
    if state not in STATE_REF: raise RuntimeError("unknown state")
    if os.path.exists(evidence): raise RuntimeError("HOLD_R1E1A3_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_R1E1A3_WORK_EXISTS")
    if sha(source_cst).lower()!=source_sha.lower(): raise RuntimeError("HOLD_R1E1A3_SOURCE_HASH_MISMATCH")
    ref_rel,theta,phi=STATE_REF[state]; ref_path=os.path.join(repo,ref_rel)
    cfg=os.path.join(repo,"source","cst","R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr")
    if not os.path.isfile(ref_path) or not os.path.isfile(cfg): raise RuntimeError("HOLD_R1E1A3_CONTEXT_MISSING")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A3_%s_%s_SOLVE_V01.cst"%(variant,state))
    shutil.copy2(source_cst,dst)
    if sha(dst).lower()!=source_sha.lower(): raise RuntimeError("HOLD_R1E1A3_COPY_HASH_MISMATCH")

    pre=os.path.join(evidence,"pre_solver_status.txt")
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E1A3 solver configuration",macro_body(cfg))
        prj.modeler.add_to_history("R1E1A3 pre-solver audit",audit_vba(pre))
        prj.save()
        st=parse_kv(pre)
        expected_shapes=15 if variant=="S1_BONDED" else 7
        meta=(int(st["SHAPE_COUNT"])==expected_shapes and int(st["PORT_COUNT"])==1 and
              abs(float(st["THETA"])-theta)<1e-9 and abs(float(st["PHI"])-phi)<1e-9 and
              abs(float(st["DS1"])-94.0)<1e-6 and abs(float(st["DS2"])-94.0)<1e-6)
        if not meta: raise RuntimeError("HOLD_R1E1A3_PRE_SOLVER_METADATA")
        prj.modeler.run_solver(); prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    rows,tree=read_s11(dst); write_csv(os.path.join(evidence,"active_s11_and_zactive.csv"),rows)
    comp=compare(rows,load_ref(ref_path)); native=parse_native(dst); pa=alerts(rows)
    numerical={
      "s11_present":PERIODIC_S11_PATH in tree,"nonempty":len(rows)>0,
      "last_two_delta_s":native["last_two_below_0p02"],"desired_accuracy":native["desired_accuracy"],
      "not_maxpasses":not native["maxpasses"],"broadband_converged":native["broadband_converged"],
      "no_error_lines":len(native["errors"])==0,
    }
    numerical["pass"]=all(numerical.values())
    benign=(numerical["pass"] and comp["max_complex_delta_s11"]<=0.05 and
            comp["max_abs_delta_zactive_ohm"]<=10.0 and not pa["abs_s11_ge_0p90"] and
            not pa["re_zactive_le_0"] and not pa["abs_zactive_ge_1000"])
    summary={"variant":variant,"state":state,"theta":theta,"phi":phi,
      "source_cst":source_cst,"source_sha256":source_sha,"reference_csv":ref_rel,
      "solver_config_sha256":sha(cfg),"result_cst":dst,"result_sha256":sha(dst),
      "result_bytes":os.path.getsize(dst),"comparison_vs_bare":comp,
      "native":native,"physics_alerts":pa,"numerical_checks":numerical,
      "pre_frozen_benign_gate":{"max_complex_delta_s11_le":0.05,"max_abs_delta_zactive_ohm_le":10.0,
                                "no_new_severe_alert":True},"benign_gate_pass":benign}
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    print(("PASS" if numerical["pass"] else "HOLD")+"_R1E1A3_"+variant+"_"+state+"_SOLVE")
    print("BENIGN_GATE_PASS="+str(benign)); print(json.dumps(comp,sort_keys=True))
    print("RESULT_SHA256="+summary["result_sha256"])

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True); ap.add_argument("--source-cst",required=True)
    ap.add_argument("--source-sha",required=True); ap.add_argument("--variant",required=True,choices=["S1_BONDED","S4_PEC"])
    ap.add_argument("--state",required=True,choices=sorted(STATE_REF))
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work,a.source_cst,a.source_sha,a.variant,a.state)

