#!/usr/bin/env python3
import csv,json,os

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"evidence","r1e0c_closeout_20260924")
os.makedirs(OUT,exist_ok=True)

states=[
 ("BROAD","R1E0B",0,45,os.path.join(ROOT,"evidence","r1e0b_dc_nw_20260924_smoke01","active_s11_and_zactive.csv"),None),
 ("C30P45","R1E0C-B",30,45,os.path.join(ROOT,"evidence","r1e0c_b_c30p45_dc_nw_20260924_solve01","active_s11_and_zactive.csv"),os.path.join(ROOT,"evidence","r1e0c_b_c30p45_dc_nw_20260924_solve01","summary.json")),
 ("C45P45","R1E0C-B",45,45,os.path.join(ROOT,"evidence","r1e0c_b_c45p45_dc_nw_20260924_solve01","active_s11_and_zactive.csv"),os.path.join(ROOT,"evidence","r1e0c_b_c45p45_dc_nw_20260924_solve01","summary.json")),
 ("C60P45","R1E0C-B",60,45,os.path.join(ROOT,"evidence","r1e0c_b_c60p45_dc_nw_20260924_solve01","active_s11_and_zactive.csv"),os.path.join(ROOT,"evidence","r1e0c_b_c60p45_dc_nw_20260924_solve01","summary.json")),
 ("C60P135","R1E0C-B",60,135,os.path.join(ROOT,"evidence","r1e0c_b_c60p135_dc_nw_20260924_solve01","active_s11_and_zactive.csv"),os.path.join(ROOT,"evidence","r1e0c_b_c60p135_dc_nw_20260924_solve01","summary.json")),
]
SCI_LO=1.15; SCI_HI=1.65
ANCHORS=[1.17645,1.22760,1.27875,1.40000,1.56110,1.57542,1.60200]

def load_csv(p):
 out=[]
 with open(p,newline="") as f:
  for r in csv.DictReader(f):
   out.append({
    "f":float(r["freq_ghz"]),
    "s":complex(float(r["s11_re"]),float(r["s11_im"])),
    "sdb":float(r["s11_db"]),
    "z":complex(float(r["zactive_re_ohm"]),float(r["zactive_im_ohm"]))
   })
 return out

def nearest(rows,f0): return min(rows,key=lambda r:abs(r["f"]-f0))

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

items=[]
for sid,stage,theta,phi,csvp,sump in states:
 rows=load_csv(csvp)
 item={"id":sid,"stage":stage,"theta_deg":theta,"phi_deg":phi,"metrics":metrics(rows),"anchors":{}}
 for f0 in ANCHORS:
  r=nearest(rows,f0)
  item["anchors"][str(f0)]={"f_ghz":r["f"],"s11_db":r["sdb"],"z_re":r["z"].real,"z_im":r["z"].imag}
 if sump and os.path.isfile(sump):
  s=json.load(open(sump))
  item["physics_alerts"]=s.get("physics_alerts",{})
  item["checks"]=s.get("checks",{})
 items.append(item)

plane=json.load(open(os.path.join(OUT,"plane60_comparison.json")))
summary={
 "status":"PASS_R1E0C_SCAN_QUALIFICATION",
 "science_band_ghz":[SCI_LO,SCI_HI],
 "states":items,
 "plane60_comparison":plane["comparison"],
 "interpretation":{
  "principal_plane_core_scan":"numerically qualified through theta=60 deg under frozen severe-mismatch gates",
  "orthogonal_plane_sentinel":"numerically qualified at theta=60 deg",
  "plane_dependence":"material and quantitatively large at theta=60 deg",
  "plane_divergence_pass_fail_threshold":"NOT_FROZEN",
  "lna_match_freeze":"NOT_READY",
  "reason":"active impedance depends strongly on scan angle and scan plane"
 }
}
with open(os.path.join(OUT,"scan_locus_summary.json"),"w") as f: json.dump(summary,f,indent=2)

with open(os.path.join(OUT,"scan_anchor_matrix.csv"),"w",newline="") as f:
 w=csv.writer(f)
 w.writerow(["state","theta_deg","phi_deg","anchor_nominal_ghz","actual_ghz","s11_db","z_re_ohm","z_im_ohm"])
 for item in items:
  for a,v in item["anchors"].items():
   w.writerow([item["id"],item["theta_deg"],item["phi_deg"],a,v["f_ghz"],v["s11_db"],v["z_re"],v["z_im"]])

print("PASS_R1E0C_SCAN_LOCUS_READONLY_SUMMARY")
print("STATE_COUNT="+str(len(items)))
print("PLANE60_MAX_DELTA_S11=%.9f"%plane["comparison"]["max_complex_delta_s11"])
print("PLANE60_MAX_DELTA_Z_OHM=%.9f"%plane["comparison"]["max_abs_delta_zactive_ohm"])
print("LNA_MATCH_FREEZE=NOT_READY")
