#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
fail=[]
contract=json.loads((ROOT/"execution/stage_contract.json").read_text(encoding="utf-8"))
auth=contract["authorization"]
for k in ("BUILD_AUTHORIZED","SOLVE_AUTHORIZED","production_solve_authorized",
          "material_ab_authorized","lna_integration_authorized","cst251_authorized"):
    if auth.get(k) is not False:
        fail.append("authorization_not_false:"+k)
for rel in (
    "docs/R1E1A4_SYSTEM_CO_DESIGN_REVIEW_20260925.md",
    "docs/R1E1A4A_RECEIVER_SHADOW_PLAN.md",
    "docs/R1E1A4A_REFERENCE_PLANE_AND_COSIM_SPEC.md",
    "docs/R1E1A4A_ACTIVE_HUB_INTERFACE_V01.md",
    "docs/R1E1A4A_GATE_R_RECEIVER_FREEZE_V01.md",
    "circuit/qpl9547/QPL9547_NOISE_REFERENCE_1P1_1P7.csv",
    "circuit/qpl9547/QPL9547_SPARAM_REFERENCE_1P15_1P65.csv",
    "circuit/qpl9547/r1e1a4a_ideal_oddmode_shadow.py",
    "circuit/qpl9547/analysis/R1E1A4A_IDEAL_ODDMODE_QPL9547_NOISE_SHADOW_SUMMARY.json",
):
    if not (ROOT/rel).exists():
        fail.append("missing:"+rel)
plan=(ROOT/"docs/R1E1A4A_REFERENCE_PLANE_AND_COSIM_SPEC.md").read_text(encoding="utf-8")
for token in ("P1A","P1B","mixed-mode","active QPL9547 device itself remains outside CST"):
    if token not in plan:
        fail.append("reference_plane_spec_missing:"+token)
if fail:
    print("HOLD_R1E1A4A_DESIGN_STATIC_AUDIT")
    [print("- "+x) for x in fail]
    raise SystemExit(3)
print("PASS_R1E1A4A_DESIGN_STATIC_AUDIT")
print("CST_AUTHORIZATION=NONE")
print("GATE_T=UNCHANGED")
print("GATE_R=FROZEN_V0P1")
print("H0_P1_INTERFACE=FROZEN")
print("DIFFERENTIAL_TO_BRANCH_MAPPING=NOT_YET_QUALIFIED")
