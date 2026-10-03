from __future__ import print_function
import argparse, importlib.util, json, shutil, sys
from collections import Counter
from pathlib import Path

def emit(phase,state,boundary="NOT_OBSERVED",message=None):
    obj={"schema_version":"simops-project-event-v0.1","event":"PHASE",
         "phase":phase,"state":state,"production_boundary":boundary}
    if message: obj["message"]=message
    print("SIMOPS_EVENT "+json.dumps(obj,separators=(",",":")),flush=True)

def load_runner(path):
    spec=importlib.util.spec_from_file_location("e2c_runner",str(path))
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

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
    parent_names=sorted(set(contract["removed_parent_objects"])|set(contract["preserved_parent_objects"]))
    if len(parent_names)!=45: raise RuntimeError("HOLD_SMOKE_PARENT_NAME_CONTRACT")
    if root.exists(): raise RuntimeError("HOLD_SMOKE_ROOT_EXISTS")
    if m.sha(parent)!=m.PARENT_SHA: raise RuntimeError("HOLD_SMOKE_PARENT_SHA")
    root.mkdir(parents=True)
    copy=root/"parent_smoke.cst"
    emit("smoke_copy","START")
    m.copy_project(parent,copy)
    emit("smoke_copy","PASS")

    inv=root/"parent_inventory.txt"
    emit("smoke_parent_inventory","START")
    de=m.ci.DesignEnvironment(m.ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(copy))
        ok=bool(m.run_named_inventory(prj,inv,parent_names,phase="smoke_parent_inventory",boundary="NOT_OBSERVED"))
        if not ok: raise RuntimeError("HOLD_SMOKE_PARENT_INVENTORY")
    finally:
        if prj is not None: prj.close()
        de.close()
    rows,kv=m.parse_inventory(inv)
    checks={
      "shape_count_45":len(rows)==45,
      "component_counts_exact":dict(Counter(x["component"] for x in rows))==m.PARENT_COMPONENT_COUNTS,
      "port_count_zero":int(kv.get("PORT_COUNT","-1"))==0
    }
    if not all(checks.values()):
        emit("smoke_parent_inventory","HOLD",message="inventory gates failed")
        raise RuntimeError("HOLD_SMOKE_PARENT_GATE")
    emit("smoke_parent_inventory","PASS")

    emit("smoke_result_tree","START")
    tree=m.solver_tree(copy)
    checks["result_tree_empty"]=len(tree)==0
    if not checks["result_tree_empty"]:
        emit("smoke_result_tree","HOLD",message="unexpected result tree")
        raise RuntimeError("HOLD_SMOKE_RESULT_TREE")
    emit("smoke_result_tree","PASS")

    result.parent.mkdir(parents=True,exist_ok=True)
    result.write_text(json.dumps({"status":"PASS_E2C_PARENT_SIMULATOR_SMOKE",
      "parent_sha256":m.PARENT_SHA,"checks":checks},indent=2)+"\n",encoding="utf-8")
    m.cleanup_project(copy)
    try: root.rmdir()
    except Exception: pass
    emit("smoke_complete","PASS")
    return 0

if __name__=="__main__":
    try: sys.exit(main())
    except Exception as ex:
        print("SMOKE_EXCEPTION="+repr(ex),file=sys.stderr,flush=True)
        sys.exit(9)
