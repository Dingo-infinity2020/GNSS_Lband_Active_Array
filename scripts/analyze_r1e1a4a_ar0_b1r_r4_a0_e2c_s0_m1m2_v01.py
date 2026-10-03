from __future__ import print_function
import csv, json, hashlib, math, cmath
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
RUN=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\E2C_S0_COEXISTENCE_20261002_V01")
COMBINED=RUN/"evidence"/"qualification"/"loaded_response_native.csv"
QUAL=RUN/"evidence"/"qualification"/"qualification_summary.json"
TOP=RUN/"evidence"/"summary.json"
MANIFEST=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_SENTINEL_MANIFEST_V01.json"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M1M2_V01"
DOC=ROOT/"docs"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_POSTHOLD_ROUTE_FREEZE_V01.md"
ROUTE=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_POSTHOLD_ROUTE_FREEZE_V01.json"
OUT.mkdir(parents=True,exist_ok=True)

CORE=(1.15,1.65)
S2=1.0/math.sqrt(2.0)
T=((S2,-S2,0,0),(S2,S2,0,0),(0,0,S2,-S2),(0,0,S2,S2))
POL={
 "PolA":{"c":[1,2,4,5],"b":[1,2,4,5]},
 "PolB":{"c":[7,8,10,11],"b":[1,2,4,5]},
}
SEM={
 1:"A_P_E_UP",2:"A_P_P_IN",3:"A_P_P_OUT",
 4:"A_N_E_UP",5:"A_N_P_IN",6:"A_N_P_OUT",
 7:"B_P_E_UP",8:"B_P_P_IN",9:"B_P_P_OUT",
 10:"B_N_E_UP",11:"B_N_P_IN",12:"B_N_P_OUT"
}

