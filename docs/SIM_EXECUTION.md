# SIM_EXECUTION

## Current stage
R1E1A4A_RECEIVER_SHADOW_INTERFACE_FREEZE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Last closed EM gate
Canonical status:
HOLD_R1E1A3_SUPPORT_SCIENCE_GATE_S1_C60P135_DELTA_Z

The S1 four-post bonded foam assembly:
- B0: Gate T PASS;
- C60P45: Gate T PASS;
- C60P135: numerical PASS but Gate T FAIL, max |Delta Z_active| = 15.09084 ohm.

S4 metal sentinel was NOT started after HOLD.

## Current design/circuit task
Primary plan:
docs/R1E1A4A_RECEIVER_SHADOW_PLAN.md

System review:
docs/R1E1A4_SYSTEM_CO_DESIGN_REVIEW_20260925.md

Required:
- freeze antenna differential reference plane P0;
- freeze per-LNA input planes P1A/P1B and local-ground/common-mode assumptions;
- validate QPL9547 G0 S/noise-parameter reference;
- compute receiver-shadow metrics for existing bare/S1 states where mapping is valid;
- freeze receiver/system Gate R before any new mechanical candidate result;
- freeze manufacturable M0/M1/M2 mechanical envelopes.

## Stop boundary
DESIGN / CIRCUIT ANALYSIS ONLY.
No CST build or solve.
No S4 sentinel.
No R1E1B pitch screen.
No material A/B.
No physical LNA transistor/package integration in CST.

## Completed non-CST design analysis

QPL9547 noise-reference conversion audit: PASS.
Ideal odd-mode Zdiff/2 receiver-shadow diagnostic: PASS as an ASSUMPTION_DIAGNOSTIC_ONLY artifact.
Gate R remains NOT FROZEN.
Differential-to-per-LNA mapping remains NOT FROZEN.

Reference-plane/co-simulation design:
`docs/R1E1A4A_REFERENCE_PLANE_AND_COSIM_SPEC.md`.
