# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

DESIGN_R1E1A0_PITCH_PARAMETERIZATION

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false

## Last completed array-physics gate

R1E0C scan qualification

Canonical status:
PASS_R1E0C_SCAN_QUALIFICATION

Qualified states:
- broadside reference
- C30P45
- C45P45
- C60P45
- C60P135

Frozen severe-mismatch alerts:
none triggered in any scan state

60-deg plane comparison:
- max complex Delta S11 = 0.67023
- max |Delta Z_active| = 208.98 ohm

Interpretation:
94-mm baseline is numerically viable through the required 0-60 deg gate, but active impedance is strongly scan-angle/scan-plane dependent.

LNA final input-match freeze:
NOT READY

R1E0C closeout evidence:
evidence/r1e0c_closeout_20260924/

## Current R1E1A0 design

Plan:
docs/R1E1_PITCH_MATERIAL_TRADE_PLAN.md

Contract:
docs/R1E1A0_PITCH_PARAMETERIZATION_CONTRACT.md

Runbook:
em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E1A0_PITCH_PARAMETERIZATION_BUILD_ONLY.md

Harness:
scripts/run_r1e1a0_pitch_parameterization_build_only_dc.py

Static audit:
PASS_R1E1A0_STATIC_AUDIT

Audit script:
scripts/audit_r1e1a0_pitch_parameterization.py

Clean source:
D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

Source SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

Pitch chain:
unit_cell_pitch_nominal -> ground_reference_span -> UNITCELL_GROUND_REFERENCE -> periodic bounding box

Parameter mutation path under test:
project.schematic.execute_vba_code with direct StoreParameter, followed by CST RebuildForParametricChange

Endpoint proof candidates:
- 88 mm
- 100 mm

## Stop

R1E1A0 build is not authorized.
No R1E1 solver is authorized.
No material A/B is authorized.
No LNA integration is authorized.
