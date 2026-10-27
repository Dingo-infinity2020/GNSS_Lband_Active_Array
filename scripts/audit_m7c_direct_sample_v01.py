"""Static/nonproduction qualification; does not import CST."""
from __future__ import print_function
import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path
from m7c_direct_sample_contract_v01 import FREQUENCIES,require_direct_config,sha

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"execution/M7C_DIRECT_SAMPLE_SOLVE_MANIFEST_V01.json"


def main(evidence):
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    checks={}
    require_direct_config((ROOT/m["execution"]["config_macro"]).read_text(encoding="utf-8"))
    checks["direct_config_exact_15_plus_adaptation"]=True
    for n,h in m["recovery"]["dependency_sha256"].items():
        checks["hash:"+n]=sha(ROOT/n)==h
    runner=ROOT/m["execution"]["runner"]
    parsed=ast.parse(runner.read_text(encoding="utf-8"))
    calls=[n for n in ast.walk(parsed) if isinstance(n,ast.Call)]
    checks["single_run_solver_call"]=sum(isinstance(n.func,ast.Attribute) and n.func.attr=="run_solver" for n in calls)==1
    checks["two_runtime_storage_grant_guards"]=sum(isinstance(n.func,ast.Name) and n.func.id=="require_ready" for n in calls)==2
    checks["no_module_level_simulator_import"]=not any(isinstance(n,(ast.Import,ast.ImportFrom)) and 'cst' in ast.dump(n).lower() for n in parsed.body)
    for path in (m["execution"]["runner"],"scripts/qualify_m7c_direct_sample_readonly_v01.py","scripts/m7c_direct_sample_contract_v01.py"):
        compile((ROOT/path).read_text(encoding="utf-8"),path,"exec")
    checks["runtime_compile"]=True
    fixture=(ROOT/"evidence/M7C_OFFLINE_REVIEW_20261027_V01/M7C_native_output.txt").read_text(encoding="utf-8")
    from m7c_direct_sample_contract_v01 import native_deltas,native_frequencies
    checks["native_parser_positive_fixture"]=len(native_frequencies(fixture))==10 and abs(native_deltas(fixture)[-1]-.0149349)<1e-12
    c=json.loads((ROOT/"execution/stage_contract.json").read_text(encoding="utf-8-sig"))
    checks["closed_permissions_during_qualification"]=c["authorization"]["BUILD_AUTHORIZED"] is False and c["authorization"]["SOLVE_AUTHORIZED"] is False and c["authorization"]["active_grant"] is None
    checks["frequency_freeze"]=tuple(m["direct_sample_diagnostic"]["frequencies_ghz"])==FREQUENCIES
    help_result=subprocess.call([sys.executable,str(runner),"--help"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    checks["help_without_cst_import"]=help_result==0
    result={"status":"PASS_M7C_DIRECT_STATIC_AND_RUNTIME_QUALIFICATION" if all(checks.values()) else "HOLD_M7C_DIRECT_QUALIFICATION",
            "checks":checks,"python":sys.version,"executable":sys.executable,
            "entrypoint_sha256":sha(runner),"manifest_sha256":sha(MANIFEST),
            "source_commit":subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"]).decode().strip(),
            "simulator_applications_launched":0,"solver_invocations":0}
    evidence=Path(evidence);evidence.mkdir(parents=True,exist_ok=True)
    (evidence/"qualification.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(result["status"])
    return 0 if all(checks.values()) else 4


if __name__=="__main__":
    a=argparse.ArgumentParser(description=__doc__);a.add_argument("--evidence",required=True)
    sys.exit(main(a.parse_args().evidence))