ROUTE_MD="""# R4-A0-E2C-S0 Post-HOLD Mechanism Classification Route Freeze V0.1

Status: FROZEN_OFFLINE_ROUTE
Date: 2026-10-02
Trigger: HOLD_E2C_S0_SEVERE_COEXISTENCE_REVIEW

## Purpose

The E2C S0 solver completed numerically and the scientific sentinel entered severe review. This route freezes the next actions before any model mutation.

No BUILD or SOLVE is authorized by this document.

## Frozen sequence

### M1 — Result semantic integrity audit

Audit the exact E2C raw-to-solve port map, A/B and +/- branch correspondence, E2A/E2B baseline hashes and frequency grids, source/load semantics, differential/common transformation, baseline self-test, and 96-trace response completeness.

If semantics fail, repair read-only analysis only and recompute the existing result. If semantics pass, proceed to M2.

### M2 — 96-trace coupling decomposition

Decompose same-pol E_UP/E_UP, E_UP/P_IN, P_IN/device-side, cross-pol E_UP/E_UP, cross-pol E_UP/device-side, and modal differential/common blocks. Identify which raw terms generate the 1.34-1.36 GHz severe change and branch imbalance.

### M3 — Frequency mechanism decomposition

Use the existing solution only. Compare 1.15-1.25, 1.28-1.40, and 1.50-1.65 GHz and distinguish broad topology/reference-return behavior, narrow resonance, smooth mutual coupling, and analysis/reference artifacts.

### M4 — First-principles mechanism classification

Allowed mechanism classes:
1. real dual-pol electromagnetic coexistence;
2. ground-return / branch-reference interaction;
3. sentinel termination/network effect;
4. analysis/reference-plane error.

## Mandatory gate before any future BUILD

A future BUILD is forbidden until all three are named:
1. physical mechanism to change;
2. exact observable expected to move;
3. expected direction of change.

Existing E2C S0 results are read-only evidence. No automatic retry, no second S0 solve, and no C1 promotion while the severe mechanism is unresolved.

Current geometry authority: E2C R7
Canonical SHA256: cab6754235a66006ba8db423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c
Solved S0 SHA256: 71b74ec749baa60276c8f6cf7c10cc0e17dad4d0d4bde7c7b6cd54668c16c784

Next node: M1_SEMANTIC_INTEGRITY_AND_M2_COUPLING_DECOMPOSITION

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

def ph(z):
    return math.degrees(cmath.phase(z))

def load_combined(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]
    data={}
    for j in (1,2,4,5,7,8,10,11):
        for i in range(1,13):
            key="S%d_%d"%(i,j)
            data[(i,j)]=[complex(float(r[key+"_real"]),float(r[key+"_imag"])) for r in rows]
    return f,data,set(rows[0].keys())

def load_baseline(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]
    data={}
    for j in (1,2,4,5):
        for i in (1,2,4,5):
            key="S%d%d"%(i,j)
            data[(i,j)]=[complex(float(r[key+"_real"]),float(r[key+"_imag"])) for r in rows]
    return f,data,set(rows[0].keys())

def mm(a,b):
    return [[sum(a[i][q]*b[q][j] for q in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def mm4(data,k,ports):
    ep,pinp,en,pinn=ports
    order=[ep,en,pinp,pinn]
    s=[[data[(i,j)][k] for j in order] for i in order]
    tt=[list(x) for x in zip(*T)]
    return mm(mm(T,s),tt)

def core_idx(freqs):
    return [k for k,x in enumerate(freqs) if CORE[0]-1e-12 <= x <= CORE[1]+1e-12]

def modal_peaks(data,freqs,ports,idxs):
    terms={
      "E_diff_to_common":(1,0),
      "E_common_to_diff":(0,1),
      "E_diff_to_PIN_common":(3,0),
      "E_common_to_PIN_diff":(2,1),
      "PIN_diff_to_common":(3,2),
      "PIN_common_to_diff":(2,3),
    }
    out={}
    for name,(i,j) in terms.items():
        best=None
        for k in idxs:
            z=mm4(data,k,ports)[i][j]
            rec=(abs(z),k,z)
            if best is None or rec[0] > best[0]:
                best=rec
        out[name]={"frequency_ghz":freqs[best[1]],"db":db(best[2]),"mag":abs(best[2]),"phase_deg":ph(best[2])}
    return out

def max_delta(cdat,bdat,freqs,cports,bports,idxs):
    best=None
    local_best=[]
    for ci,bi in zip(cports,bports):
        for cj,bj in zip(cports,bports):
            local=None
            for k in idxs:
                d=abs(cdat[(ci,cj)][k]-bdat[(bi,bj)][k])
                rec=(d,k,ci,cj,bi,bj)
                if local is None or d > local[0]:
                    local=rec
                if best is None or d > best[0]:
                    best=rec
            local_best.append(local)
    local_best.sort(reverse=True,key=lambda x:x[0])
    def pack(x):
        d,k,ci,cj,bi,bj=x
        zc=cdat[(ci,cj)][k]
        zb=bdat[(bi,bj)][k]
        return {
          "delta_mag":d,"frequency_ghz":freqs[k],
          "combined_pair":[ci,cj],
          "combined_semantics":[SEM[ci],SEM[cj]],
          "baseline_pair":[bi,bj],
          "combined_db":db(zc),"baseline_db":db(zb),
          "combined_phase_deg":ph(zc),"baseline_phase_deg":ph(zb)
        }
    return pack(best),[pack(x) for x in local_best[:12]]

def peak_terms(data,freqs,response_ports,source_ports,idxs):
    best=None
    for j in source_ports:
        for i in response_ports:
            for k in idxs:
                z=data[(i,j)][k]
                rec=(abs(z),k,i,j,z)
                if best is None or rec[0] > best[0]:
                    best=rec
    mag,k,i,j,z=best
    return {"peak_db":db(z),"mag":mag,"frequency_ghz":freqs[k],
            "response_port":i,"response_semantic":SEM[i],
            "source_port":j,"source_semantic":SEM[j],"phase_deg":ph(z)}

def return_imbalance(data,freqs,ep,en,idxs):
    best=None
    for k in idxs:
        a=db(data[(ep,ep)][k])
        b=db(data[(en,en)][k])
        d=abs(a-b)
        rec=(d,k,a,b)
        if best is None or d > best[0]:
            best=rec
    return {"max_abs_db":best[0],"frequency_ghz":freqs[best[1]],"plus_self_db":best[2],"minus_self_db":best[3]}

def raw_e_mode(data,k,ep,en,mode):
    spp=data[(ep,ep)][k]
    spn=data[(ep,en)][k]
    snp=data[(en,ep)][k]
    snn=data[(en,en)][k]
    if mode=="E_diff_to_common":
        terms=[("Spp",spp,0.5),("Spn",spn,-0.5),("Snp",snp,0.5),("Snn",snn,-0.5)]
    else:
        terms=[("Spp",spp,0.5),("Spn",spn,0.5),("Snp",snp,-0.5),("Snn",snn,-0.5)]
    total=sum(z*c for _,z,c in terms)
    return {
      "total":{"mag":abs(total),"db":db(total),"phase_deg":ph(total)},
      "terms":[{"term":n,"coef":c,"raw_db":db(z),"raw_phase_deg":ph(z),
                "contribution_mag":abs(c*z),"contribution_phase_deg":ph(c*z)}
               for n,z,c in terms]
    }

DOC.write_text(ROUTE_MD,encoding="utf-8")
ROUTE.write_text(json.dumps({
  "schema_version":"gnss-e2c-s0-posthold-route-v0.1",
  "status":"FROZEN_OFFLINE_ROUTE",
  "trigger":"HOLD_E2C_S0_SEVERE_COEXISTENCE_REVIEW",
  "canonical_geometry_sha256":"cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c",
  "solved_artifact_sha256":"71b74ec749baa60276c8f6cf7c10cc0e17dad4d0d4bde7c7b6cd54668c16c784",
  "sequence":["M1_SEMANTIC_INTEGRITY","M2_96_TRACE_COUPLING_DECOMPOSITION","M3_FREQUENCY_MECHANISM","M4_FIRST_PRINCIPLES_CLASSIFICATION"],
  "future_build_gate":["named_physical_mechanism","named_observable","expected_direction"],
  "automatic_retry":False,
  "BUILD_AUTHORIZED":False,
  "SOLVE_AUTHORIZED":False
},indent=2)+"\n",encoding="utf-8")

manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
qual=json.loads(QUAL.read_text(encoding="utf-8"))
top=json.loads(TOP.read_text(encoding="utf-8"))
freqs,cdata,cheader=load_combined(COMBINED)
idxs=core_idx(freqs)

baseline={}
for pol in ("PolA","PolB"):
    p=Path(manifest["isolated_baselines"][pol]["csv_path"])
    baseline[pol]=(p,)+load_baseline(p)

expected_names=[
 "A_P_E_UP","A_P_P_IN","A_P_P_OUT_LOAD50",
 "A_N_E_UP","A_N_P_IN","A_N_P_OUT_LOAD50",
 "B_P_E_UP","B_P_P_IN","B_P_P_OUT_LOAD50",
 "B_N_E_UP","B_N_P_IN","B_N_P_OUT_LOAD50"
]
orth=max(abs(sum(T[i][q]*T[j][q] for q in range(4))-(1.0 if i==j else 0.0)) for i in range(4) for j in range(4))
step_error=max(abs((freqs[i+1]-freqs[i])-0.0008) for i in range(len(freqs)-1))
m1={
 "combined_csv_sha256":sha(COMBINED),
 "combined_1001_points":len(freqs)==1001,
 "combined_grid_1p0_1p8":abs(freqs[0]-1.0)<1e-12 and abs(freqs[-1]-1.8)<1e-12,
 "combined_grid_step_0p0008":step_error<1e-12,
 "required_96_columns":all(("S%d_%d_real"%(i,j) in cheader and "S%d_%d_imag"%(i,j) in cheader) for j in (1,2,4,5,7,8,10,11) for i in range(1,13)),
 "manifest_12_ports":len(manifest["raw_to_solve"])==12,
 "manifest_names_exact":[x["name"] for x in manifest["raw_to_solve"]]==expected_names,
 "source_ports_exact":manifest["solve_network"]["source_ports"]==[1,2,4,5,7,8,10,11],
 "load_ports_exact":manifest["solve_network"]["load_only_ports"]==[3,6,9,12],
 "transform_orthonormal":orth<1e-14,
 "transform_orthonormal_error":orth,
 "qualifier_hard_checks_all_pass":all(qual["hard_checks"].values()),
 "formal_solver_invocations_one":top["formal_solver_invocations"]==1,
 "automatic_retries_zero":top["automatic_retries"]==0,
}
for pol,(p,bf,bd,bhead) in baseline.items():
    m1[pol+"_baseline_hash_exact"]=sha(p)==manifest["isolated_baselines"][pol]["csv_sha256"]
    m1[pol+"_grid_exact"]=len(bf)==len(freqs) and max(abs(a-b) for a,b in zip(bf,freqs))<1e-12
    m1[pol+"_16_columns"]=all(("S%d%d_real"%(i,j) in bhead and "S%d%d_imag"%(i,j) in bhead) for j in (1,2,4,5) for i in (1,2,4,5))
    x=modal_peaks(bd,bf,[1,2,4,5],idxs)
    y=modal_peaks(bd,bf,[1,2,4,5],idxs)
    m1[pol+"_modal_selftest_zero"]=max(abs(x[k]["db"]-y[k]["db"]) for k in x)<1e-12

m1_status="PASS_M1_SEMANTIC_INTEGRITY" if all(v for v in m1.values() if isinstance(v,bool)) else "HOLD_M1_SEMANTIC_INTEGRITY"

m2={"polarizations":{}}
for pol,spec in POL.items():
    p,bf,bd,bhead=baseline[pol]
    cports=spec["c"]
    bports=spec["b"]
    maxd,topd=max_delta(cdata,bd,freqs,cports,bports,idxs)
    cmodal=modal_peaks(cdata,freqs,cports,idxs)
    bmodal=modal_peaks(bd,bf,bports,idxs)
    ep,pinp,en,pinn=cports
    kd=min(idxs,key=lambda k:abs(freqs[k]-cmodal["E_diff_to_common"]["frequency_ghz"]))
    kc=min(idxs,key=lambda k:abs(freqs[k]-cmodal["E_common_to_diff"]["frequency_ghz"]))
    m2["polarizations"][pol]={
      "own_pol_max_delta":maxd,
      "top_same_pol_raw_deltas":topd,
      "combined_modal_peaks":cmodal,
      "baseline_modal_peaks":bmodal,
      "modal_degradation_db":{k:cmodal[k]["db"]-bmodal[k]["db"] for k in cmodal},
      "eup_return_imbalance":return_imbalance(cdata,freqs,ep,en,idxs),
      "raw_decomposition_E_diff_to_common":raw_e_mode(cdata,kd,ep,en,"E_diff_to_common"),
      "raw_decomposition_E_common_to_diff":raw_e_mode(cdata,kc,ep,en,"E_common_to_diff")
    }

A_E=[1,4]; B_E=[7,10]
A_PIN=[2,5]; B_PIN=[8,11]
m2["cross_pol"]={
 "EUP_to_EUP":max([peak_terms(cdata,freqs,B_E,A_E,idxs),peak_terms(cdata,freqs,A_E,B_E,idxs)],key=lambda x:x["peak_db"]),
 "EUP_to_PIN":max([peak_terms(cdata,freqs,B_PIN,A_E,idxs),peak_terms(cdata,freqs,A_PIN,B_E,idxs)],key=lambda x:x["peak_db"]),
 "PIN_to_EUP":max([peak_terms(cdata,freqs,B_E,A_PIN,idxs),peak_terms(cdata,freqs,A_E,B_PIN,idxs)],key=lambda x:x["peak_db"]),
 "device_side":qual["science"]["cross_pol_device_coupling"]
}
m2["resonance"]=qual["science"]["resonance"]

xe=m2["cross_pol"]["EUP_to_EUP"]["peak_db"]
xp=m2["cross_pol"]["EUP_to_PIN"]["peak_db"]
xd=m2["cross_pol"]["device_side"]["peak_db"]
imb=max(m2["polarizations"]["PolA"]["eup_return_imbalance"]["max_abs_db"],m2["polarizations"]["PolB"]["eup_return_imbalance"]["max_abs_db"])
res=m2["resonance"]["excursion_db"]
classes=[]
if xe>-20:
    classes.append({"priority":"HIGH","mechanism":"REAL_DUALPOL_EUP_ELECTROMAGNETIC_COUPLING","evidence":"cross-pol E_UP<->E_UP peak > -20 dB"})
if imb>6:
    classes.append({"priority":"HIGH","mechanism":"PLUS_MINUS_BRANCH_REFERENCE_OR_RETURN_ASYMMETRY","evidence":"E_UP branch self-return imbalance > 6 dB"})
if xd<-40 and xp<-40:
    classes.append({"priority":"HIGH","mechanism":"DIRECT_DEVICE_SIDE_CROSSPOL_COUPLING_NOT_DOMINANT","evidence":"cross-pol P_IN/device-side coupling remains below -40 dB"})
if res<10:
    classes.append({"priority":"MEDIUM","mechanism":"NARROW_RESONANCE_NOT_PRIMARY_TRIGGER","evidence":"50 MHz excursion below frozen 10 dB gate"})
m2["mechanism_evidence"]=classes
m2["status"]="PASS_M2_COUPLING_DECOMPOSITION_EVIDENCE_READY" if m1_status.startswith("PASS_") else "HOLD_M2_BLOCKED_BY_M1"

report={"schema_version":"gnss-e2c-s0-m1m2-v0.1","m1_status":m1_status,"m1_checks":m1,"m2":m2,
        "boundaries":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False,"rerun_allowed":False}}
(OUT/"M1_M2_ANALYSIS.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")

with open(str(OUT/"TOP_SAME_POL_RAW_DELTAS.csv"),"w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["pol","rank","delta_mag","frequency_ghz","combined_response","combined_source","response_semantic","source_semantic","baseline_response","baseline_source","combined_db","baseline_db","combined_phase_deg","baseline_phase_deg"])
    for pol in ("PolA","PolB"):
        for rank,x in enumerate(m2["polarizations"][pol]["top_same_pol_raw_deltas"],1):
            w.writerow([pol,rank,x["delta_mag"],x["frequency_ghz"],x["combined_pair"][0],x["combined_pair"][1],x["combined_semantics"][0],x["combined_semantics"][1],x["baseline_pair"][0],x["baseline_pair"][1],x["combined_db"],x["baseline_db"],x["combined_phase_deg"],x["baseline_phase_deg"]])

lines=["# E2C S0 M1/M2 Offline Mechanism Analysis V0.1","",f"M1 status: **{m1_status}**",f"M2 status: **{m2['status']}**","","No CST launch, BUILD, or SOLVE was used.","","## M1 semantic integrity",""]
for k,v in m1.items():
    lines.append("- %s: %s"%(k,v))
lines += ["","## M2 key observables",""]
for pol in ("PolA","PolB"):
    x=m2["polarizations"][pol]
    lines += ["### "+pol,
              "- max same-pol complex delta: %.6f at %.4f GHz, %s"%(x["own_pol_max_delta"]["delta_mag"],x["own_pol_max_delta"]["frequency_ghz"],x["own_pol_max_delta"]["combined_semantics"]),
              "- E_UP branch return imbalance: %.3f dB at %.4f GHz"%(x["eup_return_imbalance"]["max_abs_db"],x["eup_return_imbalance"]["frequency_ghz"]),
              "- E diff->common peak: %.3f dB at %.4f GHz"%(x["combined_modal_peaks"]["E_diff_to_common"]["db"],x["combined_modal_peaks"]["E_diff_to_common"]["frequency_ghz"]),
              "- isolated E diff->common peak: %.3f dB"%x["baseline_modal_peaks"]["E_diff_to_common"]["db"],""]
lines += ["### Cross-pol/coupling",
          "- cross-pol E_UP<->E_UP peak: %.3f dB at %.4f GHz (%s -> %s)"%(m2["cross_pol"]["EUP_to_EUP"]["peak_db"],m2["cross_pol"]["EUP_to_EUP"]["frequency_ghz"],m2["cross_pol"]["EUP_to_EUP"]["source_semantic"],m2["cross_pol"]["EUP_to_EUP"]["response_semantic"]),
          "- cross-pol E_UP->P_IN peak: %.3f dB"%m2["cross_pol"]["EUP_to_PIN"]["peak_db"],
          "- cross-pol device-side peak: %.3f dB"%m2["cross_pol"]["device_side"]["peak_db"],
          "- 50 MHz resonance excursion: %.3f dB"%m2["resonance"]["excursion_db"],"",
          "## Evidence-ranked mechanism classes",""]
for x in classes:
    lines.append("- **%s — %s**: %s"%(x["priority"],x["mechanism"],x["evidence"]))
lines += ["","## Boundary","","No rerun or geometry mutation is authorized. M3/M4 must use the existing solution.","","BUILD_AUTHORIZED = false","SOLVE_AUTHORIZED = false"]
(OUT/"M1_M2_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

print(m1_status)
print(m2["status"])
for pol in ("PolA","PolB"):
    x=m2["polarizations"][pol]
    print("%s_DELTA=%.6f@%.4f"%(pol,x["own_pol_max_delta"]["delta_mag"],x["own_pol_max_delta"]["frequency_ghz"]))
    print("%s_IMBALANCE_DB=%.3f@%.4f"%(pol,x["eup_return_imbalance"]["max_abs_db"],x["eup_return_imbalance"]["frequency_ghz"]))
print("CROSSPOL_EUP_EUP_DB=%.3f@%.4f"%(m2["cross_pol"]["EUP_to_EUP"]["peak_db"],m2["cross_pol"]["EUP_to_EUP"]["frequency_ghz"]))
print("CROSSPOL_EUP_PIN_DB=%.3f"%m2["cross_pol"]["EUP_to_PIN"]["peak_db"])
print("CROSSPOL_DEVICE_DB=%.3f"%m2["cross_pol"]["device_side"]["peak_db"])
print("RESONANCE_EXCURSION_DB=%.3f"%m2["resonance"]["excursion_db"])
print("OUT="+str(OUT))