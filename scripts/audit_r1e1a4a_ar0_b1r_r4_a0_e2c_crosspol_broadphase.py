from __future__ import print_function
import argparse, json, math, re, sys
from pathlib import Path

TOL=1e-9

def fnum(s):
    return float(str(s).strip().strip('"'))

def vec3(line,key):
    m=re.search(r'\.%s\s+"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"'%key,line)
    return tuple(float(m.group(i)) for i in (1,2,3)) if m else None

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def norm(a):
    n=math.sqrt(sum(x*x for x in a))
    if n<=0: raise ValueError("zero vector")
    return tuple(x/n for x in a)

def add(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(3))

def mul(s,v):
    return tuple(s*x for x in v)

def rotz(p,deg):
    a=math.radians(deg); c=math.cos(a); s=math.sin(a)
    return (c*p[0]-s*p[1],s*p[0]+c*p[1],p[2])

def aabb_points(points):
    return {
      "min":[min(p[i] for p in points) for i in range(3)],
      "max":[max(p[i] for p in points) for i in range(3)]
    }

def overlap(a,b,tol=TOL):
    for i in range(3):
        if a["max"][i] < b["min"][i]-tol or b["max"][i] < a["min"][i]-tol:
            return False
    return True

def classify(full):
    comp=full.split(":",1)[0]
    if comp=="E2C_ActivePolAStub" or comp.startswith("E2C_A_"): return "A"
    if comp=="E2C_ActivePolBStub" or comp.startswith("E2C_B_"): return "B"
    return None

def parse_macro(path):
    lines=Path(path).read_text(encoding="utf-8",errors="replace").splitlines()
    solids={}
    current=None
    last_created=None
    i=0
    while i<len(lines):
        s=lines[i].strip()
        if s in ("With Extrude","With Cylinder"):
            kind=s.split()[1]
            block=[]
            j=i+1
            while j<len(lines):
                block.append(lines[j].strip())
                if lines[j].strip()=="End With": break
                j+=1
            name=comp=None
            for x in block:
                m=re.match(r'\.Name "([^"]+)"',x)
                if m: name=m.group(1)
                m=re.match(r'\.Component "([^"]+)"',x)
                if m: comp=m.group(1)
            if not name or not comp: raise RuntimeError("shape identity parse")
            full=comp+":"+name
            if "ViaHoleTools" in comp:
                last_created=full; i=j+1; continue
            if kind=="Extrude":
                origin=uvec=vvec=None; height=None; uv=[]
                for x in block:
                    if x.startswith(".Origin "): origin=vec3(x,"Origin")
                    elif x.startswith(".Uvector "): uvec=vec3(x,"Uvector")
                    elif x.startswith(".Vvector "): vvec=vec3(x,"Vvector")
                    elif x.startswith(".Height "):
                        m=re.search(r'\.Height "([^"]+)"',x); height=float(m.group(1))
                    elif x.startswith(".Point ") or x.startswith(".LineTo "):
                        m=re.search(r'\.(?:Point|LineTo) "([^"]+)",\s*"([^"]+)"',x)
                        uv.append((float(m.group(1)),float(m.group(2))))
                if None in (origin,uvec,vvec,height) or not uv: raise RuntimeError("extrude parse "+full)
                nvec=norm(cross(uvec,vvec))
                pts=[]
                for q,r in uv:
                    p=add(origin,mul(q,uvec),mul(r,vvec))
                    pts.extend([p,add(p,mul(height,nvec))])
                solids[full]={"kind":"Extrude","aabb":aabb_points(pts)}
            else:
                axis=None;x1=x2=yc=zc=rad=None
                for x in block:
                    m=re.match(r'\.Axis "([^"]+)"',x)
                    if m: axis=m.group(1)
                    m=re.match(r'\.Xrange "([^"]+)",\s*"([^"]+)"',x)
                    if m: x1,x2=float(m.group(1)),float(m.group(2))
                    m=re.match(r'\.Ycenter "([^"]+)"',x)
                    if m: yc=float(m.group(1))
                    m=re.match(r'\.Zcenter "([^"]+)"',x)
                    if m: zc=float(m.group(1))
                    m=re.match(r'\.OuterRadius "([^"]+)"',x)
                    if m: rad=float(m.group(1))
                if axis!="x" or None in (x1,x2,yc,zc,rad): raise RuntimeError("cylinder parse "+full)
                solids[full]={"kind":"Cylinder","pre":{"x1":x1,"x2":x2,"y":yc,"z":zc,"r":rad},"rotation_z_deg":0.0}
            last_created=full
            i=j+1
            continue
        if s=="With Transform":
            block=[]
            j=i+1
            while j<len(lines):
                block.append(lines[j].strip())
                if lines[j].strip()=="End With": break
                j+=1
            target=None; angle=None; op=None
            for x in block:
                m=re.match(r'\.Name "([^"]+)"',x)
                if m: target=m.group(1)
                m=re.match(r'\.Angle "([^"]+)",\s*"([^"]+)",\s*"([^"]+)"',x)
                if m: angle=(float(m.group(1)),float(m.group(2)),float(m.group(3)))
                m=re.match(r'\.Transform "Shape", "([^"]+)"',x)
                if m: op=m.group(1)
            if target in solids and solids[target]["kind"]=="Cylinder" and op=="Rotate":
                if angle is None or abs(angle[0])>TOL or abs(angle[1])>TOL:
                    raise RuntimeError("unsupported cylinder rotation "+target)
                solids[target]["rotation_z_deg"]=angle[2]
            i=j+1
            continue
        i+=1

    # Finalize exact rotated-cylinder AABBs.
    for full,d in solids.items():
        if d["kind"]!="Cylinder": continue
        p=d["pre"]; deg=d["rotation_z_deg"]
        e1=rotz((p["x1"],p["y"],p["z"]),deg)
        e2=rotz((p["x2"],p["y"],p["z"]),deg)
        axis=rotz((1.0,0.0,0.0),deg)
        ext=[p["r"]*math.sqrt(max(0.0,1.0-axis[k]*axis[k])) for k in range(3)]
        d["aabb"]={
          "min":[min(e1[k],e2[k])-ext[k] for k in range(3)],
          "max":[max(e1[k],e2[k])+ext[k] for k in range(3)]
        }
        del d["pre"]

    return solids

