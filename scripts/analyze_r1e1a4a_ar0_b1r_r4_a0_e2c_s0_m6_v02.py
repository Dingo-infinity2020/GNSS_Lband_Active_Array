from __future__ import print_function
import json, math, re, hashlib
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
MACRO=ROOT/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_ONLY_V01.mcr"
INV=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_INVENTORY_V01.json"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_V02"
DOC=ROOT/"docs"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_GEOMETRY_ATTRIBUTION_FREEZE_V02.md"
ROUTE=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_GEOMETRY_ATTRIBUTION_FREEZE_V02.json"
SUPER=ROOT/"docs"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_V01_SUPERSESSION.md"
OUT.mkdir(parents=True,exist_ok=True)

PRE_CIN={"UPSTREAM_MSL","UPSTREAM_TAPER","CIN_UP_PAD"}
GROUND_PIN_PREFIX=("PIN3_","PIN4_","PIN5_","PIN6_","PIN8_")

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def vec3(vals):
    return tuple(float(x) for x in vals)

def add(a,b): return tuple(a[i]+b[i] for i in range(3))
def mul(a,s): return tuple(a[i]*s for i in range(3))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):
    q=math.sqrt(sum(x*x for x in a))
    return tuple(x/q for x in a)
def rotz(p,deg):
    t=math.radians(deg); c=math.cos(t); s=math.sin(t)
    return (c*p[0]-s*p[1],s*p[0]+c*p[1],p[2])

def bbox_points(points):
    return (min(p[0] for p in points),max(p[0] for p in points),
            min(p[1] for p in points),max(p[1] for p in points),
            min(p[2] for p in points),max(p[2] for p in points))

def parse_q3(line,key):
    m=re.match(r'\.'+re.escape(key)+r'\s+"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"',line,re.I)
    return vec3(m.groups()) if m else None

def parse_blocks(lines):
    blocks=[]
    i=0
    while i<len(lines):
        m=re.match(r'^With\s+([A-Za-z0-9_]+)',lines[i].strip(),re.I)
        if not m:
            i+=1; continue
        typ=m.group(1)
        j=i+1
        while j<len(lines) and lines[j].strip()!="End With": j+=1
        blocks.append((typ,i,j,[x.strip() for x in lines[i+1:j]]))
        i=j+1
    return blocks

def kv_str(block,key):
    for x in block:
        m=re.match(r'\.'+re.escape(key)+r'\s+"([^"]*)"',x,re.I)
        if m: return m.group(1)
    return None

def kv_float(block,key):
    x=kv_str(block,key)
    return float(x) if x is not None else None

def extrude_geom(block):
    name=kv_str(block,"Name"); comp=kv_str(block,"Component")
    origin=u=v=None; pts=[]
    for x in block:
        if x.lower().startswith(".origin "): origin=parse_q3(x,"Origin")
        if x.lower().startswith(".uvector "): u=parse_q3(x,"Uvector")
        if x.lower().startswith(".vvector "): v=parse_q3(x,"Vvector")
        m=re.match(r'\.(Point|LineTo)\s+"([^"]+)"\s*,\s*"([^"]+)"',x,re.I)
        if m: pts.append((float(m.group(2)),float(m.group(3))))
    h=kv_float(block,"Height")
    if name is None or comp is None or origin is None or u is None or v is None or h is None or not pts:
        return None
    w=norm(cross(u,v))
    world=[]
    for q,r in pts:
        base=add(origin,add(mul(u,q),mul(v,r)))
        world.append(base); world.append(add(base,mul(w,h)))
    return {"full":comp+":"+name,"kind":"Extrude","bbox":bbox_points(world),"component":comp,"name":name}

