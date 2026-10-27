from __future__ import print_function
import ast, hashlib, json, sys
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK_MANIFEST_V01.json"
INV=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_INVENTORY_V01.json"
RUNNER=ROOT/"scripts"/"run_m7_corrective_build_only_v01.py"
PKT=ROOT/"scripts"/"make_m7_corrective_build_packet_v01.py"
AUDIT=ROOT/"scripts"/"audit_m7a_formal_build_chain_v01.py"
STATIC=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_FORMAL_BUILD_PREP_V01"/"STATIC_AUDIT.json"

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

m=json.loads(MAN.read_text(encoding="utf-8"))
inv=json.loads(INV.read_text(encoding="utf-8"))
if inv["expected_final_shape_count"]!=177 or len(inv["expected_final_names"])!=177:
    raise RuntimeError("HOLD_M7A_E2C_INVENTORY")
if m["candidate"]!="M7A":
    raise RuntimeError("HOLD_M7A_MANIFEST_ID")
m["stage"]="R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK_BUILD_ONLY"
m["parent"]["inventory_contract"]=str(INV)
m["parent"]["inventory_contract_sha256"]=sha(INV)
m["execution"]["target_root"]=r"D:\GNSS_Lband_Active_Array\runs\formal\build_only\M7A_INNER_EDGE_SETBACK_V01"
m["execution"]["artifact_name"]="R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK_BUILD_ONLY_V01.cst"
m["execution"]["runner"]="scripts/run_m7_corrective_build_only_v01.py"
m["execution"]["packet_generator"]="scripts/make_m7_corrective_build_packet_v01.py"
m["execution"]["formal_build_invocations"]=1
m["execution"]["solver_invocations"]=0
MAN.write_text(json.dumps(m,indent=2)+"\n",encoding="utf-8")

RUNNER.write_text(r'''from __future__ import print_function
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
    modified_ok=(all(v>0 and v<=0.071 for v in vals) and max(vals)-min(vals)<=1e-8)

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
      "checks":checks,"modified_parent_volume_loss_mm3":losses,
      "unexpected_changed_entities":changed_unexpected,
      "human_geometry_review_required":True,"solve_authorized":False
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# M7A INNER_EDGE_SETBACK Human Geometry Review","",
      "Automated build status: "+status,"",
      "1. Confirm all four backside LOCAL_BACK_GROUND solids received only the center-facing upstream setback.",
      "2. Confirm the window is local v=3..5 mm and stops at |u|=1.5 mm, leaving 0.55 mm inner-side ground overhang beneath the upstream signal.",
      "3. Confirm all signal copper, radiator, package lands, local-ground-top copper, vias and bias/output copper are visually unchanged.",
      "4. Confirm no clearance cut intersects the signal trace or creates an unintended galvanic break in the local return path.",
      "5. Confirm the four branches are mirror/rotation symmetric.",
      "",
      "Human PASS authorizes neither SOLVE nor M7B BUILD."
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
''',encoding="utf-8")

PKT.write_text(r'''from __future__ import print_function
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
    runner=root/"scripts"/"run_m7_corrective_build_only_v01.py"
    launcher=root/"scripts"/"cst_bundled_python_launcher_v01.py"
    if subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip():
        raise SystemExit("HOLD_M7_PROJECT_DIRTY")
    head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    c=json.loads(contract.read_text(encoding="utf-8-sig")); g=c.get("authorization",{}).get("active_grant")
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
    if failed: raise SystemExit("HOLD_M7_LIVE_BUILD_GRANT:"+",".join(failed))

    target=Path(m["execution"]["target_root"])
    artifact=target/m["execution"]["artifact_name"]; evidence=target/"evidence"
    rel=lambda p:str(p.relative_to(root)).replace("\\","/")
    cstpy=Path(a.cst_python).resolve()
    packet={
      "schema_version":"runner-task-v0.2",
      "packet_id":"GNSS-M7A-INNER-EDGE-SETBACK-BUILD-V01",
      "project":{"name":"GNSS_Lband_Active_Array","repository":"Dingo-infinity2020/GNSS_Lband_Active_Array",
                 "source_commit":c["project"]["source_commit"],"model_identity":m["stage"]},
      "stage":{"name":m["stage"],"kind":"BUILD_ONLY","control_host_alias":"NW",
               "working_directory":str(root),"stop_boundary":m["execution"]["build_stop"]},
      "transport":{"type":"local","ssh_alias":"","remote_shell":""},
      "preflight":{"fail_closed":True,"checks":[
        {"id":"git_clean","type":"git_clean","path":"."},
        {"id":"git_head","type":"git_head_equals","path":".","commit":head},
        {"id":"runner_hash","type":"file_sha256_equals","path":rel(runner),"sha256":sha(runner)},
        {"id":"launcher_hash","type":"file_sha256_equals","path":rel(launcher),"sha256":sha(launcher)},
        {"id":"manifest_hash","type":"file_sha256_equals","path":rel(vm),"sha256":sha(vm)},
        {"id":"macro_hash","type":"file_sha256_equals","path":m["execution"]["macro"],"sha256":m["execution"]["macro_sha256"]},
        {"id":"inventory_hash","type":"file_sha256_equals","path":rel(Path(m["parent"]["inventory_contract"])),"sha256":m["parent"]["inventory_contract_sha256"]},
        {"id":"stage_contract_hash","type":"file_sha256_equals","path":"execution/stage_contract.json","sha256":sha(contract)},
        {"id":"parent_hash","type":"file_sha256_equals","path":m["parent"]["path"],"sha256":m["parent"]["sha256"]},
        {"id":"target_absent","type":"path_absent","path":str(target)},
        {"id":"result_absent","type":"result_path_absent"},
        {"id":"cst_gui_absent","type":"process_absent","name":"CST DESIGN ENVIRONMENT_AMD64.exe","ignore_case":True},
        {"id":"cst_modeler_absent","type":"process_absent","name":"modeler_AMD64.exe","ignore_case":True}
      ]},
      "entrypoint":{"argv":["python",rel(launcher),rel(runner),"--variant-manifest",rel(vm),
                            "--out",str(artifact),"--evidence",str(evidence)],
                    "environment":{"CST_PYTHON_EXECUTABLE":str(cstpy)},"timeout_seconds":2400},
      "authorization":{"BUILD_AUTHORIZED":True,"SOLVE_AUTHORIZED":False,
        "grant_snapshot":{"grant_id":g["grant_id"],"kind":g["kind"],"state":g["state"],"stage":g["stage"],
          "source_commit":g["source_commit"],"entrypoint_path":rel(runner),"entrypoint_sha256":sha(runner),
          "stage_contract_path":"execution/stage_contract.json","stage_contract_sha256":sha(contract),
          "granted_at":g["granted_at"],"expires_at":g.get("expires_at"),"entrypoint_arg_index":2}},
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
    print("PASS_M7_BUILD_PACKET_GENERATED")
    return 0
if __name__=="__main__": sys.exit(main())
''',encoding="utf-8")

