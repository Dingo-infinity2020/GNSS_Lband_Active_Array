# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1E0A_R1_READONLY_AUDIT_RECOVERY

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Original formal R1E0A invocation

Status:
HOLD_R1E0A_PERIODIC_CONFIG_AUDIT

Source commit:
814fbffb850d7cc35541ce61213c97c436bd6a2c

Artifact:
D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

Runtime:
48.46 s

Solver:
not run

## HOLD reason

Only the original harness Boolean parser failed:
SCAN_VALID=-1 was not accepted as True.

All boundary, geometry, pitch, scan-angle and no-solver checks passed.

## Recovery

Read-only qualifier:
scripts/qualify_r1e0a_existing_evidence.py

No CST invocation is authorized.

The recovery may only inspect:
- existing artifact hash/size;
- existing build/reopen inventories;
- existing periodic metadata;
- absence of solver output.

## Stop

No rebuild.
No solver.
No R1E0B execution.

On PASS, move to R1E0B DESIGN only.
