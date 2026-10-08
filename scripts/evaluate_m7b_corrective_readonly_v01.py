from __future__ import print_function
import csv,json,math,sys,traceback
from pathlib import Path
SOURCE_PORTS=(1,2,4,5,7,8,10,11);ALL_ROWS=tuple(range(1,13));CORE=(1.15,1.65);S2=1.0/math.sqrt(2.0)
T=[[S2,-S2,0,0],[S2,S2,0,0],[0,0,S2,-S2],[0,0,S2,S2]]
POL={"PolA":{"c":[1,2,4,5],"b":[1,2,4,5]},"PolB":{"c":[7,8,10,11],"b":[1,2,4,5]}}
def db(z):return 20.0*math.log10(max(abs(z),1e-300))
def matmul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a):return [list(x) for x in zip(*a)]
def read96(path):
 rows=list(csv.DictReader(open(str(path),"r",newline="")));f=[float(r["f_GHz"]) for r in rows];d={}
 for j in SOURCE_PORTS:
  for i in ALL_ROWS:
   k="S%d_%d"%(i,j);d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
 return f,d
def read16(path):
 rows=list(csv.DictReader(open(str(path),"r",newline="")));f=[float(r["f_GHz"]) for r in rows];d={}
 for j in (1,2,4,5):
  for i in (1,2,4,5):
   k="S%d%d"%(i,j);d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
 return f,d
def interp(xs,ys,x):
 if x<xs[0]-1e-10 or x>xs[-1]+1e-10:raise RuntimeError("HOLD_M7B_EXTRAPOLATION")
 if x<=xs[0]+1e-15:return ys[0]
 if x>=xs[-1]-1e-15:return ys[-1]
 lo=0;hi=len(xs)-1
 while hi-lo>1:
  mid=(lo+hi)//2
  if xs[mid]<=x:lo=mid
  else:hi=mid
 a=(x-xs[lo])/(xs[hi]-xs[lo]);return ys[lo]+a*(ys[hi]-ys[lo])
def interp_set(sf,sd,tf):return {k:[interp(sf,v,x) for x in tf] for k,v in sd.items()}
def mixed(d,k,ports):
 ep,pp,en,pn=ports;order=[ep,en,pp,pn];s=[[d[(i,j)][k] for j in order] for i in order]
 return matmul(matmul(T,s),tr(T))
def mode_dc(d,k,ports):return mixed(d,k,ports)[1][0]
def nearest(freqs,x):return min(range(len(freqs)),key=lambda k:abs(freqs[k]-x))
def own_delta_at(d,b,cp,bp,k):
 best=0.0;driver=None
 for ci,bi in zip(cp,bp):
  for cj,bj in zip(cp,bp):
   v=abs(d[(ci,cj)][k]-b[(bi,bj)][k])
   if v>best:best=v;driver={"response_port":ci,"source_port":cj}
 return best,driver
def mode_deg(d,b,k,cp,bp):return db(mode_dc(d,k,cp))-db(mode_dc(b,k,bp))
def imbalance(d,k,ep,en):return abs(db(d[(ep,ep)][k])-db(d[(en,en)][k]))
def guard(cand,full,freqs,max_new,width):
 idx=[k for k,f in enumerate(freqs) if CORE[0]-1e-12<=f<=CORE[1]+1e-12];worst={"new_excursion_db":-1e99}
 for j in SOURCE_PORTS:
  for i in ALL_ROWS:
   if i==j:continue
   cv=[db(cand[(i,j)][k]) for k in idx];fv=[db(full[(i,j)][k]) for k in idx];b=0
   for a in range(len(idx)):
    if b<a:b=a
    while b+1<len(idx) and freqs[idx[b+1]]-freqs[idx[a]]<=width+1e-12:b+=1
    if b<=a:continue
    gain=(max(cv[a:b+1])-min(cv[a:b+1]))-(max(fv[a:b+1])-min(fv[a:b+1]))
    if gain>worst["new_excursion_db"]:worst={"new_excursion_db":gain,"f_start_ghz":freqs[idx[a]],"f_end_ghz":freqs[idx[b]],"response_port":i,"source_port":j}
 worst["pass"]=worst["new_excursion_db"]<=max_new;return worst
