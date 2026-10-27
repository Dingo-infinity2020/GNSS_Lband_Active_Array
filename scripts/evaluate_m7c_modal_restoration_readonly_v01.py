from __future__ import print_function
import csv,json,math,sys,traceback
from pathlib import Path

SOURCE_PORTS=(1,2,4,5,7,8,10,11)
ALL_ROWS=tuple(range(1,13))
CORE=(1.15,1.65)
S2=1.0/math.sqrt(2.0)
T=[[S2,-S2,0,0],[S2,S2,0,0],[0,0,S2,-S2],[0,0,S2,S2]]
POL={"PolA":{"c":[1,2,4,5],"b":[1,2,4,5]},"PolB":{"c":[7,8,10,11],"b":[1,2,4,5]}}

def db(z): return 20.0*math.log10(max(abs(z),1e-300))
def matmul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(x) for x in zip(*a)]

def read96(path):
 rows=list(csv.DictReader(open(str(path),"r",newline=""))); f=[float(r["f_GHz"]) for r in rows]; d={}
 for j in SOURCE_PORTS:
  for i in ALL_ROWS:
   k="S%d_%d"%(i,j); d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
 return f,d

def read16(path):
 rows=list(csv.DictReader(open(str(path),"r",newline=""))); f=[float(r["f_GHz"]) for r in rows]; d={}
 for j in (1,2,4,5):
  for i in (1,2,4,5):
   k="S%d%d"%(i,j); d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
 return f,d

def interp(xs,ys,x):
 if x<xs[0]-1e-10 or x>xs[-1]+1e-10: raise RuntimeError("HOLD_M7C_EXTRAPOLATION")
 if x<=xs[0]+1e-15:return ys[0]
 if x>=xs[-1]-1e-15:return ys[-1]
 lo=0;hi=len(xs)-1
 while hi-lo>1:
  mid=(lo+hi)//2
  if xs[mid]<=x:lo=mid
  else:hi=mid
 a=(x-xs[lo])/(xs[hi]-xs[lo]); return ys[lo]+a*(ys[hi]-ys[lo])

def interp_set(sf,sd,tf): return {k:[interp(sf,v,x) for x in tf] for k,v in sd.items()}
def nearest(freqs,x): return min(range(len(freqs)),key=lambda k:abs(freqs[k]-x))

def mixed(d,k,ports):
 ep,pp,en,pn=ports; order=[ep,en,pp,pn]
 s=[[d[(i,j)][k] for j in order] for i in order]
 return matmul(matmul(T,s),tr(T))

def mode_dc(d,k,ports): return mixed(d,k,ports)[1][0]
def mode_dd(d,k,ports): return mixed(d,k,ports)[0][0]

def own_delta_at(d,b,cp,bp,k):
 best=0.0;driver=None
 for ci,bi in zip(cp,bp):
  for cj,bj in zip(cp,bp):
   v=abs(d[(ci,cj)][k]-b[(bi,bj)][k])
   if v>best: best=v; driver={"response_port":ci,"source_port":cj}
 return best,driver

def guard(cand,full,freqs,max_new,width):
 idx=[k for k,f in enumerate(freqs) if CORE[0]-1e-12<=f<=CORE[1]+1e-12]
 worst={"new_excursion_db":-1e99}
 for j in SOURCE_PORTS:
  for i in ALL_ROWS:
   if i==j:continue
   cv=[db(cand[(i,j)][k]) for k in idx]; fv=[db(full[(i,j)][k]) for k in idx]; b=0
   for a in range(len(idx)):
    if b<a:b=a
    while b+1<len(idx) and freqs[idx[b+1]]-freqs[idx[a]]<=width+1e-12:b+=1
    if b<=a:continue
    gain=(max(cv[a:b+1])-min(cv[a:b+1]))-(max(fv[a:b+1])-min(fv[a:b+1]))
    if gain>worst["new_excursion_db"]:
     worst={"new_excursion_db":gain,"f_start_ghz":freqs[idx[a]],"f_end_ghz":freqs[idx[b]],"response_port":i,"source_port":j}
 worst["pass"]=worst["new_excursion_db"]<=max_new
 return worst

