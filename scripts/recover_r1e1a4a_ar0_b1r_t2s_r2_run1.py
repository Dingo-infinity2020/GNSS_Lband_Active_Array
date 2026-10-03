from __future__ import print_function
import argparse, csv, json, math, cmath, hashlib, re, sys
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
from cst.results import ProjectFile

RUN_ID=1

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def wrap_deg(x):
    while x>180: x-=360
    while x<=-180: x+=360
    return x

def db(z): return 20*math.log10(max(abs(z),1e-300))

def read(cst):
    pf=ProjectFile(str(cst),allow_interactive=True)
    p3=pf.get_3d(); tree=p3.get_tree_items()
    out={}
    paths={}
    for i in (1,2,3):
        for j in (1,2,3):
            item=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            if item not in tree: raise RuntimeError("missing "+item)
            ids=p3.get_run_ids(item,False)
            if RUN_ID not in ids: raise RuntimeError("run id 1 missing for "+item)
            rows=p3.get_result_item(item,RUN_ID).get_data()
            out["S%d%d"%(i,j)]=[(float(r[0]),complex(r[1])) for r in rows]
            paths["S%d%d"%(i,j)]={"path":item,"run_ids":ids,"selected_run_id":RUN_ID,"points":len(rows)}
    conv=r"1D Results\Convergence\S-Parameters\All S-Parameters"
    if conv not in tree: raise RuntimeError("missing convergence path")
    ids=p3.get_run_ids(conv,False)
    seq=[{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)}
         for r in p3.get_result_item(conv,RUN_ID).get_data()]
    return out,tree,paths,seq

def calc(data):
    freqs=[r[0] for r in data["S11"]]
    rows=[]
    for k,f in enumerate(freqs):
        s11=data["S11"][k][1]; a=data["S21"][k][1]; b=data["S31"][k][1]
        ma=max(abs(a),1e-300); mb=max(abs(b),1e-300)
        amp=abs(20*math.log10(ma/mb))
        ph=abs(wrap_deg((math.degrees(cmath.phase(a))-math.degrees(cmath.phase(b)))-180.0))
        d=(a-b)/math.sqrt(2.0); c=(a+b)/math.sqrt(2.0)
        cmr=20*math.log10(max(abs(c),1e-300)/max(abs(d),1e-300))
        rr=abs(s11)**2; tt=abs(a)**2+abs(b)**2; pp=rr+tt
        eta=tt/max(1-rr,1e-15)
        loss=-10*math.log10(max(eta,1e-300))
        rows.append({
          "f_GHz":f,"S11_dB":db(s11),"S21_dB":db(a),"S31_dB":db(b),
          "S21_phase_deg":math.degrees(cmath.phase(a)),
          "S31_phase_deg":math.degrees(cmath.phase(b)),
          "amp_imbalance_dB":amp,"phase_error_deg":ph,"CMR_dB":cmr,
          "power_closure":pp,"transmitted_power":tt,
          "mismatch_normalized_eta":eta,"normalized_excess_loss_dB":loss
        })
    return rows

