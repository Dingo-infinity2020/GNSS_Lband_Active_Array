from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from pathlib import Path
from collections import Counter

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

S2=1.0/math.sqrt(2.0)
Z0=57.1428571428
PORT_LOCAL={1:(3.0,4.650),2:(3.0,6.085),3:(3.0,7.915),4:(-3.0,4.650),5:(-3.0,6.085),6:(-3.0,7.915)}
SOURCE_PORTS=(1,2,4,5); LOAD_ONLY=(3,6)

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,x in enumerate(lines):
        if x.strip()=="Sub Main()": s=i
        elif x.strip()=="End Sub": e=i
    if s is None or e is None or e<=s: raise RuntimeError("HOLD_M6_DIAG_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    s=src.with_suffix(""); d=dst.with_suffix("")
    if not s.exists(): raise RuntimeError("HOLD_M6_DIAG_SOURCE_COMPANION")
    if d.exists(): shutil.rmtree(str(d),ignore_errors=True)
    shutil.copytree(str(s),str(d))

def inventory_named_vba(path,names):
    p=str(path).replace("\\","/")
    q=lambda s:s.replace('"','""')
    z=["On Error Resume Next","Dim f As Integer, nm As String, mat As String, vol As Double, em As Long, ev As Long",
       "f=FreeFile",'Open "'+p+'" For Output As #f','Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
       'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())']
    for n in names:
        z += ['nm="'+q(n)+'"',"Err.Clear","mat=Solid.GetMaterialNameForShape(nm)","em=Err.Number",
              "Err.Clear","vol=Solid.GetVolume(nm)","ev=Err.Number",
              'Print #f, "SHAPE|" & nm & "|MAT_ERR=" & CStr(em) & "|VOL_ERR=" & CStr(ev) & "|material=" & mat & "|volume=" & CStr(vol)']
    z += ["Close #f","On Error GoTo 0"]
    return "\n".join(z)

def port_vba(path,count):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Integer, stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",'Open "'+p+'" For Output As #f','Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "For i=1 To %d"%count,
      " Err.Clear"," pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P|" & CStr(i) & "|PROP_OK=" & CStr(pok) & "|ERR=" & CStr(Err.Number) & "|TYPE=" & stype & "|ZREF=" & CStr(zref)',
      " Err.Clear"," cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "C|" & CStr(i) & "|COORD_OK=" & CStr(cok) & "|ERR=" & CStr(Err.Number) & "|P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0) & "|P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i","Close #f","On Error GoTo 0"])