def cylinder_geom(block):
    name=kv_str(block,"Name"); comp=kv_str(block,"Component")
    axis=(kv_str(block,"Axis") or "").upper()
    radius=kv_float(block,"OuterRadius")
    ranges={}
    for key in ("Xrange","Yrange","Zrange"):
        for x in block:
            m=re.match(r'\.'+key+r'\s+"([^"]+)"\s*,\s*"([^"]+)"',x,re.I)
            if m: ranges[key]=(float(m.group(1)),float(m.group(2)))
    xc=kv_float(block,"Xcenter"); yc=kv_float(block,"Ycenter"); zc=kv_float(block,"Zcenter")
    if name is None or comp is None or radius is None or axis not in ("X","Y","Z"): return None
    if axis=="X" and "Xrange" in ranges and yc is not None and zc is not None:
        p0=(ranges["Xrange"][0],yc,zc); p1=(ranges["Xrange"][1],yc,zc); d=(1,0,0)
    elif axis=="Y" and "Yrange" in ranges and xc is not None and zc is not None:
        p0=(xc,ranges["Yrange"][0],zc); p1=(xc,ranges["Yrange"][1],zc); d=(0,1,0)
    elif axis=="Z" and "Zrange" in ranges and xc is not None and yc is not None:
        p0=(xc,yc,ranges["Zrange"][0]); p1=(xc,yc,ranges["Zrange"][1]); d=(0,0,1)
    else: return None
    return {"full":comp+":"+name,"kind":"Cylinder","p0":p0,"p1":p1,"axis":d,"radius":radius,"component":comp,"name":name}

def apply_cyl_rot(g,deg):
    p0=rotz(g["p0"],deg); p1=rotz(g["p1"],deg); d=rotz(g["axis"],deg); r=g["radius"]
    ext=tuple(r*math.sqrt(max(0.0,1-d[i]*d[i])) for i in range(3))
    b=(min(p0[0],p1[0])-ext[0],max(p0[0],p1[0])+ext[0],
       min(p0[1],p1[1])-ext[1],max(p0[1],p1[1])+ext[1],
       min(p0[2],p1[2])-ext[2],max(p0[2],p1[2])+ext[2])
    g=dict(g); g["bbox"]=b; g["rotation_z_deg"]=deg; return g

def box_dist(a,b):
    dx=max(a[0]-b[1],b[0]-a[1],0.0)
    dy=max(a[2]-b[3],b[2]-a[3],0.0)
    dz=max(a[4]-b[5],b[4]-a[5],0.0)
    return math.sqrt(dx*dx+dy*dy+dz*dz)

def classify(full):
    comp,name=full.split(":",1)
    cu=comp.upper(); nu=name.upper()
    pol="A" if comp.startswith("E2C_A_") else ("B" if comp.startswith("E2C_B_") else None)
    if "_VIAHOLETOOLS" in cu: cat="TOOL"
    elif "_VIAS" in cu: cat="LOCAL_GROUND_VIA"
    elif "_BACKGROUND" in cu or "_LOCALGROUNDTOP" in cu: cat="LOCAL_GROUND"
    elif "_SIGNAL" in cu:
        cat="PRE_CIN_SIGNAL" if name in PRE_CIN else "POST_CIN_SIGNAL"
    elif "_PACKAGELANDS" in cu:
        if nu.startswith(GROUND_PIN_PREFIX) or "GND" in nu: cat="LOCAL_GROUND"
        elif "PIN2_RFIN" in nu: cat="DEVICE_INPUT"
        else: cat="DEVICE_OTHER"
    elif "_BIAS" in cu or "_OUTPUT" in cu: cat="DEVICE_OTHER"
    else: cat="OTHER"
    return pol,cat

lines=MACRO.read_text(encoding="utf-8",errors="replace").splitlines()
blocks=parse_blocks(lines)
geom={}
for bi,(typ,i,j,b) in enumerate(blocks):
    if typ.lower()=="extrude":
        g=extrude_geom(b)
        if g: geom[g["full"]]=g
    elif typ.lower()=="cylinder":
        g=cylinder_geom(b)
        if not g: continue
        deg=0.0
        if bi+1<len(blocks) and blocks[bi+1][0].lower()=="transform":
            tb=blocks[bi+1][3]
            nm=kv_str(tb,"Name")
            angle=None
            for x in tb:
                q=parse_q3(x,"Angle")
                if q is not None: angle=q
            if nm==g["full"] and angle is not None and abs(angle[0])<1e-12 and abs(angle[1])<1e-12:
                deg=angle[2]
        geom[g["full"]]=apply_cyl_rot(g,deg)

