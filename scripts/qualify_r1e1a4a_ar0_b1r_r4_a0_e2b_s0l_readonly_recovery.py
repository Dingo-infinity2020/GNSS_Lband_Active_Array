from __future__ import print_function
import argparse, hashlib, importlib.util, json, re, sys
from pathlib import Path

EXPECTED_SOLVED_SHA="2abafb4435a6f1dc7bfcadec029ee1c81436cf91f27fefe99ca64337820eba02"
EXPECTED_SOURCE_SHA="002eb117b0716cf2a47856b4552dd96ef4567358c7dd5827cbe766d10a633f39"
THRESHOLD=0.02

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def loadmod(path):
    spec=importlib.util.spec_from_file_location("e2b_formal_runner",str(path))
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def native_values(evidence):
    txt=""
    for n in ("native_output_txt","native_Model_log","native_log_tet"):
        p=evidence/n
        if p.exists():
            txt+="\n"+p.read_text(encoding="utf-8",errors="ignore")
    patterns=[
      r"All\s+S-Parameters\s*=\s*([0-9.+Ee-]+)",
      r"Maximum difference of S-parameters[^=]*=\s*([0-9.+Ee-]+)",
      r"DeltaS\s*=\s*([0-9.+Ee-]+)",
    ]
    for pat in patterns:
        vals=re.findall(pat,txt,re.I)
        if vals:
            return [float(v) for v in vals]
    return []

def main(solved,source,evidence,runner,outdir):
    solved=Path(solved); source=Path(source); evidence=Path(evidence); runner=Path(runner); outdir=Path(outdir)
    if outdir.exists(): raise RuntimeError("HOLD_RECOVERY_OUT_EXISTS")
    if not solved.exists() or sha(solved)!=EXPECTED_SOLVED_SHA: raise RuntimeError("HOLD_RECOVERY_SOLVED_SHA")
    if not source.exists() or sha(source)!=EXPECTED_SOURCE_SHA: raise RuntimeError("HOLD_RECOVERY_SOURCE_SHA")
    inv=json.loads((evidence/"solver_invocation.json").read_text(encoding="utf-8"))
    pre=json.loads((evidence/"presolve_summary.json").read_text(encoding="utf-8"))
    if inv.get("formal_solver_invocations")!=1 or inv.get("automatic_retries")!=0:
        raise RuntimeError("HOLD_RECOVERY_INVOCATION_AUTHORITY")

    mod=loadmod(runner)
    vals=native_values(evidence)
    if len(vals)<2: raise RuntimeError("HOLD_RECOVERY_NATIVE_DELTA_PARSE")
    native_pass=vals[-2]<=THRESHOLD and vals[-1]<=THRESHOLD

    data,runmeta=mod.read_responses(solved)
    metrics=mod.characterize(data)
    flags=mod.native_flags(evidence)

    outdir.mkdir(parents=True)
    mod.write_csv(outdir/"loaded_response_native.csv",data)

    hard={
      "formal_solver_invocations_exactly_one":inv.get("formal_solver_invocations")==1,
      "automatic_retries_zero":inv.get("automatic_retries")==0,
      "source_artifact_unchanged":sha(source)==EXPECTED_SOURCE_SHA,
      "solved_artifact_sha_exact":sha(solved)==EXPECTED_SOLVED_SHA,
      "presolve_all_pass":all(bool(v) for v in pre.values()),
      "required_24_responses_extracted":len(data)==24,
      "native_numerical_convergence":native_pass,
      "source_side_reciprocity":metrics["source_side_reciprocity"]["pass"],
      "loaded_power_closure":metrics["loaded_power_closure"]["pass"],
      "no_fatal_solver_error":not flags["fatal_error"],
      "no_mesh_corruption":not flags["mesh_corruption"],
      "no_new_solver_invocation":True
    }
    status=("PASS_R1E1A4A_AR0_B1R_R4_A0_E2B_S0L_READONLY_QUALIFICATION_RECOVERY"
            if all(hard.values()) else
            "HOLD_R1E1A4A_AR0_B1R_R4_A0_E2B_S0L_READONLY_QUALIFICATION_RECOVERY")
    review_gt20=any(v["review_gt_minus20db"] for v in metrics["sentinels"].values())
    severe_gt10=any(v["severe_gt_minus10db"] for v in metrics["sentinels"].values())
    disposition=("PASS_LOADED_SOURCE_WITH_REVIEW" if status.startswith("PASS_") and review_gt20
                 else ("PASS_LOADED_SOURCE_CLEAN_SENTINELS" if status.startswith("PASS_") else "HOLD"))
    result={
      "status":status,
      "disposition":disposition,
      "classification":"READONLY_POSTSOLVE_QUALIFICATION_RECOVERY",
      "formal_result_remains":"HOLD_R1E1A4A_AR0_B1R_R4_A0_E2B_S0L_EXECUTION",
      "formal_solver_invocations":1,
      "recovery_solver_invocations":0,
      "automatic_retries":0,
      "source_artifact_sha256":EXPECTED_SOURCE_SHA,
      "solved_artifact_sha256":EXPECTED_SOLVED_SHA,
      "native_delta_sequence_recovered":vals,
      "final_two_native_delta_s":vals[-2:],
      "threshold":THRESHOLD,
      "runmeta":runmeta,
      "native_flags":flags,
      "hard_checks":hard,
      "review_flags":{
        "any_review_gt_minus20db":review_gt20,
        "any_severe_gt_minus10db":severe_gt10,
        "large_reflection_warning":flags["large_reflection_warning"],
        "disconnected_conductor_warning":flags["disconnected_conductor_warning"]
      },
      "metrics":metrics,
      "interpretation":"Recovery is read-only. It parses the immutable native log and reads the existing CST result tree; it never invokes a solver or mutates the solved project."
    }
    (outdir/"summary.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    (outdir/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--solved-cst",required=True)
    ap.add_argument("--source-cst",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--runner",required=True)
    ap.add_argument("--outdir",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.solved_cst,a.source_cst,a.evidence,a.runner,a.outdir))
    except Exception as ex:
        print("EXCEPTION="+repr(ex))
        sys.exit(9)
