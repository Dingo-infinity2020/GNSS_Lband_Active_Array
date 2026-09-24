# PROJECT_HANDOFF.md

> Canonical operational handoff for design side, Desktop Commander, execution hosts, and human review.

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=7
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A3-HUMAN-CST-REVIEW
TASK_OWNER=USER_REVIEW
TASK_STATUS=AWAITING_HUMAN_REVIEW
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
L_BAND_SCALING_PERMISSION=R1A1_FROZEN_SCALE_ONLY
LNA_INTEGRATION_PERMISSION=NO
HARDWARE_PERMISSION=NO
HUMAN_CST_REVIEW_REQUIRED=YES
CST_ARTIFACT_PURGE_ALLOWED=NO
```

## 1. Global protocol

This project follows Dingo-infinity2020/SimulationOps protocol 0.2.4 at commit:
`45fcb8c89445f05a696cde524d762641ea7ea961`.

Build and solve are separate permissions.
The R1A3 build authorization has been consumed.
No solver or CST251 staging is authorized.

## 2. Architecture state

MAINLINE:
- CHARTS-inspired planar balanced active element.

R0:
- R0_CLOSED_SOURCE_LIMITED.

REF-CUI:
- REFERENCE_ONLY; scientific geometry HOLD; no solver.

## 3. Closed R1 build-only stages

R1A1:
- PASS_R1A1_SCALED_APERTURE_BUILD_ONLY
- evidence commit 094f11a25e153d5705f9b68d118b4d5ffb0dad9d

R1A2:
- PASS_R1A2_FEED_REFERENCE_BUILD_ONLY
- evidence commit 7cace83d85eb55fe4a970ce2285abf15bad76d1e
- exact-rotation feed reference symmetry PASS

R1A3:
- PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
- build source HEAD dbd879fd81c8a7b19ef2139ce03c620625c07084
- one formal invocation, exit 0, runtime 76.10 s
- fresh reopen PASS
- no solver

## 4. R1A3 frozen structure

Model:
`CHARTS_GNSS_R1A3_MATERIALIZED_FR4_V01`

Frozen build-only structure:
- board span 70.714285714 mm
- 94 mm ground-reference plane
- board height 57.142857143 mm
- FR4_COST_BASELINE, er=4.2, tanD=0.018, t=1.00 mm
- 0.035 mm top-conductor geometry, PEC for build-only
- 12 disconnected through-slots
- project-owned four-arm center copper isolation
- project-owned continuous square-ring copper isolation
- no terminal overlay solids
- no physical ports
- no LNA

Center cross and square ring are each generated from one master plus three exact 90-degree rotations.

## 5. Canonical CST artifact — DO NOT PURGE

User-review artifact:
`D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst`

SHA256:
`b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa`

Bytes:
`48527`

Macro SHA256:
`1e5bb3188c5d19146b673ec54372d0c35ae572abc775512529f71db71cfad5be`

Lifecycle:
- PROTECTED_IN_PLACE
- purge_allowed=false
- no manual edits to the canonical artifact
- no CST251 staging
- no solver

## 6. Runtime evidence

Evidence:
`evidence/r1a3_dc_nw_20260924_build01/`

Runtime inventory:
- SHAPE_COUNT=3
- UnitCellGround:UNITCELL_GROUND_REFERENCE
- Substrate:FR4_BOARD
- TopCopper:TOP_COPPER
- no SlotTools/CopperGapTools residue
- fresh-reopen inventory identical

The shape count is CST object-level and is not used as an independent electrical-connectivity proof for the disconnected copper bodies.

Design-side screenshot review:
- top view is visually fourfold symmetric;
- continuous square-ring isolation is visible;
- center cross is symmetric;
- oblique view shows substrate/top-conductor/ground separation.

## 7. Current task: human CST review

The user should inspect the canonical CST artifact above.

Review focus:
1. four-petal symmetry;
2. center-cross geometry;
3. continuous square-ring isolation;
4. preservation of the 12-slot visible topology;
5. substrate bridges versus copper-only isolation;
6. board-to-ground separation;
7. absence of unintended feed/port/LNA geometry.

Until explicit user approval:
- BUILD_AUTHORIZED=NO
- SOLVE_AUTHORIZED=NO
- CST251 staging forbidden
- canonical CST artifact must remain protected

## 8. Next design boundary

Only after human R1A3 review may DESIGN define the next gate for:
- physical differential terminal/port realization;
- passive isolated-element solver contract;
- later FR4 versus low-loss material comparison.

No such next gate is pre-authorized.
