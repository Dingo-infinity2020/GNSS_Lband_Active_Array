# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1E0C_B_C30P45_SCAN_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: false

## Host

NW / DESKTOP-GBTI6Q4

Mode:
ONE_SHOT_SCAN_SOLVE

## Immutable source

D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_recovery01\R1E0C_C30P45_SCANSTATE_BUILD_ONLY_V01.cst

SHA256:
e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2

Scan state:
theta=30 deg, phi=45 deg, outward

## Solver bundle

Contract:
docs/R1E0C_B_SCAN_SOLVE_CONTRACT.md

Config:
source/cst/R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr

Static audit:
PASS_R1E0C_B_SCAN_SOLVER_STATIC_AUDIT

Harness:
scripts/run_r1e0c_scan_solve_dc.py

## Fresh paths

Work:
D:\GNSS_Lband_Active_Array\_r1e0c_b_c30p45_scan_solve_work

Evidence:
evidence/r1e0c_b_c30p45_dc_nw_20260924_solve01/

## Numerical formulation

HF Frequency Domain
tetrahedral second order
curvature order 3
General purpose
HighFrequencyTet / ExpertSystem
MinPasses 3
MaxPasses 8
MaxDeltaS 0.02
two Delta-S checks
1.0-1.8 GHz

## Stop boundary

Exactly one formal C30P45 solve invocation.
No silent retry.
C45P45/C60P45/C60P135 remain unauthorized.
No pitch/material/LNA/CST251 work.
