from __future__ import print_function
import argparse, hashlib, importlib.util, json, shutil, sys
from collections import Counter
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci

PASS_BUILD_SHA="a0e4bda5c64ea712564db76441721ca6dc147c97c061360a16a7d21f272f787a"
EXPECTED_CURRENT_SHA="aee6bc30085c002b6063de80f110096f6b62911bf897007d133b309e5a962b36"

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def load_v03_runner(path):
    spec=importlib.util.spec_from_file_location("v03audit",str(path))
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main(source,outdir,v03runner):
    source=Path(source); outdir=Path(outdir); v03runner=Path(v03runner)
    if outdir.exists():
        raise RuntimeError("HOLD_SOURCE_DRIFT_AUDIT_DIR_EXISTS")
    if not source.exists() or not source.with_suffix("").exists():
        raise RuntimeError("HOLD_SOURCE_PROJECT_MISSING")
    before=sha(source)
    if before!=EXPECTED_CURRENT_SHA:
        raise RuntimeError("HOLD_SOURCE_CHANGED_AGAIN:"+before)
    mod=load_v03_runner(v03runner)
    outdir.mkdir(parents=True)
    tmp=outdir/"source_drift_copy.cst"
    mod.copy_project(source,tmp)

    shapes=outdir/"inventory.txt"
    ports=outdir/"ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New)
    de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(tmp))
        ok=bool(p.schematic.execute_vba_code(mod.wrap(mod.inventory_vba(shapes,ports))))
    finally:
        if p is not None: p.close()
        de.close()
    if not ok:
        raise RuntimeError("HOLD_SOURCE_DRIFT_AUDIT_VBA")

    rows,_=mod.parse_shapes(shapes)
    pdata=mod.parse_ports(ports)
    names=set(x["name"] for x in rows)
    counts=Counter(x["component"] for x in rows)
    material_ok=all(
      (x["component"]=="E1_Substrate" and x["material"]=="FR4_COST_BASELINE") or
      (x["component"]!="E1_Substrate" and x["material"]=="E1_COPPER")
      for x in rows)

    hist=source.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=hist.read_text(encoding="utf-8",errors="replace") if hist.exists() else ""
    history_ok=("R4-A0-E1 persistent V03 build" in htext and
                all(('.PortNumber "%d"'%i) in htext for i in range(1,7)) and
                "DiscretePort" in htext and "FR4_COUPON" in htext)

    tree=mod.result_tree(tmp)
    after=sha(source)
    checks={
      "source_hash_stable_during_audit":before==after,
      "shape_count_36":len(rows)==36,
      "exact_shape_name_set":names==mod.EXPECTED_NAMES,
      "component_counts_exact":dict(counts)==mod.EXPECTED_COMPONENT_COUNTS,
      "materials_exact":material_ok,
      "ports_exact_6_with_properties_coordinates":mod.ports_ok(pdata),
      "history_persistent":history_ok,
      "result_tree_empty":len(tree)==0,
    }
    status=("PASS_R4_A0_E1_V03_POST_HUMAN_SOURCE_IDENTITY"
            if all(checks.values())
            else "HOLD_R4_A0_E1_V03_POST_HUMAN_SOURCE_IDENTITY")
    result={
      "status":status,
      "classification":"BYTE_HASH_DRIFT_PROVENANCE_AUDIT",
      "formal_solver_invocations":0,
      "build_pass_sha256":PASS_BUILD_SHA,
      "post_human_current_sha256":before,
      "source_hash_changed_since_build_pass":before!=PASS_BUILD_SHA,
      "checks":checks,
      "shape_count":len(rows),
      "component_counts":dict(counts),
      "port_count":pdata.get("count"),
      "interpretation":(
        "Scientific identity checks match the V03 build contract; the .cst container hash changed after human review. "
        "If PASS, re-baselining the post-human artifact hash is provenance-only and does not authorize geometry changes."
      )
    }
    (outdir/"summary.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    (outdir/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True)
    ap.add_argument("--outdir",required=True)
    ap.add_argument("--v03-runner",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.source,a.outdir,a.v03_runner))
    except Exception as ex:
        Path(a.outdir).mkdir(parents=True,exist_ok=True)
        Path(a.outdir,"EXCEPTION.txt").write_text(repr(ex)+"\n",encoding="utf-8")
        Path(a.outdir,"FINAL_STATUS.txt").write_text("HOLD_R4_A0_E1_V03_POST_HUMAN_SOURCE_IDENTITY_EXECUTION\n",encoding="utf-8")
        raise
