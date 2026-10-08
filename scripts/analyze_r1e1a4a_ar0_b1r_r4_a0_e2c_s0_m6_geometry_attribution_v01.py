from __future__ import print_function
import json, math, re, hashlib
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
MACRO=ROOT/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_ONLY_V01.mcr"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_V01"
DOC=ROOT/"docs"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_GEOMETRY_ATTRIBUTION_FREEZE_V01.md"
ROUTE=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_GEOMETRY_ATTRIBUTION_FREEZE_V01.json"
OUT.mkdir(parents=True,exist_ok=True)

SIGNAL_KEYS=("UPSTREAM_MSL","UPSTREAM_TAPER","CIN_UP_PAD","CIN_DN_PAD","CIN_TO_RFIN_TAPER","PIN2_RFIN","RF_TONGUE","RF_TENON","SOLDER")
GROUND_KEYS=("LOCAL_BACK_GROUND","EXPOSED_PADDLE","PIN3_SPOKE","PIN4_SPOKE","PIN5_SPOKE","PIN6_SPOKE","PIN8_SPOKE","CRF_GND_PAD","LocalGroundTop","BACK_GROUND")
VIA_KEYS=("VIA","PADDLE_VIA","CRF_GROUND_VIA")

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def parse_num(s):
    try: return float(s)
    except: return None

def parse_objects(txt):
    lines=txt.splitlines()
    objs=[]
    i=0
    while i<len(lines):
        line=lines[i].strip()
        m=re.match(r"With\s+(Brick|Cylinder)",line,re.I)
        if not m:
            i+=1; continue
        kind=m.group(1).lower()
        block=[]
        j=i+1
        while j<len(lines) and lines[j].strip()!="End With":
            block.append(lines[j].strip()); j+=1
        d={"kind":kind}
        for b in block:
            mm=re.match(r'\.(Name|Component|Material)\s+"([^"]*)"',b,re.I)
            if mm: d[mm.group(1).lower()]=mm.group(2)
            for key in ("Xrange","Yrange","Zrange"):
                mm=re.match(r'\.'+key+r'\s+"?([-0-9.eE+]+)"?\s*,\s*"?([-0-9.eE+]+)"?',b,re.I)
                if mm: d[key.lower()]=(float(mm.group(1)),float(mm.group(2)))
            for key in ("Xcenter","Ycenter","Zcenter","OuterRadius","InnerRadius","Radius","Height"):
                mm=re.match(r'\.'+key+r'\s+"?([-0-9.eE+]+)"?',b,re.I)
                if mm: d[key.lower()]=float(mm.group(1))
            mm=re.match(r'\.Axis\s+"([XYZxyz])"',b)
            if mm: d["axis"]=mm.group(1).upper()
        comp=d.get("component","")
        name=d.get("name","")
        if comp.startswith("E2C_A_") or comp.startswith("E2C_B_"):
            # Construct conservative AABB.
            bbox=None
            if kind=="brick" and all(k in d for k in ("xrange","yrange","zrange")):
                bbox=(min(d["xrange"]),max(d["xrange"]),min(d["yrange"]),max(d["yrange"]),min(d["zrange"]),max(d["zrange"]))
            elif kind=="cylinder" and all(k in d for k in ("xcenter","ycenter","zrange","outerradius")):
                r=d["outerradius"]
                # most vias are z-axis in this model; conservative sphere-ish xy box.
                bbox=(d["xcenter"]-r,d["xcenter"]+r,d["ycenter"]-r,d["ycenter"]+r,min(d["zrange"]),max(d["zrange"]))
            d["bbox"]=bbox
            full=comp+":"+name
            d["full"]=full
            if comp.startswith("E2C_A_"): d["pol"]="A"
            else: d["pol"]="B"
            up=full.upper()
            if any(k.upper() in up for k in VIA_KEYS): cat="VIA"
            elif any(k.upper() in up for k in SIGNAL_KEYS): cat="SIGNAL"
            elif any(k.upper() in up for k in GROUND_KEYS): cat="GROUND"
            else: cat="OTHER"
            d["category"]=cat
            objs.append(d)
        i=j+1
    return objs

