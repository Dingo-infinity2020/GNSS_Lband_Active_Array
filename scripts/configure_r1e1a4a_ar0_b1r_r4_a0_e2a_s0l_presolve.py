from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from collections import Counter
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

import cst.interface as ci
from cst.results import ProjectFile

EXPECTED_SOURCE_SHA256="78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804"
HISTORY_LABEL="R4-A0-E2A-S0L loaded source-side presolve config V01"
S2=1.0/math.sqrt(2.0)
Z0=57.1428571428

# New semantic 6-port map after deleting raw 4/5/6/10/11/12 and renaming raw 7/8/9 -> 4/5/6.
PORT_LOCAL={
    1:(3.0,4.650,"A_E_UP","SOURCE"),
    2:(3.0,6.085,"A_P_IN","SOURCE_DEVICE_INPUT"),
    3:(3.0,7.915,"A_P_OUT_LOAD50","MATCHED_LOAD_ONLY"),
    4:(-3.0,4.650,"B_E_UP","SOURCE"),
    5:(-3.0,6.085,"B_P_IN","SOURCE_DEVICE_INPUT"),
    6:(-3.0,7.915,"B_P_OUT_LOAD50","MATCHED_LOAD_ONLY"),
}
SOURCE_PORTS=(1,2,4,5)
LOAD_ONLY_PORTS=(3,6)

REQUIRED_HISTORY_TOKENS=(
    'Port.Delete 12',
    'Port.Delete 11',
    'Port.Delete 10',
    'Port.Delete 6',
    'Port.Delete 5',
    'Port.Delete 4',
    'Port.Rename 7, 4',
    'Port.Rename 8, 5',
    'Port.Rename 9, 6',
    '.Stimulation "List", "List"',
    '.ResetExcitationList',
    '.AddToExcitationList "1", "1"',
    '.AddToExcitationList "2", "1"',
    '.AddToExcitationList "4", "1"',
    '.AddToExcitationList "5", "1"',
)

FORBIDDEN_EXCITATION_TOKENS=(
    '.AddToExcitationList "3", "1"',
    '.AddToExcitationList "6", "1"',
    '.Stimulation "All", "All"',
)

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
        raise RuntimeError("HOLD_E2A_S0L_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    srcdir=src.with_suffix(""); dstdir=dst.with_suffix("")
    if not srcdir.exists():
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_COMPANION_MISSING")
    if dstdir.exists():
        shutil.rmtree(str(dstdir),ignore_errors=True)
    shutil.copytree(str(srcdir),str(dstdir))

def inventory_vba(path):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "'+p+'" For Output As #f',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+1200",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      "  mat=Solid.GetMaterialNameForShape(nm)",
      '  Print #f, "SHAPE|" & nm & "|material=" & mat & "|volume=" & CStr(Solid.GetVolume(nm))',
      " End If",
      "Next i",
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f",
      "On Error GoTo 0"
    ])

def port_audit_vba(path):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Integer, stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",
      'Open "'+p+'" For Output As #f',
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "For i=1 To 6",
      " Err.Clear",
      " pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P|" & CStr(i) & "|PROP_OK=" & CStr(pok) & "|ERR=" & CStr(Err.Number) & "|TYPE=" & stype & "|ZREF=" & CStr(zref)',
      " Err.Clear",
      " cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "C|" & CStr(i) & "|COORD_OK=" & CStr(cok) & "|ERR=" & CStr(Err.Number) & "|P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0) & "|P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i",
      "Close #f",
      "On Error GoTo 0"
    ])

