from __future__ import print_function
import ast, hashlib, json, re, sys
from collections import Counter
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
PARENT=Path(r"D:\GNSS_Lband_Active_Array\GNSS_R4A0E2A_20260928_BUILD_R2\R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_INTEGRATED_BUILD_ONLY_V02_RECOVERY.cst")
PARENT_SHA="78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804"
PARENT_INV=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_INVENTORY_V01.json"
E2C_MACRO=ROOT/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_ONLY_V01.mcr"
M6=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_V02"/"M6_V02_ANALYSIS.json"

RUNNER=ROOT/"scripts"/"run_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_m6_attribution_build_only_v01.py"
PACKET_GEN=ROOT/"scripts"/"make_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_m6_build_packet_v01.py"
AUDITOR=ROOT/"scripts"/"audit_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_m6_d1d2_prebuild_v01.py"
DOC=ROOT/"docs"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1D2_BUILD_PREPARATION_FREEZE_V01.md"
EVIDENCE=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1D2_PREBUILD_V01"

VARIANTS={
 "D1":{
   "stage":"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_SIG_ATTRIBUTION_BUILD_ONLY",
   "macro":ROOT/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_SIG_BUILD_ONLY_V01.mcr",
   "manifest":ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_SIG_BUILD_MANIFEST_V01.json",
   "target_root":r"D:\GNSS_Lband_Active_Array\runs\formal\build_only\M6_D1_SIG_ATTRIBUTION_V01",
   "artifact":"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_SIG_BUILD_ONLY_V01.cst",
 },
 "D2":{
   "stage":"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_GND_ATTRIBUTION_BUILD_ONLY",
   "macro":ROOT/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_GND_BUILD_ONLY_V01.mcr",
   "manifest":ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_GND_BUILD_MANIFEST_V01.json",
   "target_root":r"D:\GNSS_Lband_Active_Array\runs\formal\build_only\M6_D2_GND_ATTRIBUTION_V01",
   "artifact":"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_GND_BUILD_ONLY_V01.cst",
 }
}

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def parse_blocks(lines):
    out=[]
    i=0
    while i<len(lines):
        m=re.match(r"^\s*With\s+([A-Za-z0-9_]+)",lines[i])
        if not m:
            i+=1; continue
        typ=m.group(1); j=i+1
        while j<len(lines) and lines[j].strip()!="End With": j+=1
        if j>=len(lines): raise RuntimeError("unterminated block")
        block=lines[i:j+1]
        full=None
        name=comp=None
        for x in block:
            q=re.match(r'\s*\.(Name|Component)\s+"([^"]+)"',x,re.I)
            if q:
                if q.group(1).lower()=="name": name=q.group(2)
                else: comp=q.group(2)
        if typ.lower()=="transform":
            full=name
        elif name and comp:
            full=comp+":"+name
        out.append({"type":typ,"start":i,"end":j,"lines":block,"full":full})
        i=j+1
    return out

def block_map(blocks):
    d={}
    for b in blocks:
        if b["full"] and b["type"].lower() in ("extrude","cylinder"):
            d.setdefault(b["full"],[]).append(b)
    return d

def immediate_transform(blocks,block):
    for b in blocks:
        if b["start"]==block["end"]+1 and b["type"].lower()=="transform" and b["full"]==block["full"]:
            return b
    return None

def make_macro(variant,target_names,source_lines,blocks,bmap):
    selected=[]
    target_set=set(target_names)
    for name in target_names:
        hits=bmap.get(name,[])
        if len(hits)!=1:
            raise RuntimeError("%s target block count %s=%d"%(variant,name,len(hits)))
        b=hits[0]
        selected.append((b["start"],b["lines"]))
        t=immediate_transform(blocks,b)
        if t: selected.append((t["start"],t["lines"]))

    drill_tools=[]
    if variant=="D2":
        via_names=[x for x in target_names if "_Vias:" in x]
        if len(via_names)!=8: raise RuntimeError("D2 via target count !=8")
        for via in via_names:
            comp,name=via.split(":",1)
            tool=comp.replace("_Vias","_ViaHoleTools")+":"+name+"_DRILL"
            drill_tools.append(tool)
            hits=bmap.get(tool,[])
            if len(hits)!=1: raise RuntimeError("D2 drill block count %s=%d"%(tool,len(hits)))
            b=hits[0]; selected.append((b["start"],b["lines"]))
            t=immediate_transform(blocks,b)
            if t: selected.append((t["start"],t["lines"]))
            sub_hits=[]
            for i,line in enumerate(source_lines):
                if "Solid.Subtract" in line and tool in line:
                    sub_hits.append((i,[line]))
            if len(sub_hits)!=1: raise RuntimeError("D2 subtract count %s=%d"%(tool,len(sub_hits)))
            selected.extend(sub_hits)

    selected.sort(key=lambda x:x[0])
    seen=set(); body=[]
    for idx,lines in selected:
        key=(idx,tuple(lines))
        if key in seen: continue
        seen.add(key)
        body.extend(lines); body.append("")

    label="R4-A0-E2C-S0-M6-%s attribution BUILD ONLY V01"%variant
    header=[
      "Option Explicit",
      "' GNSS_Lband_Active_Array",
      "' "+label,
      "'",
      "' Parent: canonical E2A Pol-A BUILD_ONLY baseline",
      "' Parent SHA256: "+PARENT_SHA,
      "' Diagnostic only; no ports, monitors, solver configuration, or solver invocation added.",
      "",
      "Sub Main()",
      ""
    ]
    footer=["End Sub",""]
    return "\n".join(header+["  "+x if x and not x.startswith("'") else x for x in body]+footer),drill_tools

