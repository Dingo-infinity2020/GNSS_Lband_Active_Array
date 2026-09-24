# PROJECT_HANDOFF.md

> Canonical operational handoff for design side, Desktop Commander, and execution hosts.

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=5
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A2-DESIGN-FEED-SYMMETRY-FREEZE
TASK_OWNER=DESIGN
TASK_STATUS=READY_FOR_DESIGN
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
L_BAND_SCALING_PERMISSION=R1A1_FROZEN_SCALE_ONLY
LNA_INTEGRATION_PERMISSION=NO
HARDWARE_PERMISSION=NO
```

## 1. Global execution protocol

This project now adopts:
- `Dingo-infinity2020/SimulationOps`
- protocol version 0.2.4
- adoption baseline commit `45fcb8c89445f05a696cde524d762641ea7ea961`

Project-local execution files:
- `docs/SIM_EXECUTION.md`
- `execution/stage_contract.json`
- `execution/workspace_record_NW_R1A1.json`

Global host facts remain in SimulationOps `infrastructure/HOSTS.md`.

## 2. Mainline status

MAINLINE:
- CHARTS-inspired planar balanced active element.

R0:
- `R0_CLOSED_SOURCE_LIMITED`

R1 current model:
- `CHARTS_GNSS_R1A1_SCALED_APERTURE_V01`

REF-CUI:
- REFERENCE_ONLY
- execution/replay PASS only
- scientific geometry HOLD
- no solver authorized

## 3. R1A1 scientific freeze

Purpose:
- scale only the accepted R0 V0.3 visible 12-slot aperture topology,
- use one frozen scale factor,
- prove deterministic CST construction at L-band physical size,
- stop before feed/material/ports/solver.

Frozen scale:
- `scale_factor = 0.285714285714`
- nominal 400 MHz source center -> 1.40 GHz project center

Key derived dimensions:
- board = 70.714285714 mm
- outer slot frame = 65.0 mm
- outer slot width = 1.428571429 mm
- outer segment = 26.892857143 mm
- inner slot width = 2.571428571 mm
- inner slot length = 20.857142857 mm
- visible center clear span = 17.142857143 mm
- height over ground = 57.142857143 mm
- nominal future unit-cell reference = 94 mm

The unresolved source 40 mm label is scaled and stored only for provenance; it is not used geometrically.

## 4. Symmetry rule for next stage

R1A1 contains no feed.

R1A2 feed rule is already frozen in:
- `docs/R1A2_CENTER_FEED_SYMMETRY_SPEC.md`

Only one canonical RF terminal geometry may be authored; X-/Y+/Y- must be exact rotations by 180/90/270 degrees.

## 5. Current DC/NW task

Build host:
- `NW` / `DESKTOP-GBTI6Q4`

Repository workspace:
- `D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold`

Build work:
- `D:\GNSS_Lband_Active_Array\_r1a1_scaled_aperture_work`

Source bundle:
- `source/cst/R1A1_CHARTS_SCALED_APERTURE_BUILD_ONLY_V01.mcr`
- `scripts/audit_r1a1_scaled_aperture.py`
- `scripts/run_r1a1_build_only_dc.py`
- `em/cst/R1_CHARTS_LBAND/parameters_r1a1.csv`
- `em/cst/R1_CHARTS_LBAND/RUNBOOK_R1A1_BUILD_ONLY.md`

Expected:
- static audit PASS,
- 2 final solids,
- 12 slot subtractions consumed,
- 0 ports,
- no solver,
- fresh-reopen persistence.

Allowed final status:
- `PASS_R1A1_SCALED_APERTURE_BUILD_ONLY`
- `HOLD_R1A1_STATIC_AUDIT`
- `HOLD_R1A1_CST_RUNTIME`
- `HOLD_R1A1_VISUAL_TOPOLOGY`
- `FAIL_R1A1_REPLAY`

## 6. Stop boundary

Desktop Commander may execute the authorized NW build-only task.

After fresh reopen:
- capture evidence,
- commit/push compact evidence,
- update stage contract/handoff,
- perform workspace closeout classification.

Do not:
- create ports,
- add substrate,
- add feed,
- run solver,
- start optimization,
- integrate LNA,
- stage to CST251.

No production solve is authorized by this handoff.

## 7. Execution source

Pre-execution repository HEAD before this handoff update:
`d1176b310affc9968b3c78f66926258f2345a00d`

DC must record the actual pulled HEAD at preflight and use that as the source identity.


## 8. Recovery note — 2026-09-24

Attempt 1 is preserved as:
- `HOLD_ENVIRONMENT`
- `evidence/r1a1_dc_nw_20260924_1111/`

The successor task is explicitly authorized:

`R1A1-RECOVERY-CSTPY-BUILD-ONLY-DC-NW`

Execution interpreter:
`D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python\python.exe`

Reason:
- Python 3.6.0
- `import cst, cst.interface` verified
- no scientific/model changes

See:
`docs/RECOVERY_R1A1_NW_CST_PYTHON_20260924.md`

Still forbidden:
- solver
- ports
- feed
- substrate/materialization
- LNA
- optimization
- staging to CST251


## 9. R1A1 closeout

```text
R1A1_STATUS=PASS_R1A1_SCALED_APERTURE_BUILD_ONLY
SOURCE_HEAD=bc06173084cf9c62f99f52c4cfee33afdade9770
EVIDENCE_COMMIT=094f11a25e153d5705f9b68d118b4d5ffb0dad9d
EVIDENCE=evidence/r1a1_recovery_dc_nw_20260924_1113/
CST_SHA256=fc039106312861674d13e92983688672e0fce05d77fbcec6712a075fc2343253
FINAL_SOLIDS=2
PORTS=0
SOLVER_RUN=NO
FRESH_REOPEN=PASS
```

R1A1 is closed. The baton returns to DESIGN for R1A2 center-feed geometry freeze.

NW remains the preferred build host once R1A2 BUILD_ONLY is explicitly authorized.
