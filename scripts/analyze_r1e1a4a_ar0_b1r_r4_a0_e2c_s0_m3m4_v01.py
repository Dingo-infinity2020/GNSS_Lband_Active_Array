from __future__ import print_function
import csv,json,math,cmath
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
RUN=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\E2C_S0_COEXISTENCE_20261002_V01")
COMBINED=RUN/"evidence"/"qualification"/"loaded_response_native.csv"
MANIFEST=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_SENTINEL_MANIFEST_V01.json"
M1M2=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M1M2_V01"/"M1_M2_ANALYSIS.json"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M3M4_V01"
OUT.mkdir(parents=True,exist_ok=True)

S2=1/math.sqrt(2)
BANDS={"LOW":[1.15,1.25],"MID":[1.28,1.40],"HIGH":[1.50,1.65]}
AP=[1,2,4,5]
BP=[7,8,10,11]
AE=[1,4]; BE=[7,10]
SEM={1:"A_P_E_UP",2:"A_P_P_IN",4:"A_N_E_UP",5:"A_N_P_IN",
     7:"B_P_E_UP",8:"B_P_P_IN",10:"B_N_E_UP",11:"B_N_P_IN"}

def db(z): return 20*math.log10(max(abs(z),1e-300))
def ph(z): return math.degrees(cmath.phase(z))

def load_combined(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]
    d={}
    for j in (1,2,4,5,7,8,10,11):
        for i in range(1,13):
            k="S%d_%d"%(i,j)
            d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
    return f,d

def load_baseline(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]
    d={}
    for j in (1,2,4,5):
        for i in (1,2,4,5):
            k="S%d%d"%(i,j)
            d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
    return f,d

def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def eye(n):
    return [[1+0j if i==j else 0j for j in range(n)] for i in range(n)]

def inv(a):
    n=len(a)
    aug=[list(a[i])+eye(n)[i] for i in range(n)]
    for col in range(n):
        pivot=max(range(col,n),key=lambda r:abs(aug[r][col]))
        if abs(aug[pivot][col])<1e-12:
            raise RuntimeError("SINGULAR_RETERMINATION")
        aug[col],aug[pivot]=aug[pivot],aug[col]
        q=aug[col][col]
        aug[col]=[x/q for x in aug[col]]
        for r in range(n):
            if r==col: continue
            q=aug[r][col]
            if abs(q)>0:
                aug[r]=[aug[r][c]-q*aug[col][c] for c in range(2*n)]
    return [row[n:] for row in aug]

def submat(data,k,rows,cols):
    return [[data[(i,j)][k] for j in cols] for i in rows]

def reterminate(data,k,keep,term,gamma):
    Saa=submat(data,k,keep,keep)
    Sab=submat(data,k,keep,term)
    Sba=submat(data,k,term,keep)
    Sbb=submat(data,k,term,term)
    n=len(term)
    G=[[gamma if i==j else 0j for j in range(n)] for i in range(n)]
    M=[[ (1+0j if i==j else 0j) - matmul(Sbb,G)[i][j] for j in range(n)] for i in range(n)]
    return [[Saa[i][j]+matmul(matmul(matmul(Sab,G),inv(M)),Sba)[i][j]
             for j in range(len(keep))] for i in range(len(keep))]

def max_delta_matrix(mats,baseline,freqs,idxs):
    best=(-1,None,None,None)
    for k in idxs:
        m=mats[k]
        for i in range(4):
            for j in range(4):
                d=abs(m[i][j]-baseline[(i,j)][k])
                if d>best[0]: best=(d,k,i,j)
    return {"delta_mag":best[0],"frequency_ghz":freqs[best[1]],"matrix_index":[best[2],best[3]]}

Tpol=[[S2,-S2,0,0],[S2,S2,0,0],[0,0,S2,-S2],[0,0,S2,S2]]
TpolT=[list(x) for x in zip(*Tpol)]

def modal_eup(data,k):
    order=[1,4,7,10]
    s=submat(data,k,order,order)
    return matmul(matmul(Tpol,s),TpolT)