def summarize(rows,seq):
    lo,hi=1.15,1.65
    core=[r for r in rows if lo<=r["f_GHz"]<=hi]
    refs={}
    for name,f0 in (("L5",1.17645),("L2",1.22760),("L1",1.57542)):
        refs[name]=min(rows,key=lambda r:abs(r["f_GHz"]-f0))
    corem={
      "worst_S11_dB":max(r["S11_dB"] for r in core),
      "best_S11_dB":min(r["S11_dB"] for r in core),
      "worst_amp_imbalance_dB":max(r["amp_imbalance_dB"] for r in core),
      "worst_phase_error_deg":max(r["phase_error_deg"] for r in core),
      "worst_CMR_dB":max(r["CMR_dB"] for r in core),
      "best_CMR_dB":min(r["CMR_dB"] for r in core),
      "worst_normalized_excess_loss_dB":max(r["normalized_excess_loss_dB"] for r in core),
      "min_power_closure":min(r["power_closure"] for r in core),
      "max_power_closure":max(r["power_closure"] for r in core),
      "min_transmitted_power":min(r["transmitted_power"] for r in core),
      "max_transmitted_power":max(r["transmitted_power"] for r in core)
    }
    diag={
      "return_preferred":corem["worst_S11_dB"]<=-15,
      "return_acceptable":corem["worst_S11_dB"]<=-10,
      "amp_preferred":corem["worst_amp_imbalance_dB"]<=0.25,
      "amp_acceptable":corem["worst_amp_imbalance_dB"]<=0.50,
      "phase_preferred":corem["worst_phase_error_deg"]<=5,
      "phase_acceptable":corem["worst_phase_error_deg"]<=10,
      "cmr_preferred":corem["worst_CMR_dB"]<=-20,
      "cmr_acceptable":corem["worst_CMR_dB"]<=-15,
      "loss_preferred":corem["worst_normalized_excess_loss_dB"]<=0.20,
      "loss_acceptable":corem["worst_normalized_excess_loss_dB"]<=0.50,
      "strong_return_concern":corem["worst_S11_dB"]>-3,
      "loss_concern":corem["worst_normalized_excess_loss_dB"]>1.0,
      "passivity_closure_reasonable":corem["max_power_closure"]<=1.02
    }
    if all(diag[k] for k in ("return_preferred","amp_preferred","phase_preferred","cmr_preferred","loss_preferred")):
        verdict="PREFERRED"
    elif all(diag[k] for k in ("return_acceptable","amp_acceptable","phase_acceptable","cmr_acceptable","loss_acceptable")):
        verdict="ACCEPTABLE"
    elif diag["strong_return_concern"] or diag["loss_concern"] or not diag["passivity_closure_reasonable"]:
        verdict="STRONG_CONCERN"
    else:
        verdict="NEEDS_OPTIMIZATION"
    numerical=(len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02)
    return {
      "decision_band_GHz":[lo,hi],"reference_samples":refs,"core":corem,
      "diagnostics":diag,"scientific_verdict":verdict,
      "adaptive_delta_sequence":seq,"numerical_pass":numerical,
      "passes_executed":seq[-1]["pass"] if seq else None,
      "final_two_delta_s":[seq[-2]["delta_s"],seq[-1]["delta_s"]] if len(seq)>=2 else None
    }

def native(cst):
    result=Path(cst).with_suffix("")/"Result"
    text=""
    for name in ("output.txt","Model.log"):
        p=result/name
        if p.exists():
            text+="\n"+p.read_text(encoding="utf-8",errors="ignore")
    warnings=[x.strip() for x in text.splitlines() if "warning" in x.lower()]
    errors=[x.strip() for x in text.splitlines() if "*** Error ***" in x or re.search(r"\berror\b",x,re.I)]
    return {
      "warnings":warnings[-50:],
      "errors":errors[-50:],
      "port_2_3_bad_conductor_warning_present":"Ports 2, 3" in text and "not connected to any good conductor" in text,
      "mesh_corruption_present":"mesh near the lumped element" in text.lower(),
      "large_reflection_warning_present":"input reflection seems to be large" in text.lower()
    }

def main(cst,outdir):
    cst=Path(cst); outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    data,tree,paths,seq=read(cst)
    rows=calc(data)
    metrics=summarize(rows,seq)
    nat=native(cst)
    with (outdir/"t2s_r2_run1_metrics.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    characterized=(metrics["numerical_pass"] and metrics["diagnostics"]["passivity_closure_reasonable"]
                   and not nat["port_2_3_bad_conductor_warning_present"]
                   and not nat["mesh_corruption_present"])
    status="PASS_R1E1A4A_AR0_B1R_T2S_R2_NW_BASELINE_CHARACTERIZED" if characterized else "HOLD_R1E1A4A_AR0_B1R_T2S_R2_READONLY_QUALIFICATION"
    out={
      "status":status,
      "recovery_type":"RESULT_READER_ONLY_EXPLICIT_RUN_ID_1",
      "formal_solver_rerun":False,
      "selected_run_id":RUN_ID,
      "artifact_sha256":sha(cst),
      "sparameter_paths":paths,
      "metrics":metrics,
      "native_log_checks":nat,
      "scientific_verdict":metrics["scientific_verdict"],
      "original_reader_hold":"HOLD_R1E1A4A_AR0_B1R_T2S_R2_NO_VALID_RESULTS"
    }
    (outdir/"recovery_summary.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    (outdir/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status); print(json.dumps(out,indent=2))

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--cst",required=True); ap.add_argument("--outdir",required=True)
    a=ap.parse_args(); main(a.cst,a.outdir)
