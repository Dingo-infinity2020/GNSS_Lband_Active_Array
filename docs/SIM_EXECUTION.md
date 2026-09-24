# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

DESIGN_R1E0B_BROADSIDE_PERIODIC_SMOKE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Last completed stage

R1E0A periodic configuration qualification

Canonical status:
PASS_R1E0A_PERIODIC_CONFIG_BUILD_ONLY

Recovery mode:
read-only; no CST rerun

## Qualified source for R1E0B

D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

## R1E0B design

Contract:
docs/R1E0B_BROADSIDE_PERIODIC_SMOKE_CONTRACT.md

Config:
source/cst/R1E0B_PERIODIC_BROADSIDE_SOLVER_CONFIG_V01.mcr

Harness:
scripts/run_r1e0b_broadside_periodic_smoke_dc.py

Static audit:
PASS_R1E0B_STATIC_AUDIT

Important:
the R1E0B solver config contains no Boundary commands.

## Intended solver when separately authorized

- HF Frequency Domain
- tetrahedral second order
- adaptive HighFrequencyTet / ExpertSystem
- MaxDeltaS 0.02
- two consecutive checks
- 1.0–1.8 GHz
- existing unit-cell boundary/scan metadata retained

## Required result

Broadside active S11 and Z_active for the 94-mm infinite periodic array.

No solver action is currently permitted.
