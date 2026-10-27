#!/usr/bin/env python3
"""R1E1A4A illustrative receiver-shadow diagnostic.

ASSUMPTION_DIAGNOSTIC ONLY:
- ideal odd-mode / virtual-ground symmetry;
- each single-ended LNA sees Zs = Zdiff / 2 at its device-lead reference plane;
- no feed-transition loss or transformation between CST P0 and LNA P1;
- QPL9547 noise parameters linearly interpolated in frequency.

These assumptions are NOT frozen architecture facts and MUST NOT be used as Gate R.
"""
from __future__ import print_function
import csv, cmath, json, math, os

ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOISE=os.path.join(ROOT,"circuit","qpl9547","QPL9547_NOISE_REFERENCE_1P1_1P7.csv")
OUTDIR=os.path.join(ROOT,"circuit","qpl9547","analysis")
Z0=50.0
T0=290.0
SCI_LO=1.15
SCI_HI=1.65

CASES={
 "B0":(
   os.path.join(ROOT,"evidence","r1e0b_dc_nw_20260924_smoke01","active_s11_and_zactive.csv"),
   os.path.join(ROOT,"evidence","r1e1a3r1_s1_b0_nw_20260925_solve01","active_s11_and_zactive.csv")),
 "C60P45":(
   os.path.join(ROOT,"evidence","r1e0c_b_c60p45_dc_nw_20260924_solve01","active_s11_and_zactive.csv"),
   os.path.join(ROOT,"evidence","r1e1a3r1_s1_c60p45_nw_20260925_solve01","active_s11_and_zactive.csv")),
 "C60P135":(
   os.path.join(ROOT,"evidence","r1e0c_b_c60p135_dc_nw_20260924_solve01","active_s11_and_zactive.csv"),
   os.path.join(ROOT,"evidence","r1e1a3r1_s1_c60p135_nw_20260925_solve01","active_s11_and_zactive.csv")),
}

def load_noise():
    out=[]
    for r in csv.DictReader(open(NOISE,newline="")):
        f=float(r["freq_ghz"])
        mag=float(r["gammaopt_mag"]); deg=float(r["gammaopt_deg"])
        g=mag*cmath.exp(1j*math.radians(deg))
        fmin=10.0**(float(r["nfmin_db"])/10.0)
        out.append((f,fmin,g,float(r["rn_ohm"])))
    return sorted(out)

def interp(f,tab):
    if not (tab[0][0] <= f <= tab[-1][0]):
        raise ValueError("frequency outside noise table: %s"%f)
    for a,b in zip(tab[:-1],tab[1:]):
        if a[0] <= f <= b[0]:
            t=(f-a[0])/(b[0]-a[0])
            fmin=a[1]+t*(b[1]-a[1])
            g=a[2]+t*(b[2]-a[2])
            rn=a[3]+t*(b[3]-a[3])
            return fmin,g,rn
    return tab[-1][1:]

def load_z(path):
    out={}
    for r in csv.DictReader(open(path,newline="")):
        f=float(r["freq_ghz"])
        if SCI_LO <= f <= SCI_HI:
            out[round(f,9)] = complex(float(r["zactive_re_ohm"]),float(r["zactive_im_ohm"]))
    return out

def noise_from_zdiff(f,zdiff,tab):
    zs=zdiff/2.0
    gs=(zs-Z0)/(zs+Z0)
    fmin,gopt,rn=interp(f,tab)
    den=(1.0-abs(gs)**2)*abs(1.0+gopt)**2
    if den <= 0:
        return {"valid":False}
    F=fmin + (4.0*rn/Z0)*(abs(gs-gopt)**2)/den
    return {
      "valid":True,
      "zs_re":zs.real,"zs_im":zs.imag,
      "gamma_s_mag":abs(gs),"gamma_s_deg":math.degrees(cmath.phase(gs)),
      "nf_db":10.0*math.log10(F),
      "te_k":T0*(F-1.0),
      "nfmin_db":10.0*math.log10(fmin),
      "gopt_mag":abs(gopt),"gopt_deg":math.degrees(cmath.phase(gopt)),
      "rn_ohm":rn,
    }

