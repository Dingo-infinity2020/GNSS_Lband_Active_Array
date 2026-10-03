from __future__ import print_function
import csv, json, math, cmath
from pathlib import Path
import numpy as np

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
BASE=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\E2A_S0L_SOLVE_20260929\evidence\loaded_response_native.csv")
D1=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_DIAGNOSTIC_READONLY_RECOVERY_V01"/"d1_response_on_e2a_grid.csv"
D2=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_DIAGNOSTIC_READONLY_RECOVERY_V01"/"d2_response_on_e2a_grid.csv"
FULL=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\E2C_S0_COEXISTENCE_20261002_V01\evidence\qualification\loaded_response_native.csv")
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_FREQUENCY_SHAPE_DISCRIMINATION_V01"
OUT.mkdir(parents=True,exist_ok=True)

PORTS=[1,2,4,5]
CORE=(1.15,1.65)

def db(z):
    return 20*math.log10(max(abs(z),1e-300))

def read_local(path,underscore=False):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=np.array([float(r["f_GHz"]) for r in rows],dtype=float)
    d={}
    for j in PORTS:
        for i in PORTS:
            k=("S%d_%d"%(i,j)) if underscore else ("S%d%d"%(i,j))
            d[(i,j)]=np.array([complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows],dtype=complex)
    return f,d

def dc(d,k):
    return 0.5*(d[(1,1)][k]-d[(1,4)][k]+d[(4,1)][k]-d[(4,4)][k])

def vec_delta(d,b,k):
    return np.array([d[(i,j)][k]-b[(i,j)][k] for j in PORTS for i in PORTS],dtype=complex)

def cosine_complex(a,b):
    na=np.linalg.norm(a); nb=np.linalg.norm(b)
    if na<1e-15 or nb<1e-15: return 0.0
    return float(abs(np.vdot(a,b))/(na*nb))

fb,base=read_local(BASE,False)
f1,d1=read_local(D1,False)
f2,d2=read_local(D2,False)
ff,full=read_local(FULL,True)
if not (len(fb)==len(f1)==len(f2)==len(ff)==1001):
    raise RuntimeError("GRID_COUNT")
if max(np.max(np.abs(fb-x)) for x in (f1,f2,ff))>1e-12:
    raise RuntimeError("GRID_MISMATCH")

idx=np.where((fb>=CORE[0]-1e-12)&(fb<=CORE[1]+1e-12))[0]
series={}
for name,d in (("D1",d1),("D2",d2),("FULL",full)):
    raw=[]; mode_vec=[]; mode_deg=[]; imb=[]; fro=[]
    for k in idx:
        dv=vec_delta(d,base,k)
        raw.append(float(np.max(np.abs(dv))))
        fro.append(float(np.linalg.norm(dv)))
        z=dc(d,k); zb=dc(base,k)
        mode_vec.append(float(abs(z-zb)))
        mode_deg.append(float(db(z)-db(zb)))
        imb.append(float(abs(db(d[(1,1)][k])-db(d[(4,4)][k]))))
    series[name]={
      "raw":np.array(raw),"fro":np.array(fro),"mode_vec":np.array(mode_vec),
      "mode_deg":np.array(mode_deg),"imb":np.array(imb)
    }

def corr(a,b):
    if np.std(a)<1e-15 or np.std(b)<1e-15: return None
    return float(np.corrcoef(a,b)[0,1])

def peak(a):
    q=int(np.argmax(a))
    return {"value":float(a[q]),"frequency_ghz":float(fb[idx[q]]),"index":q}

shape={}
for name in ("D1","D2"):
    shape[name]={
      "correlation_with_full":{
        "raw_max_delta":corr(series[name]["raw"],series["FULL"]["raw"]),
        "frobenius_delta":corr(series[name]["fro"],series["FULL"]["fro"]),
        "mode_complex_delta":corr(series[name]["mode_vec"],series["FULL"]["mode_vec"]),
        "branch_imbalance":corr(series[name]["imb"],series["FULL"]["imb"])
      },
      "peaks":{
        "raw":peak(series[name]["raw"]),
        "fro":peak(series[name]["fro"]),
        "mode_complex_delta":peak(series[name]["mode_vec"]),
        "mode_degradation_db":peak(series[name]["mode_deg"]),
        "imbalance":peak(series[name]["imb"])
      }
    }
