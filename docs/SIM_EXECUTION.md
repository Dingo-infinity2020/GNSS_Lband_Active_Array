# SIM_EXECUTION

## Protocol
Minimum compatible SimulationOps protocol: 0.2.6

## Current stage
R1E1A4A_H3A_V02_FR4_BRIDGED_MORTISE_BUILD_ONLY

BUILD_AUTHORIZED: true — ONE H3A V0.2 BUILD-ONLY INVOCATION
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Frozen source
Parent:
D:\GNSS_Lband_Active_Array\_r1e1a1_six_pitch_fr4_work\R1E1A1_P094_PITCH_BUILD_ONLY_V01.cst

SHA256:
fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e

Freeze:
docs/R1E1A4A_H3A_ORTHOGONAL_STALK_ARCHITECTURE_FREEZE_V02.md

## V0.2 delta
- H3A V0.1 remains immutable evidence.
- Add four 5.50 x 2.571428571426 x 1.0 mm FR4 bridges inside the parent INNER_N/S/E/W substrate slots at the +/-12-mm tenon locations.
- Unite each bridge into Substrate:FR4_BOARD.
- Recut the frozen 3.30 x 1.25-mm true mortise through the bridge.
- Do not restore top copper.
- All stalk/LNA/shield/RF-transition/service geometry remains V0.1.

Expected substrate volume after bridge-minus-mortise delta:
4518.704081623642 mm^3

## Mandatory qualification
- fresh reopen;
- shape/component inventory;
- substrate volume proof;
- bridge component fully consumed by union;
- zero RF ports / no solver results;
- CST EM auto-intersection during build;
- CST CDCheckModelIntersections after fresh reopen;
- all critical clearances positive.

## Stop boundary
Stop after H3A V0.2 human 3D review.
No solve and no H3B continuation.
