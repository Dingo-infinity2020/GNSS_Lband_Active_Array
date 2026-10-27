from __future__ import print_function
import argparse, csv, json, math, cmath
from pathlib import Path
from cst.results import ProjectFile

def wrap_deg(x):
    while x>180: x-=360
    while x<=-180: x+=360
    return x

def read(cst):
    pf=ProjectFile(str(cst),allow_interactive=True)
    p3=pf.get_3d(); tree=p3.get_tree_items()
    out={}
    for i in (1,2,3):
        for j in (1,2,3):
            item=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            if item not in tree: raise RuntimeError("missing "+item)
            rows=[]
            for row in p3.get_result_item(item).get_data():
                rows.append((float(row[0]),complex(row[1])))
            out["S%d%d"%(i,j)]=rows
    return out,tree

def nearest(vals,f0):
    return min(vals,key=lambda x:abs(x[0]-f0))

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
        r=abs(s11)**2; t=abs(a)**2+abs(b)**2; p=r+t
        eta=t/max(1-r,1e-15)
        loss=-10*math.log10(max(eta,1e-300))
        rows.append({"f_GHz":f,"S11_dB":20*math.log10(max(abs(s11),1e-300)),
                     "S21_dB":20*math.log10(ma),"S31_dB":20*math.log10(mb),
                     "S21_phase_deg":math.degrees(cmath.phase(a)),"S31_phase_deg":math.degrees(cmath.phase(b)),
                     "amp_imbalance_dB":amp,"phase_error_deg":ph,"CMR_dB":cmr,
                     "power_closure":p,"transmitted_power":t,"mismatch_normalized_eta":eta,"normalized_excess_loss_dB":loss})
    return rows

def max_in(rows,key,lo,hi): return max(r[key] for r in rows if lo<=r["f_GHz"]<=hi)
def min_in(rows,key,lo,hi): return min(r[key] for r in rows if lo<=r["f_GHz"]<=hi)

def read_adaptive(cst,tree):
    pf=ProjectFile(str(cst),allow_interactive=True)
    p3=pf.get_3d()
    delta_paths=[x for x in tree if "Adaptive Meshing" in x and x.endswith(r"Delta\All S-Parameters")]
    mesh_paths=[x for x in tree if "Adaptive Meshing" in x and x.endswith(r"Meshcells")]
    seq=[]; mesh=[]
    if delta_paths:
        d=p3.get_result_item(delta_paths[-1]).get_data()
        seq=[{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)} for r in d]
    if mesh_paths:
        m=p3.get_result_item(mesh_paths[-1]).get_data()
        mesh=[{"pass":int(round(float(r[0]))),"cells":int(round(float(complex(r[1]).real)))} for r in m]
    return {"delta_path":delta_paths[-1] if delta_paths else None,
            "mesh_path":mesh_paths[-1] if mesh_paths else None,
            "delta_sequence":seq,"meshcells":mesh}

def main(cst,outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    data,tree=read(cst); rows=calc(data)
    adaptive=read_adaptive(cst,tree)
    with (outdir/"t2s_metrics.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    lo,hi=1.15,1.65
    samples={}
    for name,f0 in (("L5",1.17645),("L2",1.22760),("L1",1.57542)):
        r=min(rows,key=lambda q:abs(q["f_GHz"]-f0)); samples[name]=r
    core={
      "worst_S11_dB":max_in(rows,"S11_dB",lo,hi),
      "worst_amp_imbalance_dB":max_in(rows,"amp_imbalance_dB",lo,hi),
      "worst_phase_error_deg":max_in(rows,"phase_error_deg",lo,hi),
      "worst_CMR_dB":max_in(rows,"CMR_dB",lo,hi),
      "worst_normalized_excess_loss_dB":max_in(rows,"normalized_excess_loss_dB",lo,hi),
      "min_power_closure":min_in(rows,"power_closure",lo,hi),
      "max_power_closure":max_in(rows,"power_closure",lo,hi)
    }
    diag={
      "return_preferred":core["worst_S11_dB"]<=-15,
      "return_acceptable":core["worst_S11_dB"]<=-10,
      "amp_preferred":core["worst_amp_imbalance_dB"]<=0.25,
      "amp_acceptable":core["worst_amp_imbalance_dB"]<=0.50,
      "phase_preferred":core["worst_phase_error_deg"]<=5,
      "phase_acceptable":core["worst_phase_error_deg"]<=10,
      "cmr_preferred":core["worst_CMR_dB"]<=-20,
      "cmr_acceptable":core["worst_CMR_dB"]<=-15,
      "loss_preferred":core["worst_normalized_excess_loss_dB"]<=0.20,
      "loss_acceptable":core["worst_normalized_excess_loss_dB"]<=0.50,
      "strong_return_concern":core["worst_S11_dB"]>-3,
      "loss_concern":core["worst_normalized_excess_loss_dB"]>1.0,
      "passivity_closure_reasonable":core["max_power_closure"]<=1.02
    }
    if all(diag[k] for k in ("return_preferred","amp_preferred","phase_preferred","cmr_preferred","loss_preferred")):
        verdict="PREFERRED"
    elif all(diag[k] for k in ("return_acceptable","amp_acceptable","phase_acceptable","cmr_acceptable","loss_acceptable")):
        verdict="ACCEPTABLE"
    elif diag["strong_return_concern"] or diag["loss_concern"] or not diag["passivity_closure_reasonable"]:
        verdict="STRONG_CONCERN"
    else:
        verdict="NEEDS_OPTIMIZATION"
    seq=adaptive["delta_sequence"]
    numerical_pass=(len(seq)>=2 and seq[-1]["delta_s"]<=0.02 and seq[-2]["delta_s"]<=0.02)
    out={"decision_band_GHz":[lo,hi],"reference_samples":samples,"core":core,"diagnostics":diag,"scientific_verdict":verdict,
         "sparameter_tree_present":all((r"1D Results\S-Parameters\S%d,%d"%(i,j)) in tree for i in (1,2,3) for j in (1,2,3)),
         "adaptive":adaptive,
         "numerical_pass":numerical_pass,
         "passes_executed":adaptive["meshcells"][-1]["pass"] if adaptive["meshcells"] else (seq[-1]["pass"] if seq else None),
         "final_two_delta_s":[seq[-2]["delta_s"],seq[-1]["delta_s"]] if len(seq)>=2 else None}
    (outdir/"t2s_metrics_summary.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--cst",required=True); ap.add_argument("--outdir",required=True)
    a=ap.parse_args(); main(a.cst,a.outdir)