inv=json.loads(INV.read_text(encoding="utf-8"))
final_names=[x for x in inv["expected_final_names"] if x.startswith("E2C_A_") or x.startswith("E2C_B_")]
records=[]
missing=[]
for full in final_names:
    pol,cat=classify(full)
    g=geom.get(full)
    if g is None or "bbox" not in g:
        missing.append(full)
    records.append({"full":full,"pol":pol,"category":cat,"bbox":g.get("bbox") if g else None,"primitive":g.get("kind") if g else None})
coverage=(len(final_names)-len(missing))/float(len(final_names)) if final_names else 0.0

counts={}
for pol in ("A","B"):
    counts[pol]={}
    for cat in sorted(set(r["category"] for r in records)):
        counts[pol][cat]=sum(1 for r in records if r["pol"]==pol and r["category"]==cat)

pairs=[]
for a in records:
    if a["pol"]!="A" or a["bbox"] is None or a["category"] in ("TOOL","OTHER"): continue
    for b in records:
        if b["pol"]!="B" or b["bbox"] is None or b["category"] in ("TOOL","OTHER"): continue
        pairs.append({"a":a["full"],"a_category":a["category"],"b":b["full"],"b_category":b["category"],
                      "aabb_lower_bound_mm":box_dist(a["bbox"],b["bbox"])})
pairs.sort(key=lambda x:x["aabb_lower_bound_mm"])

b_pre=[r["full"] for r in records if r["pol"]=="B" and r["category"]=="PRE_CIN_SIGNAL"]
b_gnd=[r["full"] for r in records if r["pol"]=="B" and r["category"] in ("LOCAL_GROUND","LOCAL_GROUND_VIA")]
b_dev=[r["full"] for r in records if r["pol"]=="B" and r["category"] in ("POST_CIN_SIGNAL","DEVICE_INPUT","DEVICE_OTHER")]

variants=[
 {"id":"M6-D1-SIG","observer":"Pol-A / E2A semantics","add_from_polB":b_pre,
  "purpose":"Isolate passive scattering/coupling caused by the opposite-pol pre-CIN signal extension connected to the existing Pol-B radiator/feed.",
  "ports":"No Pol-B ports. Preserve Pol-A E2A loaded-source solve semantics only.",
  "prediction":"If pre-CIN signal metal is dominant, Pol-A own-pol complex delta and diff/common degradation move substantially toward full-E2C values even without Pol-B ground/device metal."},
 {"id":"M6-D2-GND","observer":"Pol-A / E2A semantics","add_from_polB":b_gnd,
  "purpose":"Isolate passive scattering/common-mode perturbation caused by opposite-pol local-ground, backside-ground and via metal.",
  "ports":"No Pol-B ports. Preserve Pol-A E2A loaded-source solve semantics only.",
  "prediction":"If local-ground return geometry is dominant, Pol-A branch imbalance and diff/common degradation move substantially toward full-E2C values while D1 remains comparatively small."}
]

decision={
 "if_D1_large_D2_small":"pre-CIN signal parasitic path primary",
 "if_D1_small_D2_large":"local-ground/backside/via path primary",
 "if_D1_small_D2_small_but_full_large":"signal-ground interaction / composite mixed mode primary",
 "if_D1_large_D2_large":"both classes independently load the observer; use field-current comparison before geometry optimization"
}

