#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
macro=ROOT/"source/cst/R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY_V01.mcr"
run=ROOT/"scripts/run_r1e1a4a_h2a_build_only_dc.py"
plan=ROOT/"docs/R1E1A4A_H2A_UNIVERSAL_CENTER_STRUCTURE_V01.md"
stage=ROOT/"execution/stage_contract.json"
fail=[]
for p in (macro,run,plan,stage):
    if not p.exists(): fail.append("missing:"+str(p))
mt=macro.read_text(encoding="utf-8") if macro.exists() else ""
rt=run.read_text(encoding="utf-8") if run.exists() else ""
checks={
 "parent_hash_locked":"fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e" in rt,
 "one_port_delete":mt.count("Port.Delete (1)")==1,
 "no_ports_created":"With DiscretePort" not in mt,
 "four_ground_bars":sum(mt.count('"GROUND_'+x+'"') for x in ("N","S","E","W"))==4,
 "four_pads":sum(mt.count('"PAD_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "four_pins":sum(mt.count('"PIN_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "four_lna_envelopes":sum(mt.count('"LNA_ENV_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "shield_five":sum(mt.count('"SHIELD_'+x+'"') for x in ("N","S","E","W","LID"))==5,
 "carrier_four":sum(mt.count('"CARRIER_'+x+'"') for x in ("N","S","E","W"))==4,
 "ground_outer_20":'StoreParameter "h2a_ground_outer_half", 10.0' in mt,
 "clear_window_8":'StoreParameter "h2a_clear_half", 4.0' in mt,
 "shield_outer_18":'StoreParameter "h2a_shield_outer_half", 9.0' in mt,
 "carrier_outer_30":'StoreParameter "h2a_carrier_outer_half", 15.0' in mt,
 "carrier_inner_21":'StoreParameter "h2a_carrier_inner_half", 10.5' in mt,
 "no_solver_commands":not re.search(r'\b(Solver|FDSolver|TransientSolver|EigenmodeSolver)\.',mt),
 "no_monitor":"With Monitor" not in mt,
 "no_transistor":all(x not in mt for x in ("QPL9547","Transistor","BiasNetwork","MatchingNetwork")),
 "harness_no_solver":".run_solver(" not in rt,
 "fresh_reopen_query":"execute_vba_code" in rt,
 "evidence_guard":"snapshot_tree" in rt and "restore_snapshot" in rt,
}
for k,v in checks.items():
    if not v: fail.append("check_failed:"+k)
sc=json.loads(stage.read_text(encoding="utf-8")) if stage.exists() else {}
a=sc.get("authorization",{})
if a.get("BUILD_AUTHORIZED") is not True: fail.append("BUILD_AUTHORIZED_not_true")
if a.get("SOLVE_AUTHORIZED") is not False: fail.append("SOLVE_AUTHORIZED_not_false")
if a.get("lna_integration_authorized") is not False: fail.append("lna_integration_authorized_not_false")
if fail:
    print("HOLD_R1E1A4A_H2A_BUILD_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H2A_BUILD_STATIC_AUDIT")
for k in sorted(checks): print(k+"=PASS")
print("BUILD_AUTHORIZED=YES_ONE_H2A")
print("SOLVE_AUTHORIZED=NO")
print("ACTIVE_DEVICE=NO")