AUDIT.write_text(r'''from __future__ import print_function
import ast, hashlib, json, re, sys
from pathlib import Path
ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK_MANIFEST_V01.json"
RUN=ROOT/"scripts"/"run_m7_corrective_build_only_v01.py"
PKT=ROOT/"scripts"/"make_m7_corrective_build_packet_v01.py"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_FORMAL_BUILD_PREP_V01"/"STATIC_AUDIT.json"

def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()

def run_solver_calls(p):
 tree=ast.parse(p.read_text(encoding="utf-8")); n=0
 for x in ast.walk(tree):
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=="run_solver": n+=1
 return n

m=json.loads(MAN.read_text(encoding="utf-8"))
macro=ROOT/m["execution"]["macro"]; t=macro.read_text(encoding="utf-8")
inv=Path(m["parent"]["inventory_contract"]); j=json.loads(inv.read_text(encoding="utf-8"))
checks={
 "candidate_m7a":m["candidate"]=="M7A",
 "stage_exact":m["stage"]=="R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK_BUILD_ONLY",
 "manifest_auth_false":m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},
 "parent_inventory_177":j["expected_final_shape_count"]==177 and len(j["expected_final_names"])==177,
 "parent_inventory_hash":sha(inv)==m["parent"]["inventory_contract_sha256"],
 "macro_hash":sha(macro)==m["execution"]["macro_sha256"],
 "macro_four_creates":t.count(".Create")==4,
 "macro_four_subtracts":t.count("Solid.Subtract")==4,
 "macro_only_background_targets":all("BackGround:LOCAL_BACK_GROUND" in x for x in re.findall(r'Solid\.Subtract "([^"]+)"',t)),
 "macro_no_port_solver_monitor":all(x not in t for x in ("Port.","DiscretePort","Solver.","run_solver","StartSolver","ChangeSolverType","Monitor.")),
 "runner_zero_run_solver":run_solver_calls(RUN)==0,
 "packet_zero_run_solver":run_solver_calls(PKT)==0,
 "runner_177_24_contract":'"shape_count_exact_177"' in RUN.read_text(encoding="utf-8") and '"ports_exact_24"' in RUN.read_text(encoding="utf-8"),
 "runner_symmetry_gate":'"four_background_volume_losses_positive_symmetric"' in RUN.read_text(encoding="utf-8"),
 "packet_v02":'"schema_version":"runner-task-v0.2"' in PKT.read_text(encoding="utf-8"),
 "packet_fail_closed":"HOLD_M7_LIVE_BUILD_GRANT" in PKT.read_text(encoding="utf-8"),
}
status="PASS_M7A_FORMAL_BUILD_STATIC_CONTRACT" if all(checks.values()) else "HOLD_M7A_FORMAL_BUILD_STATIC_CONTRACT"
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({"status":status,"checks":checks,
 "runner_sha256":sha(RUN),"packet_generator_sha256":sha(PKT),"manifest_sha256":sha(MAN),
 "formal_build_invocations":0,"solver_invocations":0,
 "BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},indent=2)+"\n",encoding="utf-8")
print(status)
for k,v in checks.items():
 if not v: print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
''',encoding="utf-8")

print("PREPARED_M7A_FORMAL_BUILD_CHAIN")
print("RUNNER_SHA="+sha(RUNNER))
print("PKT_SHA="+sha(PKT))
print("MAN_SHA="+sha(MAN))