def main(candidate_csv,manifest_path,numerical_summary,evidence):
 evidence=Path(evidence); evidence.mkdir(parents=True,exist_ok=True)
 m=json.loads(Path(manifest_path).read_text(encoding="utf-8"))
 num=json.loads(Path(numerical_summary).read_text(encoding="utf-8"))
 numerical_pass=all(num["hard_checks"].values())

 cf,cd=read96(Path(candidate_csv)); ff,fd=read96(Path(m["full_e2c_reference"]["response_csv"]))
 if len(cf)!=len(ff) or any(abs(a-b)>1e-9 for a,b in zip(cf,ff)):
  cd=interp_set(cf,cd,ff); comparison_grid="candidate interpolated onto full-E2C grid"
 else: comparison_grid="native grids identical"

 bases={}
 for pol in ("PolA","PolB"):
  bf,bd=read16(Path(m["isolated_baselines"][pol]["csv_path"]))
  if len(bf)!=len(ff) or any(abs(a-b)>1e-9 for a,b in zip(bf,ff)): bd=interp_set(bf,bd,ff)
  bases[pol]=bd

 sg=m["modal_gate"]["symmetry"]; symmetry=[]
 for x in sg["anchors_ghz"]:
  k=nearest(ff,float(x))
  for pol in ("PolA","PolB"):
   cp=POL[pol]["c"];bp=POL[pol]["b"]
   full=abs(mode_dc(fd,k,cp)-mode_dc(bases[pol],k,bp))
   cand=abs(mode_dc(cd,k,cp)-mode_dc(bases[pol],k,bp))
   ratio=cand/full if full>1e-15 else 1e99
   symmetry.append({"polarization":pol,"frequency_ghz":ff[k],"full_e2c_delta_sdc":full,"candidate_delta_sdc":cand,
                    "fraction_of_full_e2c":ratio,"reduction_vs_full_fraction":1.0-ratio,
                    "pass":ratio<=sg["maximum_fraction_of_full_e2c"]})
 symmetry_pass=all(x["pass"] for x in symmetry)

 dg=m["modal_gate"]["differential_restoration"]; differential=[]
 for x in dg["anchors_ghz"]:
  k=nearest(ff,float(x)); key=("%.4f"%float(x))
  for pol in ("PolA","PolB"):
   cp=POL[pol]["c"];bp=POL[pol]["b"]
   cand=abs(mode_dd(cd,k,cp)-mode_dd(bases[pol],k,bp))
   full=abs(mode_dd(fd,k,cp)-mode_dd(bases[pol],k,bp))
   ref=float(m["m7b_reference"]["sdd_delta_vs_isolated"][pol][key])
   ratio=cand/ref if ref>1e-15 else 1e99
   differential.append({"polarization":pol,"frequency_ghz":ff[k],"full_e2c_delta_sdd":full,
                        "m7b_delta_sdd":ref,"candidate_delta_sdd":cand,"fraction_of_m7b":ratio,
                        "reduction_vs_m7b_fraction":1.0-ratio,
                        "pass":ratio<=dg["maximum_fraction_of_m7b"]})
 differential_pass=all(x["pass"] for x in differential)

 idx=[k for k,f in enumerate(ff) if CORE[0]-1e-12<=f<=CORE[1]+1e-12]
 raw={"candidate_worst_delta":-1.0}
 for pol in ("PolA","PolB"):
  cp=POL[pol]["c"];bp=POL[pol]["b"]
  for k in idx:
   v,driver=own_delta_at(cd,bases[pol],cp,bp,k)
   if v>raw["candidate_worst_delta"]:
    raw={"candidate_worst_delta":v,"frequency_ghz":ff[k],"polarization":pol,"driver":driver}
 raw["m7b_reference"]=m["modal_gate"]["secondary_raw"]["m7b_reference"]
 raw["fraction_of_m7b"]=raw["candidate_worst_delta"]/raw["m7b_reference"]
 raw["absolute_threshold"]=m["modal_gate"]["secondary_raw"]["absolute_threshold"]
 raw["pass"]=raw["candidate_worst_delta"]<=raw["absolute_threshold"]

 gd=guard(cd,fd,ff,m["modal_gate"]["guard"]["max_new_excursion_db"],m["modal_gate"]["guard"]["window_mhz"]/1000.0)
 minimp=m["modal_gate"]["partial_review"]["minimum_predicted_direction_improvement_fraction"]
 symmetry_any10=any(x["reduction_vs_full_fraction"]>=minimp for x in symmetry)
 differential_any10=any(x["reduction_vs_m7b_fraction"]>=minimp for x in differential)

 if not numerical_pass: status="HOLD_M7C_NUMERICAL"
 elif not gd["pass"]: status="HOLD_M7C_GUARD"
 elif symmetry_pass and differential_pass: status="PASS_M7C_LOCAL_RETURN_ISLAND"
 elif (symmetry_pass != differential_pass) or symmetry_any10 or differential_any10: status="REVIEW_M7C_PARTIAL"
 else: status="REJECT_M7C_LOCAL_RETURN_TOPOLOGY"

 out={
  "schema_version":"gnss-m7c-modal-evaluation-v0.1",
  "status":status,
  "numerical_pass":numerical_pass,
  "comparison_grid":comparison_grid,
  "symmetry_primary_pass":symmetry_pass,
  "differential_restoration_primary_pass":differential_pass,
  "secondary_raw_pass":raw["pass"],
  "guard_pass":gd["pass"],
  "symmetry":symmetry,
  "differential_restoration":differential,
  "secondary_raw":raw,
  "guard":gd,
  "partial_review_evidence":{"symmetry_any_item_improves_ge_10pct":symmetry_any10,
                             "differential_any_item_improves_ge_10pct":differential_any10},
  "boundary":"No automatic next BUILD/SOLVE or geometry change is authorized by this result."
 }
 (evidence/"modal_evaluation.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
 print(status); print(json.dumps(out,indent=2))
 return 0 if numerical_pass else 4

if __name__=="__main__":
 import argparse
 ap=argparse.ArgumentParser()
 ap.add_argument("--candidate-csv",required=True); ap.add_argument("--manifest",required=True)
 ap.add_argument("--numerical-summary",required=True); ap.add_argument("--evidence",required=True)
 a=ap.parse_args()
 try: sys.exit(main(a.candidate_csv,a.manifest,a.numerical_summary,a.evidence))
 except Exception:
  Path(a.evidence).mkdir(parents=True,exist_ok=True)
  Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
  traceback.print_exc(); sys.exit(9)
