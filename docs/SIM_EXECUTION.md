# SIM_EXECUTION

## Protocol
Minimum compatible SimulationOps protocol: 0.2.7

## Current stage
R1E1A4A_H3B_T01A_O3_PHYSICAL_FIDELITY_QUALIFICATION_AUTHORIZED

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## O2B
PASS_R1E1A4A_H3B_T01A_O2B_ACCEPTABLE
Winner: P20_G30_E30
Worst core return: -14.3819 dB
Max junction excess: 0.0639 dB

## Route decision
O2C = DEFERRED_CONTINGENCY_ONLY.
Authoritative route: docs/R1E1A4A_POST_O2B_ROUTE_FREEZE_V02.md

## Authorized work
O3 physical-fidelity nominal transition + paired copper straight reference.
O4 exactly six deterministic manufacturing sentinels.
No nominal O2C optimization and no T01-C.

## Stop boundary
After O3/O4: T01-A FREEZE on PASS, otherwise HOLD at the failing gate.
