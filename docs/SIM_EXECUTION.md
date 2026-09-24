# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

DESIGN_R1E0C_B_C60P45_SCAN_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Completed scan solves

### C30P45
Status: PASS_R1E0C_B_C30P45_SCAN_SOLVE
Solved SHA256: 068665b01c0cdea5338662a43fd70f1675e623ef205dbf0b910f45b40526823c
Physics alert: NO

### C45P45
Status: PASS_R1E0C_B_C45P45_SCAN_SOLVE
Formal source commit: 8b45ac4aad13d61cf8cb9494fb232f0eca22db41
Solved CST: D:\GNSS_Lband_Active_Array\_r1e0c_b_c45p45_scan_solve_work\R1E0C_B_C45P45_SCAN_SMOKE_V01.cst
Solved SHA256: c36861d616af18d06ad3dddba11ef50112646bc77181aeb54e7a23a1052eb7f1
Runtime: 114.18 s
Physics alert: NO

## Current intended next state

C60P45: theta=60 deg, phi=45 deg

Qualified source:
D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_recovery01\R1E0C_C60P45_SCANSTATE_BUILD_ONLY_V01.cst

SHA256:
94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01

Solver bundle remains:
- docs/R1E0C_B_SCAN_SOLVE_CONTRACT.md
- source/cst/R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr
- scripts/run_r1e0c_scan_solve_dc.py
- em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E0C_B_SCAN_SOLVE.md

## Stop

C60P45 solver is not authorized.
C60P135 is not authorized.
No pitch/material/LNA/CST251 work.