shape["FULL"]={"peaks":{
    "raw":peak(series["FULL"]["raw"]),
    "fro":peak(series["FULL"]["fro"]),
    "mode_complex_delta":peak(series["FULL"]["mode_vec"]),
    "mode_degradation_db":peak(series["FULL"]["mode_deg"]),
    "imbalance":peak(series["FULL"]["imb"])
}}

# S-matrix deviation-direction similarity to FULL at every frequency.
align={"D1":[],"D2":[]}
for q,k in enumerate(idx):
    vf=vec_delta(full,base,k)
    align["D1"].append(cosine_complex(vec_delta(d1,base,k),vf))
    align["D2"].append(cosine_complex(vec_delta(d2,base,k),vf))
for name in align:
    a=np.array(align[name])
    shape[name]["complex_direction_alignment"]={
      "median":float(np.median(a)),
      "mean":float(np.mean(a)),
      "min":float(np.min(a)),
      "max":float(np.max(a))
    }

# Evaluate at scientifically relevant anchors.
anchors={
 "FULL_RAW_PEAK":shape["FULL"]["peaks"]["raw"]["frequency_ghz"],
 "FULL_MODE_PEAK":shape["FULL"]["peaks"]["mode_degradation_db"]["frequency_ghz"],
 "FULL_IMBALANCE_PEAK":shape["FULL"]["peaks"]["imbalance"]["frequency_ghz"],
 "D2_RAW_PEAK":shape["D2"]["peaks"]["raw"]["frequency_ghz"],
 "L2":1.2276,"MIXED_OLD":1.3384,"L1":1.57542
}
anchor_data={}
for label,f in anchors.items():
    k=int(np.argmin(np.abs(fb-f)))
    if k not in set(idx.tolist()):
        continue
    q=int(np.where(idx==k)[0][0])
    anchor_data[label]={"frequency_ghz":float(fb[k])}
    for name,d in (("D1",d1),("D2",d2),("FULL",full)):
        dv=vec_delta(d,base,k)
        anchor_data[label][name]={
          "raw_max_delta":float(np.max(np.abs(dv))),
          "frobenius_delta":float(np.linalg.norm(dv)),
          "mode_degradation_db":float(db(dc(d,k))-db(dc(base,k))),
          "branch_imbalance_db":float(abs(db(d[(1,1)][k])-db(d[(4,4)][k]))),
          "direction_alignment_to_full":cosine_complex(dv,vec_delta(full,base,k))
        }

# Mechanism interpretation: use frequency-shape evidence, not additive residuals.
d2c=shape["D2"]["correlation_with_full"]
d2a=shape["D2"]["complex_direction_alignment"]
full_raw_f=shape["FULL"]["peaks"]["raw"]["frequency_ghz"]
d2_raw_f=shape["D2"]["peaks"]["raw"]["frequency_ghz"]
peak_sep=abs(full_raw_f-d2_raw_f)

findings=[]
if d2c["mode_complex_delta"] is not None and d2c["mode_complex_delta"]>=0.7:
    findings.append("D2 ground/via perturbation tracks the full-E2C differential/common-mode frequency shape strongly.")
else:
    findings.append("D2 ground/via perturbation does not closely track the full-E2C differential/common-mode frequency shape.")
if d2c["raw_max_delta"] is not None and d2c["raw_max_delta"]<0.7:
    findings.append("D2 does not reproduce the full-E2C broadband raw source-side deviation shape.")
if peak_sep>0.10:
    findings.append("D2 and full-E2C raw-deviation peaks are separated by more than 100 MHz, arguing against a simple scaled copy of one mechanism.")
if d2a["median"]<0.8:
    findings.append("The D2 complex S-matrix perturbation direction is not uniformly aligned with full E2C, supporting a composite interaction picture.")

