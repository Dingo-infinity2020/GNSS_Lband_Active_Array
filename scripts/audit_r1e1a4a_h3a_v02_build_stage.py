#!/usr/bin/env python3
import json,re,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
macro=ROOT/"source/cst/R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY_V02.mcr"
gen=ROOT/"scripts/generate_r1e1a4a_h3a_build_macro.py"
freeze=ROOT/"docs/R1E1A4A_H3A_ORTHOGONAL_STALK_ARCHITECTURE_FREEZE_V01.md"
manifest=ROOT/"execution/h3a_architecture_manifest_v01.json"
stage=ROOT/"execution/stage_contract.json"
fail=[]
for p in (macro,gen,freeze,manifest,stage):
    if not p.exists(): fail.append("missing:"+str(p))
mt=macro.read_text(encoding="utf-8") if macro.exists() else ""
m=json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}
checks={
 "parent_hash_frozen":m.get("parent",{}).get("sha256")=="fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e",
 "stalk_xy":m.get("stalks",{}).get("orientation")==["X","Y"],
 "stalk_t_1":m.get("stalks",{}).get("thickness_mm")==1.0,
 "mortise_clearance":m["top_tenons"]["radiator_slot_width_mm"]>m["stalks"]["thickness_mm"],
 "mortise_in_copper_corridor":m["top_tenons"]["radiator_slot_width_mm"] < 2.571428571426 and min(abs(x) for x in m["top_tenons"]["centers_mm"])>8.57142857142,
 "shield_in_cavity":m["electronics_cavity"]["shield_envelope_max_mm"][0] < m["electronics_cavity"]["plan_clear_span_mm"],
 "mech_rf_separated":min(abs(abs(x)-abs(y)) for x in m["top_tenons"]["centers_mm"] for y in m["rf_transition"]["centers_mm"])>=2.0,
 "auto_intersection_check":'.SetAutoIntersectionCheckElMag "True"' in mt,
 "one_port_delete":mt.count("Port.Delete (1)")==1,
 "no_port_create":"With DiscretePort" not in mt,
 "no_solver_commands":not re.search(r'\b(Solver|FDSolver|TransientSolver|EigenmodeSolver)\.',mt),
 "no_active_device":all(x not in mt for x in ("QPL9547","Transistor","SPICE","Touchstone")),
 "four_fr4_bridges":sum(mt.count('.Name "FR4_BRIDGE_'+a+'_'+s+'"') for a in ("X","Y") for s in ("N","P"))==4,
 "four_bridge_unions":sum(mt.count('Solid.Add "Substrate:FR4_BOARD", "H3A_RadiatorBridge:FR4_BRIDGE_'+a+'_'+s+'"') for a in ("X","Y") for s in ("N","P"))==4,
 "bridge_len_5p5":'StoreParameter "h3a_v02_bridge_len", 5.5' in mt,
 "bridge_width_matches_inner_slot":'StoreParameter "h3a_v02_bridge_width", 2.57142857143' in mt,
 "top_copper_not_bridged":not any("FR4_BRIDGE" in ln and "TopCopper" in ln for ln in mt.splitlines()),
 "four_rad_mortises":sum(mt.count('"CUT_RAD_'+a+'_'+s+'"') for a in ("X","Y") for s in ("N","P"))==4,
 "four_bp_mortises":sum(mt.count('"CUT_BP_'+a+'_'+s+'"') for a in ("X","Y") for s in ("N","P"))==4,
 "two_stalk_bodies":mt.count('"X_STALK_BODY"')==1 and mt.count('"Y_STALK_BODY"')==1,
 "four_top_tenons":sum(mt.count(f'"{a}_TOP_TENON_{s}"') for a in ("X","Y") for s in ("N","P"))==4,
 "four_bottom_tenons":sum(mt.count(f'"{a}_BOTTOM_TENON_{s}"') for a in ("X","Y") for s in ("N","P"))==4,
 "four_lna_env":sum(mt.count(f'"LNA_ENV_{x}"') for x in ("NE","NW","SW","SE"))==4,
 "shield_nine":sum(mt.count(f'"SHIELD_{x}"') for x in ("N_L","N_R","S_L","S_R","E_B","E_T","W_B","W_T","LID"))==9,
 "service_four":sum(mt.count(f'"{a}_SERVICE_ENV_{s}"') for a in ("X","Y") for s in ("N","P"))==4,
 "intersection_gate_required":m.get("intersection_gate",{}).get("required") is True,
}
for k,v in checks.items():
    if not v: fail.append("check_failed:"+k)
sc=json.loads(stage.read_text(encoding="utf-8")) if stage.exists() else {}
a=sc.get("authorization",{})
if a.get("BUILD_AUTHORIZED") is not True: fail.append("BUILD_AUTHORIZED_not_true")
if a.get("SOLVE_AUTHORIZED") is not False: fail.append("SOLVE_AUTHORIZED_not_false")
if fail:
    print("HOLD_R1E1A4A_H3A_V02_BUILD_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H3A_V02_BUILD_STATIC_AUDIT")
for k in sorted(checks): print(k+"=PASS")
print("BUILD_AUTHORIZED=YES_ONE_H3A")
print("SOLVE_AUTHORIZED=NO")
