#!/usr/bin/env python3
"""R4-A0-C0 QPL9547 G0 committed-data sanity audit.

This is a local/circuit-data audit only.
It does not authorize CST, ADS, NW/XW/251, or any differential Z/2 mapping.
"""
from __future__ import print_function
import csv, cmath, json, math, os

ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOISE=os.path.join(ROOT,"circuit","qpl9547","QPL9547_NOISE_REFERENCE_1P1_1P7.csv")
SPAR=os.path.join(ROOT,"circuit","qpl9547","QPL9547_SPARAM_REFERENCE_1P15_1P65.csv")
OUT=os.path.join(ROOT,"circuit","qpl9547","analysis","R4_A0_C0_G0_DATA_SANITY.json")
Z0=50.0
EXPECTED_S2P_SHA="fad334a226acb9fbe1e4bd769f474afa14e2c23c18f31f4750c091f3d5d0424f"

def nf_from_noise_params(gs,fmin,gopt,rn):
    den=(1.0-abs(gs)**2)*abs(1.0+gopt)**2
    if den<=0:
        raise ValueError("non-passive source reflection coefficient")
    return fmin+(4.0*rn/Z0)*abs(gs-gopt)**2/den

def main():
    noise=list(csv.DictReader(open(NOISE,newline="")))
    spar=list(csv.DictReader(open(SPAR,newline="")))
    if not noise or not spar:
        raise SystemExit("HOLD_R4_A0_C0_EMPTY_REFERENCE_DATA")

    zerr=0.0
    nf50=[]
    for r in noise:
        mag=float(r["gammaopt_mag"])
        deg=float(r["gammaopt_deg"])
        g=mag*cmath.exp(1j*math.radians(deg))
        z=Z0*(1.0+g)/(1.0-g)
        ztab=complex(float(r["zopt_re_ohm"]),float(r["zopt_im_ohm"]))
        zerr=max(zerr,abs(z-ztab))
        fmin=10.0**(float(r["nfmin_db"])/10.0)
        F=nf_from_noise_params(0j,fmin,g,float(r["rn_ohm"]))
        nf50.append({"freq_ghz":float(r["freq_ghz"]),"nf_50ohm_db":10.0*math.log10(F)})

    source_hashes=sorted(set(r["source_sha256"] for r in spar))
    checks={
      "noise_anchor_count_nonzero":len(noise)>0,
      "sparam_anchor_count_nonzero":len(spar)>0,
      "zopt_reconstruction_error_lt_1e-4_ohm":zerr<1e-4,
      "single_expected_s2p_hash":source_hashes==[EXPECTED_S2P_SHA],
      "K_gt_1_all":all(float(r["K"])>1.0 for r in spar),
      "mu_gt_1_all":all(float(r["mu"])>1.0 for r in spar),
      "mu_prime_gt_1_all":all(float(r["mu_prime"])>1.0 for r in spar),
      "delta_lt_1_all":all(float(r["delta_mag"])<1.0 for r in spar),
    }

    payload={
      "status":"PASS_R4_A0_C0_G0_COMMITTED_DATA_SANITY" if all(checks.values()) else "HOLD_R4_A0_C0_G0_COMMITTED_DATA_SANITY",
      "checks":checks,
      "reference_plane":"QPL9547 device leads",
      "bias_reference":"5 V / 65 mA",
      "Z0_ohm":Z0,
      "noise_anchor_band_GHz":[min(float(r["freq_ghz"]) for r in noise),max(float(r["freq_ghz"]) for r in noise)],
      "sparam_anchor_band_GHz":[min(float(r["freq_ghz"]) for r in spar),max(float(r["freq_ghz"]) for r in spar)],
      "max_zopt_table_error_ohm":zerr,
      "Zopt_real_range_ohm":[min(float(r["zopt_re_ohm"]) for r in noise),max(float(r["zopt_re_ohm"]) for r in noise)],
      "Zopt_imag_range_ohm":[min(float(r["zopt_im_ohm"]) for r in noise),max(float(r["zopt_im_ohm"]) for r in noise)],
      "illustrative_2xZopt_real_range_ohm":[min(float(r["illustrative_2xzopt_re_ohm"]) for r in noise),max(float(r["illustrative_2xzopt_re_ohm"]) for r in noise)],
      "illustrative_2xZopt_imag_range_ohm":[min(float(r["illustrative_2xzopt_im_ohm"]) for r in noise),max(float(r["illustrative_2xzopt_im_ohm"]) for r in noise)],
      "NF_50ohm_anchor_range_db":[min(x["nf_50ohm_db"] for x in nf50),max(x["nf_50ohm_db"] for x in nf50)],
      "NF_50ohm_anchors":nf50,
      "S21_anchor_range_db":[min(float(r["s21_db"]) for r in spar),max(float(r["s21_db"]) for r in spar)],
      "S11_anchor_range_db":[min(float(r["s11_db"]) for r in spar),max(float(r["s11_db"]) for r in spar)],
      "stability_bounds":{
        "K_min":min(float(r["K"]) for r in spar),
        "mu_min":min(float(r["mu"]) for r in spar),
        "mu_prime_min":min(float(r["mu_prime"]) for r in spar),
        "delta_mag_max":max(float(r["delta_mag"]) for r in spar)
      },
      "differential_mapping_frozen":False,
      "note":"2xZopt remains scale context only; it is not a differential target until the finite local-ground mixed-mode interface is qualified."
    }

    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    with open(OUT,"w") as f:
        json.dump(payload,f,indent=2)
        f.write("\n")
    print(json.dumps(payload,indent=2))
    if not payload["status"].startswith("PASS_"):
        raise SystemExit(4)

if __name__=="__main__":
    main()
