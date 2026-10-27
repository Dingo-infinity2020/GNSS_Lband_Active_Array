#!/usr/bin/env python3
"""Read-only QPL9547 source-conditioned noise shadow for solved H0/P1 branches."""
import csv,cmath,json,math,os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MIX=os.path.join(ROOT,"evidence","r1e1a4a_h0_p1_b0_nw_20260925_solve01","mixed_mode_2port_readonly.csv")
NOISE=os.path.join(ROOT,"circuit","qpl9547","QPL9547_NOISE_REFERENCE_1P1_1P7.csv")
OUT=os.path.join(ROOT,"circuit","qpl9547","analysis","R1E1A4A_H0_P1_B0_QPL9547_RECEIVER_SHADOW.json")
Z0=50.0; T0=290.0; LO=1.15; HI=1.65

def load_noise():
    rows=[]
    for r in csv.DictReader(open(NOISE,newline="")):
        f=float(r["freq_ghz"])
        g=float(r["gammaopt_mag"])*cmath.exp(1j*math.radians(float(r["gammaopt_deg"])))
        fmin=10**(float(r["nfmin_db"])/10.0)
        rows.append((f,fmin,g,float(r["rn_ohm"])))
    return rows

def interp(f,t):
    for a,b in zip(t[:-1],t[1:]):
        if a[0]<=f<=b[0]:
            q=(f-a[0])/(b[0]-a[0])
            return (a[1]+q*(b[1]-a[1]), a[2]+q*(b[2]-a[2]), a[3]+q*(b[3]-a[3]))
    raise ValueError(f)

def noise(z,f,t):
    gs=(z-Z0)/(z+Z0)
    fmin,go,rn=interp(f,t)
    den=(1-abs(gs)**2)*abs(1+go)**2
    if den<=0: return None
    F=fmin+(4*rn/Z0)*abs(gs-go)**2/den
    return {"nf_db":10*math.log10(F),"te_k":T0*(F-1),"gamma_s_mag":abs(gs)}

def main():
    t=load_noise(); vals=[]
    for r in csv.DictReader(open(MIX,newline="")):
        f=float(r["freq_ghz"])
        if not LO<=f<=HI: continue
        z1=complex(float(r["zb1_re"]),float(r["zb1_im"]))
        z2=complex(float(r["zb2_re"]),float(r["zb2_im"]))
        n1=noise(z1,f,t); n2=noise(z2,f,t)
        vals.append((f,z1,z2,n1,n2))
    if not vals: raise SystemExit("HOLD_NO_H0_P1_ROWS")
    out={"status":"READONLY_SOURCE_CONDITIONED_DEVICE_NOISE_SHADOW",
         "gate_r_r_nf0_limit_db":0.40,"sample_count":len(vals),"branches":{}}
    for idx in (1,2):
        ns=[x[2+idx] for x in vals]
        fs=[x[0] for x in vals]
        mx=max(range(len(ns)),key=lambda i:ns[i]["nf_db"])
        mn=min(range(len(ns)),key=lambda i:ns[i]["nf_db"])
        failing=[i for i,n in enumerate(ns) if n["nf_db"]>0.40]
        out["branches"]["P1A" if idx==1 else "P1B"]={
          "nf_db_min":ns[mn]["nf_db"],"nf_db_min_freq_ghz":fs[mn],
          "nf_db_max":ns[mx]["nf_db"],"nf_db_max_freq_ghz":fs[mx],
          "te_k_max":max(n["te_k"] for n in ns),
          "gamma_s_mag_max":max(n["gamma_s_mag"] for n in ns),
          "r_nf0_fail_count":len(failing),
          "r_nf0_fail_fraction":len(failing)/len(ns),
          "r_nf0_fail_freq_min_ghz":fs[min(failing)] if failing else None,
          "r_nf0_fail_freq_max_ghz":fs[max(failing)] if failing else None,
          "r_nf0_pass":ns[mx]["nf_db"]<=0.40}
    out["r_nf0_both_branches_pass"]=all(x["r_nf0_pass"] for x in out["branches"].values())
    # Anchor branch impedances and NFs.
    anchors={}
    for f0 in (1.15,1.2,1.3,1.4,1.5,1.6,1.65):
        x=min(vals,key=lambda y:abs(y[0]-f0))
        anchors[str(f0)]={"freq_ghz":x[0],
          "zb1_re":x[1].real,"zb1_im":x[1].imag,"zb2_re":x[2].real,"zb2_im":x[2].imag,
          "nf1_db":x[3]["nf_db"],"nf2_db":x[4]["nf_db"]}
    out["anchors"]=anchors
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    json.dump(out,open(OUT,"w"),indent=2)
    print(json.dumps(out,indent=2))

if __name__=="__main__": main()
