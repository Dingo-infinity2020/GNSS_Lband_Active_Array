"""R1E1A4A H0/P1 one-shot broadside 2-port mixed-mode solve harness."""
from __future__ import print_function
import argparse,csv,hashlib,json,math,os,re,shutil,sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="d1ebb6f4a6e8b48f3484cc5459790dd5c9bbd29482832c491076c84f783b3deb"
SCI_LO=1.15; SCI_HI=1.65
ZSE=50.0; ZDIFF=100.0
SPATH={(1,1):r"1D Results\S-Parameters\S1(1),1(1)",
       (1,2):r"1D Results\S-Parameters\S1(1),2(1)",
       (2,1):r"1D Results\S-Parameters\S2(1),1(1)",
       (2,2):r"1D Results\S-Parameters\S2(1),2(1)"}

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def macro_body(path):
    lines=open(path,encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=lines.index("Sub Main()"); e=lines.index("End Sub")
    return "\n".join(lines[s+1:e])

def snapshot_tree(root):
    snap=[]
    if not os.path.isdir(root): return snap
    for d,_,files in os.walk(root):
        for name in files:
            p=os.path.join(d,name)
            with open(p,"rb") as f: snap.append((p,f.read()))
    return snap

def restore_snapshot(snap):
    changed=[]
    for path,data in snap:
        cur=None
        if os.path.isfile(path):
            with open(path,"rb") as f: cur=f.read()
        if cur!=data: changed.append(path)
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,"wb") as f: f.write(data)
    for path,data in snap:
        with open(path,"rb") as f:
            if f.read()!=data: raise RuntimeError("HOLD_R1E1A4A_EVIDENCE_RESTORE_FAILED:"+path)
    return changed

def audit_vba(path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, th As Double, ph As Double, idir As Long, ok As Boolean",
      "Dim i As Long, stype As String, zref As Double, cur As Double, vol As Double",
      "Dim vimp As Double, rad As Double, mon As Boolean, pok As Boolean",
      "ok=Boundary.GetUnitCellScanAngle(th,ph,idir)",
      "f=FreeFile", 'Open "%s" For Output As #f'%path,
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "THETA=" & CStr(th)', 'Print #f, "PHI=" & CStr(ph)',
      'Print #f, "DS1=" & CStr(Boundary.GetUnitCellDs1)',
      'Print #f, "DS2=" & CStr(Boundary.GetUnitCellDs2)',
      "For i=1 To 2",
      " zref=0: cur=0: vol=0: vimp=0: rad=0: mon=False",
      " pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P" & CStr(i) & "_PROP_OK=" & CStr(pok)',
      ' Print #f, "P" & CStr(i) & "_TYPE=" & stype',
      ' Print #f, "P" & CStr(i) & "_ZREF=" & CStr(zref)',
      "Next i","Close #f","On Error GoTo 0"
    ])

def parse_kv(path):
    out={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k.strip()]=v.strip()
    return out