status="PASS_M6_V02_EXACT_ENTITY_ATTRIBUTION_READY" if coverage==1.0 and b_pre and b_gnd else "HOLD_M6_V02_GEOMETRY_COVERAGE"
report={
 "schema_version":"gnss-e2c-s0-m6-v0.2","status":status,
 "supersedes":"M6_V01 invalid: parser recognized Brick/Cylinder only and returned zero E2C geometry; no v0.1 geometry conclusion is authoritative.",
 "final_e2c_entity_count":len(final_names),"geometry_coverage":coverage,"missing_geometry":missing,
 "counts":counts,"nearest_cross_pol_aabb_lower_bounds":pairs[:60],
 "diagnostic_variants":variants,"decision_logic":decision,
 "notes":["AABB distances are conservative lower bounds, not exact conductor-to-conductor distances.",
          "Exact entity membership comes from the final E2C inventory contract, not primitive creation count.",
          "M6-D1/D2 are observer-polarization ablation diagnostics; they do not require Pol-B ports."],
 "boundary":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
}
(OUT/"M6_V02_ANALYSIS.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
(OUT/"M6_D1_POLB_PRE_CIN_SIGNAL_ENTITIES.txt").write_text("\n".join(b_pre)+"\n",encoding="utf-8")
(OUT/"M6_D2_POLB_GROUND_ENTITIES.txt").write_text("\n".join(b_gnd)+"\n",encoding="utf-8")
(OUT/"M6_DEVICE_SIDE_DEFERRED_ENTITIES.txt").write_text("\n".join(b_dev)+"\n",encoding="utf-8")

SUPER.write_text("""# M6 V0.1 Supersession

M6 V0.1 is non-authoritative for geometry attribution.

Reason: its static parser handled only Brick/Cylinder primitives. The E2C landing-zone copper is primarily created with CST Extrude, so V0.1 incorrectly reported zero classified A/B entities while still labeling the result PASS.

No CST, BUILD, or SOLVE occurred in V0.1.

M6 V0.2 replaces V0.1 using:
- expected_final_names from the frozen E2C final inventory as entity authority;
- Extrude geometry reconstruction;
- Cylinder plus immediate z-rotation reconstruction;
- explicit fail-closed geometry coverage.

Do not use V0.1 geometry counts or distances.
""",encoding="utf-8")

ROUTE.write_text(json.dumps({
 "schema_version":"gnss-e2c-s0-m6-freeze-v0.2","status":status,
 "method":"literature-guided structure-evolution attribution with one-polarization observer",
 "diagnostic_order":["M6-D1-SIG","M6-D2-GND"],
 "interaction_inference":"Use already-solved full E2C as SIG+GND(+device) endpoint; if D1/D2 are small individually but full is severe, interaction is primary.",
 "field_monitor_recommendation_if_future_solve_authorized":["L2 1.2276 GHz","mixed-mode worst region 1.3384 GHz","L1 1.57542 GHz"],
 "BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False
},indent=2)+"\n",encoding="utf-8")

DOC.write_text("""# R4-A0-E2C-S0 M6 Geometry Attribution Freeze V0.2

Status: %s

M6 V0.1 is superseded because its primitive parser omitted CST Extrude copper and produced a false zero-entity PASS.

V0.2 follows a literature-style structure-evolution/current-path methodology.

## Diagnostic architecture

Use Pol-A/E2A as the observer network. Do not create Pol-B ports.

### M6-D1-SIG

Add only the exact Pol-B PRE-CIN signal-extension entities listed in the V0.2 evidence.

Question: does opposite-pol signal metal alone drive the observer toward the full-E2C mixed-mode degradation?

### M6-D2-GND

Add only the exact Pol-B local-ground/backside/via entities listed in the V0.2 evidence.

Question: does opposite-pol return/ground metal alone drive branch imbalance and common-mode conversion?

### Interaction decision

Full E2C is already the combined SIG+GND(+device) endpoint.

If D1 and D2 are both weak but full E2C is severe, the primary mechanism is a signal-ground interaction/composite eigenchannel and the next design action should target that interaction, not either metal class independently.

If future diagnostic solves are authorized, include surface-current monitors at L2, approximately 1.3384 GHz, and L1 so that the S-parameter attribution is backed by current-path evidence.

No geometry optimization is authorized in M6.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
"""%status,encoding="utf-8")

print(status)
print("FINAL_E2C_ENTITIES=%d"%len(final_names))
print("GEOMETRY_COVERAGE=%.6f"%coverage)
print("MISSING=%d"%len(missing))
print("D1_PRE_CIN_SIGNAL_COUNT=%d"%len(b_pre))
print("D2_GROUND_COUNT=%d"%len(b_gnd))
for p in pairs[:16]:
    print("NEAR %.6f | %s [%s] <-> %s [%s]"%(p["aabb_lower_bound_mm"],p["a"],p["a_category"],p["b"],p["b_category"]))