def modal_same_pol_from_matrix(m):
    # m order E_P,PIN_P,E_N,PIN_N; reuse same convention as earlier qualifier
    t=[[S2,-S2,0,0],[S2,S2,0,0],[0,0,S2,-S2],[0,0,S2,S2]]
    tt=[list(x) for x in zip(*t)]
    order=[0,2,1,3]
    s=[[m[i][j] for j in order] for i in order]
    return matmul(matmul(t,s),tt)

def max_metric(freqs,idxs,fn):
    best=None
    for k in idxs:
        v=fn(k)
        rec=(abs(v),k,v)
        if best is None or rec[0]>best[0]: best=rec
    return {"db":db(best[2]),"mag":abs(best[2]),"phase_deg":ph(best[2]),"frequency_ghz":freqs[best[1]]}

manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
m1m2=json.loads(M1M2.read_text(encoding="utf-8"))
if m1m2["m1_status"]!="PASS_M1_SEMANTIC_INTEGRITY":
    raise RuntimeError("M1_NOT_PASS")
freqs,data=load_combined(COMBINED)
bases={}
for pol in ("PolA","PolB"):
    p=Path(manifest["isolated_baselines"][pol]["csv_path"])
    bases[pol]=load_baseline(p)

idx_all=[k for k,f in enumerate(freqs) if 1.15<=f<=1.65]
band_idx={name:[k for k,f in enumerate(freqs) if lo<=f<=hi] for name,(lo,hi) in BANDS.items()}

# Cross-pol E_UP modal transform.
terms={
 "A_diff_to_B_diff":(2,0),"A_diff_to_B_common":(3,0),
 "A_common_to_B_diff":(2,1),"A_common_to_B_common":(3,1),
 "B_diff_to_A_diff":(0,2),"B_diff_to_A_common":(1,2),
 "B_common_to_A_diff":(0,3),"B_common_to_A_common":(1,3)
}
modal_cross={}
for name,(i,j) in terms.items():
    modal_cross[name]=max_metric(freqs,idx_all,lambda k,i=i,j=j:modal_eup(data,k)[i][j])

