# SIM_EXECUTION

## Current state

SimulationOps version: 0.2.4

Current stage:
DESIGN_R1A5M2_MAXPASS_EXTENSION

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Last run

R1A5M adaptive second-order:

Status:
HOLD_R1A5M_ADAPTIVE_NOT_CONVERGED

Native Delta-S sequence:
0.0673917 -> 0.0497934 -> 0.0274924 -> 0.0203932 -> 0.0173369

Reason for HOLD:
MaxPasses=6 reached before two consecutive Delta-S checks satisfied the 0.02 threshold.

## Recovery design boundary

Only proposed change:
MaxPasses 6 -> 8.

No current solver action is allowed.

Material A/B and production science remain blocked.
