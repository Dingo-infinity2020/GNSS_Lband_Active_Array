# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

DESIGN_R1E0C_B_C60P135_SCAN_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Completed principal-plane scan solves

### C30P45
Status: PASS_R1E0C_B_C30P45_SCAN_SOLVE
Solved SHA256: 068665b01c0cdea5338662a43fd70f1675e623ef205dbf0b910f45b40526823c
Physics alert: NO

### C45P45
Status: PASS_R1E0C_B_C45P45_SCAN_SOLVE
Solved SHA256: c36861d616af18d06ad3dddba11ef50112646bc77181aeb54e7a23a1052eb7f1
Physics alert: NO

### C60P45
Status: PASS_R1E0C_B_C60P45_SCAN_SOLVE
Formal source commit: 4df0ac815b4b0c4134634a3e540ff3c48f2061e0
Solved CST: D:\GNSS_Lband_Active_Array\_r1e0c_b_c60p45_scan_solve_work\R1E0C_B_C60P45_SCAN_SMOKE_V01.cst
Solved SHA256: 58018c0ffa058c46a16fdca92948a6477ff77124960b027f0a2d071b4f368828
Runtime: 76.68 s
Physics alert: NO

## Core-scan interpretation

The 94-mm periodic array has numerically passed the principal-plane core scan sequence through theta=60 deg without the frozen severe-mismatch/scan-blindness alerts.

The active-impedance locus moves substantially with scan, so the result does not justify freezing an LNA match yet.

## Current intended next state

C60P135: theta=60 deg, phi=135 deg

Role:
orthogonal-plane sentinel at the core-scan boundary

Qualified source:
D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_recovery01\R1E0C_C60P135_SCANSTATE_BUILD_ONLY_V01.cst

SHA256:
c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1

Solver bundle remains:
- docs/R1E0C_B_SCAN_SOLVE_CONTRACT.md
- source/cst/R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr
- scripts/run_r1e0c_scan_solve_dc.py
- em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E0C_B_SCAN_SOLVE.md

## Stop

C60P135 solver is not authorized.
No pitch/material variation.
No LNA integration.
No CST251 production solve.
