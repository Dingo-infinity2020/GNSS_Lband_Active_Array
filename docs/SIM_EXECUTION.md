# SIM_EXECUTION

## 1. Global Protocol

- Repository: Dingo-infinity2020/SimulationOps
- Protocol: GLOBAL_DC_SIMULATION_PROTOCOL.md
- Protocol version used: 0.2.8
- Minimum compatible version: >=0.2.8
- Host registry: infrastructure/HOSTS.md
- Workspace lifecycle: WORKSPACE_LIFECYCLE.md
- DC call policy: DC_CALL_EFFICIENCY.md

## 2. Current stage

R1E1A4A_H3B_C0_COMPLETE_PASSIVE_BUILD_ONLY_AWAIT_AUTH

- BUILD_AUTHORIZED: false
- SOLVE_AUTHORIZED: false

## 3. Proven prerequisite

T01-A = PASS_R1E1A4A_H3B_T01A_FREEZE
H3A V0.2 = PASS_R1E1A4A_H3A_V02_FR4_BRIDGED_MORTISE_BUILD_ONLY

## 4. H3B frozen route

Authority:
- docs/R1E1A4A_H3B_COMPLETE_PASSIVE_ROUTE_FREEZE_V01.md
- docs/R1E1A4A_H3B_C0_BUILD_ONLY_PLAN_V01.md
- docs/R1E1A4A_H3B_I01_PASSIVE_PILOT_PLAN_V01.md
- execution/R1E1A4A_H3B_C0_REPLACEMENT_MAP_V01.json

Route:
H3B-C0 build-only -> human 3D review -> H3B-I01 six-state A/B passive pilot -> Passive Unit V1 freeze -> LNA-on-stalk A0.

## 5. Immediate authorization boundary

The next executable action is H3B-C0 BUILD-ONLY on NW.

Task packet:
execution/task_packets/R1E1A4A_H3B_C0_task.json

C0 creates two fresh zero-port/zero-solver artifacts:
A = H3A_MECH_ONLY_PHYSICALIZED
B = H3B_COMPLETE_PASSIVE_V1

No solve, no LNA device, no A0, no pitch sweep.

## 6. DC Call Budget

GitHub/authority first.
Target C0 execution: one batched build transaction + one task-node inspection.
No periodic polling.

## 7. Stop boundary

Await explicit BUILD authorization for H3B-C0.
I01 SOLVE remains separately unauthorized.
