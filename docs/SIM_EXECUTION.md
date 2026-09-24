# SIM_EXECUTION

## 1. Global Protocol

- Repository: `Dingo-infinity2020/SimulationOps`
- Protocol: `GLOBAL_DC_SIMULATION_PROTOCOL.md`
- Protocol version used: `0.2.4`
- Minimum compatible version: `>=0.2`
- Host registry: `infrastructure/HOSTS.md`
- Workspace lifecycle: `WORKSPACE_LIFECYCLE.md`

SimulationOps main commit at adoption:
`45fcb8c89445f05a696cde524d762641ea7ea961`

## 2. Project Identity

- Project: GNSS L-band Active Array
- Current model identity: `CHARTS_GNSS_R1A1_SCALED_APERTURE_V01`
- Repository: `Dingo-infinity2020/GNSS_Lband_Active_Array`
- Source branch: `project/r0-charts-scaffold`
- Source commit: resolve and record exact HEAD at build preflight
- Owner / operator: project design side + DC/NW

## 3. Toolchain

- Simulator: CST Studio Suite
- Simulator version: 2022.5
- Builder: `source/cst/R1A1_CHARTS_SCALED_APERTURE_BUILD_ONLY_V01.mcr`
- Build host alias: `NW`
- Solve host alias: `CST251-C` reserved for later production solve unless a later stage contract explicitly authorizes an NW smoke solve
- Required container: none for current NW build-only
- Runtime: CST bundled Python / cst.interface

## 4. Artifact Locations

- Source bundle: repository files under `source/cst/`, `em/cst/R1_CHARTS_LBAND/`, `execution/`
- Build artifact: `D:\GNSS_Lband_Active_Array\_r1a1_scaled_aperture_work\R1A1_CHARTS_SCALED_APERTURE_BUILD_ONLY_V01.cst`
- Staging artifact: not authorized yet
- Fresh run directory: not authorized yet
- Large-result storage: not applicable
- Qualification output: `evidence/r1a1_dc_nw_<timestamp>/`
- Handoff: `PROJECT_HANDOFF.md`

## 5. Scientific Freeze

- Geometry manifest: `em/cst/R1_CHARTS_LBAND/parameters_r1a1.csv`
- Material table: PEC topology proxy only; substrate/material is intentionally deferred
- Source modes: none
- Frequency range: project target 1.15–1.65 GHz; no solver in R1A1
- Required outputs: parameter inventory, object inventory, top/oblique views, fresh-reopen inventory, CST SHA256
- Scientific metric: exact deterministic scale/provenance + topology preservation
- PASS threshold: `PASS_R1A1_SCALED_APERTURE_BUILD_ONLY`
- HOLD conditions: manifest/audit failure, CST syntax failure, slot connectivity error, wrong solid count, fresh-reopen mismatch
- Stop boundary: fresh-reopen audit; do not start solver

## 6. Execution State

- Current stage: `BUILD_ONLY_R1A1`
- `BUILD_AUTHORIZED`: true
- `SOLVE_AUTHORIZED`: false
- Last completed stage: `R0_CLOSED_SOURCE_LIMITED`
- Last status: `READY_FOR_NW_BUILD_ONLY`
- Last artifact SHA256: none
- Last handoff: `PROJECT_HANDOFF.md`

## 7. Workspace Lifecycle

- Workspace host: `NW`
- Workspace path: `D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold`
- Workspace record: `execution/workspace_record_NW_R1A1.json`
- Workspace state: `ACTIVE`
- Archive mode: `REFERENCE_ONLY` for clean Git checkout; build artifact separately hash-recorded
- Archive trigger / task node: R1A1 PASS or HOLD
- Archive destination / protected path: remote Git + evidence; build artifact may become PURGE_READY after design review
- Purge allowed after: explicit closeout record
- Cleanup completed: false
- Cleanup evidence: none

## 8. Project-Specific Exceptions

NONE.

## 9. Recovery Notes

- REF-CUI solver path is stopped by Decision D0008.
- CHARTS R0 is closed source-limited.
- Current authorized action is only R1A1 scaled visible-aperture BUILD-ONLY on NW.
- Explicitly forbidden: solver, ports, monitors, LNA, GNSS optimization, material optimization.