def main():
    os.makedirs(OUTDIR,exist_ok=True)
    tab=load_noise()
    all_summary={}
    for state,(barep,s1p) in CASES.items():
        bare=load_z(barep); s1=load_z(s1p)
        freqs=sorted(set(bare)&set(s1))
        rows=[]
        for f in freqs:
            nb=noise_from_zdiff(f,bare[f],tab)
            ns=noise_from_zdiff(f,s1[f],tab)
            if not nb["valid"] or not ns["valid"]:
                continue
            rows.append({
              "freq_ghz":f,
              "bare_zdiff_re":bare[f].real,"bare_zdiff_im":bare[f].imag,
              "s1_zdiff_re":s1[f].real,"s1_zdiff_im":s1[f].imag,
              "bare_branch_nf_db":nb["nf_db"],"s1_branch_nf_db":ns["nf_db"],
              "delta_nf_db":ns["nf_db"]-nb["nf_db"],
              "bare_branch_te_k":nb["te_k"],"s1_branch_te_k":ns["te_k"],
              "delta_te_k":ns["te_k"]-nb["te_k"],
              "bare_branch_zs_re":nb["zs_re"],"bare_branch_zs_im":nb["zs_im"],
              "s1_branch_zs_re":ns["zs_re"],"s1_branch_zs_im":ns["zs_im"],
              "nfmin_db":nb["nfmin_db"],
            })
        if not rows:
            raise SystemExit("HOLD_NO_ROWS_"+state)
        max_abs_dnf=max(rows,key=lambda r:abs(r["delta_nf_db"]))
        max_abs_dte=max(rows,key=lambda r:abs(r["delta_te_k"]))
        summary={
          "sample_count":len(rows),
          "bare_nf_db_min":min(r["bare_branch_nf_db"] for r in rows),
          "bare_nf_db_max":max(r["bare_branch_nf_db"] for r in rows),
          "s1_nf_db_min":min(r["s1_branch_nf_db"] for r in rows),
          "s1_nf_db_max":max(r["s1_branch_nf_db"] for r in rows),
          "max_abs_delta_nf_db":abs(max_abs_dnf["delta_nf_db"]),
          "max_abs_delta_nf_db_signed":max_abs_dnf["delta_nf_db"],
          "max_abs_delta_nf_freq_ghz":max_abs_dnf["freq_ghz"],
          "max_abs_delta_te_k":abs(max_abs_dte["delta_te_k"]),
          "max_abs_delta_te_k_signed":max_abs_dte["delta_te_k"],
          "max_abs_delta_te_freq_ghz":max_abs_dte["freq_ghz"],
          "mean_delta_te_k":sum(r["delta_te_k"] for r in rows)/len(rows),
        }
        all_summary[state]=summary
        outcsv=os.path.join(OUTDIR,"R1E1A4A_%s_IDEAL_ODDMODE_QPL9547_NOISE_SHADOW.csv"%state)
        with open(outcsv,"w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        print(state+" "+json.dumps(summary,sort_keys=True))
    payload={
      "status":"ASSUMPTION_DIAGNOSTIC_ONLY_NOT_GATE_R",
      "assumption":"ideal virtual ground; each LNA sees Zdiff/2 directly at QPL9547 device-lead plane",
      "noise_parameter_source":"QPL9547 Rev D anchor table in project",
      "states":all_summary,
    }
    with open(os.path.join(OUTDIR,"R1E1A4A_IDEAL_ODDMODE_QPL9547_NOISE_SHADOW_SUMMARY.json"),"w") as f:
        json.dump(payload,f,indent=2)
    print("PASS_R1E1A4A_IDEAL_ODDMODE_DIAGNOSTIC")
    print("GATE_R_FROZEN=NO")

if __name__=="__main__":
    main()
