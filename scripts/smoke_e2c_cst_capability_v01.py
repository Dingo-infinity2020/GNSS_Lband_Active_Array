from __future__ import print_function
import argparse, importlib.util, json, sys
from pathlib import Path

def emit(phase,state,boundary="NOT_OBSERVED",message=None):
    obj={"schema_version":"simops-project-event-v0.1","event":"PHASE",
         "phase":phase,"state":state,"production_boundary":boundary}
    if message: obj["message"]=message
    print("SIMOPS_EVENT "+json.dumps(obj,separators=(",",":")),flush=True)

def load_runner(path):
    spec=importlib.util.spec_from_file_location("e2c_runner",str(path))
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def write_result(path,obj):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")

def norm_item(x):
    return str(x).replace("/","\\").strip("\\")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runner",required=True)
    ap.add_argument("--parent-cst",required=True)
    ap.add_argument("--inventory-contract",required=True)
    ap.add_argument("--smoke-root",required=True)
    ap.add_argument("--result",required=True)
    a=ap.parse_args()
    m=load_runner(Path(a.runner))
    parent=Path(a.parent_cst); root=Path(a.smoke_root); result=Path(a.result)
    contract=json.loads(Path(a.inventory_contract).read_text(encoding="utf-8"))
    expected=set(contract["removed_parent_objects"])|set(contract["preserved_parent_objects"])
    probe_name="UnitCellGround:UNITCELL_GROUND_REFERENCE"
    if probe_name not in expected:
        raise RuntimeError("HOLD_CAPABILITY_PROBE_NAME_CONTRACT")
    state={"status":"HOLD_E2C_CST_CAPABILITY_SMOKE","parent_sha256":m.PARENT_SHA,"checks":{},"tree_items":[],"probe_name":probe_name}
    write_result(result,state)
    if len(expected)!=45 or m.sha(parent)!=m.PARENT_SHA or root.exists():
        raise RuntimeError("HOLD_CAPABILITY_PREFLIGHT")
    root.mkdir(parents=True); copy=root/"parent_capability.cst"
    emit("capability_copy","START"); m.copy_project(parent,copy); emit("capability_copy","PASS")

    emit("capability_open","START")
    de=m.ci.DesignEnvironment(m.ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(copy))
        emit("capability_open","PASS")
        attrs=[x for x in dir(prj.modeler) if "tree" in x.lower() or "solid" in x.lower() or "component" in x.lower()]
        state["modeler_attrs"]=attrs
        write_result(result,state)

        emit("capability_tree","START")
        if hasattr(prj.modeler,"get_tree_items"):
            items=[norm_item(x) for x in prj.modeler.get_tree_items()]
            state["tree_items"]=items
            actual=set()
            for item in items:
                parts=[p for p in item.split("\\") if p]
                if len(parts)>=3 and parts[0]=="Components":
                    comp="/".join(parts[1:-1]); shape=parts[-1]
                    actual.add(comp+":"+shape)
            state["checks"]["tree_api_available"]=True
            state["checks"]["expected_names_in_tree"]=expected.issubset(actual)
            state["checks"]["tree_shape_count_exact"]=len(actual)==45
            state["actual_shape_names"]=sorted(actual)
            emit("capability_tree","PASS",message="tree API available")
        else:
            state["checks"]["tree_api_available"]=False
            emit("capability_tree","PASS",message="tree API unavailable in CST 2022; continue targeted VBA probe")
        write_result(result,state)

        emit("capability_targeted_vba","START")
        probe=root/"targeted_probe.txt"
        p=str(probe).replace("\\","/")
        body="\n".join([
          "On Error Resume Next","Dim f As Integer, v As Double, mat As String","f=FreeFile",
          'Open "'+p+'" For Output As #f',
          'Err.Clear',
          'v=Solid.GetVolume("'+probe_name+'")',
          'Print #f, "VOLUME_ERR=" & CStr(Err.Number)',
          'Print #f, "VOLUME=" & CStr(v)',
          'Err.Clear',
          'mat=Solid.GetMaterialNameForShape("'+probe_name+'")',
          'Print #f, "MATERIAL_ERR=" & CStr(Err.Number)',
          'Print #f, "MATERIAL=" & mat',
          "Close #f","On Error GoTo 0"])
        ok=bool(prj.schematic.execute_vba_code(m.wrap(body)))
        state["checks"]["targeted_vba_execute"]=ok
        state["targeted_vba_text"]=probe.read_text(encoding="utf-8",errors="replace") if probe.exists() else ""
        state["checks"]["targeted_vba_volume_ok"]="VOLUME_ERR=0" in state["targeted_vba_text"]
        state["checks"]["targeted_vba_material_ok"]="MATERIAL_ERR=0" in state["targeted_vba_text"]
        write_result(result,state)
        if not ok or not state["checks"]["targeted_vba_volume_ok"] or not state["checks"]["targeted_vba_material_ok"]:
            emit("capability_targeted_vba","HOLD",message="single-solid VBA probe failed")
            raise RuntimeError("HOLD_CAPABILITY_TARGETED_VBA")
        emit("capability_targeted_vba","PASS")
    finally:
        if prj is not None: prj.close()
        de.close()

    emit("capability_result_tree","START")
    tree=m.solver_tree(copy)
    state["checks"]["result_tree_empty"]=len(tree)==0
    if not state["checks"]["result_tree_empty"]:
        emit("capability_result_tree","HOLD")
        raise RuntimeError("HOLD_CAPABILITY_RESULT_TREE")
    emit("capability_result_tree","PASS")
    state["status"]="PASS_E2C_CST_CAPABILITY_SMOKE"
    write_result(result,state)
    m.cleanup_project(copy)
    try: root.rmdir()
    except Exception: pass
    emit("capability_complete","PASS")
    return 0

if __name__=="__main__":
    try: sys.exit(main())
    except Exception as ex:
        print("CAPABILITY_EXCEPTION="+repr(ex),file=sys.stderr,flush=True)
        sys.exit(9)