def parse_inv(path):
    rows={}; meta={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            p=line.split("|"); d={}
            for x in p[2:]:
                k,v=x.split("=",1); d[k]=v
            rows[p[1]]={"material":d["material"],"volume":float(d["volume"]),
                        "mat_err":int(d["MAT_ERR"]),"vol_err":int(d["VOL_ERR"])}
        elif "=" in line:
            k,v=line.split("=",1); meta[k]=v
    return rows,meta

def parse_ports(path):
    out={"count":None,"properties":{},"coordinates":{}}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("PORT_COUNT="): out["count"]=int(line.split("=",1)[1])
        elif line.startswith(("P|","C|")):
            p=line.split("|"); kind=p[0]; idx=int(p[1]); d={}
            for x in p[2:]:
                k,v=x.split("=",1); d[k]=v
            out["properties" if kind=="P" else "coordinates"][idx]=d
    return out

def xyz(s): return tuple(float(x) for x in s.split(","))

def expected_xyz(i):
    u,v=PORT_LOCAL[i]; z=Z0-v
    return (S2*u,S2*u,z),(S2*(u+1.0),S2*(u-1.0),z)

def ports6_exact(data,tol=2e-8):
    if data["count"]!=6: return False
    for i in range(1,7):
        p=data["properties"].get(i,{}); c=data["coordinates"].get(i,{})
        if p.get("PROP_OK") not in ("True","TRUE","1","-1"): return False
        if c.get("COORD_OK") not in ("True","TRUE","1","-1"): return False
        if p.get("TYPE")!="SParameter" or abs(float(p.get("ZREF","nan"))-50)>tol: return False
        e1,e2=expected_xyz(i)
        if any(abs(a-b)>tol for a,b in zip(xyz(c["P1"]),e1)): return False
        if any(abs(a-b)>tol for a,b in zip(xyz(c["P2"]),e2)): return False
    return True

def sig(rows): return {k:(v["material"],round(v["volume"],12)) for k,v in rows.items()}

def result_solver_paths(cst):
    try:
        items=ProjectFile(str(cst),allow_interactive=True).get_3d().get_tree_items()
        return [x for x in items if ("S-Parameters" in x or "Convergence" in x or "Adaptive Meshing" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+repr(ex)]

def configure(manifest_path,out,evidence):
    manifest_path=Path(manifest_path); out=Path(out); evidence=Path(evidence)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    src=Path(m["source_build"]["path"])
    config=Path(ROOT/m["execution"]["config_macro"]) if not Path(m["execution"]["config_macro"]).is_absolute() else Path(m["execution"]["config_macro"])
    names=json.loads(Path(ROOT/("execution/R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_%s_%s_BUILD_MANIFEST_V01.json"%(
      m["variant"],"SIG" if m["variant"]=="D1" else "GND"))).read_text(encoding="utf-8"))["geometry"]["expected_final_names"]
    if sha(src)!=m["source_build"]["sha256"] or not src.with_suffix("").exists(): raise RuntimeError("HOLD_M6_DIAG_SOURCE")
    if sha(config)!=m["execution"]["config_macro_sha256"]: raise RuntimeError("HOLD_M6_DIAG_CONFIG_SHA")
    if out.exists() or out.with_suffix("").exists() or evidence.exists(): raise RuntimeError("HOLD_M6_DIAG_DEST_EXISTS")
    evidence.mkdir(parents=True)
    copy_project(src,out)

    bi=evidence/"before_inventory.txt"; bp=evidence/"before_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inventory_named_vba(bi,names))): raise RuntimeError("HOLD_M6_DIAG_BEFORE_INV")
        if not p.schematic.execute_vba_code(wrap(port_vba(bp,12))): raise RuntimeError("HOLD_M6_DIAG_BEFORE_PORTS")
    finally:
        if p is not None: p.close()
        de.close()
    br,bm=parse_inv(bi)
    if int(bm.get("SHAPE_COUNT","-1"))!=m["source_build"]["shape_count"] or int(bm.get("PORT_COUNT","-1"))!=12 or len(br)!=len(names):
        raise RuntimeError("HOLD_M6_DIAG_SOURCE_GATE")
    if any(v["mat_err"] or v["vol_err"] for v in br.values()): raise RuntimeError("HOLD_M6_DIAG_SOURCE_QUERY")
    before=sig(br)
    if result_solver_paths(out): raise RuntimeError("HOLD_M6_DIAG_SOURCE_HAS_RESULTS")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out)); p.modeler.add_to_history("M6 %s diagnostic presolve config V01"%m["variant"],macro_body(config)); p.save()
    finally:
        if p is not None: p.close()
        de.close()
    configured_sha=sha(out)

    ai=evidence/"configured_inventory.txt"; ap=evidence/"configured_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inventory_named_vba(ai,names))): raise RuntimeError("HOLD_M6_DIAG_AFTER_INV")
        if not p.schematic.execute_vba_code(wrap(port_vba(ap,6))): raise RuntimeError("HOLD_M6_DIAG_AFTER_PORTS")
    finally:
        if p is not None: p.close()
        de.close()
    ar,am=parse_inv(ai); pd=parse_ports(ap)
    hist=out.with_suffix("")/"Model"/"3D"/"Model.mod"
    ht=hist.read_text(encoding="utf-8",errors="replace") if hist.exists() else ""
    required=[
      'Port.Delete 12','Port.Delete 11','Port.Delete 10','Port.Delete 6','Port.Delete 5','Port.Delete 4',
      'Port.Rename 7, 4','Port.Rename 8, 5','Port.Rename 9, 6',
      '.AddToExcitationList "1", "1"','.AddToExcitationList "2", "1"',
      '.AddToExcitationList "4", "1"','.AddToExcitationList "5", "1"',
      '.FieldType "Hfield"','.Frequency "1.2276"','.Frequency "1.3384"','.Frequency "1.57542"']
    checks={
      "source_hash_exact":sha(src)==m["source_build"]["sha256"],
      "shape_count_unchanged":int(am.get("SHAPE_COUNT","-1"))==m["source_build"]["shape_count"],
      "geometry_signature_unchanged":sig(ar)==before,
      "six_ports_exact":ports6_exact(pd),
      "history_tokens_exact":all(x in ht for x in required),
      "load_ports_not_excited":'.AddToExcitationList "3", "1"' not in ht and '.AddToExcitationList "6", "1"' not in ht,
      "three_hfield_monitors":ht.count('.FieldType "Hfield"')>=3,
      "result_tree_empty_before_solve":len(result_solver_paths(out))==0,
      "configured_hash_stable":sha(out)==configured_sha
    }
    (evidence/"presolve_summary.json").write_text(json.dumps({"status":"PASS_M6_DIAG_PRESOLVE" if all(checks.values()) else "HOLD_M6_DIAG_PRESOLVE","checks":checks,"configured_sha256":configured_sha},indent=2)+"\n",encoding="utf-8")
    if not all(checks.values()): raise RuntimeError("HOLD_M6_DIAG_PRESOLVE")
    return {"configured_sha256":configured_sha,"source_sha256":m["source_build"]["sha256"]}

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--variant-manifest",required=True); ap.add_argument("--out",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        print(json.dumps(configure(a.variant_manifest,a.out,a.evidence),indent=2))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
