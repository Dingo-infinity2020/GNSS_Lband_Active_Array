#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
macro=ROOT/"source/cst/R1E1A4A_H3B_T01_ORTHOGONAL_TRANSITION_BUILD_ONLY_V01.mcr"
freeze=ROOT/"docs/R1E1A4A_H3B_T01_TRANSITION_COUPON_FREEZE_V01.md"
stage=ROOT/"execution/stage_contract.json"
run=ROOT/"scripts/run_r1e1a4a_h3b_t01_build_only_dc.py"
fail=[]
for p in (macro,freeze,stage,run):
    if not p.exists(): fail.append("missing:"+str(p))
mt=macro.read_text(encoding="utf-8") if macro.exists() else ""
checks={
 "auto_intersection":'.SetAutoIntersectionCheckElMag "True"' in mt,
 "no_ports_created":"DiscretePort" not in mt and "WaveguidePort" not in mt,
 "no_solver_commands":not re.search(r'\\b(FDSolver|TransientSolver|EigenmodeSolver)\\.',mt),
 "standalone_two_boards":mt.count('.Name "HORIZONTAL_FR4"')==1 and mt.count('.Name "VERTICAL_FR4"')==1,
 "six_lines":sum(mt.count('.Name "'+x+'"') for x in ("H_SIG","H_GND_L","H_GND_R","V_SIG","V_GND_L","V_GND_R"))==6,
 "six_transition_pads":sum(mt.count('.Name "'+p+'_'+x+'"') for p in ("H_PAD","V_PAD") for x in ("SIG","GND_L","GND_R"))==6,
 "three_edge_caps":sum(mt.count('.Name "EDGE_CAP_'+x+'"') for x in ("SIG","GND_L","GND_R"))==3,
 "three_solder":sum(mt.count('.Name "SOLDER_'+x+'"') for x in ("SIG","GND_L","GND_R"))==3,
 "sixteen_vias":sum(mt.count('.Name "'+o+'_VIA_'+s+'_'+str(i)+'"') for o in ("H","V") for s in ("L","R") for i in range(1,5))==16,
 "sixteen_via_holes":sum(mt.count('.Name "'+o+'_VIAHOLE_'+s+'_'+str(i)+'"') for o in ("H","V") for s in ("L","R") for i in range(1,5))==16,
 "rp1_rp2_frozen":'StoreParameter "h3b_t01_rp1_y", 12' in mt and 'StoreParameter "h3b_t01_rp2_z", -12' in mt,
 "decision_band":'StoreParameter "h3b_t01_decision_lo", 1.15' in mt and 'StoreParameter "h3b_t01_decision_hi", 1.65' in mt,
 "via_barrel_radii":'StoreParameter "h3b_t01_via_outer_r", 0.2' in mt and 'StoreParameter "h3b_t01_via_inner_r", 0.15' in mt,
}
for k,v in checks.items():
    if not v: fail.append("check_failed:"+k)
sc=json.loads(stage.read_text(encoding="utf-8")) if stage.exists() else {}
a=sc.get("authorization",{})
if a.get("BUILD_AUTHORIZED") is not True: fail.append("BUILD_AUTHORIZED_not_true")
if a.get("SOLVE_AUTHORIZED") is not False: fail.append("SOLVE_AUTHORIZED_not_false")
if fail:
    print("HOLD_R1E1A4A_H3B_T01_BUILD_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H3B_T01_BUILD_STATIC_AUDIT")
for k in sorted(checks): print(k+"=PASS")
print("BUILD_AUTHORIZED=YES_ONE_H3B_T01")
print("SOLVE_AUTHORIZED=NO")
