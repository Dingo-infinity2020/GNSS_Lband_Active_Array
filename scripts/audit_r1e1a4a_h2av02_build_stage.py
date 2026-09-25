#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
macro=ROOT/"source/cst/R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY_V01.mcr"
run=ROOT/"scripts/run_r1e1a4a_h2av02_build_only_dc.py"
plan=ROOT/"docs/R1E1A4A_H2A_V02_SERVICE_ARCHITECTURE.md"
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
 "no_solver_commands":not re.search(r'\b(Solver|FDSolver|TransientSolver|EigenmodeSolver)\.',mt),
 "no_monitor":"With Monitor" not in mt,
 "no_transistor":all(x not in mt for x in ("QPL9547","Transistor","BiasNetwork","MatchingNetwork")),
 "no_old_carrier_solids":all(('Name "CARRIER_'+x+'"' not in mt) for x in ("N","S","E","W")),
 "four_mhf_env":sum(mt.count('"MHF_ENV_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "four_mmcx_env":sum(mt.count('"MMCX_ENV_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "four_tubes":sum(mt.count('"COPPER_TUBE_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "four_top_spacers":sum(mt.count('"TOP_SPACER_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "four_bottom_spacers":sum(mt.count('"BOTTOM_SPACER_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "four_vertical_coax":sum(mt.count('"MICROCOAX_VERT_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "four_backplane_cuts":sum(mt.count('"CUT_BACKPLANE_'+x+'"') for x in ("NE","NW","SW","SE"))==4,
 "tube_3x3":'StoreParameter "h2av02_tube_outer_half", 1.50' in mt,
 "tube_open_1p4":'StoreParameter "h2av02_tube_inner_half", 0.70' in mt,
 "microcoax_0p81":'StoreParameter "h2av02_cable_half", 0.405' in mt,
 "mhf_r_9":'StoreParameter "h2av02_mhf_r", 9.0' in mt,
 "tube_r_13p5":'StoreParameter "h2av02_tube_r", 13.50' in mt,
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
    print("HOLD_R1E1A4A_H2AV02_BUILD_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H2AV02_BUILD_STATIC_AUDIT")
for k in sorted(checks): print(k+"=PASS")
print("BUILD_AUTHORIZED=YES_ONE_H2AV02")
print("SOLVE_AUTHORIZED=NO")
print("ACTIVE_DEVICE=NO")