def component_counts(names):
    return dict(Counter(x.split(":",1)[0] for x in names))

m6=json.loads(M6.read_text(encoding="utf-8"))
if m6["status"]!="PASS_M6_V02_EXACT_ENTITY_ATTRIBUTION_READY":
    raise RuntimeError("M6 v0.2 not pass")
parent=json.loads(PARENT_INV.read_text(encoding="utf-8"))
parent_names=list(parent["expected_final_names"])
if parent["expected_final_shape_count"]!=107 or len(parent_names)!=107:
    raise RuntimeError("E2A parent inventory mismatch")
if not PARENT.exists() or sha(PARENT)!=PARENT_SHA or not PARENT.with_suffix("").exists():
    raise RuntimeError("canonical E2A build parent unavailable")
if sha(PARENT_INV)=="" or sha(E2C_MACRO)=="":
    raise RuntimeError("source hash failure")

vmap={x["id"]:x for x in m6["diagnostic_variants"]}
d1=list(vmap["M6-D1-SIG"]["add_from_polB"])
d2=list(vmap["M6-D2-GND"]["add_from_polB"])
if len(d1)!=6 or len(d2)!=34:
    raise RuntimeError("M6 target count drift")

source_lines=E2C_MACRO.read_text(encoding="utf-8",errors="replace").splitlines()
blocks=parse_blocks(source_lines); bmap=block_map(blocks)

for key,targets in (("D1",d1),("D2",d2)):
    cfg=VARIANTS[key]
    macro,drills=make_macro(key,targets,source_lines,blocks,bmap)
    cfg["macro"].write_text(macro,encoding="utf-8")
    expected_names=parent_names+targets
    expected_counts=dict(parent["expected_final_component_counts"])
    for comp,n in component_counts(targets).items():
        expected_counts[comp]=expected_counts.get(comp,0)+n
    modified=[] if key=="D1" else ["B0_Stalk:B_P_PRONG","B0_Stalk:B_N_PRONG"]
    manifest={
      "schema_version":"gnss-m6-attribution-build-v0.1",
      "status":"FROZEN_PREBUILD_AWAIT_AUTH",
      "variant":key,
      "stage":cfg["stage"],
      "scientific_question":vmap["M6-"+key+("-SIG" if key=="D1" else "-GND")]["purpose"],
      "parent":{
        "path":str(PARENT),"sha256":PARENT_SHA,
        "shape_count":107,
        "inventory_contract":str(PARENT_INV),
        "inventory_contract_sha256":sha(PARENT_INV),
        "ports":12,
        "result_tree":"EMPTY_BUILD_ONLY"
      },
      "source":{
        "macro":str(cfg["macro"]),
        "macro_sha256":sha(cfg["macro"]),
        "entity_source":str(E2C_MACRO),
        "entity_source_sha256":sha(E2C_MACRO)
      },
      "geometry":{
        "added_final_entities":targets,
        "added_final_entity_count":len(targets),
        "drill_tool_entities":drills,
        "drill_tool_count":len(drills),
        "modified_parent_entities":modified,
        "expected_final_shape_count":107+len(targets),
        "expected_final_names":expected_names,
        "expected_final_component_counts":expected_counts,
        "port_policy":"EXACT_PARENT_12_PORTS_UNCHANGED_NO_POLB_PORTS",
        "monitor_policy":"NO_MONITORS_IN_BUILD_ONLY",
        "human_geometry_review_required":True
      },
      "future_solve_contract":{
        "not_authorized":True,
        "observer":"Pol-A E2A loaded-source semantics",
        "polB_ports":"NONE",
        "surface_current_monitors_ghz":[1.2276,1.3384,1.57542],
        "primary_observables":[
          "Pol-A own-pol complex delta versus E2A isolated baseline",
          "Pol-A E_UP differential-to-common degradation",
          "Pol-A E_UP plus/minus return imbalance"
        ],
        "directional_prediction":vmap["M6-"+key+("-SIG" if key=="D1" else "-GND")]["prediction"]
      },
      "execution":{
        "target_root":cfg["target_root"],
        "artifact_name":cfg["artifact"],
        "stop_boundary":"STOP_AFTER_BUILD_FRESH_REOPEN_EXACT_INVENTORY_PORT_INVARIANCE_AND_HUMAN_REVIEW_COPY_NO_SOLVER"
      },
      "authorization":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
    }
    cfg["manifest"].write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