def box_dist(a,b):
    if a is None or b is None: return None
    dx=max(a[0]-b[1],b[0]-a[1],0.0)
    dy=max(a[2]-b[3],b[2]-a[3],0.0)
    dz=max(a[4]-b[5],b[4]-a[5],0.0)
    return math.sqrt(dx*dx+dy*dy+dz*dz)

def center(box):
    return ((box[0]+box[1])/2,(box[2]+box[3])/2,(box[4]+box[5])/2)

txt=MACRO.read_text(encoding="utf-8",errors="replace")
objs=parse_objects(txt)
usable=[o for o in objs if o["bbox"] is not None]
pairs=[]
for a in usable:
    if a["pol"]!="A" or a["category"]=="OTHER": continue
    for b in usable:
        if b["pol"]!="B" or b["category"]=="OTHER": continue
        dist=box_dist(a["bbox"],b["bbox"])
        pairs.append({"distance_mm":dist,"a":a["full"],"a_category":a["category"],"b":b["full"],"b_category":b["category"],
                      "a_center":center(a["bbox"]),"b_center":center(b["bbox"])})
pairs.sort(key=lambda x:x["distance_mm"])

byclass={}
for ca in ("SIGNAL","GROUND","VIA"):
    for cb in ("SIGNAL","GROUND","VIA"):
        q=[p for p in pairs if p["a_category"]==ca and p["b_category"]==cb]
        if q: byclass[ca+"_to_"+cb]=q[:12]

# Count physical classes and nearest distances.
counts={}
for p in ("A","B"):
    counts[p]={c:sum(1 for o in usable if o["pol"]==p and o["category"]==c) for c in ("SIGNAL","GROUND","VIA","OTHER")}

# Literature-guided attribution variants, deliberately minimal and diagnostic.
variants=[
 {
  "id":"M6-SIG",
  "purpose":"Test whether opposite-polarization pre-CIN signal copper is the dominant mixed-mode coupling path.",
  "geometry_action":"In a disposable E2C copy, suppress only the opposite-pol active landing-zone SIGNAL extensions from upstream MSL/taper through E_UP-side C_IN pad while preserving radiator/feed parent geometry and all local-ground/via geometry.",
  "must_not_change":["radiator arms","RF tenon/tongue parent feed before frozen handoff","all local-ground copper","all vias","backside ground"],
  "primary_observables":["A/B E_UP modal cross-block principal singular value","A_diff<->B_diff","A_diff<->B_common","same-pol E diff->common"],
  "prediction_if_signal_dominant":"principal A/B modal coupling and same-pol diff/common degradation both improve strongly; ground-related branch imbalance may remain."
 },
 {
  "id":"M6-GND",
  "purpose":"Test whether branch-local ground/backside/via structures are the dominant mixed-mode coupling path.",
  "geometry_action":"In a disposable E2C copy, retain all signal copper but remove only the added opposite-pol local-ground/paddle/spoke/backside-ground/via system that was absent in the isolated baseline comparison, using an electrically well-defined audit replacement only if required to keep ports valid.",
  "must_not_change":["radiator arms","pre-CIN signal copper","E_UP signal pads"],
  "primary_observables":["E_UP +/- return imbalance","same-pol E diff->common","A/B modal cross-block singular value"],
  "prediction_if_ground_dominant":"branch imbalance and diff/common conversion improve more than raw E_UP signal-to-signal coupling."
 },
 {
  "id":"M6-INT",
  "purpose":"Test signal-ground interaction if neither pure signal nor pure ground ablation explains the mixed eigenchannel.",
  "geometry_action":"Retain both classes but selectively increase only the closest A/B signal-to-ground separation identified by the static geometry audit, without changing radiator dimensions or device-side geometry.",
  "must_not_change":["radiator electrical length","P_IN/P_OUT/package geometry","far ground topology"],
  "primary_observables":["global A/B cross-modal principal sigma","worst-region A/B singular-mode purity","same-pol diff/common degradation"],
  "prediction_if_interaction_dominant":"modal coupling improves only when the nearest signal-ground adjacency is perturbed, while pure-class ablations are incomplete."
 }
]