def read_2port(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    p3=pf.get_3d(); tree=p3.get_tree_items()
    data={}
    for ij,path in SPATH.items():
        if path not in tree: raise RuntimeError("HOLD_R1E1A4A_MISSING_RESULT:"+path)
        raw=p3.get_result_item(path).get_data()
        data[ij]=[(float(r[0]),complex(r[1])) for r in raw]
        if not data[ij]: raise RuntimeError("HOLD_R1E1A4A_EMPTY_RESULT:"+path)
    n=min(len(v) for v in data.values())
    rows=[]
    for k in range(n):
        f=data[(1,1)][k][0]
        vals={}
        for ij in SPATH:
            fj,z=data[ij][k]
            if abs(fj-f)>1e-9: raise RuntimeError("HOLD_R1E1A4A_FREQ_GRID_MISMATCH")
            vals[ij]=z
        rows.append((f,vals))
    return rows,tree

def inv2(m):
    a,b=m[0]; c,d=m[1]; det=a*d-b*c
    if abs(det)<1e-14: raise ZeroDivisionError("singular 2x2")
    return [[d/det,-b/det],[-c/det,a/det]]

def mmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def s_to_z(s,z0=ZSE):
    I=[[1+0j,0j],[0j,1+0j]]
    ap=[[I[i][j]+s[i][j] for j in range(2)] for i in range(2)]
    im=[[I[i][j]-s[i][j] for j in range(2)] for i in range(2)]
    x=mmul(ap,inv2(im))
    return [[z0*x[i][j] for j in range(2)] for i in range(2)]

def wrap_deg(x):
    return (x+180.0)%360.0-180.0

def mixed_row(f,v):
    s11=v[(1,1)]; s12=v[(1,2)]; s21=v[(2,1)]; s22=v[(2,2)]
    sdd=(s11-s12-s21+s22)/2.0
    sdc=(s11+s12-s21-s22)/2.0
    scd=(s11-s12+s21-s22)/2.0
    scc=(s11+s12+s21+s22)/2.0
    zdd=ZDIFF*(1+sdd)/(1-sdd) if abs(1-sdd)>1e-14 else complex(float("inf"),0)
    z=s_to_z([[s11,s12],[s21,s22]])
    zb1=z[0][0]-z[0][1]
    zb2=z[1][1]-z[1][0]
    zavg=(zb1+zb2)/2.0
    magimb=20*math.log10(max(abs(zb1),1e-300)/max(abs(zb2),1e-300))
    phaseerr=wrap_deg(math.degrees(math.atan2(zb1.imag,zb1.real)-math.atan2(zb2.imag,zb2.real)))
    return {"freq_ghz":f,"s11":s11,"s12":s12,"s21":s21,"s22":s22,
            "sdd":sdd,"sdc":sdc,"scd":scd,"scc":scc,"zdd":zdd,
            "zb1":zb1,"zb2":zb2,"zavg":zavg,
            "branch_mag_imbalance_db":magimb,"branch_phase_error_deg":phaseerr,
            "zdd_minus_2zavg":zdd-2*zavg}

def db(z): return 20*math.log10(max(abs(z),1e-300))

def write_complex_csv(path,rows):
    fields=["freq_ghz"]
    keys=("s11","s12","s21","s22","sdd","sdc","scd","scc","zdd","zb1","zb2","zavg","zdd_minus_2zavg")
    for k in keys: fields += [k+"_re",k+"_im"]
    fields += ["sdd_db","sdc_db","scd_db","scc_db","branch_mag_imbalance_db","branch_phase_error_deg"]
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in rows:
            o={"freq_ghz":r["freq_ghz"]}
            for k in keys:
                o[k+"_re"]=r[k].real; o[k+"_im"]=r[k].imag
            for k in ("sdd","sdc","scd","scc"): o[k+"_db"]=db(r[k])
            o["branch_mag_imbalance_db"]=r["branch_mag_imbalance_db"]
            o["branch_phase_error_deg"]=r["branch_phase_error_deg"]
            w.writerow(o)

def parse_native(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(p): raise RuntimeError("HOLD_R1E1A4A_OUTPUT_MISSING")
    text=open(p,encoding="utf-8",errors="ignore").read()
    cur=None; seq=[]
    for line in text.splitlines():
        m=re.search(r"Adaptive mesh refinement pass\s+(\d+)",line,re.I)
        if m: cur=int(m.group(1))
        m=re.search(r"All S-Parameters\s*=\s*([0-9eE+\-.]+)",line,re.I)
        if m and cur is not None: seq.append({"pass":cur,"delta_s":float(m.group(1))})
    return {"delta_s_sequence":seq,
      "last_two_below_0p02":len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02,
      "desired_accuracy":"desired accuracy limit is reached" in text.lower(),
      "maxpasses":"maximum number of passes is reached" in text.lower(),
      "broadband_converged":"all broadband sweep convergence criteria have been satisfied" in text.lower(),
      "errors":[x.strip() for x in text.splitlines() if "error" in x.lower()]}

def load_p0(repo):
    path=os.path.join(repo,"evidence","r1e0b_dc_nw_20260924_smoke01","active_s11_and_zactive.csv")
    out=[]
    with open(path,newline="") as f:
        for r in csv.DictReader(f):
            out.append((float(r["freq_ghz"]),complex(float(r["s11_re"]),float(r["s11_im"])),
                        complex(float(r["zactive_re_ohm"]),float(r["zactive_im_ohm"]))))
    return out,path

def compare_p0(rows,ref):
    mxs=(0,None); mxz=(0,None); ss=0; sz=0; n=0
    for r in rows:
        f=r["freq_ghz"]
        if not SCI_LO<=f<=SCI_HI: continue
        fr,s0,z0=min(ref,key=lambda x:abs(x[0]-f))
        ds=abs(r["sdd"]-s0); dz=abs(r["zdd"]-z0)
        if ds>mxs[0]: mxs=(ds,f)
        if dz>mxz[0]: mxz=(dz,f)
        ss+=ds*ds; sz+=dz*dz; n+=1
    return {"sample_count":n,"max_abs_delta_sdd_vs_p0":mxs[0],"max_abs_delta_sdd_freq_ghz":mxs[1],
            "rms_abs_delta_sdd_vs_p0":math.sqrt(ss/max(n,1)),
            "max_abs_delta_zdd_vs_p0_ohm":mxz[0],"max_abs_delta_zdd_freq_ghz":mxz[1],
            "rms_abs_delta_zdd_vs_p0_ohm":math.sqrt(sz/max(n,1))}

def gate_r(rows):
    sci=[r for r in rows if SCI_LO<=r["freq_ghz"]<=SCI_HI]
    max_sdc=max(sci,key=lambda r:abs(r["sdc"]))
    max_scd=max(sci,key=lambda r:abs(r["scd"]))
    max_mag=max(sci,key=lambda r:abs(r["branch_mag_imbalance_db"]))
    max_phase=max(sci,key=lambda r:abs(r["branch_phase_error_deg"]))
    max_zid=max(sci,key=lambda r:abs(r["zdd_minus_2zavg"]))
    g={"max_sdc_db":db(max_sdc["sdc"]),"max_sdc_freq_ghz":max_sdc["freq_ghz"],
       "max_scd_db":db(max_scd["scd"]),"max_scd_freq_ghz":max_scd["freq_ghz"],
       "max_abs_branch_mag_imbalance_db":abs(max_mag["branch_mag_imbalance_db"]),
       "max_branch_mag_imbalance_freq_ghz":max_mag["freq_ghz"],
       "max_abs_branch_phase_error_deg":abs(max_phase["branch_phase_error_deg"]),
       "max_branch_phase_error_freq_ghz":max_phase["freq_ghz"],
       "max_abs_zdd_minus_2zavg_ohm":abs(max_zid["zdd_minus_2zavg"])}
    g["mode_conversion_pass"]=g["max_sdc_db"]<=-30.0 and g["max_scd_db"]<=-30.0
    g["branch_symmetry_pass"]=g["max_abs_branch_mag_imbalance_db"]<=0.20 and g["max_abs_branch_phase_error_deg"]<=2.0
    g["virtual_ground_mapping_diagnostic"]="QUALIFIED_BY_MODE_CONVERSION_AND_BRANCH_SYMMETRY_GATES"
    g["pass"]=g["mode_conversion_pass"] and g["branch_symmetry_pass"]
    return g

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_R1E1A4A_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_R1E1A4A_WORK_EXISTS")
    if sha(source).lower()!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A4A_SOURCE_HASH_MISMATCH")
    cfg=os.path.join(repo,"source","cst","R1E1A4A_H0_P1_BROADSIDE_SOLVER_CONFIG_V01.mcr")
    if not os.path.isfile(cfg): raise RuntimeError("HOLD_R1E1A4A_SOLVER_CONFIG_MISSING")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H0_P1_BROADSIDE_SOLVE_V01.cst")
    shutil.copy2(source,dst)
    if sha(dst).lower()!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A4A_COPY_HASH_MISMATCH")

    protected=[]
    for rel in ("evidence/r1e1a4a_h0_p1_nw_20260925_build01","evidence/r1e1a1_dc_nw_20260924_build01/P094"):
        protected += snapshot_tree(os.path.join(repo,rel))
    rewrites=[]
    pre=os.path.join(evidence,"pre_solver_status.txt")
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E1A4A broadside solver configuration",macro_body(cfg))
        prj.modeler.add_to_history("R1E1A4A pre-solver audit",audit_vba(pre))
        prj.save()
        st=parse_kv(pre)
        ok=(int(st["SHAPE_COUNT"])==4 and int(st["PORT_COUNT"])==2 and
            abs(float(st["THETA"]))<1e-9 and abs(float(st["DS1"])-94)<1e-6 and abs(float(st["DS2"])-94)<1e-6 and
            all(st["P%d_TYPE"%i].lower()=="sparameter" and abs(float(st["P%d_ZREF"%i])-50)<1e-9 for i in (1,2)))
        if not ok: raise RuntimeError("HOLD_R1E1A4A_PRE_SOLVER_METADATA")
        prj.modeler.run_solver(); prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()
        rewrites=restore_snapshot(protected)

    raw,tree=read_2port(dst)
    rows=[mixed_row(f,v) for f,v in raw]
    write_complex_csv(os.path.join(evidence,"mixed_mode_2port.csv"),rows)
    native=parse_native(dst)
    numerical={"all_four_s_present":all(p in tree for p in SPATH.values()),"nonempty":len(rows)>0,
               "last_two_delta_s":native["last_two_below_0p02"],"desired_accuracy":native["desired_accuracy"],
               "not_maxpasses":not native["maxpasses"],"broadband_converged":native["broadband_converged"],
               "no_error_lines":len(native["errors"])==0}
    numerical["pass"]=all(numerical.values())
    p0,p0path=load_p0(repo); comp=compare_p0(rows,p0); gr=gate_r(rows)
    summary={"source_cst":source,"source_sha256":SOURCE_SHA,"solver_config_sha256":sha(cfg),
             "result_cst":dst,"result_sha256":sha(dst),"result_bytes":os.path.getsize(dst),
             "protected_evidence_rewrites_detected":rewrites,"protected_evidence_restored":True,
             "native":native,"numerical_checks":numerical,"p0_reference_csv":p0path,
             "comparison_vs_p0":comp,"gate_r_mixed_mode":gr,
             "gate_r_mixed_mode_pass":numerical["pass"] and gr["pass"]}
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    print(("PASS" if numerical["pass"] else "HOLD")+"_R1E1A4A_H0_P1_BROADSIDE_SOLVE")
    print("GATE_R_MIXED_MODE_PASS="+str(summary["gate_r_mixed_mode_pass"]))
    print(json.dumps(gr,sort_keys=True))
    print(json.dumps(comp,sort_keys=True))
    print("RESULT_SHA256="+summary["result_sha256"])

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True); ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work,a.source_cst)
