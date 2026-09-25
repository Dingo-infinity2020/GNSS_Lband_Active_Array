# SIM_EXECUTION

## Protocol
Minimum compatible SimulationOps protocol: 0.2.6

## Current stage
R1E1A4A_H3B_T01A_NUMERICAL_RECOVERY_AWAIT_AUTH

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Closed T01-A passive baseline solve
Formal solver invocation count: 1
Solver returned complete two-port S-parameters: YES
Native adaptive convergence qualified: NO

Canonical status:
HOLD_R1E1A4A_H3B_T01A_ADAPTIVE_MAXPASS8_NOT_CONVERGED

Solved artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h3b_t01a_solve_work\R1E1A4A_H3B_T01A_PASSIVE_BASELINE_V01.cst

SHA256:
846919954fc99f541d8d0cfa3b4246fb49bf520d51b6c14de675d6fed54b0734

## Native adaptation evidence
- adaptation frequency = 2.0 GHz;
- 8 passes executed;
- mesh cells: 43521, 51980, 61554, 74117, 78237, 82457, 88182, 98391;
- pass-7 All-S DeltaS = 0.0320727160;
- pass-8 All-S DeltaS = 0.0309454700;
- frozen MaxDeltaS = 0.02;
- two consecutive checks required;
- therefore adaptive convergence gate = FAIL.

## Provisional diagnostics only
- core-band S11/S22 approximately -14.7 to -10.3 dB;
- core-band S21/S12 approximately -0.257 to -0.570 dB;
- no sharp S21 notch below -3 dB;
- reciprocity difference approximately 4e-5 dB.

These values are not science-qualified because adaptive convergence failed.

## Next node
H3B_T01A_NUMERICAL_RECOVERY_FREEZE

Recovery may evaluate additional max passes / mesh strategy only under a new explicit solve authorization.
No geometry optimization, T01-C, H3B-I01 or active-device work is currently authorized.
