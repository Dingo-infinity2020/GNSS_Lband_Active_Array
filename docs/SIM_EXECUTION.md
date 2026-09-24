# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1E0B_R1_READONLY_RESULT_RECOVERY

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Original formal solve

Status:
HOLD_R1E0B_RESULT_PATH_QUALIFICATION

Source commit:
10b50b0102cd50a4f21ed2d5ee07da80e9c01a63

Artifact:
D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work\R1E0B_POLA_PERIODIC_BROADSIDE_SMOKE_V01.cst

SHA256:
339021e580efa6aae6dfcfa229e4194b4dcf0bbef854398d44a0efed65aac7ad

Runtime:
99.99 s

Solver itself:
completed adaptive convergence and broadband sweep.

Formal harness failure:
periodic result-path naming mismatch.

## Actual periodic driven-port result path

1D Results\S-Parameters\S1(1),1(1)

## Recovery

Qualifier:
scripts/qualify_r1e0b_existing_periodic_result.py

Recovery mode:
read-only.

No DesignEnvironment.
No modeler.
No solver.

## Stop

Read-only qualification only.

On PASS, move to R1E0C first-scan DESIGN.