band_profiles={}
for b,idxs in band_idx.items():
    band_profiles[b]={}
    for name,(i,j) in terms.items():
        vals=[db(modal_eup(data,k)[i][j]) for k in idxs]
        band_profiles[b][name]={
          "peak_db":max(vals),
          "median_db":sorted(vals)[len(vals)//2],
          "fraction_above_minus10":sum(v>-10 for v in vals)/float(len(vals)),
          "fraction_above_minus20":sum(v>-20 for v in vals)/float(len(vals))
        }

# Build per-pol 4x4 baseline matrices keyed local index 0..3.
baseline_local={}
for pol in ("PolA","PolB"):
    bf,bd=bases[pol]
    baseline_local[pol]={}
    ports=[1,2,4,5]
    for i,pi in enumerate(ports):
        for j,pj in enumerate(ports):
            baseline_local[pol][(i,j)]=bd[(pi,pj)]

# Retermination diagnostics: current matched (gamma=0), opposite E_UP open,
# opposite PIN open, and all opposite source ports open.
ret={}
for pol,keep,opp,opp_e,opp_pin in (
    ("PolA",AP,BP,[7,10],[8,11]),
    ("PolB",BP,AP,[1,4],[2,5]),
):
    mats={}
    for label,term,g in (
      ("matched",[],0),
      ("opp_EUP_open",opp_e,1),
      ("opp_PIN_open",opp_pin,1),
      ("opp_all_open",opp,1),
    ):
        mats[label]={}
        for k in idx_all:
            if not term:
                mats[label][k]=submat(data,k,keep,keep)
            else:
                mats[label][k]=reterminate(data,k,keep,term,g)
    ret[pol]={}
    for label,mmats in mats.items():
        md=max_delta_matrix(mmats,baseline_local[pol],freqs,idx_all)
        # same-pol E diff->common modal peak and E self-return imbalance
        bestdc=None; bestimb=None
        for k in idx_all:
            mmx=modal_same_pol_from_matrix(mmats[k])
            z=mmx[1][0]
            r=(abs(z),k,z)
            if bestdc is None or r[0]>bestdc[0]: bestdc=r
            a=db(mmats[k][0][0]); b=db(mmats[k][2][2]); d=abs(a-b)
            rr=(d,k,a,b)
            if bestimb is None or d>bestimb[0]: bestimb=rr
        ret[pol][label]={
          "max_vs_isolated":md,
          "E_diff_to_common_peak":{"db":db(bestdc[2]),"frequency_ghz":freqs[bestdc[1]]},
          "EUP_return_imbalance":{"db":bestimb[0],"frequency_ghz":freqs[bestimb[1]],"plus_db":bestimb[2],"minus_db":bestimb[3]}
        }

# Bandwise original severe observables.
band_science={}
for b,idxs in band_idx.items():
    band_science[b]={}
    for pol,ports in (("PolA",AP),("PolB",BP)):
        bf,bd=bases[pol]
        keep=ports
        # same-pol raw max delta
        best=(-1,None)
        for k in idxs:
            for i,ci in enumerate(keep):
                for j,cj in enumerate(keep):
                    bi=[1,2,4,5][i]; bj=[1,2,4,5][j]
                    d=abs(data[(ci,cj)][k]-bd[(bi,bj)][k])
                    if d>best[0]: best=(d,k)
        # modal d->c
        if pol=="PolA":
            ep,en=1,4
        else:
            ep,en=7,10
        def dc(k):
            spp=data[(ep,ep)][k]; spn=data[(ep,en)][k]; snp=data[(en,ep)][k]; snn=data[(en,en)][k]
            return 0.5*(spp-spn+snp-snn)
        peakdc=max_metric(freqs,idxs,dc)
        band_science[b][pol]={"max_raw_delta":best[0],"max_raw_delta_freq":freqs[best[1]],"E_diff_to_common_peak":peakdc}

# Classification.
matched=max(ret["PolA"]["matched"]["max_vs_isolated"]["delta_mag"],ret["PolB"]["matched"]["max_vs_isolated"]["delta_mag"])
open_e=max(ret["PolA"]["opp_EUP_open"]["max_vs_isolated"]["delta_mag"],ret["PolB"]["opp_EUP_open"]["max_vs_isolated"]["delta_mag"])
open_all=max(ret["PolA"]["opp_all_open"]["max_vs_isolated"]["delta_mag"],ret["PolB"]["opp_all_open"]["max_vs_isolated"]["delta_mag"])
dd=max(modal_cross["A_diff_to_B_diff"]["db"],modal_cross["B_diff_to_A_diff"]["db"])
dc=max(modal_cross["A_diff_to_B_common"]["db"],modal_cross["B_diff_to_A_common"]["db"])
classification=[]
classification.append({"finding":"ANALYSIS_SEMANTICS_NOT_PRIMARY","confidence":"HIGH","basis":"M1 semantic integrity PASS"})
if open_e < 0.5*matched:
    classification.append({"finding":"OPPOSITE_POL_EUP_50OHM_TERMINATION_IS_MAJOR_CONTRIBUTOR","confidence":"HIGH","basis":"opening opposite-pol E_UP analytically reduces max isolated delta by >50%"})
else:
    classification.append({"finding":"OPPOSITE_POL_EUP_50OHM_TERMINATION_NOT_SUFFICIENT_TO_EXPLAIN_HOLD","confidence":"HIGH","basis":"open retermination leaves >50% of matched delta"})
if dd<-20 and dc>-15:
    classification.append({"finding":"SINGLE_ENDED_MINUS3DB_DOES_NOT_EQUAL_DIFF_TO_DIFF_CROSSPOL","confidence":"HIGH","basis":"balanced diff-to-diff remains low while diff/common cross-modal path is much larger"})
elif dd>-20:
    classification.append({"finding":"TRUE_BALANCED_CROSSPOL_COUPLING_IS_STRONG","confidence":"HIGH","basis":"A/B differential-to-differential E_UP coupling exceeds -20 dB"})
if open_all < open_e*0.8:
    classification.append({"finding":"PIN_TERMINATION_ALSO_MATTERS","confidence":"MEDIUM","basis":"opening all opposite source nodes materially improves over E_UP-open only"})
classification.append({"finding":"NARROW_RESONANCE_NOT_PRIMARY","confidence":"HIGH","basis":"previous 50 MHz resonance gate remained below 10 dB"})

out={
 "schema_version":"gnss-e2c-s0-m3m4-v0.1",
 "status":"PASS_M3M4_OFFLINE_MECHANISM_CLASSIFICATION",
 "modal_cross_pol_eup":modal_cross,
 "band_profiles":band_profiles,
 "band_science":band_science,
 "retermination":ret,
 "summary_metrics":{"matched_max_delta":matched,"opp_EUP_open_max_delta":open_e,"opp_all_open_max_delta":open_all,
                    "max_diff_to_diff_crosspol_db":dd,"max_diff_to_common_crosspol_db":dc},
 "classification":classification,
 "boundary":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False,"rerun_allowed":False}
}
(OUT/"M3_M4_ANALYSIS.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")

