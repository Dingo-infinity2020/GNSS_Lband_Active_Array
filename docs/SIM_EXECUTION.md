# SIM_EXECUTION

## 1. Global Protocol

- Repository: Dingo-infinity2020/SimulationOps
- Protocol: GLOBAL_DC_SIMULATION_PROTOCOL.md
- Protocol version used: 0.2.4
- Minimum compatible version: >=0.2
- Host registry: infrastructure/HOSTS.md
- Workspace lifecycle: WORKSPACE_LIFECYCLE.md
- Adoption commit: 45fcb8c89445f05a696cde524d762641ea7ea961

## 2. Project Identity

- Project: GNSS L-band Active Array
- Current model identity: CHARTS_GNSS_R1A3_MATERIALIZED_FR4_V01
- Repository: Dingo-infinity2020/GNSS_Lband_Active_Array
- Source branch: project/r0-charts-scaffold
- Source commit: resolve and record exact HEAD at build preflight
- Operator: project design side + DC/NW

## 3. Toolchain

- Simulator: CST Studio Suite
- Simulator version: 2022.5
- Builder: source/cst/R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr
- Audit: scripts/audit_r1a3_materialized_fr4.py
- Harness: scripts/run_r1a3_build_only_dc.py
- Build host: NW
- Solve host: CST251-C reserved for a later explicitly authorized gate
- Runtime: CST bundled Python 3.6 / cst.interface
- Required container: none

## 4. Artifact Locations

- Source bundle: repository source/cst + em/cst/R1_CHARTS_LBAND + execution
- Build artifact: D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst
- Evidence: evidence/r1a3_dc_nw_20260924_build01/
- Staging artifact: NOT AUTHORIZED
- Fresh solve directory: NOT AUTHORIZED
- Handoff: PROJECT_HANDOFF.md

## 5. Scientific Freeze

- Geometry manifest: em/cst/R1_CHARTS_LBAND/parameters_r1a3_materialized_fr4.csv
- Design freeze: docs/R1A3_SCIENTIFIC_FREEZE.md
- Material: FR4_COST_BASELINE, er 4.2, tanD 0.018, 1.00 mm
- Conductor geometry: 0.035 mm top conductor, PEC at BUILD_ONLY
- Source modes: none
- Ports: none
- Frequency target: 1.15-1.65 GHz; no solver in R1A3
- Required outputs: inventory, screenshots, fresh reopen, hashes, bytes
- Scientific metric: deterministic materialization and topology preservation
- PASS threshold: PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
- Stop boundary: manual user review of canonical CST artifact

## 6. Execution State

- Current stage: BUILD_ONLY_R1A3
- BUILD_AUTHORIZED: true
- SOLVE_AUTHORIZED: false
- Last completed stage: BUILD_ONLY_R1A2
- Last status: PASS_R1A2_FEED_REFERENCE_BUILD_ONLY
- Static audit: PASS_R1A3_STATIC_AUDIT
- Hash lock required: true
- Silent retry allowed: false

## 7. Workspace Lifecycle

- Workspace host: NW
- Repository workspace: D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold
- Workspace record: execution/workspace_record_NW_R1A3.json
- Build work: D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work
- Current state: ACTIVE
- Archive mode: PROTECTED_IN_PLACE for canonical CST artifact
- Archive trigger: R1A3 PASS/HOLD
- Purge allowed for canonical CST artifact: false
- Human review required before any change to artifact lifecycle

## 8. Project-Specific Exceptions

NONE.

## 9. Recovery Notes

- Ordinary NW python is not authoritative for this task; use CST bundled Python path above.
- REF-CUI solver path remains stopped.
- R1A3 authorizes build-only only.
- No CST251 staging or solver is allowed before manual CST review.
