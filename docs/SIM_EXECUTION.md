# SIM_EXECUTION

## 1. Global Protocol

- Repository: Dingo-infinity2020/SimulationOps
- Protocol version used: 0.2.8
- Minimum compatible version: >=0.2.8
- DC policy: GitHub/authority first; stage-level transactions only

## 2. Current stage

R1E1A4A_AR0_B0G_FEED_HEAD_BUILD_ONLY_AWAIT_AUTH

- BUILD_AUTHORIZED: false
- SOLVE_AUTHORIZED: false
- LNA_INTEGRATION_AUTHORIZED: false

## 3. Architecture decision

First priority:
AR0-B0_STALK_TOP_TWIN_MSL_TWIN_LNA

Authority:
- docs/R1E1A4A_AR0_B0_STALK_TOP_TWIN_MSL_ARCHITECTURE_FREEZE_V01.md
- execution/R1E1A4A_AR0_B0_ARCHITECTURE_MANIFEST_V01.json
- docs/R1E1A4A_AR0_B0G_FEED_HEAD_BUILD_ONLY_PLAN_V01.md

B0 hard rules:
- balanced radiator remains ground-free on both faces;
- stalk ground never contacts radiator copper;
- two signal branches per polarization;
- two QPL9547 first-stage candidates per polarization;
- ordinary nominal 1.90-mm MSL begins after a 3.0-mm ground setback;
- no passive pre-LNA balun;
- old T01-A is post-LNA technology only.

## 4. Superseded branch

H3B-C0 status remains:
HOLD_R1E1A4A_H3B_C0_GEOMETRY_OVERLAP

Its artifacts/evidence remain protected.
No recovery build is authorized.

## 5. Next executable node

AR0-B0G feed-head BUILD-ONLY on NW after explicit authorization.

The build contains:
- radiator;
- two orthogonal fork-head stalks;
- four signal-only tongues;
- four nominal MSL traces;
- stalk-only backside ground rails;
- four nonconductive QPL9547 envelopes;
- via-reserve predicates.

No transistor, port, load, solve, or T01 antenna-feed geometry.

## 6. Stop boundary

AWAIT AR0-B0G BUILD-ONLY AUTHORIZATION.