route={
 "schema_version":"gnss-e2c-s0-m6-freeze-v0.1",
 "status":"FROZEN_M6_GEOMETRY_ATTRIBUTION",
 "input_macro":str(MACRO),"input_macro_sha256":sha(MACRO),
 "method":"literature-guided current-path / modal attribution using static geometry and minimum ablation sentinels",
 "variant_order":["M6-SIG","M6-GND","M6-INT"],
 "build_gate":"No variant may be built until static geometry attribution names exact entities and expected observables.",
 "BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False
}
ROUTE.write_text(json.dumps(route,indent=2)+"\n",encoding="utf-8")

report={
 "schema_version":"gnss-e2c-s0-m6-geometry-attribution-v0.1",
 "status":"PASS_M6_STATIC_GEOMETRY_ATTRIBUTION_READY",
 "macro_sha256":sha(MACRO),
 "object_counts":counts,
 "nearest_cross_pol_pairs":pairs[:40],
 "nearest_by_class":byclass,
 "variants":variants,
 "boundary":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
}
(OUT/"M6_GEOMETRY_ATTRIBUTION.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")

lines=["# E2C S0 M6 Static Geometry Attribution V0.1","",
       "Status: **PASS_M6_STATIC_GEOMETRY_ATTRIBUTION_READY**","",
       "No CST launch, BUILD, or SOLVE was used.","",
       "## Geometry inventory","",
       "- Pol-A: "+str(counts["A"]),
       "- Pol-B: "+str(counts["B"]),
       "",
       "## Closest cross-polarization classified pairs",""]
for p in pairs[:20]:
    lines.append("- %.4f mm | %s [%s] <-> %s [%s]"%(p["distance_mm"],p["a"],p["a_category"],p["b"],p["b_category"]))
lines += ["","## Minimum attribution variants",""]
for v in variants:
    lines += ["### "+v["id"],v["purpose"],"",
              "**Action:** "+v["geometry_action"],"",
              "**Prediction:** "+v["prediction_if_signal_dominant"] if "prediction_if_signal_dominant" in v else "**Prediction:** "+v.get("prediction_if_ground_dominant",v.get("prediction_if_interaction_dominant","")),""]
lines += ["## Boundary","","This is an attribution plan only. No BUILD or SOLVE authorization is created.","","BUILD_AUTHORIZED = false","SOLVE_AUTHORIZED = false"]
(OUT/"M6_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

DOC.write_text("""# R4-A0-E2C-S0 M6 Geometry Attribution Freeze V0.1

Status: FROZEN_M6_GEOMETRY_ATTRIBUTION

This node adopts the literature-style mechanism workflow used in high-isolation dual-polarized antennas: identify differential/common current paths and modal coupling first, then perturb only the structure associated with the suspected path.

Frozen diagnostic order:

1. M6-SIG — pre-CIN signal-copper attribution;
2. M6-GND — local-ground/backside/via attribution;
3. M6-INT — nearest signal-ground interaction attribution, only if needed.

Each future diagnostic build must preserve the E2C R7 radiator dimensions and must state a directional prediction for a frozen modal observable before execution.

A diagnostic result may reject a mechanism. It may not be used as an excuse for unconstrained geometry optimization.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
""",encoding="utf-8")

print("PASS_M6_STATIC_GEOMETRY_ATTRIBUTION_READY")
print("OBJECT_COUNTS="+json.dumps(counts,sort_keys=True))
for p in pairs[:12]:
    print("NEAR %.4f | %s [%s] <-> %s [%s]"%(p["distance_mm"],p["a"],p["a_category"],p["b"],p["b_category"]))
print("OUT="+str(OUT))
