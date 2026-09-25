# SIM_EXECUTION

## Current stage
R1E1A3R1_NUMERICAL_RECOVERY_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: true
CST251_AUTHORIZED: false

## Recovery scope
First: S1_BONDED_B0 recovery only.
Sole solver change: MaxPasses 8 -> 12.
Config: source/cst/R1E1A3R1_SUPPORT_SOLVER_CONFIG_V02.mcr
Harness: scripts/run_r1e1a3r1_support_recovery_solve_dc.py
Evidence protection: snapshot/restore/verify prior immutable build evidence.

If and only if recovery B0 PASSes:
S1_BONDED_C60P45 -> S1_BONDED_C60P135 -> S4_PEC_B0
under the identical recovery solver config.

Any HOLD stops the sequence.
Physical benign thresholds remain unchanged: max |Delta S11| <= 0.05 and max |Delta Z_active| <= 10 ohm.
No R1E1B pitch screen, material A/B, LNA integration or CST251 solve.
