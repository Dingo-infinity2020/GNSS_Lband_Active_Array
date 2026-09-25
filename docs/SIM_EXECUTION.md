# SIM_EXECUTION

## Protocol
Minimum compatible SimulationOps protocol: 0.2.6

## Current stage
R1E1A4A_H3B_T01A_NUMERICAL_RECOVERY_MAXPASS16

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true — ONE T01A MAXPASS16 RECOVERY
PRODUCTION_SOLVE_AUTHORIZED: true
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Recovery authority
docs/R1E1A4A_H3B_T01A_NUMERICAL_RECOVERY_FREEZE_V01.md

Source BUILD SHA256:
f321b678d390470a2420df40fd6d0cf6553cc041f9219bfcd011c7e41fbadf3d

Only solver delta from the failed baseline:
MaxPasses 8 -> 16.

Native PASS criterion:
final two CST Adaptive Meshing / All-S Delta values <= 0.02.

No geometry/RF optimization is authorized.