RUNNER.write_text(r'''from __future__ import print_function
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
''',encoding="utf-8")

PACKET_GEN.write_text(r'''from __future__ import print_function
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",required=True)
    ap.add_argument("--variant-manifest",required=True)
    ap.add_argument("--packet",required=True)
    ap.add_argument("--state-root",required=True)
    ap.add_argument("--result-packet",required=True)
    ap.add_argument("--cst-python",required=True)
    a=ap.parse_args()
    root=Path(a.project_root).resolve(); vm=Path(a.variant_manifest).resolve()
    m=json.loads(vm.read_text(encoding="utf-8"))
    contract=root/"execution"/"stage_contract.json"
    runner=root/"scripts"/"run_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_m6_attribution_build_only_v01.py"
    if subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip():
        raise SystemExit("HOLD_M6_PROJECT_DIRTY")
    head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    c=json.loads(contract.read_text(encoding="utf-8-sig"))
    g=c.get("authorization",{}).get("active_grant")
    failed=[]
    if c.get("authorization",{}).get("BUILD_AUTHORIZED") is not True: failed.append("build_live")
    if c.get("authorization",{}).get("SOLVE_AUTHORIZED") is not False: failed.append("solve_false")
    if not isinstance(g,dict): failed.append("active_grant")
    if isinstance(g,dict):
        if g.get("kind")!="BUILD": failed.append("grant_kind")
        if g.get("state")!="GRANTED": failed.append("grant_state")
        if g.get("stage")!=m["stage"]: failed.append("grant_stage")
        if g.get("entrypoint_sha256")!=sha(runner): failed.append("entrypoint_sha")
        if g.get("source_commit")!=c.get("project",{}).get("source_commit"): failed.append("source_commit")
    if c.get("execution",{}).get("current_stage")!=m["stage"]: failed.append("current_stage")
    if failed: raise SystemExit("HOLD_M6_LIVE_BUILD_GRANT:"+",".join(failed))
    target=Path(m["execution"]["target_root"]); artifact=target/m["execution"]["artifact_name"]; evidence=target/"evidence"
    packet={
      "schema_version":"runner-task-v0.2",
      "packet_id":"GNSS-"+m["variant"]+"-ATTRIBUTION-BUILD",
      "project":{"name":"GNSS_Lband_Active_Array","repository":"Dingo-infinity2020/GNSS_Lband_Active_Array",
                 "source_commit":c["project"]["source_commit"],"model_identity":m["stage"]},
      "stage":{"name":m["stage"],"kind":"BUILD_ONLY","control_host_alias":"NW","working_directory":str(root),
               "stop_boundary":m["execution"]["stop_boundary"]},
      "transport":{"type":"local","ssh_alias":"","remote_shell":""},
      "preflight":{"fail_closed":True,"checks":[
        {"id":"git_clean","type":"git_clean","path":"."},
        {"id":"git_head","type":"git_head_equals","path":".","commit":head},
        {"id":"runner_hash","type":"file_sha256_equals","path":str(runner.relative_to(root)).replace("\\","/"),"sha256":sha(runner)},
        {"id":"variant_manifest_hash","type":"file_sha256_equals","path":str(vm.relative_to(root)).replace("\\","/"),"sha256":sha(vm)},
        {"id":"stage_contract_hash","type":"file_sha256_equals","path":"execution/stage_contract.json","sha256":sha(contract)},
        {"id":"parent_hash","type":"file_sha256_equals","path":m["parent"]["path"],"sha256":m["parent"]["sha256"]},
        {"id":"target_absent","type":"path_absent","path":str(target)},
        {"id":"result_absent","type":"result_path_absent"},
        {"id":"cst_gui_absent","type":"process_absent","name":"CST DESIGN ENVIRONMENT_AMD64.exe","ignore_case":True},
        {"id":"cst_modeler_absent","type":"process_absent","name":"modeler_AMD64.exe","ignore_case":True}
      ]},
      "entrypoint":{"argv":[str(Path(a.cst_python).resolve()),str(runner.relative_to(root)).replace("\\","/"),
                            "--variant-manifest",str(vm.relative_to(root)).replace("\\","/"),
                            "--out",str(artifact),"--evidence",str(evidence)],
                    "environment":{},"timeout_seconds":2400},
      "authorization":{"BUILD_AUTHORIZED":True,"SOLVE_AUTHORIZED":False,
        "grant_snapshot":{"grant_id":g["grant_id"],"kind":g["kind"],"state":g["state"],"stage":g["stage"],
                          "source_commit":g["source_commit"],
                          "entrypoint_path":str(runner.relative_to(root)).replace("\\","/"),
                          "entrypoint_sha256":sha(runner),
                          "stage_contract_path":"execution/stage_contract.json",
                          "stage_contract_sha256":sha(contract),
                          "granted_at":g["granted_at"],"expires_at":g.get("expires_at"),
                          "entrypoint_arg_index":1}},
      "dc_call_budget":{"target_calls":1,"polling_policy":"no_polling","remote_mcp_calls_target":3},
      "expected_outputs":[
        {"path":str(artifact),"required":True,"sha256":True},
        {"path":str(evidence/"FINAL_STATUS.txt"),"required":True,"sha256":True},
        {"path":str(evidence/"summary.json"),"required":True,"sha256":True},
        {"path":str(evidence/"HUMAN_3D_REVIEW.md"),"required":True,"sha256":True}],
      "result":{"state_root":str(Path(a.state_root).resolve()),"result_packet_path":str(Path(a.result_packet).resolve())}
    }
    p=Path(a.packet); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(packet,indent=2)+"\n",encoding="utf-8")
    print("PASS_M6_BUILD_PACKET_GENERATED")
    return 0
if __name__=="__main__": sys.exit(main())
''',encoding="utf-8")

