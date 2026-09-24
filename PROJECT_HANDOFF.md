# PROJECT_HANDOFF.md

> Canonical operational handoff for design side, Desktop Commander, and execution hosts.

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=6
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A3-MATERIALIZED-FR4-BUILD-ONLY-DC-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_BUILD_ONLY
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES
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

Read in this order before execution:
1. SimulationOps CHATGPT_ROUTING.md
2. GLOBAL_DC_SIMULATION_PROTOCOL.md
3. infrastructure/HOSTS.md
4. WORKSPACE_LIFECYCLE.md
5. docs/SIM_EXECUTION.md
6. execution/stage_contract.json
7. this handoff

Build and solve are separate permissions. This handoff authorizes only BUILD_ONLY.

## 2. Architecture state

MAINLINE:
- CHARTS-inspired planar balanced active element.

R0:
- R0_CLOSED_SOURCE_LIMITED.

REF-CUI:
- REFERENCE_ONLY.
- CST automation/replay evidence only.
- scientific geometry HOLD.
- no solver authorized.

## 3. Closed R1 stages

R1A1:
- PASS_R1A1_SCALED_APERTURE_BUILD_ONLY
- evidence commit: 094f11a25e153d5705f9b68d118b4d5ffb0dad9d
- frozen scale: 0.285714285714
- 0 ports, no solver.

R1A2:
- PASS_R1A2_FEED_REFERENCE_BUILD_ONLY
- evidence commit: 7cace83d85eb55fe4a970ce2285abf15bad76d1e
- one center-gap master + exact 90-degree copies
- one terminal-reference master + exact 90-degree copies
- gap and terminal volume spread = 0
- 0 ports, no solver.

## 4. R1A3 scientific freeze

Authoritative design files:
- docs/R1A3_MATERIALIZED_APERTURE_DESIGN.md
- docs/R1A3_SCIENTIFIC_FREEZE.md
- em/cst/R1_CHARTS_LBAND/parameters_r1a3_materialized_fr4.csv

R1A3 materializes exactly one FR4 cost baseline:
- board span 70.714285714 mm
- substrate thickness 1.00 mm
- FR4 nominal er 4.2
- FR4 nominal tanD 0.018
- top conductor physical thickness 0.035 mm
- conductor modeled as PEC for BUILD_ONLY
- 12 accepted disconnected through-slots
- project-owned center cross copper isolation
- project-owned continuous square-ring copper isolation

The center cross and square ring are each generated from one master plus three exact 90-degree CST Transform copies.

R1A2 terminal coordinates remain metadata only in R1A3.
No terminal PEC overlays, physical ports, LNA, or solver are present.

## 5. Authorized NW task

Task:
`R1A3-MATERIALIZED-FR4-BUILD-ONLY-DC-NW`

Host:
- NW / DESKTOP-GBTI6Q4

Repository:
`D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold`

Canonical build work:
`D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work`

Canonical CST artifact:
`D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst`

Source bundle:
- source/cst/R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr
- scripts/audit_r1a3_materialized_fr4.py
- scripts/run_r1a3_build_only_dc.py
- em/cst/R1_CHARTS_LBAND/parameters_r1a3_materialized_fr4.csv
- em/cst/R1_CHARTS_LBAND/RUNBOOK_R1A3_BUILD_ONLY.md

Static audit has passed before authorization:
`PASS_R1A3_STATIC_AUDIT`

Execution interpreter:
`D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python\python.exe`

## 6. Required return

Required evidence:
- exact source HEAD
- macro SHA256
- CST absolute path
- CST SHA256
- CST bytes
- object inventory
- parameter inventory
- top view
- perspective view
- fresh-reopen inventory
- fresh-reopen screenshot
- 0 ports
- no solver

Allowed status:
- PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
- HOLD_R1A3_STATIC_AUDIT
- HOLD_R1A3_CST_RUNTIME
- HOLD_R1A3_RUNTIME_AUDIT
- FAIL_R1A3_REPLAY

## 7. Mandatory human CST review gate

The user explicitly requires the canonical R1A3 CST artifact for manual inspection.

Therefore after build/fresh reopen:
- preserve the exact canonical CST file on NW;
- record path/hash/bytes/source;
- lifecycle state = PROTECTED or CHECKPOINTED with purge_allowed=false;
- do not hand-edit a review copy and substitute it for the canonical artifact;
- do not stage it to CST251;
- do not run any solver.

A BUILD_ONLY PASS stops at:
`PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW`

Only explicit user review/approval can close this gate and allow a later port/solver design stage.

## 8. Workspace closeout

At R1A3 PASS/HOLD:
- commit/push compact source/evidence/handoff;
- check git status and active processes;
- update execution/workspace_record_NW_R1A3.json;
- keep the canonical CST artifact protected;
- do not purge the CST work directory.

No production solve is authorized.
