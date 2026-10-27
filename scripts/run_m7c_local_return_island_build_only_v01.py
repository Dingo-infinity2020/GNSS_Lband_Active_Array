from __future__ import print_function
import argparse, hashlib, json, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    s=src.with_suffix(""); d=dst.with_suffix("")
    if not s.exists(): raise RuntimeError("HOLD_M7_PARENT_COMPANION")
    if d.exists(): raise RuntimeError("HOLD_M7_DEST_COMPANION_EXISTS")
    shutil.copytree(str(s),str(d))

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,x in enumerate(lines):
        if x.strip()=="Sub Main()": s=i
        elif x.strip()=="End Sub": e=i
    if s is None or e is None or e<=s: raise RuntimeError("HOLD_M7_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def named_inventory_vba(path,names):
    p=str(path).replace("\\","/")
    q=lambda s:s.replace('"','""')
    z=["On Error Resume Next",
       "Dim f As Integer, nm As String, mat As String, vol As Double, em As Long, ev As Long",
       "f=FreeFile",'Open "'+p+'" For Output As #f',
       'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
       'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())']
    for n in names:
        z += ['nm="'+q(n)+'"',"Err.Clear","mat=Solid.GetMaterialNameForShape(nm)","em=Err.Number",
              "Err.Clear","vol=Solid.GetVolume(nm)","ev=Err.Number",
              'Print #f, "SHAPE|" & nm & "|MAT_ERR=" & CStr(em) & "|VOL_ERR=" & CStr(ev) & "|material=" & mat & "|volume=" & CStr(vol)']
    z += ["Close #f","On Error GoTo 0"]
    return "\n".join(z)

def ports_vba(path,count):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Integer, stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",'Open "'+p+'" For Output As #f',
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
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

def solver_result_files(companion):
    companion=Path(companion)
    if not companion.exists(): return []
    bad=[]
    for p in companion.rglob("*"):
        if not p.is_file(): continue
        rel=str(p.relative_to(companion)).replace("\\","/").lower()
        name=p.name.lower()
        if name=="output.txt" or "/result/" in ("/"+rel) and name.endswith((".sig",".m3d",".m1d",".c3d",".c1d")):
            bad.append(str(p))
    return bad

def main(manifest_path,out,evidence):
    manifest_path=Path(manifest_path); out=Path(out); evidence=Path(evidence)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    parent=Path(m["parent"]["path"])
    inv=Path(m["parent"]["inventory_contract"])
    macro=Path(ROOT/m["execution"]["macro"]) if not Path(m["execution"]["macro"]).is_absolute() else Path(m["execution"]["macro"])
    names=list(json.loads(inv.read_text(encoding="utf-8"))["expected_final_names"])
    modified=set(m["geometry"]["modified_entities"])
    if m["authorization"]!={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}:
        raise RuntimeError("HOLD_M7_MANIFEST_AUTH")
    if sha(parent)!=m["parent"]["sha256"] or not parent.with_suffix("").exists(): raise RuntimeError("HOLD_M7_PARENT")
    if sha(inv)!=m["parent"]["inventory_contract_sha256"]: raise RuntimeError("HOLD_M7_INVENTORY_SHA")
    if sha(macro)!=m["execution"]["macro_sha256"]: raise RuntimeError("HOLD_M7_MACRO_SHA")
    if len(names)!=177 or len(modified)!=4: raise RuntimeError("HOLD_M7_STATIC_COUNTS")
    if out.exists() or out.with_suffix("").exists() or evidence.exists(): raise RuntimeError("HOLD_M7_DEST_EXISTS")
    evidence.mkdir(parents=True)
    copy_project(parent,out)

    prei=evidence/"pre_inventory.txt"; prep=evidence/"pre_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(named_inventory_vba(prei,names))): raise RuntimeError("HOLD_M7_PRE_INV_VBA")
        if not p.schematic.execute_vba_code(wrap(ports_vba(prep,24))): raise RuntimeError("HOLD_M7_PRE_PORT_VBA")
    finally:
        if p is not None: p.close()
        de.close()
    prerows,premeta=parse_inv(prei)
    prechecks={
      "shape_count_177":int(premeta.get("SHAPE_COUNT","-1"))==177,
      "ports_24":int(premeta.get("PORT_COUNT","-1"))==24,
      "all_177_names_query":len(prerows)==177 and all(v["mat_err"]==0 and v["vol_err"]==0 for v in prerows.values()),
      "parent_has_no_solver_result_files":len(solver_result_files(out.with_suffix("")))==0
    }
    if not all(prechecks.values()): raise RuntimeError("HOLD_M7_PARENT_GATE")

    label=m["stage"]+" V01"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        p.modeler.add_to_history(label,macro_body(macro))
        p.save()
    finally:
        if p is not None: p.close()
        de.close()
    built_sha=sha(out)

    posti=evidence/"post_inventory.txt"; postp=evidence/"post_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(named_inventory_vba(posti,names))): raise RuntimeError("HOLD_M7_POST_INV_VBA")
        if not p.schematic.execute_vba_code(wrap(ports_vba(postp,24))): raise RuntimeError("HOLD_M7_POST_PORT_VBA")
    finally:
        if p is not None: p.close()
        de.close()
    postrows,postmeta=parse_inv(posti)

    preserved=True
    changed_unexpected=[]
    for n in names:
        if n in modified: continue
        a=prerows[n]; b=postrows.get(n)
        if b is None or a["material"]!=b["material"] or abs(a["volume"]-b["volume"])>1e-9:
            preserved=False; changed_unexpected.append(n)

    losses={}
    for n in sorted(modified):
        if n not in postrows: raise RuntimeError("HOLD_M7_MODIFIED_ENTITY_MISSING:"+n)
        losses[n]=prerows[n]["volume"]-postrows[n]["volume"]
    vals=list(losses.values())
    expected_loss=float(m["geometry"]["area_removed_per_branch_mm2"])*float(m["geometry"]["copper_thickness_mm"])
    modified_ok=(all(v>0 and abs(v-expected_loss)<=1e-6 for v in vals) and max(vals)-min(vals)<=1e-8)

    history=out.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=history.read_text(encoding="utf-8",errors="replace") if history.exists() else ""
    checks={
      "pre_parent_gate":all(prechecks.values()),
      "shape_count_exact_177":int(postmeta.get("SHAPE_COUNT","-1"))==177,
      "ports_exact_24":int(postmeta.get("PORT_COUNT","-1"))==24,
      "all_expected_names_query":len(postrows)==177 and all(v["mat_err"]==0 and v["vol_err"]==0 for v in postrows.values()),
      "173_unmodified_solids_preserved":preserved,
      "four_background_volume_losses_positive_symmetric":modified_ok,
      "ports_byte_semantics_unchanged":prep.read_text(encoding="utf-8")==postp.read_text(encoding="utf-8"),
      "history_persistent":label in htext,
      "fresh_reopen_hash_stable":sha(out)==built_sha,
      "no_solver_result_files_after_build":len(solver_result_files(out.with_suffix("")))==0
    }
    status=("PASS_"+m["stage"]) if all(checks.values()) else ("HOLD_"+m["stage"])
    summary={
      "status":status,"candidate":m["candidate"],"formal_build_invocations":1,"solver_invocations":0,
      "parent_sha256":m["parent"]["sha256"],"artifact_sha256":sha(out),
      "checks":checks,"modified_parent_volume_loss_mm3":losses,"expected_volume_loss_per_branch_mm3":expected_loss,
      "unexpected_changed_entities":changed_unexpected,
      "human_geometry_review_required":True,"solve_authorized":False
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# M7C LOCAL_RETURN_ISLAND_MOAT Human Geometry Review","",
      "Automated build status: "+status,"",
      "1. Confirm each of the four backside LOCAL_BACK_GROUND solids has one closed 0.25-mm copper moat surrounding the intended branch-local island.",
      "2. Confirm positive-branch island u=2.45..4.05, negative-branch island u=-4.05..-2.45, all with v=4.15..7.40; moat outer envelope is offset 0.25 mm.",
      "3. Confirm all signal copper, radiator, package lands, local-ground-top copper, all vias, bias/output copper and ports are visually unchanged.",
      "4. Confirm all three paddle vias for each branch remain inside and connected to the local island, none of the moat cuts intersects a via annulus, and the island does not touch an orthogonal-polarization backside ground.",
      "5. Confirm the four branch-local islands/moats are mirror/rotation symmetric and the moat is a copper etch only, not a substrate slot.",
      "",
      "Human PASS authorizes neither SOLVE nor any further geometry change."
    ]
    (evidence/"HUMAN_3D_REVIEW.md").write_text("\n".join(review)+"\n",encoding="utf-8")
    print(status)
    print("ARTIFACT_SHA256="+sha(out))
    print("LOSSES="+json.dumps(losses,sort_keys=True))
    return 0 if status.startswith("PASS_") else 4

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--variant-manifest",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.variant_manifest,a.out,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_M7_CORRECTIVE_BUILD_EXECUTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
