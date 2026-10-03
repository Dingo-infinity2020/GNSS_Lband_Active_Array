from __future__ import print_function
import argparse, hashlib, json, re, sys
from pathlib import Path

EXPECTED_SOLVED_SHA="811a31eabcd193bcf5f9cbecdf05f8aab1b1ab945bad4bda51a94d21d57b04b3"
THRESHOLD=0.02

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def main(solved,evidence,outdir):
    solved=Path(solved); evidence=Path(evidence); outdir=Path(outdir)
    if not solved.exists() or sha(solved)!=EXPECTED_SOLVED_SHA:
        raise RuntimeError("HOLD_RECOVERY_SOLVED_SHA")
    if outdir.exists():
        raise RuntimeError("HOLD_RECOVERY_OUTDIR_EXISTS")
    outdir.mkdir(parents=True)

    formal=json.loads((evidence/"summary.json").read_text(encoding="utf-8"))
    native=(evidence/"native_output_txt").read_text(encoding="utf-8",errors="ignore")

    vals=[float(x) for x in re.findall(r"All\s+S-Parameters\s*=\s*([0-9.+\-Ee]+)",native,re.I)]
    if len(vals)<2:
        raise RuntimeError("HOLD_RECOVERY_NATIVE_DELTA_PARSE")

    final_two=vals[-2:]
    parser_pass=(final_two[0]<=THRESHOLD and final_two[1]<=THRESHOLD)

    invariant_hard={k:v for k,v in formal["hard_checks"].items() if k!="native_numerical_convergence"}
    invariant_pass=all(bool(v) for v in invariant_hard.values())

    checks={
      "formal_solver_invocations_exactly_one":formal.get("formal_solver_invocations")==1,
      "automatic_retries_zero":formal.get("automatic_retries")==0,
      "solved_artifact_sha_exact":sha(solved)==EXPECTED_SOLVED_SHA,
      "formal_native_parser_was_empty":formal.get("native_delta_sequence")==[],
      "other_frozen_hard_checks_all_pass":invariant_pass,
      "native_all_s_parameters_values_found":len(vals)>=2,
      "final_two_native_delta_s_lte_0p02":parser_pass,
      "no_new_solver_invocation":True
    }

    status=("PASS_R4_A0_E2A_S0L_READONLY_QUALIFICATION_RECOVERY"
            if all(checks.values())
            else "HOLD_R4_A0_E2A_S0L_READONLY_QUALIFICATION_RECOVERY")

    review=formal.get("review_flags",{})
    disposition=("PASS_LOADED_SOURCE_WITH_REVIEW"
                 if status.startswith("PASS_") and review.get("any_review_gt_minus20db",False)
                 else ("PASS_LOADED_SOURCE_CLEAN_SENTINELS" if status.startswith("PASS_") else "HOLD"))

    result={
      "status":status,
      "disposition":disposition,
      "classification":"READONLY_QUALIFICATION_PARSER_RECOVERY",
      "formal_solve_result_remains":"HOLD_R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_QUALIFICATION",
      "formal_solver_invocations":1,
      "recovery_solver_invocations":0,
      "automatic_retries":0,
      "solved_artifact_sha256":EXPECTED_SOLVED_SHA,
      "native_delta_sequence_recovered":vals,
      "final_two_native_delta_s":final_two,
      "threshold":THRESHOLD,
      "checks":checks,
      "carried_forward_hard_checks":invariant_hard,
      "review_flags":review,
      "metrics":{
        "source_side_reciprocity":formal["metrics"]["source_side_reciprocity"],
        "loaded_power_closure":formal["metrics"]["loaded_power_closure"],
        "sentinels":formal["metrics"]["sentinels"],
        "gnss_reference_samples":formal["metrics"]["gnss_reference_samples"]
      },
      "interpretation":"Scientific convergence criterion is unchanged. Recovery only recognizes CST 2022.5 native 'All S-Parameters = value' log syntax on the immutable solved artifact. No CST solve/build/configuration is executed."
    }
    (outdir/"summary.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    (outdir/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--solved-cst",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--outdir",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.solved_cst,a.evidence,a.outdir))
    except Exception as ex:
        print("EXCEPTION="+repr(ex))
        sys.exit(9)