lines=["# E2C S0 M3/M4 Offline Mechanism Classification V0.1","",
       "Status: **PASS_M3M4_OFFLINE_MECHANISM_CLASSIFICATION**","",
       "No CST launch, BUILD, or SOLVE was used.","",
       "## A/B balanced modal coupling at E_UP",""]
for k,v in modal_cross.items():
    lines.append("- %s: %.3f dB at %.4f GHz"%(k,v["db"],v["frequency_ghz"]))
lines += ["","## Analytical opposite-polarization retermination",""]
for pol in ("PolA","PolB"):
    lines.append("### "+pol)
    for label in ("matched","opp_EUP_open","opp_PIN_open","opp_all_open"):
        x=ret[pol][label]
        lines.append("- %s: max delta=%.6f; E diff->common peak=%.3f dB; E_UP imbalance=%.3f dB"%(
          label,x["max_vs_isolated"]["delta_mag"],x["E_diff_to_common_peak"]["db"],x["EUP_return_imbalance"]["db"]))
    lines.append("")
lines += ["## Band decomposition",""]
for b in ("LOW","MID","HIGH"):
    lines.append("### "+b+" "+str(BANDS[b][0])+"-"+str(BANDS[b][1])+" GHz")
    for pol in ("PolA","PolB"):
        x=band_science[b][pol]
        lines.append("- %s: max raw delta=%.6f; E diff->common peak=%.3f dB"%(pol,x["max_raw_delta"],x["E_diff_to_common_peak"]["db"]))
    lines.append("")
lines += ["## Evidence-based classification",""]
for x in classification:
    lines.append("- **%s — %s**: %s"%(x["confidence"],x["finding"],x["basis"]))
lines += ["","## Decision boundary","",
          "Do not BUILD yet. A geometry change is justified only if the residual after physically relevant retermination still points to a named geometric/ground mechanism.",
          "The next offline task, if needed, is to convert the retermination result into a concrete physical circuit interpretation and define the minimum future sentinel that separates loading from geometry.",
          "",
          "BUILD_AUTHORIZED = false",
          "SOLVE_AUTHORIZED = false"]
(OUT/"M3_M4_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

print("PASS_M3M4_OFFLINE_MECHANISM_CLASSIFICATION")
print("A_DIFF_TO_B_DIFF_DB=%.3f"%modal_cross["A_diff_to_B_diff"]["db"])
print("A_DIFF_TO_B_COMMON_DB=%.3f"%modal_cross["A_diff_to_B_common"]["db"])
print("B_DIFF_TO_A_DIFF_DB=%.3f"%modal_cross["B_diff_to_A_diff"]["db"])
print("B_DIFF_TO_A_COMMON_DB=%.3f"%modal_cross["B_diff_to_A_common"]["db"])
for pol in ("PolA","PolB"):
    print(pol+"_MATCHED_DELTA=%.6f"%ret[pol]["matched"]["max_vs_isolated"]["delta_mag"])
    print(pol+"_EUP_OPEN_DELTA=%.6f"%ret[pol]["opp_EUP_open"]["max_vs_isolated"]["delta_mag"])
    print(pol+"_ALL_OPEN_DELTA=%.6f"%ret[pol]["opp_all_open"]["max_vs_isolated"]["delta_mag"])
print("OUT="+str(OUT))