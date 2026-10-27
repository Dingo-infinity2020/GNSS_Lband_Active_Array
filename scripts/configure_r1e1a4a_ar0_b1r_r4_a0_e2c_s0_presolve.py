from __future__ import print_function
import argparse, hashlib, json, shutil, sys, traceback
from collections import Counter
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

import cst.interface as ci
from cst.results import ProjectFile

EXPECTED_SOURCE_SHA256="cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c"
HISTORY_LABEL="R4-A0-E2C-S0 dual-pol coexistence presolve config V01"
SOURCE_PORTS=(1,2,4,5,7,8,10,11)
LOAD_ONLY_PORTS=(3,6,9,12)
DELETED_RAW_PORTS=(24,23,22,18,17,16,12,11,10,6,5,4)
RENAME_PAIRS=((7,4),(8,5),(9,6),(13,7),(14,8),(15,9),(19,10),(20,11),(21,12))

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def wrap(body):
    return "Sub Main()\n"+body+"\nEnd Sub"

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,line in enumerate(lines):
        if line.strip()=="Sub Main()": s=i
        elif line.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("HOLD_E2C_S0_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    srcdir=src.with_suffix(""); dstdir=dst.with_suffix("")
    if not srcdir.exists():
        raise RuntimeError("HOLD_E2C_S0_SOURCE_COMPANION_MISSING")
    if dstdir.exists():
        shutil.rmtree(str(dstdir),ignore_errors=True)
    shutil.copytree(str(srcdir),str(dstdir))

def meta_vba(path):
    p=str(path).replace("\\","/")
    return "\n".join([
      "Dim f As Integer","f=FreeFile",
      'Open "'+p+'" For Output As #f',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f"
    ])

def named_inventory_vba(path,names):
    p=str(path).replace("\\","/")
    q=lambda s:s.replace('"','""')
    lines=["On Error Resume Next","Dim f As Integer, nm As String, mat As String, vol As Double, em As Long, ev As Long",
           "f=FreeFile",'Open "'+p+'" For Append As #f']
    for name in names:
        lines += [
          'nm="'+q(name)+'"',
          "Err.Clear","mat=Solid.GetMaterialNameForShape(nm)","em=Err.Number",
          "Err.Clear","vol=Solid.GetVolume(nm)","ev=Err.Number",
          'Print #f, "SHAPE|" & nm & "|MAT_ERR=" & CStr(em) & "|VOL_ERR=" & CStr(ev) & "|material=" & mat & "|volume=" & CStr(vol)'
        ]
    lines += ["Close #f","On Error GoTo 0"]
    return "\n".join(lines)

def run_inventory(prj,path,names,batch_size=16):
    if not prj.schematic.execute_vba_code(wrap(meta_vba(path))):
        raise RuntimeError("HOLD_E2C_S0_INVENTORY_META")
    for start in range(0,len(names),batch_size):
        if not prj.schematic.execute_vba_code(wrap(named_inventory_vba(path,names[start:start+batch_size]))):
            raise RuntimeError("HOLD_E2C_S0_INVENTORY_BATCH_%d"%start)

def port_audit_vba(path,count=12):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Integer, stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",'Open "'+p+'" For Output As #f',
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "For i=1 To %d"%count,
      " Err.Clear",
      " pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P|" & CStr(i) & "|PROP_OK=" & CStr(pok) & "|ERR=" & CStr(Err.Number) & "|TYPE=" & stype & "|ZREF=" & CStr(zref)',
      " Err.Clear",
      " cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "C|" & CStr(i) & "|COORD_OK=" & CStr(cok) & "|ERR=" & CStr(Err.Number) & "|P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0) & "|P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i","Close #f","On Error GoTo 0"
    ])
