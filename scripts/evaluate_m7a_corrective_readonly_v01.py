from __future__ import print_function
import csv, json, math, sys, traceback
from pathlib import Path

SOURCE_PORTS=(1,2,4,5,7,8,10,11)
ALL_ROWS=tuple(range(1,13))
CORE=(1.15,1.65)
S2=1.0/math.sqrt(2.0)
T=[[S2,-S2,0,0],[S2,S2,0,0],[0,0,S2,-S2],[0,0,S2,S2]]
POL={"PolA":{"c":[1,2,4,5],"b":[1,2,4,5]},
     "PolB":{"c":[7,8,10,11],"b":[1,2,4,5]}}

def db(z): return 20.0*math.log10(max(abs(z),1e-300))
def matmul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(x) for x in zip(*a)]

def read96(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]; d={}
    for j in SOURCE_PORTS:
      for i in ALL_ROWS:
        k="S%d_%d"%(i,j)
        d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
    return f,d

def read16(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]; d={}
    for j in (1,2,4,5):
      for i in (1,2,4,5):
        k="S%d%d"%(i,j)
        d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
    return f,d

def interp(xs,ys,x):
    if x<xs[0]-1e-10 or x>xs[-1]+1e-10: raise RuntimeError("HOLD_M7A_EXTRAPOLATION")
    if x<=xs[0]+1e-15:return ys[0]
    if x>=xs[-1]-1e-15:return ys[-1]
    lo=0;hi=len(xs)-1
    while hi-lo>1:
      mid=(lo+hi)//2
      if xs[mid]<=x:lo=mid
      else:hi=mid
    a=(x-xs[lo])/(xs[hi]-xs[lo])
    return ys[lo]+a*(ys[hi]-ys[lo])

def interp_set(sf,sd,tf):
    return {k:[interp(sf,v,x) for x in tf] for k,v in sd.items()}

def mixed(d,k,ports):
    ep,pp,en,pn=ports; order=[ep,en,pp,pn]
    s=[[d[(i,j)][k] for j in order] for i in order]
    return matmul(matmul(T,s),tr(T))

def mode_dc(d,k,ports): return mixed(d,k,ports)[1][0]

def nearest(freqs,x): return min(range(len(freqs)),key=lambda k:abs(freqs[k]-x))

def own_delta(d,b,cp,bp,idx):
    best=0.0
    for ci,bi in zip(cp,bp):
      for cj,bj in zip(cp,bp):
        for k in idx: best=max(best,abs(d[(ci,cj)][k]-b[(bi,bj)][k]))
    return best

def imbalance(d,k,ep,en): return abs(db(d[(ep,ep)][k])-db(d[(en,en)][k]))

def local_excursion_guard(cand,full,freqs,max_new=6.0,width=0.05):
    idx=[k for k,f in enumerate(freqs) if CORE[0]-1e-12<=f<=CORE[1]+1e-12]
    worst={"new_excursion_db":-1e99}
    for j in SOURCE_PORTS:
      for i in ALL_ROWS:
        if i==j: continue
        cv=[db(cand[(i,j)][k]) for k in idx]; fv=[db(full[(i,j)][k]) for k in idx]
        b=0
        for a in range(len(idx)):
          if b<a:b=a
          while b+1<len(idx) and freqs[idx[b+1]]-freqs[idx[a]]<=width+1e-12:b+=1
          if b<=a:continue
          ce=max(cv[a:b+1])-min(cv[a:b+1]); fe=max(fv[a:b+1])-min(fv[a:b+1])
          gain=ce-fe
          if gain>worst["new_excursion_db"]:
            worst={"new_excursion_db":gain,"candidate_excursion_db":ce,"full_excursion_db":fe,
                   "f_start_ghz":freqs[idx[a]],"f_end_ghz":freqs[idx[b]],
                   "response_port":i,"source_port":j}
    worst["pass"]=worst["new_excursion_db"]<=max_new
    return worst

