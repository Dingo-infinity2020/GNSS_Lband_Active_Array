#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
h=ROOT/"scripts/run_r1e1a1_six_pitch_source_set_build_only_dc.py"
c=ROOT/"docs/R1E1A1_SIX_PITCH_FR4_SOURCE_SET_CONTRACT.md"
r=ROOT/"em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E1A1_SIX_PITCH_FR4_BUILD_ONLY.md"
fail=[]
for p in (h,c,r):
    if not p.exists(): fail.append("missing:"+str(p))
ht=h.read_text(encoding="utf-8") if h.exists() else ""
ct=c.read_text(encoding="utf-8") if c.exists() else ""
rt=r.read_text(encoding="utf-8") if r.exists() else ""
SHA="585929d5bf9cbf46c4a6d0ae40b42baa8e2efff673f79c1026dcff33cb014fc2"
for req in (SHA,'ENDPOINTS=[("P088",88.0),("P090",90.0),("P092",92.0),("P094",94.0),("P096",96.0),("P100",100.0)]','"pitch_count_6":len(results)==6','"artifact_hashes_unique":len(set(x["cst_sha256"] for x in results))==6',"PASS_R1E1A1_SIX_PITCH_FR4_SOURCE_SET_BUILD_ONLY"):
    if req not in ht: fail.append("harness_missing:"+req)
for forbidden in (".run_solver(", ".start_solver(", "Solver.Start", "FDSolver.Start", "Optimizer.", "ParameterSweep"):
    if forbidden in ht: fail.append("harness_forbidden:"+forbidden)
for t,name in ((ct,"contract"),(rt,"runbook")):
    if SHA not in t: fail.append(name+":source_sha_missing")
if fail:
    print("HOLD_R1E1A1_STATIC_AUDIT")
    [print("- "+x) for x in fail]
    raise SystemExit(3)
print("PASS_R1E1A1_STATIC_AUDIT")
print("PITCHES=88,90,92,94,96,100")
print("SOLVER_COMMANDS=0")
