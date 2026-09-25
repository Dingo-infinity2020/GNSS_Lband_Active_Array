# SIM_EXECUTION

## Protocol
Minimum compatible SimulationOps protocol: 0.2.6

## Current stage
R1E1A4A_H3B_T01_OPTIMIZATION_ROUTE_FROZEN

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Accepted mechanical baseline
H3A V0.2 FR4-bridged mortise build is accepted.

Artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h3a_v02_build_work\R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY_V02.cst

SHA256:
9e810560fc8fc759a88d4ac5fc39067863a1e078b6f01e6e343b004891201db5

## Project-level optimization authority
docs/R1E1A4A_H3B_ACTIVE_ELEMENT_OPTIMIZATION_ROUTE_FREEZE_V01.md

Frozen method:
HIERARCHICAL_MODULAR_CODESIGN_WITH_SYSTEM_LEVEL_CLOSURE

Key rules:
- final objective is robust A_eff/T_sys or G/T, not standalone S11;
- antenna/LNA interface is not forced to 50 ohms;
- final LNA source condition comes from scan-dependent active array impedance;
- local modules are qualified first;
- only a small Class-C set of cross-domain variables is exposed to later system optimization;
- EM/circuit back-annotation must reach self-consistency before final system optimization.

## Immediate next node
H3B_T01_POST_LNA_ORTHOGONAL_TRANSITION_COUPON_FREEZE

Scope:
post-LNA radiator-board to vertical-stalk 90-degree passive RF transition only.

No BUILD or SOLVE authorization currently exists.