AUDITOR.write_text(r'''from __future__ import print_function
import ast, hashlib, json, re, sys
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1D2_PREBUILD_V01"/"STATIC_AUDIT.json"
RUNNER=ROOT/"scripts"/"run_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_m6_attribution_build_only_v01.py"
PKT=ROOT/"scripts"/"make_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_m6_build_packet_v01.py"
PARENT_SHA="78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804"

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def solver_calls(path):
    tree=ast.parse(Path(path).read_text(encoding="utf-8"))
    n=0
    for x in ast.walk(tree):
        if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=="run_solver": n+=1
    return n

def names_in_macro(txt):
    blocks=[]; comp=name=None
    for line in txt.splitlines():
        m=re.match(r'\s*\.Component\s+"([^"]+)"',line)
        if m: comp=m.group(1)
        m=re.match(r'\s*\.Name\s+"([^"]+)"',line)
        if m: name=m.group(1)
        if ".Create" in line and comp and name:
            blocks.append(comp+":"+name); comp=name=None
    return blocks

checks={}
details={}
for key,base,count,drills,subs in (
 ("D1","R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_SIG",6,0,0),
 ("D2","R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_GND",34,8,8)):
    mp=ROOT/"source"/"cst"/(base+"_BUILD_ONLY_V01.mcr")
    jp=ROOT/"execution"/(base+"_BUILD_MANIFEST_V01.json")
    m=json.loads(jp.read_text(encoding="utf-8")); txt=mp.read_text(encoding="utf-8")
    created=names_in_macro(txt)
    final=set(m["geometry"]["added_final_entities"]); tools=set(m["geometry"]["drill_tool_entities"])
    checks[key+"_parent_hash_declared"]=m["parent"]["sha256"]==PARENT_SHA
    checks[key+"_added_count"]=len(final)==count
    checks[key+"_expected_shape_count"]=m["geometry"]["expected_final_shape_count"]==107+count
    checks[key+"_created_final_exact"]=final.issubset(set(created))
    checks[key+"_tool_count"]=len(tools)==drills
    checks[key+"_created_tools_exact"]=tools.issubset(set(created))
    checks[key+"_subtract_count"]=txt.count("Solid.Subtract")==subs
    checks[key+"_no_port_mutation"]=all(x not in txt for x in ("DiscretePort","Port.","Solver.","ChangeSolverType","Monitor."))
    checks[key+"_no_solver_tokens"]=all(x not in txt for x in ("run_solver","StartSolver","Solver.Start"))
    checks[key+"_auth_false"]=m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
    checks[key+"_future_monitors_frozen"]=m["future_solve_contract"]["surface_current_monitors_ghz"]==[1.2276,1.3384,1.57542]
    details[key]={"macro_sha256":sha(mp),"manifest_sha256":sha(jp),"created_count":len(created),"created":created}

checks["runner_ast_zero_run_solver"]=solver_calls(RUNNER)==0
checks["packet_generator_ast_zero_run_solver"]=solver_calls(PKT)==0
checks["runner_has_fresh_reopen"]="post_inventory.txt" in RUNNER.read_text(encoding="utf-8")
checks["runner_checks_port_invariance"]="ports_byte_semantics_unchanged" in RUNNER.read_text(encoding="utf-8")
checks["runner_no_pairwise_explosion"]="Solid.Intersect" not in RUNNER.read_text(encoding="utf-8")
checks["packet_schema_v02"]='"schema_version":"runner-task-v0.2"' in PKT.read_text(encoding="utf-8")
status="PASS_M6_D1D2_PREBUILD_STATIC_CONTRACT" if all(checks.values()) else "HOLD_M6_D1D2_PREBUILD_STATIC_CONTRACT"
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({"status":status,"checks":checks,"details":details,
                           "formal_build_invocations":0,"solver_invocations":0,
                           "BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},indent=2)+"\n",encoding="utf-8")
print(status)
for k,v in checks.items():
    if not v: print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
''',encoding="utf-8")

