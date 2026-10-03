from __future__ import print_function
import csv, json, math, cmath, hashlib
from pathlib import Path
import numpy as np

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
RUN=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\E2C_S0_COEXISTENCE_20261002_V01")
COMBINED=RUN/"evidence"/"qualification"/"loaded_response_native.csv"
MANIFEST=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_SENTINEL_MANIFEST_V01.json"
M3M4=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M3M4_V01"/"M3_M4_ANALYSIS.json"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M5_V01"
DOC=ROOT/"docs"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M5_LOAD_EIGENMODE_FREEZE_V01.md"
ROUTE=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M5_LOAD_EIGENMODE_FREEZE_V01.json"
OUT.mkdir(parents=True,exist_ok=True)

SOURCE_PORTS=[1,2,4,5,7,8,10,11]
AP=[1,2,4,5]
BP=[7,8,10,11]
A_E=[1,4]
B_E=[7,10]
CORE=(1.15,1.65)
THRESH={"delta":0.10,"mode_degradation_db":3.0,"imbalance_db":1.0}
S2=1.0/math.sqrt(2.0)
T_E=np.array([[S2,-S2,0,0],[S2,S2,0,0],[0,0,S2,-S2],[0,0,S2,S2]],dtype=complex)
T_POL=np.array([[S2,-S2,0,0],[S2,S2,0,0],[0,0,S2,-S2],[0,0,S2,S2]],dtype=complex)

ROUTE_MD="""# R4-A0-E2C-S0 M5 Load-Sensitivity and Eigenmode Freeze V0.1

Status: FROZEN_OFFLINE_M5
Date: 2026-10-02

M5 uses only the already solved E2C S0 S-parameter data.

## M5-A — Passive E_UP load-sensitivity

Scan a frequency-independent, identical passive reflection coefficient Gamma on the opposite-polarization E_UP +/- pair.

Grid:
- magnitude |Gamma| = 0.00..1.00 in 0.05 steps;
- phase = 0..350 deg in 10 deg steps;
- Gamma=0 evaluated once.

For each load state and each polarization, analytically reterminate the existing 8-source S-subnetwork and evaluate:
1. maximum same-pol 4x4 complex deviation versus isolated E2A/E2B baseline;
2. E_UP differential-to-common degradation versus isolated baseline;
3. E_UP +/- return imbalance.

This is a constant-Gamma passive-load sensitivity study, not a claim that a real broadband component has frequency-independent Gamma.

A second per-frequency optimum is calculated only as an optimistic mathematical lower bound and is not treated as a realizable broadband termination.

## M5-B — E_UP eigen/singular modes

Transform the four E_UP ports into [A_diff, A_common, B_diff, B_common].

At L5, L2, the worst balanced cross-pol region near 1.3384 GHz, and L1:
- compute the full 4x4 modal S matrix;
- compute eigenvectors/eigenvalues;
- compute singular vectors/singular values;
- report A/B participation and differential/common participation;
- compute the 2x2 A-to-B cross-modal coupling block singular values.

Interpretation:
- A/B participation near 1/0 means nominal polarizations remain eigenlike;
- A/B participation near 0.5/0.5 means the physical eigenchannels are strongly mixed A/B combinations;
- large cross-block singular value means no choice of a single nominal A/B basis removes the coupling.

## Gate

M5 may recommend the next physical sentinel, but it cannot authorize BUILD or SOLVE.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
"""

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def db(z):
    return 20.0*math.log10(max(abs(z),1e-300))

