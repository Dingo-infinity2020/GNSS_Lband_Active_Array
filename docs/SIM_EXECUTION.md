# SIM_EXECUTION

## Protocol
Minimum compatible SimulationOps protocol: 0.2.7

## Current stage
R1E1A4A_H3B_T01A_O0_REFERENCE_LINE_AWAIT_AUTH

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Qualified T01-A baseline
Numerical status:
PASS_R1E1A4A_H3B_T01A_NUMERICALLY_CONVERGED_MAXPASS16

Solved artifact SHA256:
928400031803e62665df0a17890b2158b8d56b2673e9af1a9e0c7a7d171266df

Native adaptive convergence:
- pass 11 DeltaS = 0.01971590799;
- pass 12 DeltaS = 0.01570656518.

## Master plan authority
docs/R1E1A4A_H3B_TO_ACTIVE_ARRAY_MASTERPLAN_V01.md

## Immediate next node
H3B_T01A_O0_REFERENCE_LINE_FREEZE

Purpose: separate straight GCPW line mismatch/loss from the 90-degree junction before any geometry optimization.

No sweep/DOE is authorized.
T01-C remains deferred.
H3B-I01 remains blocked until T01-A local RF freeze.
No BUILD or SOLVE authorization is currently open.
