# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1E0C_A_SCANSTATE_BUILD_ONLY

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Host

NW / DESKTOP-GBTI6Q4

Mode:
BUILD_ONLY

## Immutable source

D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

## Authorized scan states

- C30P45: theta=30 deg, phi=45 deg
- C45P45: theta=45 deg, phi=45 deg
- C60P45: theta=60 deg, phi=45 deg
- C60P135: theta=60 deg, phi=135 deg

Direction:
outward

## Frozen source bundle

Plan:
docs/R1E0C_FIRST_SCAN_QUALIFICATION_PLAN.md

Generator:
scripts/generate_r1e0c_scan_state_macros.py

Static audit:
PASS_R1E0C_SCAN_MACRO_STATIC_AUDIT

Harness:
scripts/run_r1e0c_scanstate_build_only_dc.py

Runbook:
em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E0C_SCANSTATE_BUILD_ONLY.md

## Invariants

For all four states:
- boundary type unchanged;
- X/Y remain unit cell;
- Z remains expanded open;
- cell remains 94 x 94 mm;
- geometry unchanged;
- material unchanged;
- one discrete differential port remains;
- only theta/phi scan metadata change;
- no solver output.

## Formal execution paths

Work:
D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_work

Evidence:
evidence/r1e0c_dc_nw_20260924_build01/

## Stop boundary

Exactly one formal build-only invocation.
Any state failure => HOLD.
No silent retry.
No R1E0C-B solver.
No pitch/material variation.
No LNA integration.
No CST251 staging.
