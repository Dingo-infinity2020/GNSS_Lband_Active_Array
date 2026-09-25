#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
fail=[]

required=[
 "docs/R1E1A4A_ACTIVE_HUB_INTERFACE_V01.md",
 "docs/R1E1A4A_GATE_R_RECEIVER_FREEZE_V01.md",
 "docs/R1E1A4A_MIXEDMODE_BUILD_ONLY_CONTRACT_DRAFT.md",
 "circuit/qpl9547/QPL9547_NOISE_REFERENCE_1P1_1P7.csv",
 "circuit/qpl9547/QPL9547_SPARAM_REFERENCE_1P15_1P65.csv",
 "circuit/qpl9547/analysis/QPL9547_SPARAM_STABILITY_SUMMARY.json",
 "circuit/qpl9547/analysis/R1E1A4A_IDEAL_ODDMODE_QPL9547_NOISE_SHADOW_SUMMARY.json",
]
for rel in required:
    if not (ROOT/rel).exists():
        fail.append("missing:"+rel)

gate=(ROOT/"docs/R1E1A4A_GATE_R_RECEIVER_FREEZE_V01.md").read_text(encoding="utf-8")
for token in ("NF_device_shadow <= 0.40 dB","IL_preLNA <= 0.05 dB",
              "NF_receiver_nominal <= 0.45 dB","Delta NF_receiver <= +0.05 dB",
              "|Sdc| <= -30 dB","|Scd| <= -30 dB"):
    if token not in gate:
        fail.append("gate_missing:"+token)

hub=(ROOT/"docs/R1E1A4A_ACTIVE_HUB_INTERFACE_V01.md").read_text(encoding="utf-8")
for token in ("11.0 x 11.0 mm","10.0 x 10.0 mm","P1A","P1B","Z_branch = Z_diff/2"):
    if token not in hub:
        fail.append("hub_missing:"+token)

contract=(ROOT/"docs/R1E1A4A_MIXEDMODE_BUILD_ONLY_CONTRACT_DRAFT.md").read_text(encoding="utf-8")
for token in ("BUILD NOT AUTHORIZED","exactly two 50-ohm single-ended discrete ports","Do not add support candidates"):
    if token not in contract:
        fail.append("contract_missing:"+token)

sparam=json.loads((ROOT/"circuit/qpl9547/analysis/QPL9547_SPARAM_STABILITY_SUMMARY.json").read_text())
if not sparam.get("unconditional_stability_2port_in_band"):
    fail.append("sparam_inband_stability_false")
if not (sparam["K_min"]>1 and sparam["mu_min"]>1 and sparam["mu_prime_min"]>1 and sparam["delta_mag_max"]<1):
    fail.append("sparam_stability_predicate")

shadow=json.loads((ROOT/"circuit/qpl9547/analysis/R1E1A4A_IDEAL_ODDMODE_QPL9547_NOISE_SHADOW_SUMMARY.json").read_text())
for state,data in shadow["states"].items():
    if data["bare_nf_db_max"]>0.40 or data["s1_nf_db_max"]>0.40:
        fail.append("illustrative_shadow_exceeds_R_NF0:"+state)

stage=json.loads((ROOT/"execution/stage_contract.json").read_text())
a=stage["authorization"]
for k in ("BUILD_AUTHORIZED","SOLVE_AUTHORIZED","production_solve_authorized"):
    if a.get(k) is not False:
        fail.append("execution_permission_open:"+k)

raw=ROOT/"circuit/qpl9547/analysis/QPL9547_FORUM_TEMP.S2P"
if raw.exists():
    fail.append("raw_external_s2p_should_not_be_committed")

if fail:
    print("HOLD_R1E1A4A_INTERFACE_GATE_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)
print("PASS_R1E1A4A_INTERFACE_GATE_AUDIT")
print("GATE_R=FROZEN_V0P1")
print("H0_P1_INTERFACE=FROZEN_FOR_BUILD_CONTRACT")
print("ILLUSTRATIVE_SHADOW_R_NF0=PASS_NONAUTHORITATIVE")
print("CST_BUILD_AUTHORIZED=NO")
print("CST_SOLVE_AUTHORIZED=NO")
