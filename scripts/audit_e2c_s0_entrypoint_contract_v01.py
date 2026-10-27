from __future__ import print_function
import argparse, ast, hashlib, json, subprocess, sys
from pathlib import Path

EXPECTED_SOURCE_SHA="cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c"
SOURCE_PORTS=(1,2,4,5,7,8,10,11)
LOAD_PORTS=(3,6,9,12)

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def solver_calls(path):
    tree=ast.parse(Path(path).read_text(encoding="utf-8"))
    parents={}
    for n in ast.walk(tree):
        for c in ast.iter_child_nodes(n):
            parents[c]=n
    calls=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="run_solver":
            loop=False; p=parents.get(n)
            while p is not None:
                if isinstance(p,(ast.For,ast.While,ast.AsyncFor)):
                    loop=True; break
                p=parents.get(p)
            calls.append({"lineno":n.lineno,"inside_loop":loop})
    return calls

def main(root,cst_python,out):
    root=Path(root).resolve(); out=Path(out).resolve()
    files={
      "presolve":root/"scripts"/"configure_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_presolve.py",
      "runner":root/"scripts"/"run_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_coexistence_solve.py",
      "qualifier":root/"scripts"/"qualify_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_readonly.py",
      "generator":root/"scripts"/"make_e2c_s0_runner_packet_v01.py",
      "macro":root/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_CONFIG_V01.mcr",
      "manifest":root/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_SENTINEL_MANIFEST_V01.json",
      "inventory":root/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_INVENTORY_V01.json",
      "watchdog":root/"scripts"/"e2c_simops_watchdog_adapter_v01.py",
    }
    missing=[k for k,p in files.items() if not p.exists()]
    if missing:
        raise RuntimeError("HOLD_E2C_S0_AUDIT_MISSING:"+",".join(missing))

    for k in ("presolve","runner","qualifier","generator","watchdog"):
        compile(files[k].read_text(encoding="utf-8"),str(files[k]),"exec")

    calls={k:solver_calls(files[k]) for k in ("presolve","runner","qualifier")}
    manifest=json.loads(files["manifest"].read_text(encoding="utf-8"))
    macro=files["macro"].read_text(encoding="utf-8")
    runner=files["runner"].read_text(encoding="utf-8")

    baselines=manifest["isolated_baselines"]
    baseline_hashes={}
    baseline_ok=True
    for pol in ("PolA","PolB"):
        p=Path(baselines[pol]["csv_path"])
        ok=p.exists() and sha(p)==baselines[pol]["csv_sha256"]
        baseline_ok=baseline_ok and ok
        baseline_hashes[pol]={"path":str(p),"expected":baselines[pol]["csv_sha256"],
                              "observed":sha(p) if p.exists() else None,"pass":ok}

    source=Path(manifest["canonical_build"]["path"])
    source_ok=source.exists() and sha(source)==EXPECTED_SOURCE_SHA and source.with_suffix("").exists()

    checks={
      "presolve_run_solver_zero":len(calls["presolve"])==0,
      "formal_runner_run_solver_exactly_one":len(calls["runner"])==1,
      "formal_runner_solver_not_in_loop":len(calls["runner"])==1 and not calls["runner"][0]["inside_loop"],
      "qualifier_run_solver_zero":len(calls["qualifier"])==0,
      "manifest_12_ports":len(manifest["raw_to_solve"])==12,
      "manifest_8_sources":tuple(manifest["solve_network"]["source_ports"])==SOURCE_PORTS,
      "manifest_4_loads":tuple(manifest["solve_network"]["load_only_ports"])==LOAD_PORTS,
      "manifest_96_traces":manifest["solve_network"]["required_complex_traces"]==96,
      "canonical_source_hash_and_companion":source_ok,
      "baseline_hashes_exact":baseline_ok,
      "macro_delete_12":macro.count("Port.Delete ")==12,
      "macro_rename_9":macro.count("Port.Rename ")==9,
      "macro_excitation_8":macro.count(".AddToExcitationList ")==8,
      "macro_has_no_solver_start":all(x not in macro for x in ("run_solver","Solver.Start","StartSolver")),
      "observability_presolve":'simops_phase("presolve_config","START","NOT_OBSERVED"' in runner,
      "observability_solver_boundary":'simops_phase("solver_run","START","OBSERVED"' in runner,
      "observability_qualification":'simops_phase("qualification","START","OBSERVED"' in runner,
      "no_automatic_retry_contract":'"automatic_retries":0' in runner and '"retry_authorized":False' in runner,
    }

    cstpy=Path(cst_python)
    help_rc=None; help_tail=""
    if cstpy.exists():
        cp=subprocess.run([str(cstpy),str(files["runner"]),"--help"],
                          cwd=str(root),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                          text=True,timeout=60)
        help_rc=cp.returncode; help_tail=cp.stdout[-4000:]
    checks["cst_runtime_runner_help"]=help_rc==0

    status="PASS_E2C_S0_ENTRYPOINT_STATIC_CONTRACT" if all(checks.values()) else "HOLD_E2C_S0_ENTRYPOINT_STATIC_CONTRACT"
    result={
      "schema_version":"gnss-e2c-s0-entrypoint-qualification-v0.1",
      "status":status,
      "mode":"READ_ONLY_STATIC_AND_RUNTIME_HELP",
      "source_files":{k:{"path":str(p),"sha256":sha(p)} for k,p in files.items()},
      "solver_call_ast":calls,
      "baseline_hashes":baseline_hashes,
      "canonical_source":{"path":str(source),"expected_sha256":EXPECTED_SOURCE_SHA,
                          "observed_sha256":sha(source) if source.exists() else None},
      "cst_python":str(cstpy),"runner_help_exit_code":help_rc,
      "runner_help_tail":help_tail,
      "checks":checks,
      "formal_build_invocations":0,"formal_solver_invocations":0,
      "production_boundary":"NOT_OBSERVED"
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(status)
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",required=True)
    ap.add_argument("--cst-python",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    sys.exit(main(a.project_root,a.cst_python,a.out))
