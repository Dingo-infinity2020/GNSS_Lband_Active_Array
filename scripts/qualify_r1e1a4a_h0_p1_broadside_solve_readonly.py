"""Read-only qualification of the consumed R1E1A4A H0/P1 broadside solve."""
from __future__ import print_function
import argparse,json,os,sys

HERE=os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0,HERE)
from run_r1e1a4a_h0_p1_broadside_solve_dc import (
    sha, read_2port, mixed_row, write_complex_csv, parse_native,
    load_p0, compare_p0, gate_r, SPATH
)

FORMAL_STATUS="HOLD_R1E1A4A_H0_P1_BROADSIDE_POSTPROCESS_RESULT_PATH"

def run(repo,evidence,artifact):
    if not os.path.isdir(evidence): os.makedirs(evidence)
    if not os.path.isfile(artifact): raise RuntimeError("HOLD_R1E1A4A_SOLVED_ARTIFACT_MISSING")

    raw,tree=read_2port(artifact)
    rows=[mixed_row(f,v) for f,v in raw]
    csvp=os.path.join(evidence,"mixed_mode_2port_readonly.csv")
    write_complex_csv(csvp,rows)

    native=parse_native(artifact)
    numerical={
      "all_four_s_present":all(p in tree for p in SPATH.values()),
      "nonempty":len(rows)>0,
      "last_two_delta_s":native["last_two_below_0p02"],
      "desired_accuracy":native["desired_accuracy"],
      "not_maxpasses":not native["maxpasses"],
      "broadband_converged":native["broadband_converged"],
      "no_error_lines":len(native["errors"])==0,
    }
    numerical["pass"]=all(numerical.values())

    p0,p0path=load_p0(repo)
    comp=compare_p0(rows,p0)
    gr=gate_r(rows)
    canonical=("PASS_R1E1A4A_H0_P1_BROADSIDE_MIXEDMODE_READONLY_RECOVERY"
               if numerical["pass"] and gr["pass"] else
               "HOLD_R1E1A4A_H0_P1_BROADSIDE_MIXEDMODE_SCIENCE_OR_NUMERICAL")

    summary={
      "formal_status":FORMAL_STATUS,
      "formal_solve_invocation_count":1,
      "solver_rerun":False,
      "read_only_recovery":True,
      "artifact":artifact,
      "artifact_sha256":sha(artifact),
      "artifact_bytes":os.path.getsize(artifact),
      "result_paths":{"S11":SPATH[(1,1)],"S12":SPATH[(1,2)],
                      "S21":SPATH[(2,1)],"S22":SPATH[(2,2)]},
      "native":native,
      "numerical_checks":numerical,
      "p0_reference_csv":p0path,
      "comparison_vs_p0":comp,
      "gate_r_mixed_mode":gr,
      "canonical_status":canonical,
    }
    with open(os.path.join(evidence,"readonly_summary.json"),"w") as f:
        json.dump(summary,f,indent=2)

    print(canonical)
    print("FORMAL_STATUS="+FORMAL_STATUS)
    print("NUMERICAL_PASS="+str(numerical["pass"]))
    print("GATE_R_MIXED_MODE_PASS="+str(gr["pass"]))
    print(json.dumps(gr,sort_keys=True))
    print(json.dumps(comp,sort_keys=True))
    print("ARTIFACT_SHA256="+summary["artifact_sha256"])

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--artifact",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.artifact)