def parse_inventory(path):
    rows=[]; kv={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            parts=line.split("|")
            d={"name":parts[1]}
            for item in parts[2:]:
                k,v=item.split("=",1); d[k]=v
            rows.append({
              "name":d["name"],"component":d["name"].split(":",1)[0],
              "material":d["material"],"volume":float(d["volume"]),
              "mat_err":int(d["MAT_ERR"]),"vol_err":int(d["VOL_ERR"])
            })
        elif "=" in line:
            k,v=line.split("=",1); kv[k]=v
    return rows,kv

def parse_ports(path):
    out={"count":None,"properties":{},"coordinates":{}}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("PORT_COUNT="):
            out["count"]=int(line.split("=",1)[1])
        elif line.startswith("P|"):
            parts=line.split("|"); idx=int(parts[1]); d={}
            for x in parts[2:]:
                k,v=x.split("=",1); d[k]=v
            out["properties"][idx]=d
        elif line.startswith("C|"):
            parts=line.split("|"); idx=int(parts[1]); d={}
            for x in parts[2:]:
                k,v=x.split("=",1); d[k]=v
            out["coordinates"][idx]=d
    return out

def xyz(s):
    return tuple(float(x) for x in s.split(","))

def ports_exact(data,manifest,tol=2e-8):
    if data["count"]!=12:
        return False
    by_solve={int(x["solve"]):x for x in manifest["raw_to_solve"]}
    for i in range(1,13):
        p=data["properties"].get(i,{})
        c=data["coordinates"].get(i,{})
        e=by_solve.get(i)
        if e is None: return False
        if p.get("PROP_OK") not in ("True","TRUE","1","-1"): return False
        if c.get("COORD_OK") not in ("True","TRUE","1","-1"): return False
        if p.get("TYPE")!="SParameter": return False
        if abs(float(p.get("ZREF","nan"))-50.0)>tol: return False
        if any(abs(a-b)>tol for a,b in zip(xyz(c["P1"]),e["p1"])): return False
        if any(abs(a-b)>tol for a,b in zip(xyz(c["P2"]),e["p2"])): return False
    return True

def signature(rows):
    return {r["name"]:(r["material"],round(r["volume"],12)) for r in rows}

def result_tree_paths(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return p3.get_tree_items()
    except Exception as ex:
        return ["RESULT_API_ERROR:"+repr(ex)]

def solver_result_paths(items):
    return [x for x in items if (
      "S-Parameters" in x or "Convergence" in x or
      "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def history_exact(history):
    if HISTORY_LABEL not in history:
        return False
    for n in DELETED_RAW_PORTS:
        if "Port.Delete %d"%n not in history: return False
    for a,b in RENAME_PAIRS:
        if "Port.Rename %d, %d"%(a,b) not in history: return False
    if '.Stimulation "List", "List"' not in history: return False
    if '.ResetExcitationList' not in history: return False
    for p in SOURCE_PORTS:
        if history.count('.AddToExcitationList "%d", "1"'%p)!=1: return False
    for p in LOAD_ONLY_PORTS:
        if '.AddToExcitationList "%d", "1"'%p in history: return False
    if '.Stimulation "All", "All"' in history: return False
    if 'Solver.FrequencyRange "1.0", "1.8"' not in history: return False
    return True
def main(source,config_macro,inventory_contract,sentinel_manifest,out,evidence):
    source=Path(source); config_macro=Path(config_macro)
    inventory_contract=Path(inventory_contract); sentinel_manifest=Path(sentinel_manifest)
    out=Path(out); evidence=Path(evidence)

    manifest=json.loads(sentinel_manifest.read_text(encoding="utf-8"))
    contract=json.loads(inventory_contract.read_text(encoding="utf-8"))
    expected_names=list(contract["expected_final_names"])
    expected_name_set=set(expected_names)
    expected_counts=contract["expected_final_component_counts"]

    if not source.exists() or sha(source)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E2C_S0_SOURCE_SHA")
    if not source.with_suffix("").exists():
        raise RuntimeError("HOLD_E2C_S0_SOURCE_COMPANION")
    if manifest["canonical_build"]["sha256"]!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E2C_S0_MANIFEST_SOURCE_SHA")
    if not config_macro.exists() or not inventory_contract.exists():
        raise RuntimeError("HOLD_E2C_S0_SOURCE_FILES")
    if out.exists() or out.with_suffix("").exists():
        raise RuntimeError("HOLD_E2C_S0_DEST_EXISTS")
    if evidence.exists():
        raise RuntimeError("HOLD_E2C_S0_EVIDENCE_EXISTS")

    evidence.mkdir(parents=True)
    source_sha_before=sha(source)
    copy_project(source,out)
    if sha(out)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E2C_S0_COPY_SHA")

    before_inv=evidence/"before_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        run_inventory(p,before_inv,expected_names)
    finally:
        if p is not None: p.close()
        de.close()

    before_rows,before_kv=parse_inventory(before_inv)
    before_counts=Counter(r["component"] for r in before_rows)
    source_gate={
      "source_sha_exact":source_sha_before==EXPECTED_SOURCE_SHA256,
      "shape_count_177":int(before_kv.get("SHAPE_COUNT","-1"))==177,
      "all_177_expected_names_queried":len(before_rows)==177 and set(r["name"] for r in before_rows)==expected_name_set,
      "all_named_queries_success":all(r["mat_err"]==0 and r["vol_err"]==0 for r in before_rows),
      "component_counts_exact":dict(before_counts)==expected_counts,
      "raw_port_count_24":int(before_kv.get("PORT_COUNT","-1"))==24,
      "source_result_tree_empty":len(solver_result_paths(result_tree_paths(out)))==0
    }
    (evidence/"source_gate.json").write_text(json.dumps(source_gate,indent=2)+"\n",encoding="utf-8")
    if not all(source_gate.values()):
        raise RuntimeError("HOLD_E2C_S0_SOURCE_GATE")

    before_sig=signature(before_rows)

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        p.modeler.add_to_history(HISTORY_LABEL,macro_body(config_macro))
        p.save()
    finally:
        if p is not None: p.close()
        de.close()

    configured_sha=sha(out)

    after_inv=evidence/"configured_inventory.txt"
    after_ports=evidence/"configured_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        run_inventory(p,after_inv,expected_names)
        if not p.schematic.execute_vba_code(wrap(port_audit_vba(after_ports,12))):
            raise RuntimeError("HOLD_E2C_S0_PORT_AUDIT")
    finally:
        if p is not None: p.close()
        de.close()

    after_rows,after_kv=parse_inventory(after_inv)
    pdata=parse_ports(after_ports)
    hpath=out.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=hpath.read_text(encoding="utf-8",errors="replace") if hpath.exists() else ""
    after_tree=solver_result_paths(result_tree_paths(out))

    checks={
      "source_artifact_unchanged":sha(source)==EXPECTED_SOURCE_SHA256,
      "configured_shape_count_177":int(after_kv.get("SHAPE_COUNT","-1"))==177,
      "configured_all_expected_names":len(after_rows)==177 and set(r["name"] for r in after_rows)==expected_name_set,
      "configured_named_queries_success":all(r["mat_err"]==0 and r["vol_err"]==0 for r in after_rows),
      "configured_component_counts_exact":dict(Counter(r["component"] for r in after_rows))==expected_counts,
      "geometry_material_volume_signature_unchanged":signature(after_rows)==before_sig,
      "twelve_ports_exact":ports_exact(pdata,manifest),
      "history_persistent_and_exact_excitation_list":history_exact(htext),
      "result_tree_empty_before_solve":len(after_tree)==0,
      "configured_hash_stable_after_fresh_reopen":sha(out)==configured_sha
    }

    status=("PASS_E2C_S0_PRESOLVE_CONFIG_READY" if all(checks.values())
            else "HOLD_E2C_S0_PRESOLVE_CONFIG")
    semantic_ports={str(x["solve"]):{
        "name":x["name"],"role":x["role"],
        "source_excited":int(x["solve"]) in SOURCE_PORTS,"zref_ohm":50.0
      } for x in manifest["raw_to_solve"]}

    summary={
      "status":status,
      "simulationops":"0.2.25",
      "formal_solver_invocations":0,
      "formal_build_invocations":0,
      "source_artifact_sha256":EXPECTED_SOURCE_SHA256,
      "configured_copy_sha256":sha(out),
      "config_macro":str(config_macro),
      "config_macro_sha256":sha(config_macro),
      "sentinel_manifest_sha256":sha(sentinel_manifest),
      "port_count":pdata["count"],
      "semantic_ports":semantic_ports,
      "source_excitation_set":list(SOURCE_PORTS),
      "matched_load_only_set":list(LOAD_ONLY_PORTS),
      "deleted_raw_audit_ports":list(DELETED_RAW_PORTS),
      "required_response_terms":96,
      "source_side_terms":64,
      "output_load_pickup_terms":32,
      "checks":checks,
      "result_tree_paths_before_solve":after_tree,
      "interpretation":[
        "Configured presolve copy only; no solver has run.",
        "P_OUT ports are retained as 50-ohm passive matched loads and excluded from selected excitation.",
        "E_DN/VDD/VBIAS ports are deleted only from the solve copy; physical copper remains open.",
        "C_IN remains absent; final QPL9547 source impedance is not directly claimed.",
        "No fallback to twelve-source excitation is permitted."
      ]
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status)
    print("CONFIGURED_SHA256="+sha(out))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-cst",required=True)
    ap.add_argument("--config-macro",required=True)
    ap.add_argument("--inventory-contract",required=True)
    ap.add_argument("--sentinel-manifest",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.source_cst,a.config_macro,a.inventory_contract,a.sentinel_manifest,a.out,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_E2C_S0_PRESOLVE_CONFIG_EXECUTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
