from __future__ import print_function
import argparse,csv,hashlib,json,math,os,shutil,sys
LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile
SOURCE_SHA="f321b678d390470a2420df40fd6d0cf6553cc041f9219bfcd011c7e41fbadf3d"

def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def macro_body(p):
    a=open(p,encoding="utf-8").read().replace("\r\n","\n").split("\n")
    return "\n".join(a[a.index("Sub Main()")+1:a.index("End Sub")])

def read_s(cst):
    p3=ProjectFile(cst,allow_interactive=True).get_3d(); out={}
    for i,j in ((1,1),(1,2),(2,1),(2,2)):
        item=r"1D Results\S-Parameters\S%d,%d"%(i,j)
        rows=p3.get_result_item(item).get_data()
        vals=[]
        for r in rows:
            f=float(r[0]); z=complex(r[1]); vals.append((f,z.real,z.imag,20*math.log10(max(abs(z),1e-300))))
        out["S%d%d"%(i,j)]=vals
    return out

def read_adapt(cst):
    p3=ProjectFile(cst,allow_interactive=True).get_3d()
    d=p3.get_result_item(r"1D Results\Adaptive Meshing\f=2\S-Parameters\Delta\All S-Parameters").get_data()
    m=p3.get_result_item(r"1D Results\Adaptive Meshing\f=2\Meshcells").get_data()
    seq=[{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)} for r in d]
    mesh=[{"pass":int(round(float(r[0]))),"cells":int(round(float(complex(r[1]).real)))} for r in m]
    return seq,mesh

def finite(data):
    for vals in data.values():
        for r in vals:
            if not all(math.isfinite(float(x)) for x in r): return False
    return True

def core_summary(data):
    out={}
    for k,vals in data.items():
        cv=[r for r in vals if 1.15-1e-9<=r[0]<=1.65+1e-9]
        out[k]={"core_db_min":min(r[3] for r in cv),"core_db_max":max(r[3] for r in cv)}
    out["reciprocity_max_abs_db"]=max(abs(a[3]-b[3]) for a,b in zip(data["S21"],data["S12"]))
    return out

def compare_prior(data,path):
    rows=list(csv.DictReader(open(path,encoding="utf-8")))
    prior={float(r["f_GHz"]):r for r in rows}
    mx=0.0
    for n,r in enumerate(data["S21"]):
        if 1.15<=r[0]<=1.65 and r[0] in prior:
            mx=max(mx,abs(r[3]-float(prior[r[0]]["S21_dB"])))
    return mx

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_WORK_EXISTS")
    if sha(source)!=SOURCE_SHA: raise RuntimeError("HOLD_SOURCE_HASH")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H3B_T01A_RECOVERY_MAXPASS16_V01.cst")
    shutil.copy2(source,dst)
    port=os.path.join(repo,"source","cst","R1E1A4A_H3B_T01A_PORTS_V01.mcr")
    sol=os.path.join(repo,"source","cst","R1E1A4A_H3B_T01A_SOLVER_CONFIG_MAXPASS16_V01.mcr")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("H3B-T01A Ports V0.1",macro_body(port))
        prj.modeler.add_to_history("H3B-T01A Recovery MaxPass16 V0.1",macro_body(sol))
        prj.save()
        prj.modeler.run_solver()
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()
    data=read_s(dst); seq,mesh=read_adapt(dst)
    last2=(len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02)
    summary=core_summary(data)
    prior=os.path.join(repo,"evidence","r1e1a4a_h3b_t01a_nw_20260925_solve01","sparams.csv")
    prior_d=compare_prior(data,prior)
    checks={
      "full_2port":all(len(v)>0 for v in data.values()),
      "finite":finite(data),
      "native_two_final_below_0p02":last2,
      "reciprocity_0p1db":summary["reciprocity_max_abs_db"]<=0.1,
      "source_hash_locked":sha(source)==SOURCE_SHA
    }
    passed=all(checks.values())
    result={
      "mode":"H3B_T01A_NUMERICAL_RECOVERY_MAXPASS16",
      "formal_solver_invocations":1,
      "source_sha256":SOURCE_SHA,
      "solved_cst":dst,
      "solved_sha256":sha(dst),
      "adaptive_delta_sequence":seq,
      "adaptive_meshcells":mesh,
      "passes_executed":mesh[-1]["pass"] if mesh else None,
      "final_two_delta_s":[seq[-2]["delta_s"],seq[-1]["delta_s"]] if len(seq)>=2 else None,
      "core_summary":summary,
      "max_core_s21_db_change_vs_maxpass8":prior_d,
      "checks":checks,
      "pass":passed
    }
    json.dump(result,open(os.path.join(evidence,"summary.json"),"w"),indent=2)
    status="PASS_R1E1A4A_H3B_T01A_NUMERICALLY_CONVERGED_MAXPASS16" if passed else "HOLD_R1E1A4A_H3B_T01A_MAXPASS16_NOT_CONVERGED"
    open(os.path.join(evidence,"FINAL_STATUS.txt"),"w").write(status+"\n")
    print(status)
    print("SOLVED_SHA256="+result["solved_sha256"])
    print(json.dumps({"passes":result["passes_executed"],"final_two_delta_s":result["final_two_delta_s"],"core_summary":summary,"max_core_s21_db_change_vs_maxpass8":prior_d},sort_keys=True))
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True); ap.add_argument("--work",required=True); ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work,a.source_cst)
