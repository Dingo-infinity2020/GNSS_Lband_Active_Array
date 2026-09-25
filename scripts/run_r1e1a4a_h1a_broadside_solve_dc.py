"""R1E1A4A-H1A one-shot broadside mixed-mode solve harness."""
from __future__ import print_function
import argparse,csv,json,math,os,shutil,sys

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
for _p in (HERE,ROOT):
    if _p not in sys.path: sys.path.insert(0,_p)
from run_r1e1a4a_h0_p1_broadside_solve_dc import (
    ci,sha,macro_body,snapshot_tree,restore_snapshot,audit_vba,parse_kv,
    read_2port,mixed_row,write_complex_csv,parse_native,load_p0,compare_p0,gate_r,SPATH
)
from circuit.qpl9547.r1e1a4a_h0_p1_receiver_shadow_readonly import load_noise,noise

SOURCE_SHA="b903d678a7039105ad4d91bea2f82e9c1e5e9f8bbf5a5977360c85e34ced3b94"
SCI_LO=1.15; SCI_HI=1.65

def load_mixed_csv(path):
    rows=[]
    with open(path,newline="") as f:
        for r in csv.DictReader(f):
            z=lambda k: complex(float(r[k+"_re"]),float(r[k+"_im"]))
            rows.append({"freq_ghz":float(r["freq_ghz"]),"sdd":z("sdd"),"zdd":z("zdd"),
                         "zb1":z("zb1"),"zb2":z("zb2")})
    return rows

def compare_rows(rows,ref,key):
    vals=[]
    for r in rows:
        f=r["freq_ghz"]
        if not SCI_LO<=f<=SCI_HI: continue
        q=min(ref,key=lambda x:abs(x["freq_ghz"]-f))
        vals.append((f,abs(r[key]-q[key])))
    m=max(vals,key=lambda x:x[1])
    return {"sample_count":len(vals),"max_abs_delta":m[1],"max_abs_delta_freq_ghz":m[0],
            "rms_abs_delta":math.sqrt(sum(x[1]*x[1] for x in vals)/len(vals))}

def receiver_shadow(rows):
    tab=load_noise(); out={"limit_db":0.40,"branches":{}}
    for label,key in (("P1A","zb1"),("P1B","zb2")):
        vals=[]
        for r in rows:
            f=r["freq_ghz"]
            if SCI_LO<=f<=SCI_HI:
                n=noise(r[key],f,tab)
                vals.append((f,n))
        mx=max(vals,key=lambda x:x[1]["nf_db"]); mn=min(vals,key=lambda x:x[1]["nf_db"])
        fail=[x for x in vals if x[1]["nf_db"]>0.40]
        out["branches"][label]={"nf_db_min":mn[1]["nf_db"],"nf_db_min_freq_ghz":mn[0],
          "nf_db_max":mx[1]["nf_db"],"nf_db_max_freq_ghz":mx[0],
          "fail_count":len(fail),"fail_fraction":len(fail)/len(vals),
          "fail_freq_min_ghz":fail[0][0] if fail else None,
          "fail_freq_max_ghz":fail[-1][0] if fail else None,
          "pass":len(fail)==0}
    out["pass"]=all(v["pass"] for v in out["branches"].values())
    return out

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_R1E1A4A_H1A_SOLVE_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_R1E1A4A_H1A_SOLVE_WORK_EXISTS")
    if sha(source).lower()!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A4A_H1A_SOLVE_SOURCE_HASH_MISMATCH")
    cfg=os.path.join(repo,"source","cst","R1E1A4A_H1A_BROADSIDE_SOLVER_CONFIG_V01.mcr")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H1A_BROADSIDE_SOLVE_V01.cst")
    shutil.copy2(source,dst)
    if sha(dst).lower()!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A4A_H1A_SOLVE_COPY_HASH_MISMATCH")

    protected=[]
    for rel in ("evidence/r1e1a4a_h1a_nw_20260925_build01",
                "evidence/r1e1a1_dc_nw_20260924_build01/P094"):
        protected += snapshot_tree(os.path.join(repo,rel))
    rewrites=[]
    pre=os.path.join(evidence,"pre_solver_status.txt")

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E1A4A H1A broadside solver configuration",macro_body(cfg))
        prj.modeler.add_to_history("R1E1A4A H1A pre-solver audit",audit_vba(pre))
        prj.save()
        st=parse_kv(pre)
        ok=(int(st["SHAPE_COUNT"])==4 and int(st["PORT_COUNT"])==2 and
            abs(float(st["THETA"]))<1e-9 and
            abs(float(st["DS1"])-94)<1e-6 and abs(float(st["DS2"])-94)<1e-6 and
            all(st["P%d_TYPE"%i].lower()=="sparameter" and
                abs(float(st["P%d_ZREF"%i])-50)<1e-9 for i in (1,2)))
        if not ok: raise RuntimeError("HOLD_R1E1A4A_H1A_PRE_SOLVER_METADATA")
        prj.modeler.run_solver()
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()
        rewrites=restore_snapshot(protected)

    raw,tree=read_2port(dst)
    rows=[mixed_row(f,v) for f,v in raw]
    mixed=os.path.join(evidence,"mixed_mode_2port.csv")
    write_complex_csv(mixed,rows)
    native=parse_native(dst)
    numerical={"all_four_s_present":all(p in tree for p in SPATH.values()),
      "nonempty":len(rows)>0,"last_two_delta_s":native["last_two_below_0p02"],
      "desired_accuracy":native["desired_accuracy"],"not_maxpasses":not native["maxpasses"],
      "broadband_converged":native["broadband_converged"],"no_error_lines":len(native["errors"])==0}
    numerical["pass"]=all(numerical.values())
    p0,_=load_p0(repo); p0comp=compare_p0(rows,p0); gr=gate_r(rows)
    h0ref=load_mixed_csv(os.path.join(repo,"evidence","r1e1a4a_h0_p1_b0_nw_20260925_solve01","mixed_mode_2port_readonly.csv"))
    h0comp={"sdd":compare_rows(rows,h0ref,"sdd"),"zdd":compare_rows(rows,h0ref,"zdd")}
    nf=receiver_shadow(rows)
    summary={"source_sha256":SOURCE_SHA,"result_cst":dst,"result_sha256":sha(dst),
      "result_bytes":os.path.getsize(dst),"protected_evidence_rewrites_detected":rewrites,
      "native":native,"numerical_checks":numerical,"gate_r_mixed_mode":gr,
      "comparison_vs_p0":p0comp,"comparison_vs_h0":h0comp,"receiver_shadow":nf}
    summary["canonical_pass"]=numerical["pass"] and gr["pass"] and nf["pass"]
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    print(("PASS" if numerical["pass"] else "HOLD")+"_R1E1A4A_H1A_BROADSIDE_SOLVE")
    print("MIXED_MODE_PASS="+str(gr["pass"]))
    print("R_NF0_PASS="+str(nf["pass"]))
    print("CANONICAL_PASS="+str(summary["canonical_pass"]))
    print(json.dumps(nf,sort_keys=True))
    print(json.dumps(p0comp,sort_keys=True))
    print(json.dumps(h0comp,sort_keys=True))
    print("RESULT_SHA256="+summary["result_sha256"])

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True); ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work,a.source_cst)
