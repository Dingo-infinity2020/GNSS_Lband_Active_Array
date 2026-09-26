#!/usr/bin/env python3
import argparse,csv,json,math,os

SCI_LO=1.15
SCI_HI=1.65
ANCHORS=[1.17645,1.22760,1.27875,1.40000,1.56110,1.57542,1.60200]

def load(path):
    out=[]
    with open(path,newline="") as f:
        for r in csv.DictReader(f):
            out.append({
              "f":float(r["freq_ghz"]),
              "s":complex(float(r["s11_re"]),float(r["s11_im"])),
              "z":complex(float(r["zactive_re_ohm"]),float(r["zactive_im_ohm"]))
            })
    return out

def nearest(rows,f0):
    return min(rows,key=lambda r:abs(r["f"]-f0))

def compare(a,b):
    pairs=[]
    for ra in a:
        if SCI_LO<=ra["f"]<=SCI_HI:
            rb=nearest(b,ra["f"])
            ds=abs(ra["s"]-rb["s"])
            dz=abs(ra["z"]-rb["z"])
            pairs.append((ra["f"],ds,dz,ra["z"],rb["z"]))
    maxds=max(pairs,key=lambda x:x[1])
    maxdz=max(pairs,key=lambda x:x[2])
    rmsds=math.sqrt(sum(x[1]*x[1] for x in pairs)/len(pairs))
    rmsdz=math.sqrt(sum(x[2]*x[2] for x in pairs)/len(pairs))
    anchors={}
    for f0 in ANCHORS:
        ra=nearest(a,f0); rb=nearest(b,f0)
        anchors[str(f0)]={
          "f_ghz":ra["f"],
          "principal_z_re":ra["z"].real,"principal_z_im":ra["z"].imag,
          "orthogonal_z_re":rb["z"].real,"orthogonal_z_im":rb["z"].imag,
          "delta_z_abs":abs(ra["z"]-rb["z"]),
          "delta_s11_abs":abs(ra["s"]-rb["s"])
        }
    return {
      "sample_count":len(pairs),
      "max_complex_delta_s11":maxds[1],
      "max_complex_delta_s11_freq_ghz":maxds[0],
      "rms_complex_delta_s11":rmsds,
      "max_abs_delta_zactive_ohm":maxdz[2],
      "max_abs_delta_zactive_freq_ghz":maxdz[0],
      "rms_abs_delta_zactive_ohm":rmsdz,
      "anchors":anchors
    }

def metrics(rows):
    sci=[r for r in rows if SCI_LO<=r["f"]<=SCI_HI]
    return {
      "re_min":min(r["z"].real for r in sci),
      "re_max":max(r["z"].real for r in sci),
      "im_min":min(r["z"].imag for r in sci),
      "im_max":max(r["z"].imag for r in sci),
      "max_abs_z":max(abs(r["z"]) for r in sci),
      "max_abs_s11":max(abs(r["s"]) for r in sci)
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--principal",required=True)
    ap.add_argument("--orthogonal",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    p=load(a.principal); o=load(a.orthogonal)
    summary={
      "mode":"READ_ONLY_60DEG_PLANE_COMPARISON",
      "science_band_ghz":[SCI_LO,SCI_HI],
      "principal":{"state":"C60P45","metrics":metrics(p)},
      "orthogonal":{"state":"C60P135","metrics":metrics(o)},
      "comparison":compare(p,o),
      "classification":{
        "numerical_pass_fail_threshold_for_plane_divergence":"NOT_FROZEN",
        "retroactive_threshold_added":False,
        "interpretation":"Quantitative plane dependence only; no post-hoc PASS/FAIL threshold applied."
      }
    }
    os.makedirs(os.path.dirname(a.out),exist_ok=True)
    with open(a.out,"w") as f: json.dump(summary,f,indent=2)
    c=summary["comparison"]
    print("PASS_R1E0C_60DEG_PLANE_READONLY_COMPARISON")
    print("MAX_DELTA_S11=%.9f"%c["max_complex_delta_s11"])
    print("RMS_DELTA_S11=%.9f"%c["rms_complex_delta_s11"])
    print("MAX_DELTA_Z_OHM=%.9f"%c["max_abs_delta_zactive_ohm"])
    print("RMS_DELTA_Z_OHM=%.9f"%c["rms_abs_delta_zactive_ohm"])

if __name__=="__main__": main()
