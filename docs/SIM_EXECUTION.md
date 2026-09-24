# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1E0C_A_R2_READONLY_QUALIFICATION

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Original formal R1E0C-A invocation

Status:
HOLD_R1E0C_A_HARNESS_MACRO_PATH_FORMAT

Source commit:
746b34d35e6ae4ee948a6fc510bc6c072584e654

Runtime:
24.23 s

## Recovery R1E0C-A-R1 invocation

Status:
HOLD_R1E0C_A_RECOVERY_NO_SOLVER_PREDICATE

Source commit:
cde5f8827d82473750c1a6e92510ac617d3835ab

Runtime:
197.31 s

Exit code:
0

All four CSTs were generated and fresh-reopened.

Geometry/boundary/scan checks passed for every state.

Formal artifact hashes:
- C30P45 e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2
- C45P45 ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed
- C60P45 94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01
- C60P135 c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1

HOLD reason:
the harness treated Result/output.txt existence as solver execution.

Read-only inspection already shows no solver markers and no solver-generated result-tree items.

## Current read-only qualifier

scripts/qualify_r1e0c_existing_scanstate_artifacts.py

Inputs:
- work: D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_recovery01
- evidence: evidence/r1e0c_dc_nw_20260924_recovery01/

Qualifier checks:
- artifact hashes;
- build/reopen shape inventories;
- periodic boundary and scan metadata;
- persisted R1E0_scan_theta_deg/R1E0_scan_phi_deg parameters;
- message log solver markers;
- solver-generated result-tree items.

## Stop boundary

Read-only qualification only.
No rebuild.
No solver.
No R1E0C-B execution.
On PASS, close R1E0C-A and move to R1E0C-B DESIGN only.
