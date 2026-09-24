# SIM_EXECUTION

## 1. Global Protocol

- Repository: Dingo-infinity2020/SimulationOps
- Protocol version: 0.2.4
- Host registry: infrastructure/HOSTS.md
- Workspace lifecycle: WORKSPACE_LIFECYCLE.md
- Adoption commit: 45fcb8c89445f05a696cde524d762641ea7ea961

## 2. Project Identity

- Project: GNSS L-band Active Array
- Current model identity: CHARTS_GNSS_R1A3_MATERIALIZED_FR4_V01
- Repository: Dingo-infinity2020/GNSS_Lband_Active_Array
- Source branch: project/r0-charts-scaffold
- Build source commit: dbd879fd81c8a7b19ef2139ce03c620625c07084

## 3. Toolchain

- Simulator: CST Studio Suite 2022.5
- Builder: source/cst/R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr
- Harness: scripts/run_r1a3_build_only_dc.py
- Build host: NW
- Solve host: CST251-C reserved only for a later explicit solve authorization
- Runtime: CST bundled Python 3.6 / cst.interface

## 4. Artifact Locations

- Canonical CST: D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst
- CST SHA256: b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa
- CST bytes: 48527
- Evidence: evidence/r1a3_dc_nw_20260924_build01/
- Staging artifact: NOT AUTHORIZED
- Solve directory: NOT AUTHORIZED

## 5. Scientific Freeze

- Geometry manifest: em/cst/R1_CHARTS_LBAND/parameters_r1a3_materialized_fr4.csv
- Design freeze: docs/R1A3_SCIENTIFIC_FREEZE.md
- Material: FR4_COST_BASELINE er=4.2 tanD=0.018 t=1.00 mm
- Top conductor: 0.035 mm PEC build-only geometry
- Ports: none
- LNA: none
- Frequency target: 1.15-1.65 GHz; no solver result exists
- PASS: PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
- Stop boundary: explicit user review of canonical CST

## 6. Execution State

- Current stage: HUMAN_REVIEW_R1A3
- BUILD_AUTHORIZED: false
- SOLVE_AUTHORIZED: false
- Last completed stage: BUILD_ONLY_R1A3
- Last status: PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
- Formal invocation count: 1
- Formal invocation exit code: 0
- Fresh reopen: PASS
- Silent retry: NO

## 7. Workspace Lifecycle

- Host: NW
- Repository workspace: D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold
- Record: execution/workspace_record_NW_R1A3.json
- Canonical build work: D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work
- State: PROTECTED
- Archive mode: PROTECTED_IN_PLACE
- Purge allowed: false
- Reason: user-requested manual CST review is pending

## 8. Recovery Notes

The R1A3 canonical CST file is not ordinary temporary build output.
Do not delete, overwrite, manually edit, stage, or solve it before explicit user review.
