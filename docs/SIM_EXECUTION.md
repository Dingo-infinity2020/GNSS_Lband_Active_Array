# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

DESIGN_R1E0C_B_SCAN_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Last completed stage

R1E0C-A scan-state build-only qualification

Canonical status:
PASS_R1E0C_SCANSTATE_BUILD_ONLY

Read-only qualification:
PASS_R1E0C_SCANSTATE_BUILD_ONLY_READONLY_QUALIFICATION

## Qualified scan-state inputs

Root:
D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_recovery01

- C30P45: e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2
- C45P45: ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed
- C60P45: 94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01
- C60P135: c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1

All four are PROTECTED_IN_PLACE.

## R1E0C-B design bundle

Contract:
docs/R1E0C_B_SCAN_SOLVE_CONTRACT.md

Solver config:
source/cst/R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr

Static audit:
PASS_R1E0C_B_SCAN_SOLVER_STATIC_AUDIT

Harness:
scripts/run_r1e0c_scan_solve_dc.py

Runbook:
em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E0C_B_SCAN_SOLVE.md

## Solver-config invariants

- Boundary commands = 0
- geometry/material/port changes = 0
- YZ postprocessor = 0
- solver-start commands in config = 0

## Future solve discipline

One state per formal invocation.
Fresh work/evidence per state.
No silent retry.

Suggested order:
C30P45 -> C45P45 -> C60P45 -> C60P135

## Stop

No scan solve is currently authorized.
No pitch/material variation.
No LNA integration.
No CST251 production solve.