def main(macro,out):
    solids=parse_macro(macro)
    A=sorted([n for n in solids if classify(n)=="A"])
    B=sorted([n for n in solids if classify(n)=="B"])
    if len(A)!=72 or len(B)!=72:
        raise RuntimeError("expected 72 A and 72 B solids, got %d/%d"%(len(A),len(B)))
    candidates=[]
    for a in A:
        for b in B:
            if overlap(solids[a]["aabb"],solids[b]["aabb"]):
                candidates.append({"a":a,"b":b,"aabb_a":solids[a]["aabb"],"aabb_b":solids[b]["aabb"]})
    result={
      "schema_version":"0.2.12",
      "classification":"SOURCE_GEOMETRY_AABB_BROADPHASE_ONLY",
      "macro":str(macro),
      "a_solid_count":len(A),
      "b_solid_count":len(B),
      "all_cross_pairs":len(A)*len(B),
      "candidate_pair_count":len(candidates),
      "candidate_pairs":candidates,
      "rule":"Every candidate must receive a qualified pairwise intersection test on a complete disposable CST project copy after build. Non-candidates are separated by exact/conservative source-derived AABBs.",
      "positive_volume_contact_allowed":False
    }
    Path(out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("A_SOLIDS=%d"%len(A))
    print("B_SOLIDS=%d"%len(B))
    print("ALL_CROSS_PAIRS=%d"%(len(A)*len(B)))
    print("CANDIDATE_PAIRS=%d"%len(candidates))
    return 0

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--macro",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.macro,a.out))
    except Exception as ex:
        print("EXCEPTION="+repr(ex))
        sys.exit(9)
