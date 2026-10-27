"""Standalone CST-results extraction; no simulator application or solver launch."""
from __future__ import print_function
import argparse
import base64
import csv
import json
import math
import shutil
import sys
from pathlib import Path
from m7c_direct_sample_contract_v01 import (FREQUENCIES,SOURCES,sha,exact_index,
    native_frequencies,native_deltas,require_direct_config,classify)

LIBS = r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"


def dump(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,allow_nan=False)+"\n",encoding="utf-8")


def main(solved, manifest, evidence):
    solved,evidence = Path(solved),Path(evidence)
    evidence.mkdir(parents=True,exist_ok=True)
    m = json.loads(Path(manifest).read_text(encoding="utf-8"))
    before = sha(solved)
    result = solved.with_suffix("")/"Result"
    for name in ("output.txt","Model.log","log.tet","fd.fdp","fd_rfm.fdp"):
        source = result/name
        if source.exists():
            payload = source.read_bytes()
            (evidence/("native_"+name+".base64.txt")).write_text(base64.b64encode(payload).decode("ascii")+"\n",encoding="utf-8")
            if name in ("output.txt","Model.log","log.tet"):
                (evidence/("native_"+name+".txt")).write_text(payload.decode("utf-8",errors="replace"),encoding="utf-8")
    text = (evidence/"native_output.txt.txt").read_text(encoding="utf-8")
    history = (solved.with_suffix("")/"Model/3D/Model.mod").read_text(encoding="utf-8",errors="replace")
    # Full history has parent settings. Audit only the exact persistent config block.
    marker = "R4-A0-E2C-S0 M7C direct-sample presolve config V01"
    at = history.find(marker)
    if at < 0:
        raise RuntimeError("HOLD_M7C_DIRECT_HISTORY_MARKER")
    require_direct_config(history[at:])
    if LIBS not in sys.path:
        sys.path.insert(0,LIBS)
    from cst.results import ProjectFile
    p3 = ProjectFile(str(solved),allow_interactive=False).get_3d()
    tree = p3.get_tree_items()
    paths = [r"1D Results\S-Parameters\S%d,%d"%(i,j) for j in SOURCES for i in range(1,13)]
    runids = {p:list(p3.get_run_ids(p,False)) for p in paths}
    common = set.intersection(*(set(v) for v in runids.values()))
    if not common:
        raise RuntimeError("HOLD_M7C_DIRECT_NO_COMMON_RUN")
    rid = max(common)
    data,f = {},None
    for j in SOURCES:
        for i in range(1,13):
            path = r"1D Results\S-Parameters\S%d,%d"%(i,j)
            values = [(float(x),complex(y)) for x,y in p3.get_result_item(path,rid).get_data()]
            xx = [x for x,y in values]
            if f is None:
                f = xx
            if xx != f or not all(math.isfinite(y.real) and math.isfinite(y.imag) for x,y in values):
                raise RuntimeError("HOLD_M7C_DIRECT_NONFINITE_OR_GRID")
            data[(i,j)] = [y for x,y in values]
    direct_idx = [exact_index(f,x) for x in FREQUENCIES]
    residuals = {}
    for j in SOURCES:
        path = r"1D Results\Convergence\Equation System Solver\Relative Residual\[%d]"%j
        ids = list(p3.get_run_ids(path,False))
        if rid not in ids:
            raise RuntimeError("HOLD_M7C_DIRECT_RESIDUAL_RUN_MISSING")
        residuals[str(j)] = [[float(x),float(complex(y).real)] for x,y in p3.get_result_item(path,rid).get_data()]
    # CST's native residual plot may store logarithmic (negative) ordinates.
    # Preserve its ordinate unchanged; it is not a linear error bound.
    residual_complete = all(all(any(abs(x-target)<=1e-9 and math.isfinite(y)
                                   for x,y in rows) for target in FREQUENCIES) for rows in residuals.values())
    delta = native_deltas(text)
    native_f = native_frequencies(text)
    native_complete = all(any(abs(x-y)<=1e-9 for y in native_f) for x in FREQUENCIES)
    max_recip = max(abs(data[(i,j)][k]-data[(j,i)][k]) for i in SOURCES for j in SOURCES for k in direct_idx)
    max_power = max(sum(abs(data[(i,j)][k])**2 for i in range(1,13)) for j in SOURCES for k in direct_idx)
    lower = text.lower()
    checks = {"required_96_responses":len(data)==96,
              "exact_15_direct_samples":len(direct_idx)==15 and len(f)==16 and all(any(abs(x-y)<=1e-9 for y in FREQUENCIES+(1.8,)) for x in f),
              "native_logs_confirm_direct_frequencies":native_complete,
              "native_final_two_delta_s_lte_0p02":len(delta)>=2 and all(x<=.02 for x in delta[-2:]),
              "source_side_reciprocity":max_recip<=.02,
              "loaded_power_upper_bound":max_power<=1.02,
              "native_residual_records_complete":residual_complete,
              "no_fatal_solver_error":not any(s in lower for s in ("fatal error","solver failed","aborted due to")),
              "no_mesh_corruption":not any(s in lower for s in ("corrupt mesh","mesh near the lumped element")),
              "solved_artifact_unchanged_during_read":sha(solved)==before}
    fieldnames=["f_GHz"]+["S%d_%d_%s"%(i,j,part) for j in SOURCES for i in range(1,13) for part in ("real","imag")]
    with (evidence/"direct_response_native.csv").open("w",newline="",encoding="utf-8") as stream:
        writer=csv.writer(stream);writer.writerow(fieldnames)
        for k in direct_idx:
            writer.writerow([f[k]]+[v for j in SOURCES for i in range(1,13) for v in (data[(i,j)][k].real,data[(i,j)][k].imag)])
    from evaluate_m7c_modal_restoration_readonly_v01 import read96
    ref=m["direct_sample_diagnostic"]["comparison_csv"]
    if sha(ref["path"]) != ref["sha256"]:
        raise RuntimeError("HOLD_M7C_DIRECT_REFERENCE_HASH")
    old_f,old=read96(Path(ref["path"]))
    outcome=classify(f,data,old_f,old,all(checks.values()))
    summary={"status":outcome["status"],"hard_checks":checks,"diagnostic":outcome,
             "solved_sha256_before":before,"solved_sha256_after":sha(solved),
             "selected_run_id":rid,"run_ids":runids,"native_frequencies_ghz":native_f,
             "output_frequencies_ghz":f,"native_delta_sequence":delta,"relative_residuals":residuals,
             "residual_ordinate_semantics":"native plotted ordinate retained unconverted; not an EM error bound",
             "source_reciprocity_max_abs":max_recip,"loaded_power_max":max_power,
             "native_warnings":{"thin_pec_edges":"infinitely thin pec wires" in lower,
                                "partial_excitation_yz":"no calculation of yz matrices" in lower},
             "new_build":False,"new_solve":False,"solver_launches":0}
    dump(evidence/"qualification_summary.json",summary)
    dump(evidence/"diagnostic_evaluation.json",outcome)
    (evidence/"FINAL_STATUS.txt").write_text(outcome["status"]+"\n",encoding="utf-8")
    return 0 if all(checks.values()) else 4


if __name__ == "__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solved-cst",required=True);ap.add_argument("--manifest",required=True);ap.add_argument("--evidence",required=True)
    a=ap.parse_args();sys.exit(main(a.solved_cst,a.manifest,a.evidence))
