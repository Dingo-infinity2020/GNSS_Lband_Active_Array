# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1E0B_BROADSIDE_PERIODIC_SMOKE_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: false

## Host

NW / DESKTOP-GBTI6Q4

This is a lightweight smoke solve, not a CST251 production run.

## Immutable source

D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

## Solver config

source/cst/R1E0B_PERIODIC_BROADSIDE_SOLVER_CONFIG_V01.mcr

Static audit:
PASS_R1E0B_STATIC_AUDIT

Important:
Boundary commands = 0.

## Numerical formulation

HF Frequency Domain
tetrahedral second order
curvature order 3
General purpose
HighFrequencyTet / ExpertSystem adaptive
MinPasses 3
MaxPasses 8
MaxDeltaS 0.02
two Delta-S checks
1.0–1.8 GHz

## Fresh execution paths

Work:
D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work

Evidence:
evidence/r1e0b_dc_nw_20260924_smoke01/

## Primary output

Broadside periodic active differential impedance:

Z_active = 100*(1+S11)/(1-S11)

## Stop

Exactly one formal invocation.
No silent retry.
No scan sweep.
No pitch/material variation.
No LNA.
No CST251 migration.