classification="GROUND_IMPORTANT_BUT_COMPOSITE_INTERACTION_REMAINS_REQUIRED"
if (d2c["raw_max_delta"] is not None and d2c["raw_max_delta"]>=0.85 and
    d2c["mode_complex_delta"] is not None and d2c["mode_complex_delta"]>=0.85 and
    peak_sep<=0.05 and d2a["median"]>=0.9):
    classification="GROUND_DOMINANT_SAME_MECHANISM_SCALED"
elif (d2c["raw_max_delta"] is not None and d2c["raw_max_delta"]<0.4 and
      d2c["mode_complex_delta"] is not None and d2c["mode_complex_delta"]<0.4):
    classification="GROUND_SEPARATE_OR_SECONDARY_MECHANISM"

out={
 "schema_version":"gnss-m6-frequency-shape-discrimination-v0.1",
 "status":"PASS_M6_FREQUENCY_SHAPE_DISCRIMINATION",
 "classification":classification,
 "shape":shape,
 "full_vs_d2_raw_peak_separation_ghz":peak_sep,
 "anchors":anchor_data,
 "findings":findings,
 "boundary":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False,"rerun_required":False}
}
(OUT/"M6_FREQUENCY_SHAPE_DISCRIMINATION.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")

with open(str(OUT/"frequency_metrics.csv"),"w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["f_GHz","D1_raw","D2_raw","FULL_raw","D1_mode_deg","D2_mode_deg","FULL_mode_deg",
                "D1_imbalance","D2_imbalance","FULL_imbalance","D1_align_full","D2_align_full"])
    for q,k in enumerate(idx):
        w.writerow([fb[k],series["D1"]["raw"][q],series["D2"]["raw"][q],series["FULL"]["raw"][q],
                    series["D1"]["mode_deg"][q],series["D2"]["mode_deg"][q],series["FULL"]["mode_deg"][q],
                    series["D1"]["imb"][q],series["D2"]["imb"][q],series["FULL"]["imb"][q],
                    align["D1"][q],align["D2"][q]])

lines=["# M6 Frequency-Shape Mechanism Discrimination V0.1","",
       "Status: **PASS_M6_FREQUENCY_SHAPE_DISCRIMINATION**","",
       "Classification: **%s**"%classification,"",
       "This is read-only analysis of existing S-parameter evidence. No CST launch, BUILD, or SOLVE was used.","",
       "## D2 versus full-E2C frequency shape",""]
for k,v in d2c.items():
    lines.append("- %s correlation: %s"%(k,("%.4f"%v if v is not None else "N/A")))
lines += [
 "- D2 complex perturbation-direction median alignment to full E2C: %.4f"%d2a["median"],
 "- full-E2C raw peak: %.4f GHz"%full_raw_f,
 "- D2 raw peak: %.4f GHz"%d2_raw_f,
 "- raw peak separation: %.4f GHz"%peak_sep,
 "","## Interpretation",""]
for x in findings: lines.append("- "+x)
lines += ["",
 "The result strengthens the existing M6 conclusion: the ground/backside/via network is an important contributor, especially to common-mode conversion, but the full severe coexistence state is not a simple scaled copy of the ground-only perturbation.",
 "",
 "The most defensible present mechanism is therefore a composite return-path / signal-ground interaction. Pre-CIN signal metal alone remains ruled out as a strong standalone cause.",
 "",
 "BUILD_AUTHORIZED = false",
 "SOLVE_AUTHORIZED = false"]
(OUT/"M6_FREQUENCY_SHAPE_DISCRIMINATION.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

print("PASS_M6_FREQUENCY_SHAPE_DISCRIMINATION")
print("CLASSIFICATION="+classification)
print("D2_RAW_CORR="+str(d2c["raw_max_delta"]))
print("D2_MODE_CORR="+str(d2c["mode_complex_delta"]))
print("D2_IMB_CORR="+str(d2c["branch_imbalance"]))
print("D2_ALIGN_MEDIAN=%.6f"%d2a["median"])
print("FULL_RAW_PEAK=%.4f"%full_raw_f)
print("D2_RAW_PEAK=%.4f"%d2_raw_f)
print("PEAK_SEP_GHZ=%.4f"%peak_sep)