DOC.write_text("""# R4-A0-E2C-S0 M6 D1/D2 BUILD Preparation Freeze V0.1

Status: PREPARED_OFFLINE_AWAIT_BUILD_AUTH

Parent authority is the protected E2A Pol-A BUILD_ONLY baseline:
- 107 solids
- 12 audit/reference ports
- empty result tree
- SHA256 78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804

## D1 — SIG attribution

Add exactly six Pol-B pre-CIN signal solids:
- P/N UPSTREAM_MSL
- P/N UPSTREAM_TAPER
- P/N CIN_UP_PAD

Expected final shape count: 113.

No parent solid may be modified.
No Pol-B port is added.
No monitor or solver configuration is added.

Prediction: if pre-CIN signal metal is dominant, Pol-A own-pol complex delta and E_UP differential/common degradation should move strongly toward the full-E2C severe state.

## D2 — GND attribution

Add exactly 34 Pol-B ground/via solids:
- 2 local backside grounds
- 10 grounded package lands
- 14 local-ground-top paddle/spoke/pad solids
- 8 plated vias

Only B0_Stalk:B_P_PRONG and B0_Stalk:B_N_PRONG may be modified, and only by the eight declared via-hole subtract operations.

Expected final shape count: 141.

No Pol-B port is added.
No monitor or solver configuration is added.

Prediction: if the return structure is dominant, Pol-A branch imbalance and E_UP differential/common degradation should move strongly toward full E2C while D1 remains comparatively weak.

## Future solve evidence, if separately authorized

The build artifact remains a 12-port geometry/audit model. A future solve-copy must preserve the E2A observer semantics and add no Pol-B excitation ports.

Surface-current evidence must be captured at:
- L2 1.2276 GHz
- mixed-mode region 1.3384 GHz
- L1 1.57542 GHz

The first attribution comparison is D1 vs D2 vs existing isolated E2A vs existing full E2C.

## Automation boundary

A generic future BUILD runner and runner-task-v0.2 packet generator are prepared, but the packet generator fails closed without a live BUILD grant bound to the exact stage and runner SHA.

No destructive pairwise-intersection fan-out is part of these diagnostic BUILDs. Fresh-reopen inventory, port invariance and mandatory human geometry review are the build gates.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
""",encoding="utf-8")

print("PREPARED_D1_D2_SOURCES")
print("D1_MACRO="+str(VARIANTS["D1"]["macro"]))
print("D2_MACRO="+str(VARIANTS["D2"]["macro"]))
print("RUNNER="+str(RUNNER))
print("PACKET_GEN="+str(PACKET_GEN))
print("AUDITOR="+str(AUDITOR))
