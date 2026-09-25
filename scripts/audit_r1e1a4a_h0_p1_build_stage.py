#!/usr/bin/env python3
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
macro=ROOT/"source/cst/R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_V01.mcr"
harness=ROOT/"scripts/run_r1e1a4a_h0_p1_build_only_dc.py"
contract=ROOT/"docs/R1E1A4A_MIXEDMODE_BUILD_ONLY_CONTRACT_DRAFT.md"
stage=ROOT/"execution/stage_contract.json"
fail=[]

for p in (macro,harness,contract,stage):
    if not p.exists(): fail.append("missing:"+str(p))

mt=macro.read_text(encoding="utf-8") if macro.exists() else ""
ht=harness.read_text(encoding="utf-8") if harness.exists() else ""
ct=contract.read_text(encoding="utf-8") if contract.exists() else ""
sc=json.loads(stage.read_text(encoding="utf-8")) if stage.exists() else {}

checks={
 "one_port_delete": mt.count("Port.Delete (1)")==1,
 "one_ground_brick": mt.count('With Brick')==1 and 'H0_LOCAL_GROUND' in mt,
 "two_discrete_ports": mt.count("With DiscretePort")==2,
 "two_50ohm_via_parameter": mt.count('.Impedance "r1e1a4a_p1_ref_ohm"')==2,
 "ground_half_5": 'StoreParameter "r1e1a4a_h0_ground_half", 5.0' in mt,
 "ref_50": 'StoreParameter "r1e1a4a_p1_ref_ohm", 50.0' in mt,
 "port_xy_from_terminal_r": 'StoreParameter "r1e1a4a_port_xy", "terminal_r*r1e1a4a_port_s2"' in mt,
 "no_solver_in_macro": not re.search(r'\b(Solver|FDSolver|TransientSolver|EigenmodeSolver)\.',mt),
 "no_monitor_create": 'With Monitor' not in mt,
 "no_support_tokens": all(x not in mt for x in ("FOAM_","BOND_","PEC_POST_","SupportAssembly")),
 "no_active_device_tokens": all(x not in mt for x in ("QPL9547","LNA","Transistor")),
 "harness_source_hash": 'fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e' in ht,
 "harness_getproperties": "DiscretePort.GetProperties" in ht,
 "harness_getcoordinates": "DiscretePort.GetCoordinates" in ht,
 "harness_no_run_solver": ".run_solver(" not in ht,
 "parent_evidence_guard": "snapshot_tree" in ht and "restore_snapshot" in ht,
 "contract_build_only": "BUILD-ONLY" in ct and "no solver" in ct.lower(),
}
for k,v in checks.items():
    if not v: fail.append("check_failed:"+k)

auth=sc.get("authorization",{})
if auth.get("BUILD_AUTHORIZED") is not True: fail.append("BUILD_AUTHORIZED_not_true")
if auth.get("SOLVE_AUTHORIZED") is not False: fail.append("SOLVE_AUTHORIZED_not_false")
if auth.get("production_solve_authorized") is not False: fail.append("production_solve_authorized_not_false")

if fail:
    print("HOLD_R1E1A4A_H0_P1_BUILD_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_H0_P1_BUILD_STATIC_AUDIT")
for k in sorted(checks): print(k+"=PASS")
print("BUILD_AUTHORIZED=YES")
print("SOLVE_AUTHORIZED=NO")