def parse_inventory(path):
    rows=[]; kv={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            _,nm,mat,vol=line.split("|",3)
            rows.append({
              "name":nm,
              "component":nm.split(":",1)[0],
              "material":mat.split("=",1)[1],
              "volume":float(vol.split("=",1)[1])
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

def expected_port_xyz(i):
    u,v,_,_=PORT_LOCAL[i]
    z=Z0-v
    p1=(S2*u,S2*u,z)
    p2=(S2*(u+1.0),S2*(u-1.0),z)
    return p1,p2

def ports_exact(data,tol=2e-8):
    if data["count"]!=6:
        return False
    for i in range(1,7):
        p=data["properties"].get(i,{})
        c=data["coordinates"].get(i,{})
        if p.get("PROP_OK") not in ("True","TRUE","1","-1"): return False
        if c.get("COORD_OK") not in ("True","TRUE","1","-1"): return False
        if p.get("TYPE")!="SParameter": return False
        if abs(float(p.get("ZREF","nan"))-50.0)>tol: return False
        e1,e2=expected_port_xyz(i)
        if any(abs(a-b)>tol for a,b in zip(xyz(c["P1"]),e1)): return False
        if any(abs(a-b)>tol for a,b in zip(xyz(c["P2"]),e2)): return False
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
    if not all(tok in history for tok in REQUIRED_HISTORY_TOKENS):
        return False
    if any(tok in history for tok in FORBIDDEN_EXCITATION_TOKENS):
        return False

    # Each source excitation appears exactly once in the S0L history block.
    for p in SOURCE_PORTS:
        tok='.AddToExcitationList "%d", "1"'%p
        if history.count(tok)!=1:
            return False
    for p in LOAD_ONLY_PORTS:
        tok='.AddToExcitationList "%d", "1"'%p
        if tok in history:
            return False
    return True

def main(source,config_macro,inventory_contract,out,evidence):
    source=Path(source); config_macro=Path(config_macro)
    inventory_contract=Path(inventory_contract); out=Path(out); evidence=Path(evidence)

    if not source.exists() or sha(source)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_SHA")
    if not source.with_suffix("").exists():
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_COMPANION")
    if not config_macro.exists() or not inventory_contract.exists():
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_FILES")
    if out.exists() or out.with_suffix("").exists():
        raise RuntimeError("HOLD_E2A_S0L_DEST_EXISTS")
    if evidence.exists():
        raise RuntimeError("HOLD_E2A_S0L_EVIDENCE_EXISTS")

    evidence.mkdir(parents=True)
    contract=json.loads(inventory_contract.read_text(encoding="utf-8"))
    expected_names=set(contract["expected_final_names"])
    expected_counts=contract["expected_final_component_counts"]

    source_sha_before=sha(source)
    copy_project(source,out)
    if sha(out)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError("HOLD_E2A_S0L_COPY_SHA")

    # Audit the copied qualified build before any solver-copy mutation.
    before_inv=evidence/"before_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inventory_vba(before_inv))):
            raise RuntimeError("HOLD_E2A_S0L_BEFORE_INVENTORY")
    finally:
        if p is not None: p.close()
        de.close()

    before_rows,before_kv=parse_inventory(before_inv)
    before_names=set(r["name"] for r in before_rows)
    before_counts=Counter(r["component"] for r in before_rows)
    source_gate={
      "source_sha_exact":source_sha_before==EXPECTED_SOURCE_SHA256,
      "shape_count_107":len(before_rows)==107,
      "exact_shape_name_set":before_names==expected_names,
      "component_counts_exact":dict(before_counts)==expected_counts,
      "raw_port_count_12":int(before_kv.get("PORT_COUNT","-1"))==12,
      "source_result_tree_empty":len(solver_result_paths(result_tree_paths(out)))==0,
    }
    (evidence/"source_gate.json").write_text(json.dumps(source_gate,indent=2)+"\n",encoding="utf-8")
    if not all(source_gate.values()):
        raise RuntimeError("HOLD_E2A_S0L_SOURCE_GATE")

    before_sig=signature(before_rows)

    # Persistent solver-copy configuration only. No solver invocation in this runner.
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        p.modeler.add_to_history(HISTORY_LABEL,macro_body(config_macro))
        p.save()
    finally:
        if p is not None: p.close()
        de.close()

    configured_sha=sha(out)

    # Fresh-reopen presolve audit.
    after_inv=evidence/"configured_inventory.txt"
    after_ports=evidence/"configured_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inventory_vba(after_inv))):
            raise RuntimeError("HOLD_E2A_S0L_AFTER_INVENTORY")
        if not p.schematic.execute_vba_code(wrap(port_audit_vba(after_ports))):
            raise RuntimeError("HOLD_E2A_S0L_PORT_AUDIT")
    finally:
        if p is not None: p.close()
        de.close()

    after_rows,after_kv=parse_inventory(after_inv)
    pdata=parse_ports(after_ports)
    hpath=out.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=hpath.read_text(encoding="utf-8",errors="replace") if hpath.exists() else ""
    after_tree=solver_result_paths(result_tree_paths(out))

    after_names=set(r["name"] for r in after_rows)
    after_counts=Counter(r["component"] for r in after_rows)
    checks={
      "source_artifact_unchanged":sha(source)==EXPECTED_SOURCE_SHA256,
      "configured_shape_count_107":len(after_rows)==107,
      "configured_exact_shape_name_set":after_names==expected_names,
      "configured_component_counts_exact":dict(after_counts)==expected_counts,
      "geometry_material_volume_signature_unchanged":signature(after_rows)==before_sig,
      "six_ports_exact":ports_exact(pdata),
      "history_persistent_and_exact_excitation_list":history_exact(htext),
      "result_tree_empty_before_solve":len(after_tree)==0,
      "configured_hash_stable_after_fresh_reopen":sha(out)==configured_sha,
    }

    status=("PASS_R4_A0_E2A_S0L_PRESOLVE_CONFIG_READY"
            if all(checks.values())
            else "HOLD_R4_A0_E2A_S0L_PRESOLVE_CONFIG")

    semantic_ports={
      str(i):{
        "name":PORT_LOCAL[i][2],
        "role":PORT_LOCAL[i][3],
        "source_excited":i in SOURCE_PORTS,
        "zref_ohm":50.0
      } for i in range(1,7)
    }

    summary={
      "status":status,
      "simulationops":"0.2.12",
      "formal_solver_invocations":0,
      "formal_build_invocations":0,
      "source_artifact_sha256":EXPECTED_SOURCE_SHA256,
      "configured_copy_sha256":sha(out),
      "config_macro":str(config_macro),
      "config_macro_sha256":sha(config_macro),
      "port_count":pdata["count"],
      "semantic_ports":semantic_ports,
      "source_excitation_set":list(SOURCE_PORTS),
      "matched_load_only_set":list(LOAD_ONLY_PORTS),
      "deleted_raw_audit_ports":[4,5,6,10,11,12],
      "required_response_terms":24,
      "source_side_terms":16,
      "output_load_pickup_terms":8,
      "checks":checks,
      "result_tree_paths_before_solve":after_tree,
      "interpretation":[
        "This artifact is a configured presolve copy only; no solver has run.",
        "Ports 3 and 6 are retained 50-ohm S-parameter ports but excluded from the FDSolver excitation list, so they act as matched passive output terminations.",
        "Auxiliary E_DN/VDD/VBIAS audit ports are deleted from the solve copy; physical copper pads remain unchanged/open.",
        "C_IN remains absent; direct final QPL9547 source impedance is not yet claimed.",
        "No fallback to six-source excitation is permitted if selected excitation cannot be proven at runtime."
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
    ap.add_argument("--out",required=True)
    ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.source_cst,a.config_macro,a.inventory_contract,a.out,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R4_A0_E2A_S0L_PRESOLVE_CONFIG_EXECUTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
