#!/usr/bin/env python3
import csv,json,math,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIX=os.path.join(ROOT,"evidence","r1e1a4a_h0_p1_b0_nw_20260925_solve01","mixed_mode_2port_readonly.csv")
P0=os.path.join(ROOT,"evidence","r1e0b_dc_nw_20260924_smoke01","active_s11_and_zactive.csv")
OUT=os.path.join(ROOT,"evidence","r1e1a4a_h0_p1_b0_nw_20260925_solve01","physics_analysis.json")
def c(r,k): return complex(float(r[k+"_re"]),float(r[k+"_im"]))
def db(z): return 20*math.log10(max(abs(z),1e-300))
m=[]
for r in csv.DictReader(open(MIX,newline="")):
    f=float(r["freq_ghz"])
    m.append({"f":f,"sdd":c(r,"sdd"),"scc":c(r,"scc"),"sdc":c(r,"sdc"),"scd":c(r,"scd"),
              "zdd":c(r,"zdd"),"zb1":c(r,"zb1"),"zb2":c(r,"zb2")})
p0=[]
for r in csv.DictReader(open(P0,newline="")):
    p0.append((float(r["freq_ghz"]),complex(float(r["s11_re"]),float(r["s11_im"])),
               complex(float(r["zactive_re_ohm"]),float(r["zactive_im_ohm"]))))
anchors={}
for f0 in (1.15,1.2,1.3,1.4,1.5,1.6,1.65):
    r=min(m,key=lambda x:abs(x["f"]-f0)); q=min(p0,key=lambda x:abs(x[0]-r["f"]))
    anchors[str(f0)]={"freq_ghz":r["f"],
      "p0_zdiff_re":q[2].real,"p0_zdiff_im":q[2].imag,
      "h0_zdd_re":r["zdd"].real,"h0_zdd_im":r["zdd"].imag,
      "delta_z_abs_ohm":abs(r["zdd"]-q[2]),
      "sdd_db":db(r["sdd"]),"scc_db":db(r["scc"]),
      "sdc_db":db(r["sdc"]),"scd_db":db(r["scd"])}
sci=[r for r in m if 1.15<=r["f"]<=1.65]
out={"anchors":anchors,
 "sdd_db_min":min(db(r["sdd"]) for r in sci),"sdd_db_max":max(db(r["sdd"]) for r in sci),
 "scc_db_min":min(db(r["scc"]) for r in sci),"scc_db_max":max(db(r["scc"]) for r in sci),
 "zdd_re_min":min(r["zdd"].real for r in sci),"zdd_re_max":max(r["zdd"].real for r in sci),
 "zdd_im_min":min(r["zdd"].imag for r in sci),"zdd_im_max":max(r["zdd"].imag for r in sci)}
json.dump(out,open(OUT,"w"),indent=2)
print(json.dumps(out,indent=2))
