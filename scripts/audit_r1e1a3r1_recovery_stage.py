#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
old=ROOT/"source/cst/R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr"
new=ROOT/"source/cst/R1E1A3R1_SUPPORT_SOLVER_CONFIG_V02.mcr"
run=ROOT/"scripts/run_r1e1a3r1_support_recovery_solve_dc.py"
plan=ROOT/"docs/R1E1A3R1_NUMERICAL_RECOVERY_PLAN.md"
fail=[]
for p in (old,new,run,plan):
    if not p.exists(): fail.append("missing:"+str(p))
ot=old.read_text(encoding="utf-8") if old.exists() else ""
nt=new.read_text(encoding="utf-8") if new.exists() else ""
rt=run.read_text(encoding="utf-8") if run.exists() else ""
if '.MaxPasses "8"' not in ot: fail.append("old_maxpasses_not_8")
if '.MaxPasses "12"' not in nt: fail.append("new_maxpasses_not_12")
def effective(text):
    return "\n".join(line.rstrip() for line in text.splitlines()
                     if line.strip() and not line.lstrip().startswith("'"))
norm_old=effective(ot).replace('.MaxPasses "8"','.MaxPasses "12"')
if norm_old!=effective(nt):
    fail.append("config_diff_not_only_maxpasses")
for token in ('Boundary','Brick','Material','Port','StoreParameter'):
    if token in nt: fail.append("forbidden_config_token:"+token)
for token in ('protected_build_evidence','snapshot_files','restore_snapshot',
              'R1E1A3R1_SUPPORT_SOLVER_CONFIG_V02.mcr','prj.modeler.run_solver()'):
    if token not in rt: fail.append("recovery_harness_missing:"+token)
for token in ('comp["max_complex_delta_s11"]<=0.05','comp["max_abs_delta_zactive_ohm"]<=10.0'):
    if token not in rt: fail.append("physical_gate_changed_or_missing:"+token)
if fail:
    print("HOLD_R1E1A3R1_STATIC_AUDIT")
    [print("- "+x) for x in fail]
    raise SystemExit(3)
print("PASS_R1E1A3R1_STATIC_AUDIT")
print("SOLE_SOLVER_CHANGE=MAXPASSES_8_TO_12")
print("EVIDENCE_PROTECTION=SNAPSHOT_RESTORE_VERIFY")
print("PHYSICAL_GATE=UNCHANGED")
