#!/usr/bin/env python3
from pathlib import Path
import hashlib

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA="585929d5bf9cbf46c4a6d0ae40b42baa8e2efff673f79c1026dcff33cb014fc2"
files={
 "harness":ROOT/"scripts/run_r1e1a0r2_pitch_endpoint_proof_build_only_dc.py",
 "contract":ROOT/"docs/R1E1A0R2_ENDPOINT_PROOF_CONTRACT.md",
 "runbook":ROOT/"em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E1A0R2_ENDPOINT_PROOF_BUILD_ONLY.md",
}
fail=[]
texts={}
for k,p in files.items():
    if not p.exists(): fail.append('missing:'+str(p)); continue
    texts[k]=p.read_text(encoding='utf-8')

h=texts.get('harness','')
for req in (SOURCE_SHA,'ENDPOINTS=[("P088",88.0),("P100",100.0)]','RebuildForParametricChange','no_pitch_history_warning','no_solver_result_items'):
    if req not in h: fail.append('harness_missing:'+req)
for forbidden in ('.run_solver(','.start_solver(','Solver.Start','FDSolver.Start','Optimizer.','ParameterSweep'):
    if forbidden in h: fail.append('harness_forbidden:'+forbidden)
for k in ('contract','runbook'):
    if SOURCE_SHA not in texts.get(k,''): fail.append(k+':source_sha_missing')
if fail:
    print('HOLD_R1E1A0R2_STATIC_AUDIT')
    [print('- '+x) for x in fail]
    raise SystemExit(3)
print('PASS_R1E1A0R2_STATIC_AUDIT')
print('SOURCE_SHA='+SOURCE_SHA)
print('ENDPOINTS=88,100')
print('SOLVER_COMMANDS=0')
