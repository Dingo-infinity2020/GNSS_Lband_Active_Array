# R1A3 Materialized FR4 BUILD-ONLY — NW/DC Return Report

**FINAL_STATUS = PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW**

- Task: R1A3-MATERIALIZED-FR4-BUILD-ONLY-DC-NW
- Host: NW / DESKTOP-GBTI6Q4
- Source HEAD: dbd879fd81c8a7b19ef2139ce03c620625c07084
- SimulationOps: 0.2.4
- CST: 2022.5
- Interpreter: CST bundled Python 3.6.0
- Formal build invocation count: 1
- Exit code: 0
- Runtime: 76.10 s
- Solver: NOT RUN
- Ports: NONE in frozen source; no port creation commands
- LNA: NOT PRESENT
- CST251 staging: NOT PERFORMED

## Static preflight

PASS_R1A3_STATIC_AUDIT

Frozen construction:
- one 70.714285714 mm FR4 board;
- FR4 nominal er=4.2, tanD=0.018, thickness=1.00 mm;
- top conductor physical thickness=0.035 mm, PEC for build-only;
- 12 disconnected through-slot coordinates applied to both substrate and copper;
- one center-cross gap master + 3 exact 90-degree copies;
- one square-ring gap master + 3 exact 90-degree copies.

## Runtime / fresh reopen

Build/save: PASS
Evidence extraction: PASS
Fresh reopen: PASS
Tool residue: NONE

Final object inventory:
- UnitCellGround:UNITCELL_GROUND_REFERENCE
- Substrate:FR4_BOARD
- TopCopper:TOP_COPPER
- SHAPE_COUNT=3

Fresh-reopen inventory is identical.

## Canonical CST artifact for user review

Path:
D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst

SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

Bytes:
48527

Macro SHA256:
1e5bb3188c5d19146b673ec54372d0c35ae572abc775512529f71db71cfad5be

This exact CST artifact is the canonical review object. It must remain protected in place and must not be manually edited, purged, staged to CST251, or used for solver execution before explicit user review.

## Visual design-side check

Top and oblique evidence are consistent with:
- exact fourfold center isolation;
- continuous square-ring copper isolation;
- mechanically connected slotted FR4 board;
- intended board-to-ground separation.

Caveat:
the object inventory is shape-object level, not an independent electrical-connectivity proof. Human CST review is intentionally retained as the next gate.

## Stop boundary

Build authorization is consumed.

Next state:
HUMAN_REVIEW_R1A3

BUILD_AUTHORIZED=NO
SOLVE_AUTHORIZED=NO
CST_ARTIFACT_PURGE_ALLOWED=NO
CST251_STAGING=NO