def main(candidate_csv,manifest_path,numerical_summary,evidence):
    candidate_csv=Path(candidate_csv); manifest_path=Path(manifest_path)
    numerical_summary=Path(numerical_summary); evidence=Path(evidence); evidence.mkdir(parents=True,exist_ok=True)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    num=json.loads(numerical_summary.read_text(encoding="utf-8"))
    numerical_pass=all(num["hard_checks"].values())

    cf,cd=read96(candidate_csv)
    ff,fd=read96(Path(m["full_e2c_reference"]["response_csv"]))
    # Compare on immutable full-E2C 1001 point grid; interpolation is read-only if candidate differs.
    if len(cf)!=len(ff) or any(abs(a-b)>1e-9 for a,b in zip(cf,ff)):
        cd=interp_set(cf,cd,ff); cf=ff
        comparison_grid="candidate complex responses linearly interpolated onto full-E2C grid"
    else: comparison_grid="native grids identical"
    idx=[k for k,f in enumerate(ff) if CORE[0]-1e-12<=f<=CORE[1]+1e-12]

    polout={}
    primary_reductions=[]
    for pol in ("PolA","PolB"):
      bm=m["isolated_baselines"][pol]; bf,bd=read16(Path(bm["csv_path"]))
      if len(bf)!=len(ff) or any(abs(a-b)>1e-9 for a,b in zip(bf,ff)):
        bd=interp_set(bf,bd,ff); bf=ff
      cp=POL[pol]["c"]; bp=POL[pol]["b"]
      # Freeze mode anchor from full-E2C itself: peak |E_diff->common| in core.
      ak=max(idx,key=lambda k:abs(mode_dc(fd,k,cp)))
      anchor=ff[ak]
      full_deg=db(mode_dc(fd,ak,cp))-db(mode_dc(bd,ak,bp))
      cand_deg=db(mode_dc(cd,ak,cp))-db(mode_dc(bd,ak,bp))
      mode_red=(full_deg-cand_deg)/full_deg if full_deg>1e-12 else 0.0

      ik=nearest(ff,float(m["full_e2c_reference"]["imbalance_anchor_ghz"]))
      full_imb=imbalance(fd,ik,cp[0],cp[2]); cand_imb=imbalance(cd,ik,cp[0],cp[2])
      imb_red=(full_imb-cand_imb)/full_imb if full_imb>1e-12 else 0.0

      fraw=own_delta(fd,bd,cp,bp,idx); craw=own_delta(cd,bd,cp,bp,idx)
      raw_red=(fraw-craw)/fraw if fraw>1e-12 else 0.0
      polout[pol]={
        "mode_anchor_ghz":anchor,"full_mode_degradation_db":full_deg,
        "candidate_mode_degradation_db":cand_deg,"mode_reduction_fraction":mode_red,
        "imbalance_anchor_ghz":ff[ik],"full_imbalance_db":full_imb,
        "candidate_imbalance_db":cand_imb,"imbalance_reduction_fraction":imb_red,
        "full_own_pol_max_complex_delta":fraw,"candidate_own_pol_max_complex_delta":craw,
        "raw_reduction_fraction":raw_red
      }
      primary_reductions += [mode_red,imb_red]

    worst_full_raw=max(polout[p]["full_own_pol_max_complex_delta"] for p in polout)
    worst_cand_raw=max(polout[p]["candidate_own_pol_max_complex_delta"] for p in polout)
    secondary_red=(worst_full_raw-worst_cand_raw)/worst_full_raw
    primary_pass=min(primary_reductions)>=float(m["corrective_gate"]["primary"]["minimum_reduction_fraction"])
    secondary_pass=secondary_red>=float(m["corrective_gate"]["secondary"]["minimum_reduction_fraction"])
    guard=local_excursion_guard(cd,fd,ff,float(m["corrective_gate"]["guard"]["max_new_excursion_db"]),
                                 float(m["corrective_gate"]["guard"]["window_mhz"])/1000.0)
    if not numerical_pass: status="HOLD_M7A_NUMERICAL"
    elif not guard["pass"]: status="HOLD_M7A_CORRECTIVE_GUARD"
    elif primary_pass: status="PASS_M7A_CORRECTIVE"
    elif max(primary_reductions)>=0.10 or secondary_pass: status="REVIEW_M7A_PARTIAL_CORRECTION"
    else: status="REJECT_M7A_INNER_EDGE_LEVER"

    out={"schema_version":"gnss-m7a-corrective-evaluation-v0.1","status":status,
         "numerical_pass":numerical_pass,"comparison_grid":comparison_grid,
         "primary_pass":primary_pass,"secondary_pass":secondary_pass,"guard_pass":guard["pass"],
         "polarizations":polout,
         "secondary":{"worst_full_raw_delta":worst_full_raw,"worst_candidate_raw_delta":worst_cand_raw,
                      "reduction_fraction":secondary_red},
         "guard":guard,
         "boundary":"No M7B BUILD or further SOLVE is authorized by this result."}
    (evidence/"corrective_evaluation.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status); print(json.dumps(out,indent=2))
    return 0 if numerical_pass else 4

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--candidate-csv",required=True); ap.add_argument("--manifest",required=True)
    ap.add_argument("--numerical-summary",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.candidate_csv,a.manifest,a.numerical_summary,a.evidence))
    except Exception:
      Path(a.evidence).mkdir(parents=True,exist_ok=True)
      Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
      traceback.print_exc(); sys.exit(9)