def load_combined(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=np.array([float(r["f_GHz"]) for r in rows],dtype=float)
    d={}
    for j in SOURCE_PORTS:
        for i in range(1,13):
            k="S%d_%d"%(i,j)
            d[(i,j)]=np.array([complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows],dtype=complex)
    return f,d

def load_baseline(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=np.array([float(r["f_GHz"]) for r in rows],dtype=float)
    d={}
    for j in (1,2,4,5):
        for i in (1,2,4,5):
            k="S%d%d"%(i,j)
            d[(i,j)]=np.array([complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows],dtype=complex)
    return f,d

def mat_at(data,k,rows,cols):
    return np.array([[data[(i,j)][k] for j in cols] for i in rows],dtype=complex)

def reterminate(data,k,keep,term,gamma):
    Saa=mat_at(data,k,keep,keep)
    if not term:
        return Saa
    Sab=mat_at(data,k,keep,term)
    Sba=mat_at(data,k,term,keep)
    Sbb=mat_at(data,k,term,term)
    G=np.eye(len(term),dtype=complex)*gamma
    return Saa + Sab @ G @ np.linalg.inv(np.eye(len(term),dtype=complex)-Sbb@G) @ Sba

def same_pol_modal(m):
    order=[0,2,1,3]
    s=m[np.ix_(order,order)]
    return T_POL @ s @ T_POL.T

def baseline_metrics(bdata,idxs):
    ports=[1,2,4,5]
    peaks=[]
    for k in idxs:
        m=mat_at(bdata,k,ports,ports)
        mm=same_pol_modal(m)
        peaks.append(abs(mm[1,0]))
    peak=max(peaks)
    return {"mode_peak_db":db(peak)}

def metrics_for_gamma(data,bdata,freqs,idxs,keep,term,gamma,bmode_db):
    max_delta=-1.0
    max_mode=-1.0
    max_imb=-1.0
    max_delta_f=None
    max_mode_f=None
    max_imb_f=None
    for k in idxs:
        m=reterminate(data,k,keep,term,gamma)
        bm=mat_at(bdata,k,[1,2,4,5],[1,2,4,5])
        d=np.max(np.abs(m-bm))
        if d>max_delta:
            max_delta=float(d); max_delta_f=float(freqs[k])
        mm=same_pol_modal(m)
        md=abs(mm[1,0])
        if md>max_mode:
            max_mode=float(md); max_mode_f=float(freqs[k])
        a=db(m[0,0]); b=db(m[2,2]); imb=abs(a-b)
        if imb>max_imb:
            max_imb=float(imb); max_imb_f=float(freqs[k])
    mode_db=db(max_mode)
    degr=mode_db-bmode_db
    score=max(max_delta/THRESH["delta"], max(degr,0.0)/THRESH["mode_degradation_db"], max_imb/THRESH["imbalance_db"])
    return {
      "gamma_real":float(gamma.real),"gamma_imag":float(gamma.imag),
      "gamma_mag":float(abs(gamma)),"gamma_phase_deg":float(math.degrees(cmath.phase(gamma))) if abs(gamma)>1e-15 else 0.0,
      "max_delta":max_delta,"max_delta_freq_ghz":max_delta_f,
      "mode_peak_db":mode_db,"mode_degradation_db":degr,"mode_peak_freq_ghz":max_mode_f,
      "imbalance_db":max_imb,"imbalance_freq_ghz":max_imb_f,
      "normalized_worst_score":score,
      "passes_all":max_delta<=THRESH["delta"] and degr<=THRESH["mode_degradation_db"] and max_imb<=THRESH["imbalance_db"]
    }

def gamma_to_z(gamma,z0=50.0):
    if abs(1-gamma)<1e-12:
        return {"kind":"OPEN","real_ohm":None,"imag_ohm":None}
    z=z0*(1+gamma)/(1-gamma)
    return {"kind":"FINITE","real_ohm":float(z.real),"imag_ohm":float(z.imag)}

def participation(v):
    p=np.abs(v)**2
    s=float(np.sum(p))
    if s<=0: s=1.0
    p=p/s
    return {
      "A_fraction":float(p[0]+p[1]),
      "B_fraction":float(p[2]+p[3]),
      "diff_fraction":float(p[0]+p[2]),
      "common_fraction":float(p[1]+p[3]),
      "components":{
        "A_diff":float(p[0]),"A_common":float(p[1]),
        "B_diff":float(p[2]),"B_common":float(p[3])
      }
    }

DOC.write_text(ROUTE_MD,encoding="utf-8")
ROUTE.write_text(json.dumps({
 "schema_version":"gnss-e2c-s0-m5-freeze-v0.1",
 "status":"FROZEN_OFFLINE_M5",
 "gamma_scan":{"magnitude_step":0.05,"phase_step_deg":10,"passive_unit_disk":True,"same_gamma_on_opposite_pol_eup_pair":True},
 "thresholds":THRESH,
 "modal_basis":["A_diff","A_common","B_diff","B_common"],
 "frequencies_ghz":[1.17645,1.2276,1.3384,1.57542],
 "BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False
},indent=2)+"\n",encoding="utf-8")

manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
m3m4=json.loads(M3M4.read_text(encoding="utf-8"))
if m3m4["status"]!="PASS_M3M4_OFFLINE_MECHANISM_CLASSIFICATION":
    raise RuntimeError("M3M4_NOT_PASS")

freqs,data=load_combined(COMBINED)
idxs=np.where((freqs>=CORE[0]-1e-12)&(freqs<=CORE[1]+1e-12))[0].tolist()
baselines={}
for pol in ("PolA","PolB"):
    p=Path(manifest["isolated_baselines"][pol]["csv_path"])
    bf,bd=load_baseline(p)
    if len(bf)!=len(freqs) or np.max(np.abs(bf-freqs))>1e-12:
        raise RuntimeError("BASELINE_GRID_"+pol)
    baselines[pol]=bd

bmetric={pol:baseline_metrics(baselines[pol],idxs) for pol in ("PolA","PolB")}

gammas=[0+0j]
for ri in range(1,21):
    r=0.05*ri
    for deg in range(0,360,10):
        gammas.append(r*cmath.exp(1j*math.radians(deg)))

scan=[]
for g in gammas:
    a=metrics_for_gamma(data,baselines["PolA"],freqs,idxs,AP,B_E,g,bmetric["PolA"]["mode_peak_db"])
    b=metrics_for_gamma(data,baselines["PolB"],freqs,idxs,BP,A_E,g,bmetric["PolB"]["mode_peak_db"])
    rec={
      "gamma":{"real":float(g.real),"imag":float(g.imag),"mag":float(abs(g)),"phase_deg":float(math.degrees(cmath.phase(g))) if abs(g)>1e-15 else 0.0},
      "equivalent_load_50ohm":gamma_to_z(g),
      "PolA":a,"PolB":b,
      "worst_delta":max(a["max_delta"],b["max_delta"]),
      "worst_mode_degradation_db":max(a["mode_degradation_db"],b["mode_degradation_db"]),
      "worst_imbalance_db":max(a["imbalance_db"],b["imbalance_db"]),
      "worst_score":max(a["normalized_worst_score"],b["normalized_worst_score"]),
      "passes_both":a["passes_all"] and b["passes_all"]
    }
    scan.append(rec)

best_delta=min(scan,key=lambda x:x["worst_delta"])
best_score=min(scan,key=lambda x:x["worst_score"])
pass_states=[x for x in scan if x["passes_both"]]
special={}
for name,g in (("matched",0+0j),("open",1+0j),("short",-1+0j)):
    special[name]=min(scan,key=lambda x:abs(x["gamma"]["real"]-g.real)+abs(x["gamma"]["imag"]-g.imag))

# Per-frequency optimistic lower bound for max same-pol deviation using the same gamma grid.
perfreq=[]
for k in idxs:
    best=None
    for g in gammas:
        vals=[]
        for pol,keep,term in (("PolA",AP,B_E),("PolB",BP,A_E)):
            m=reterminate(data,k,keep,term,g)
            bm=mat_at(baselines[pol],k,[1,2,4,5],[1,2,4,5])
            vals.append(float(np.max(np.abs(m-bm))))
        w=max(vals)
        if best is None or w<best[0]:
            best=(w,g)
    perfreq.append({"frequency_ghz":float(freqs[k]),"min_worst_delta":best[0],
                    "best_gamma_mag":float(abs(best[1])),
                    "best_gamma_phase_deg":float(math.degrees(cmath.phase(best[1]))) if abs(best[1])>1e-15 else 0.0})
perfreq_worst=max(perfreq,key=lambda x:x["min_worst_delta"])
perfreq_best=max(x["min_worst_delta"] for x in perfreq)

# Modal/eigen/singular analysis.
keyfreqs={"L5":1.17645,"L2":1.2276,"WORST_REGION":1.3384,"L1":1.57542}
modal_analysis={}
for label,target in keyfreqs.items():
    k=int(np.argmin(np.abs(freqs-target)))
    raw=mat_at(data,k,[1,4,7,10],[1,4,7,10])
    sm=T_E @ raw @ T_E.T
    evals,evecs=np.linalg.eig(sm)
    u,svals,vh=np.linalg.svd(sm)
    cross=sm[0:2,2:4]
    cu,cs,cvh=np.linalg.svd(cross)
    eig=[]
    for n in range(4):
        eig.append({
          "eigenvalue_real":float(evals[n].real),"eigenvalue_imag":float(evals[n].imag),
          "eigenvalue_mag":float(abs(evals[n])),"eigenvalue_db":db(evals[n]),
          "participation":participation(evecs[:,n])
        })
    sing=[]
    for n in range(4):
        v=vh.conj().T[:,n]
        sing.append({"singular_value":float(svals[n]),"singular_value_db":20*math.log10(max(float(svals[n]),1e-300)),
                     "right_vector_participation":participation(v)})
    modal_analysis[label]={
      "frequency_ghz":float(freqs[k]),
      "modal_matrix":[[{"real":float(z.real),"imag":float(z.imag),"db":db(z)} for z in row] for row in sm],
      "eigenmodes":eig,
      "singular_modes":sing,
      "cross_AB_block_singular_values":[float(x) for x in cs],
      "cross_AB_block_singular_values_db":[20*math.log10(max(float(x),1e-300)) for x in cs]
    }

# Global worst cross-block singular value and modal basis mixing.
global_cross=[]
for k in idxs:
    raw=mat_at(data,k,[1,4,7,10],[1,4,7,10])
    sm=T_E @ raw @ T_E.T
    cs=np.linalg.svd(sm[0:2,2:4],compute_uv=False)
    global_cross.append((float(cs[0]),k,float(cs[1])))
gx=max(global_cross,key=lambda x:x[0])

# Determine if singular eigenchannels are A/B mixed at worst region.
worst=modal_analysis["WORST_REGION"]
purities=[]
for m in worst["singular_modes"]:
    p=m["right_vector_participation"]
    purities.append(max(p["A_fraction"],p["B_fraction"]))
min_purity=min(purities)
max_purity=max(purities)

classification=[]
if not pass_states:
    classification.append({"finding":"NO_CONSTANT_PASSIVE_EUP_LOAD_MEETS_FROZEN_SENTINEL_THRESHOLDS","confidence":"HIGH",
                           "basis":"0 scanned passive constant-Gamma states pass both polarizations"})
if best_delta["worst_delta"]>0.20:
    classification.append({"finding":"PASSIVE_EUP_LOADING_CANNOT_REMOVE_SEVERE_GEOMETRY_COUPLING","confidence":"HIGH",
                           "basis":"best constant-Gamma worst delta remains above severe 0.20 threshold"})
if perfreq_best>0.20:
    classification.append({"finding":"EVEN_FREQUENCY_ADAPTIVE_PASSIVE_LOAD_LOWER_BOUND_REMAINS_SEVERE","confidence":"HIGH",
                           "basis":"per-frequency optimistic unit-disk load scan still exceeds 0.20 somewhere in decision band"})
if 20*math.log10(max(gx[0],1e-300))>-20:
    classification.append({"finding":"A_B_MODAL_COUPLING_BLOCK_HAS_STRONG_PRINCIPAL_CHANNEL","confidence":"HIGH",
                           "basis":"largest A-B modal cross-block singular value exceeds -20 dB"})
if min_purity<0.70:
    classification.append({"finding":"WORST_REGION_SINGULAR_CHANNELS_ARE_STRONGLY_MIXED_AB_MODES","confidence":"HIGH",
                           "basis":"at least one dominant orthogonal channel has A/B purity below 0.70"})

out={
 "schema_version":"gnss-e2c-s0-m5-v0.1",
 "status":"PASS_M5_LOAD_SENSITIVITY_AND_EIGENMODE_ANALYSIS",
 "input":{"combined_sha256":sha(COMBINED),"gamma_states":len(scan),"core_band_ghz":list(CORE)},
 "baseline_mode_peak_db":bmetric,
 "load_scan":{
   "best_constant_gamma_by_delta":best_delta,
   "best_constant_gamma_by_worst_score":best_score,
   "passing_state_count":len(pass_states),
   "special_states":special,
   "per_frequency_optimistic_lower_bound":{"worst_min_delta":perfreq_worst,"max_of_min_delta":perfreq_best}
 },
 "modal_analysis":modal_analysis,
 "global_cross_block":{"peak_sigma":gx[0],"peak_sigma_db":20*math.log10(max(gx[0],1e-300)),
                       "second_sigma":gx[2],"second_sigma_db":20*math.log10(max(gx[2],1e-300)),
                       "frequency_ghz":float(freqs[gx[1]])},
 "worst_region_singular_ab_purity":{"min":min_purity,"max":max_purity,"all":purities},
 "classification":classification,
 "boundary":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False,"rerun_allowed":False}
}
(OUT/"M5_ANALYSIS.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")

with open(str(OUT/"LOAD_SCAN_TOP.csv"),"w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["rank","gamma_mag","gamma_phase_deg","z_real_ohm","z_imag_ohm","worst_delta","worst_mode_degradation_db","worst_imbalance_db","worst_score","passes_both"])
    for rank,x in enumerate(sorted(scan,key=lambda z:z["worst_score"])[:30],1):
        z=x["equivalent_load_50ohm"]
        w.writerow([rank,x["gamma"]["mag"],x["gamma"]["phase_deg"],z["real_ohm"],z["imag_ohm"],x["worst_delta"],x["worst_mode_degradation_db"],x["worst_imbalance_db"],x["worst_score"],x["passes_both"]])

with open(str(OUT/"PER_FREQUENCY_LOAD_LOWER_BOUND.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(perfreq[0].keys()))
    w.writeheader(); w.writerows(perfreq)

lines=["# E2C S0 M5 Load-Sensitivity and Eigenmode Analysis V0.1","",
       "Status: **PASS_M5_LOAD_SENSITIVITY_AND_EIGENMODE_ANALYSIS**","",
       "No CST launch, BUILD, or SOLVE was used.","",
       "## Passive E_UP load scan","",
       "- scanned constant passive Gamma states: %d"%len(scan),
       "- passing states under all frozen thresholds: %d"%len(pass_states),
       "- best constant-Gamma worst delta: %.6f at |Gamma|=%.2f, phase=%.1f deg"%(best_delta["worst_delta"],best_delta["gamma"]["mag"],best_delta["gamma"]["phase_deg"]),
       "- best constant-Gamma worst normalized score: %.3f at |Gamma|=%.2f, phase=%.1f deg"%(best_score["worst_score"],best_score["gamma"]["mag"],best_score["gamma"]["phase_deg"]),
       "- optimistic per-frequency load lower-bound max delta across band: %.6f"%perfreq_best,
       "",
       "### Special states"]
for name in ("matched","open","short"):
    x=special[name]
    lines.append("- %s: worst delta=%.6f, worst mode degradation=%.3f dB, worst imbalance=%.3f dB"%(name,x["worst_delta"],x["worst_mode_degradation_db"],x["worst_imbalance_db"]))
lines += ["","## E_UP modal/eigenmode results","",
          "- global A/B cross-modal principal coupling sigma: %.3f dB at %.4f GHz"%(out["global_cross_block"]["peak_sigma_db"],out["global_cross_block"]["frequency_ghz"]),
          "- second A/B cross-modal sigma there: %.3f dB"%out["global_cross_block"]["second_sigma_db"],
          "- worst-region singular-mode A/B purity range: %.3f .. %.3f"%(min_purity,max_purity),""]
for label in ("L5","L2","WORST_REGION","L1"):
    x=modal_analysis[label]
    lines.append("### %s %.5f GHz"%(label,x["frequency_ghz"]))
    lines.append("- A/B cross-block singular values: %.3f dB, %.3f dB"%(x["cross_AB_block_singular_values_db"][0],x["cross_AB_block_singular_values_db"][1]))
    for n,m in enumerate(x["singular_modes"][:2],1):
        p=m["right_vector_participation"]
        lines.append("- singular mode %d: sigma %.3f dB; A %.3f / B %.3f; diff %.3f / common %.3f"%(n,m["singular_value_db"],p["A_fraction"],p["B_fraction"],p["diff_fraction"],p["common_fraction"]))
    lines.append("")
lines += ["## Evidence-based classification",""]
for x in classification:
    lines.append("- **%s — %s**: %s"%(x["confidence"],x["finding"],x["basis"]))
lines += ["","## Boundary","","M5 does not authorize a geometry change. The next step is to use the M5 result to choose a minimum physical attribution sentinel, not to retune the full antenna blindly.","","BUILD_AUTHORIZED = false","SOLVE_AUTHORIZED = false"]
(OUT/"M5_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

print("PASS_M5_LOAD_SENSITIVITY_AND_EIGENMODE_ANALYSIS")
print("GAMMA_STATES=%d"%len(scan))
print("PASSING_STATES=%d"%len(pass_states))
print("BEST_DELTA=%.6f |G|=%.2f PH=%.1f"%(best_delta["worst_delta"],best_delta["gamma"]["mag"],best_delta["gamma"]["phase_deg"]))
print("BEST_SCORE=%.3f |G|=%.2f PH=%.1f"%(best_score["worst_score"],best_score["gamma"]["mag"],best_score["gamma"]["phase_deg"]))
print("PERFREQ_LOWER_BOUND_MAX_DELTA=%.6f"%perfreq_best)
print("GLOBAL_CROSS_SIGMA_DB=%.3f@%.4f"%(out["global_cross_block"]["peak_sigma_db"],out["global_cross_block"]["frequency_ghz"]))
print("WORST_REGION_AB_PURITY_MIN=%.3f"%min_purity)
print("OUT="+str(OUT))
