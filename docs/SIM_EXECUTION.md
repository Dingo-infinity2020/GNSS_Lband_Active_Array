# SIM_EXECUTION

## Current stage
R1E1A2A3_SUPPORT_BUILD_AND_SENSITIVITY

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: true
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Scientific freeze
Contract: docs/R1E1A2A3_SUPPORT_SENSITIVITY_CONTRACT.md
Material table: em/cst/R1_CHARTS_LBAND/materials_r1e1a2_support.csv
Bare P094 SHA256: fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e
Build matrix: S1 B0 / S1 C60P45 / S1 C60P135 / S4 B0
Solve matrix: same four, each independent one-shot on NW

## Stop boundary
Close R1E1A3 support sensitivity gate.
Do not start R1E1B pitch screen.
No material A/B and no LNA integration.
