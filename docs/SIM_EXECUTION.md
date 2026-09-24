# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1E0C_A_R1_RECOVERY_BUILD_ONLY

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Original formal R1E0C-A invocation

Status:
HOLD_R1E0C_A_HARNESS_MACRO_PATH_FORMAT

Source commit:
746b34d35e6ae4ee948a6fc510bc6c072584e654

Runtime:
24.23 s

Exit code:
1

Failure:
macro filename was not formatted with the state id before file open.

No scan metadata was applied.
No solver ran.

## Recovery fix

- macro path now formats `% state`;
- all four macro files are checked before any recovery work/evidence directory is created.

## Immutable source

D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

## Recovery states

- C30P45: theta=30 deg, phi=45 deg
- C45P45: theta=45 deg, phi=45 deg
- C60P45: theta=60 deg, phi=45 deg
- C60P135: theta=60 deg, phi=135 deg

Direction:
outward

## Fresh recovery paths

Work:
D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_recovery01

Evidence:
evidence/r1e0c_dc_nw_20260924_recovery01/

## Stop boundary

Exactly one recovery build-only invocation.
Any state failure => HOLD.
No silent retry.
No R1E0C-B solver.
No pitch/material variation.
No LNA integration.
No CST251 staging.
