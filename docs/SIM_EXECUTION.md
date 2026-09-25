# SIM_EXECUTION

## Current stage
R1E1A3R1_NUMERICAL_RECOVERY_DESIGN

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Last completed execution
R1E1A3 S1_BONDED_B0 one-shot solve
Status: HOLD_R1E1A3_S1_BONDED_B0_NUMERICAL_MAXPASSES
Formal solve invocation count: 1
Solved SHA256: 55a55f56ad4981fb30d31624cc656f2a6f4affc5438d3879176531b633480ce3

Provisional movement versus bare:
max |Delta S11| = 0.01111983
max |Delta Z_active| = 4.27463 ohm

## Recovery
Plan: docs/R1E1A3R1_NUMERICAL_RECOVERY_PLAN.md
Proposed sole change: MaxPasses 8 -> 12.
Recovery solve requires separate authorization.

## Stop
Do not start remaining support solves or R1E1B.