def main(candidate_csv,manifest_path,numerical_summary,evidence):
 evidence=Path(evidence);evidence.mkdir(parents=True,exist_ok=True);m=json.loads(Path(manifest_path).read_text(encoding="utf-8"));num=json.loads(Path(numerical_summary).read_text(encoding="utf-8"));numerical_pass=all(num["hard_checks"].values())
 cf,cd=read96(Path(candidate_csv));ff,fd=read96(Path(m["full_e2c_reference"]["response_csv"]))
 if len(cf)!=len(ff) or any(abs(a-b)>1e-9 for a,b in zip(cf,ff)):cd=interp_set(cf,cd,ff);comparison_grid="candidate interpolated onto full-E2C grid"
 else:comparison_grid="native grids identical"
 bases={}
 for pol in ("PolA","PolB"):
  bf,bd=read16(Path(m["isolated_baselines"][pol]["csv_path"]))
  if len(bf)!=len(ff) or any(abs(a-b)>1e-9 for a,b in zip(bf,ff)):bd=interp_set(bf,bd,ff)
  bases[pol]=bd
 rk=nearest(ff,float(m["corrective_gate"]["primary"]["raw"]["anchor_ghz"]));raw={}
 for pol in ("PolA","PolB"):
  cp=POL[pol]["c"];bp=POL[pol]["b"];fv,fdri=own_delta_at(fd,bases[pol],cp,bp,rk);cv,cdri=own_delta_at(cd,bases[pol],cp,bp,rk);raw[pol]={"full_delta":fv,"candidate_delta":cv,"full_driver":fdri,"candidate_driver":cdri}
 full_raw=max(v["full_delta"] for v in raw.values());cand_raw=max(v["candidate_delta"] for v in raw.values());raw_red=(full_raw-cand_raw)/full_raw if full_raw>1e-15 else 0.0;raw_pass=raw_red>=m["corrective_gate"]["primary"]["raw"]["minimum_reduction_fraction"]
 mb=m["corrective_gate"]["primary"]["mode"]["search_band_ghz"];midx=[k for k,f in enumerate(ff) if mb[0]<=f<=mb[1]];sev=None
 for pol in ("PolA","PolB"):
  cp=POL[pol]["c"];bp=POL[pol]["b"]
  for k in midx:
   v=mode_deg(fd,bases[pol],k,cp,bp)
   if sev is None or v>sev["full_db"]:sev={"pol":pol,"k":k,"frequency_ghz":ff[k],"full_db":v}
 pol=sev["pol"];k=sev["k"];cand_mode=mode_deg(cd,bases[pol],k,POL[pol]["c"],POL[pol]["b"]);mode_red_db=sev["full_db"]-cand_mode;mode_red_frac=mode_red_db/abs(sev["full_db"]) if abs(sev["full_db"])>1e-12 else 0.0;mode_pass=mode_red_db>=m["corrective_gate"]["primary"]["mode"]["minimum_reduction_db"]
 ik=nearest(ff,float(m["corrective_gate"]["secondary"]["anchor_ghz"]));imb={}
 for pol in ("PolA","PolB"):
  cp=POL[pol]["c"];imb[pol]={"full_db":imbalance(fd,ik,cp[0],cp[2]),"candidate_db":imbalance(cd,ik,cp[0],cp[2])}
 full_imb=max(v["full_db"] for v in imb.values());cand_imb=max(v["candidate_db"] for v in imb.values());imb_red=(full_imb-cand_imb)/full_imb if full_imb>1e-12 else 0.0;secondary_pass=imb_red>=m["corrective_gate"]["secondary"]["minimum_reduction_fraction"]
 gd=guard(cd,fd,ff,m["corrective_gate"]["guard"]["max_new_excursion_db"],m["corrective_gate"]["guard"]["window_mhz"]/1000.0);primary_pass=raw_pass and mode_pass;rf=m["corrective_gate"]["falsification"]["maximum_primary_fraction_for_reject"]
 if not numerical_pass:status="HOLD_M7B_NUMERICAL"
 elif not gd["pass"]:status="HOLD_M7B_CORRECTIVE_GUARD"
 elif primary_pass:status="PASS_M7B_CORRECTIVE"
 elif raw_red<rf and mode_red_frac<rf and not secondary_pass:status="REJECT_M7B_CIN_SHUNT_LEVER"
 else:status="REVIEW_M7B_PARTIAL_CORRECTION"
 out={"schema_version":"gnss-m7b-corrective-evaluation-v0.1","status":status,"numerical_pass":numerical_pass,"comparison_grid":comparison_grid,"primary_pass":primary_pass,"secondary_pass":secondary_pass,"guard_pass":gd["pass"],"raw_anchor":{"frequency_ghz":ff[rk],"polarizations":raw,"full_worst_delta":full_raw,"candidate_worst_delta":cand_raw,"reduction_fraction":raw_red,"pass":raw_pass},"mode_anchor":{"search_band_ghz":mb,"selected_from":"full_E2C_only","polarization":pol,"frequency_ghz":sev["frequency_ghz"],"full_degradation_db":sev["full_db"],"candidate_degradation_db":cand_mode,"reduction_db":mode_red_db,"reduction_fraction":mode_red_frac,"pass":mode_pass},"imbalance_anchor":{"frequency_ghz":ff[ik],"polarizations":imb,"full_worst_db":full_imb,"candidate_worst_db":cand_imb,"reduction_fraction":imb_red,"pass":secondary_pass},"guard":gd,"boundary":"No automatic next BUILD/SOLVE or geometry change is authorized by this result."}
 (evidence/"corrective_evaluation.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8");(evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8");print(status);print(json.dumps(out,indent=2));return 0 if numerical_pass else 4
if __name__=="__main__":
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument("--candidate-csv",required=True);ap.add_argument("--manifest",required=True);ap.add_argument("--numerical-summary",required=True);ap.add_argument("--evidence",required=True);a=ap.parse_args()
 try:sys.exit(main(a.candidate_csv,a.manifest,a.numerical_summary,a.evidence))
 except Exception:
  Path(a.evidence).mkdir(parents=True,exist_ok=True);Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8");traceback.print_exc();sys.exit(9)
