from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    s=src.with_suffix(""); d=dst.with_suffix("")
    if not s.exists(): raise RuntimeError("HOLD_M6_PARENT_COMPANION")
    if d.exists(): shutil.rmtree(str(d),ignore_errors=True)
    shutil.copytree(str(s),str(d))

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,x in enumerate(lines):
        if x.strip()=="Sub Main()": s=i
        elif x.strip()=="End Sub": e=i
    if s is None or e is None or e<=s: raise RuntimeError("HOLD_M6_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def named_inventory_vba(path,names):
    p=str(path).replace("\\","/")
    q=lambda s:s.replace('"','""')
    lines=["On Error Resume Next","Dim f As Integer, nm As String, mat As String, vol As Double, em As Long, ev As Long",
           "f=FreeFile",'Open "'+p+'" For Output As #f',
           'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
           'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())']
    for name in names:
        lines += ['nm="'+q(name)+'"',"Err.Clear","mat=Solid.GetMaterialNameForShape(nm)","em=Err.Number",
                  "Err.Clear","vol=Solid.GetVolume(nm)","ev=Err.Number",
                  'Print #f, "SHAPE|" & nm & "|MAT_ERR=" & CStr(em) & "|VOL_ERR=" & CStr(ev) & "|material=" & mat & "|volume=" & CStr(vol)']
    lines += ["Close #f","On Error GoTo 0"]
    return "\n".join(lines)

def ports_vba(path,count=12):
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

def run_audit(prj,invpath,portpath,names):
    if not prj.schematic.execute_vba_code(wrap(named_inventory_vba(invpath,names))):
        raise RuntimeError("HOLD_M6_INVENTORY_VBA")
    if not prj.schematic.execute_vba_code(wrap(ports_vba(portpath,12))):
        raise RuntimeError("HOLD_M6_PORT_VBA")

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

def result_tree(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return [x for x in p3.get_tree_items() if ("S-Parameters" in x or "Convergence" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+repr(ex)]

def main(manifest_path,out,evidence):
    manifest_path=Path(manifest_path); out=Path(out); evidence=Path(evidence)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    parent=Path(m["parent"]["path"]); macro=Path(m["source"]["macro"])
    parent_names=list(json.loads(Path(m["parent"]["inventory_contract"]).read_text(encoding="utf-8"))["expected_final_names"])
    final_names=list(m["geometry"]["expected_final_names"])
    modified=set(m["geometry"]["modified_parent_entities"])
    if m["authorization"]["BUILD_AUTHORIZED"] or m["authorization"]["SOLVE_AUTHORIZED"]:
        raise RuntimeError("HOLD_M6_MANIFEST_AUTH_MUST_REMAIN_FALSE")
    if sha(parent)!=m["parent"]["sha256"] or not parent.with_suffix("").exists(): raise RuntimeError("HOLD_M6_PARENT")
    if sha(macro)!=m["source"]["macro_sha256"]: raise RuntimeError("HOLD_M6_MACRO_SHA")
    if out.exists() or out.with_suffix("").exists() or evidence.exists(): raise RuntimeError("HOLD_M6_DEST_EXISTS")
    evidence.mkdir(parents=True)
    copy_project(parent,out)

    prei=evidence/"pre_inventory.txt"; prep=evidence/"pre_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out)); run_audit(p,prei,prep,parent_names)
    finally:
        if p is not None: p.close()
        de.close()
    prerows,premeta=parse_inv(prei)
    prechecks={
      "shape_count_parent_107":int(premeta.get("SHAPE_COUNT","-1"))==107,
      "ports_parent_12":int(premeta.get("PORT_COUNT","-1"))==12,
      "all_parent_names_query":len(prerows)==107 and all(v["mat_err"]==0 and v["vol_err"]==0 for v in prerows.values()),
      "result_tree_empty":len(result_tree(out))==0
    }
    if not all(prechecks.values()): raise RuntimeError("HOLD_M6_PARENT_GATE")

    label=m["stage"]+" V01"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out)); p.modeler.add_to_history(label,macro_body(macro)); p.save()
    finally:
        if p is not None: p.close()
        de.close()
    built_sha=sha(out)

    posti=evidence/"post_inventory.txt"; postp=evidence/"post_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out)); run_audit(p,posti,postp,final_names)
    finally:
        if p is not None: p.close()
        de.close()
    postrows,postmeta=parse_inv(posti)
    history=out.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=history.read_text(encoding="utf-8",errors="replace") if history.exists() else ""
    parent_preserved=True
    for n in parent_names:
        if n in modified: continue
        a=prerows[n]; b=postrows.get(n)
        if b is None or a["material"]!=b["material"] or abs(a["volume"]-b["volume"])>1e-9:
            parent_preserved=False; break
    losses={}
    modified_ok=True
    if modified:
        for n in sorted(modified):
            if n not in postrows: modified_ok=False; continue
            loss=prerows[n]["volume"]-postrows[n]["volume"]; losses[n]=loss
            if loss<=0: modified_ok=False
        if len(losses)==2 and abs(list(losses.values())[0]-list(losses.values())[1])>1e-7: modified_ok=False

    drill_tools=m["geometry"]["drill_tool_entities"]
    tools_absent=all(x not in postrows for x in drill_tools)
    vias=[n for n in m["geometry"]["added_final_entities"] if "_Vias:" in n]
    via_target=math.pi*(0.175**2-0.125**2)*1.07
    via_ok=all(n in postrows and abs(postrows[n]["volume"]-via_target)<=1e-7 for n in vias)
    checks={
      "pre_parent_gate":all(prechecks.values()),
      "shape_count_exact":int(postmeta.get("SHAPE_COUNT","-1"))==m["geometry"]["expected_final_shape_count"],
      "ports_12":int(postmeta.get("PORT_COUNT","-1"))==12,
      "all_expected_names_query":len(postrows)==len(final_names) and all(v["mat_err"]==0 and v["vol_err"]==0 for v in postrows.values()),
      "parent_signature_preserved_except_declared_modifications":parent_preserved,
      "declared_modified_parent_entities_valid":modified_ok,
      "drill_tools_consumed":tools_absent,
      "vias_exact_volume":via_ok,
      "ports_byte_semantics_unchanged":prep.read_text(encoding="utf-8")==postp.read_text(encoding="utf-8"),
      "history_persistent":label in htext,
      "result_tree_empty_after_build":len(result_tree(out))==0,
      "fresh_reopen_hash_stable":sha(out)==built_sha
    }
    status="PASS_"+m["stage"] if all(checks.values()) else "HOLD_"+m["stage"]
    summary={"status":status,"variant":m["variant"],"formal_build_invocations":1,"solver_invocations":0,
             "parent_sha256":m["parent"]["sha256"],"artifact_sha256":sha(out),"checks":checks,
             "modified_parent_volume_loss_mm3":losses,"human_geometry_review_required":True,
             "future_solve_not_authorized":True}
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# "+m["stage"]+" Human Geometry Review","",
      "Automated build status: "+status,"",
      "Do not save over the protected artifact.",
      "1. Confirm canonical E2A Pol-A geometry remains unchanged.",
      "2. Confirm only the variant-declared Pol-B passive entity class was added.",
      "3. Confirm no new Pol-B discrete ports or solver monitors exist.",
      "4. Inspect the orthogonal crossing region and all nearest ground/signal clearances.",
      "5. For D2, inspect all eight B-prong plated-via holes and ground connectivity.",
      "6. Confirm no unexpected signal-ground galvanic contact or positive-volume interference.",
      "",
      "Human PASS authorizes neither SOLVE nor geometry optimization."
    ]
    (evidence/"HUMAN_3D_REVIEW.md").write_text("\n".join(review)+"\n",encoding="utf-8")
    print(status); print("ARTIFACT_SHA256="+sha(out))
    return 0 if status.startswith("PASS_") else 4

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
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_M6_ATTRIBUTION_BUILD_EXECUTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
