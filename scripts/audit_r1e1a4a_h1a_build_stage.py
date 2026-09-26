#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
macro=ROOT/"source/cst/R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY_V01.mcr"
run=ROOT/"scripts/run_r1e1a4a_h1a_build_only_dc.py"
plan=ROOT/"docs/R1E1A4A_H1_LOCAL_GROUND_REDESIGN_PLAN.md"
stage=ROOT/"execution/stage_contract.json"
fail=[]
for p in (macro,run,plan,stage):
    if not p.exists(): fail.append("missing:"+str(p))
mt=macro.read_text(encoding="utf-8") if macro.exists() else ""
rt=run.read_text(encoding="utf-8") if run.exists() else ""
checks={
 "one_port_delete":mt.count("Port.Delete (1)")==1,
 "one_ground_brick":mt.count("With Brick")==1 and "H1A_OFFSET_LOCAL_GROUND" in mt,
 "two_discrete_ports":mt.count("With DiscretePort")==2,
 "ground_half_5":'StoreParameter "r1e1a4a_h1a_ground_half", 5.0' in mt,
 "air_gap_2":'StoreParameter "r1e1a4a_h1a_air_gap", 2.0' in mt,
 "ground_top_formula":'"height_ground-r1e1a4a_h1a_air_gap"' in mt,
 "ports_50ohm":mt.count('.Impedance "r1e1a4a_h1a_p1_ref_ohm"')==2,
 "port_xy_from_terminal_r":'terminal_r*r1e1a4a_h1a_port_s2' in mt,
 "no_solver":not re.search(r'\b(Solver|FDSolver|TransientSolver|EigenmodeSolver)\.',mt),
 "no_monitor_create":"With Monitor" not in mt,
 "no_active_device":all(x not in mt for x in ("QPL9547","Transistor","LNA")),
 "no_carrier":all(x not in mt for x in ("PEEK","PTFE","FOAM","SupportAssembly")),
 "source_hash_lock":"fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e" in rt,
 "fresh_reopen":"execute_vba_code" in rt,
 "evidence_guard":"snapshot_tree" in rt and "restore_snapshot" in rt,
 "no_run_solver":".run_solver(" not in rt,
}
for k,v in checks.items():
    if not v: fail.append("check_failed:"+k)
sc=json.loads(stage.read_text(encoding="utf-8")) if stage.exists() else {}
a=sc.get("authorization",{})
if a.get("BUILD_AUTHORIZED") is not True: fail.append("BUILD_AUTHORIZED_not_true")
if a.get("SOLVE_AUTHORIZED") is not False: fail.append("SOLVE_AUTHORIZED_not_false_during_build")
if a.get("solve_authorized_after_build_pass") is not True: fail.append("conditional_solve_auth_missing")
if fail:
    print("HOLD_R1E1A4A_H1A_BUILD_STATIC_AUDIT")
    [print("- "+x) for x in fail]
    raise SystemExit(3)
print("PASS_R1E1A4A_H1A_BUILD_STATIC_AUDIT")
for k in sorted(checks): print(k+"=PASS")
print("BUILD_AUTHORIZED=YES_ONE_H1A")
print("SOLVE_AUTHORIZED=NO_UNTIL_BUILD_PASS")
print("SOLVE_AUTHORIZED_AFTER_BUILD_PASS=YES_ONE_BROADSIDE")
