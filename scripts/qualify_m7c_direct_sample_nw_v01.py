"""NW nonproduction qualification. Never launches a CST application/solver."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from m7c_direct_sample_contract_v01 import artifact_checks,storage_check,QUALIFIED,sha

ROOT=Path(__file__).resolve().parents[1]
CST_PYTHON=Path(r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python\python.exe")
CST_LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
SHIM=Path(r"D:\quest_naoc_tarminal\SimulationOps\runner\nw\simops.cmd")


def main(evidence):
    evidence=Path(evidence)
    evidence.mkdir(parents=True,exist_ok=False)
    m=json.loads((ROOT/"execution/M7C_DIRECT_SAMPLE_SOLVE_MANIFEST_V01.json").read_text())
    commands=[]
    def run(label,args,expected=0):
        p=subprocess.run([str(x) for x in args],cwd=str(ROOT),capture_output=True,timeout=180)
        (evidence/(label+".stdout.txt")).write_bytes(p.stdout)
        (evidence/(label+".stderr.txt")).write_bytes(p.stderr)
        commands.append({"label":label,"argv":[str(x) for x in args],"returncode":p.returncode,"expected":expected,"pass":p.returncode==expected})
        return p
    run("control_audit",[sys.executable,ROOT/"scripts/audit_m7c_direct_sample_v01.py","--evidence",evidence/"control"])
    run("control_tests",[sys.executable,ROOT/"scripts/test_m7c_direct_sample_v01.py"])
    run("cst_runtime_audit",[CST_PYTHON,ROOT/"scripts/audit_m7c_direct_sample_v01.py","--evidence",evidence/"cst_runtime"])
    run("cst_runtime_tests",[CST_PYTHON,ROOT/"scripts/test_m7c_direct_sample_v01.py"])
    blocked=run("ungranted_entrypoint",[CST_PYTHON,ROOT/m["execution"]["runner"],"--manifest",ROOT/"execution/M7C_DIRECT_SAMPLE_SOLVE_MANIFEST_V01.json","--out",evidence/"must_not_exist.cst","--evidence",evidence/"must_not_exist_evidence"],expected=9)
    checks=artifact_checks(m,ROOT)
    checks["ungranted_entrypoint_failed_before_cst_import"]=b"HOLD_M7C_DIRECT_NO_LIVE_SOLVE_GRANT" in blocked.stderr and not (evidence/"must_not_exist.cst").exists() and not (evidence/"must_not_exist_evidence").exists()
    storage=storage_check(m["storage_policy"],m["execution"]["target_root"])
    checks["storage_reservations"]=storage["status"]=="PASS_M7C_STORAGE_PREFLIGHT"
    checks["fresh_production_path"]=not Path(m["execution"]["target_root"]).exists()
    ref=m["direct_sample_diagnostic"]["comparison_csv"]
    checks["old_M7C_response_hash"]=sha(ref["path"])==ref["sha256"]
    help_path=Path(r"D:\Program Files (x86)\CST Studio Suite 2022\Online Help\mergedProjects\VBA_3D\special_vbasolver\special_vbasolver_fdsolver_object.htm")
    text=help_path.read_text(errors="replace")
    checks["installed_help_supports_direct_samples"]=all(s in text for s in ("Discrete samples only","ResetSampleIntervals","AddSampleInterval"))
    run("native_contract_check",["cmd.exe","/c",SHIM,"contract-check","--contract",ROOT/"execution/stage_contract.json"])
    checks["all_commands_expected"]=all(c["pass"] for c in commands)
    result={"status":QUALIFIED if all(checks.values()) else "HOLD_M7C_DIRECT_HOST_QUALIFICATION",
            "checks":checks,"commands":commands,"storage":storage,
            "source_commit":subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"],text=True).strip(),
            "source_dirty":bool(subprocess.check_output(["git","-C",str(ROOT),"status","--porcelain"],text=True).strip()),
            "entrypoint_sha256":sha(ROOT/m["execution"]["runner"]),"installed_help_sha256":sha(help_path),
            "simulator_applications_launched":0,"solver_invocations":0,"next_boundary":"Fresh one-shot grant under the explicit delegated stage authority only after this qualification PASS."}
    checks["source_checkout_clean"]=not result["source_dirty"]
    if not all(checks.values()):result["status"]="HOLD_M7C_DIRECT_HOST_QUALIFICATION"
    (evidence/"RECEIPT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"source_commit":result["source_commit"],"evidence":str(evidence),"failed":[k for k,v in checks.items() if not v]},indent=2))
    return 0 if all(checks.values()) else 4


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--evidence",required=True)
    sys.exit(main(p.parse_args().evidence))
