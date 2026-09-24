# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

DESIGN_R1E0C_A_SCANSTATE_BUILD_ONLY

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Last completed stage

R1E0B broadside periodic active-impedance smoke

Canonical status:
PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE

Formal solver invocation:
1

Read-only recovery:
PASS

Solver rerun:
none

## Broadside reference

Solved CST:
D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work\R1E0B_POLA_PERIODIC_BROADSIDE_SMOKE_V01.cst

SHA256:
339021e580efa6aae6dfcfa229e4194b4dcf0bbef854398d44a0efed65aac7ad

Compact active result:
evidence/r1e0b_dc_nw_20260924_smoke01/active_s11_and_zactive.csv

## Clean source for R1E0C scan-state builds

D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

## R1E0C-A design

States:
- 30/45
- 45/45
- 60/45
- 60/135

Generator:
scripts/generate_r1e0c_scan_state_macros.py

Static audit:
PASS_R1E0C_SCAN_MACRO_STATIC_AUDIT

Harness:
scripts/run_r1e0c_scanstate_build_only_dc.py

No build is currently authorized.

## Later R1E0C-B

Scan solves will be separately authorized one-shot cases.

No solver action is currently permitted.
