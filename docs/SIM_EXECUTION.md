# SIM_EXECUTION

## Protocol
Minimum compatible SimulationOps protocol: 0.2.6

## Current stage
R1E1A4A_H3B_T01_TRANSITION_COUPON_BUILD_ONLY

BUILD_AUTHORIZED: true — ONE H3B-T01 BUILD-ONLY INVOCATION
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Design authority
Optimization route:
docs/R1E1A4A_H3B_ACTIVE_ELEMENT_OPTIMIZATION_ROUTE_FREEZE_V01.md

T01 geometry freeze:
docs/R1E1A4A_H3B_T01_TRANSITION_COUPON_FREEZE_V01.md

## Build-only scope
- standalone blank MWS; no inherited antenna model;
- 1.0-mm horizontal and vertical FR4 coupon boards;
- same G-S-G controlled-line geometry on both boards;
- local backing grounds and plated via fences;
- explicit signal/GND pads, edge caps and solder envelopes;
- RP1 y=+12 mm and RP2 z=-12 mm stored as parameters only;
- 0 RF ports; no solver.

## Mandatory qualification
- exact component/shape inventory;
- all via-hole tools consumed;
- CST EM auto-intersection during build;
- CST CDCheckModelIntersections after fresh reopen;
- positive signal/ground, board-edge and via clearances;
- no solver markers/results.

## Stop boundary
Stop after human 3D/manufacturing review.
No passive solve, optimization sweep, H3B-I01 integration or active-device model.
