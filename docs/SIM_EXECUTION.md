# SIM_EXECUTION

## Current stage
R1E1A3_SUPPORT_SENSITIVITY_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: true
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## R1E1A2 build closeout
Formal invocation: 1
Original status: HOLD_R1E1A2_SUPPORT_BUILD_ONLY_IN_SESSION_AUDIT_PERSISTENCE
Canonical status: PASS_R1E1A2_SUPPORT_BUILD_ONLY_READONLY_RECOVERY
Evidence: evidence/r1e1a2_support_build_nw_20260925_01/

## Solve order
S1_BONDED_B0 -> S1_BONDED_C60P45 -> S1_BONDED_C60P135 -> S4_PEC_B0
Each is a separate one-shot NW solve with no retry.

## Stop
Close R1E1A3 support science gate.
Do not start R1E1B pitch screen.
