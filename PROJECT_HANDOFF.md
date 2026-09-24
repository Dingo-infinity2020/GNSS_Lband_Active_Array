# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=27
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1E0-PERIODIC-UNIT-CELL-BASELINE
CURRENT_TASK_ID=R1E0A-PERIODIC-CONFIG-BUILD-ONLY-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_BUILD_ONLY
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES_R1E0A_CONFIG_ONLY
SOLVER_PERMISSION=NO
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO
CST251_PERMISSION=NO
```

## Long-horizon authority

Read `PROJECT_MAINLINE.md` first.

The isolated-element passive stage is closed.

R1E0 is now the first primary array-physics gate.

## R1E0 design

Plan:
`docs/R1E0_PERIODIC_UNIT_CELL_PLAN.md`

CST API notes:
`docs/R1E0_CST_UNIT_CELL_API_NOTES.md`

Initial lattice:
- square
- pitch 94 mm
- Pol-A clean feed
- FR4 baseline

## R1E0A authorized build-only task

Purpose:
validate that the actual clean antenna CST can persist the intended unit-cell boundary and scan metadata.

Input:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst`

Required SHA256:
`74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce`

Config:
`source/cst/R1E0A_PERIODIC_BROADSIDE_BUILD_ONLY_V01.mcr`

Static audit:
`PASS_R1E0A_STATIC_AUDIT`

Runbook:
`em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E0A_PERIODIC_BUILD_ONLY.md`

Harness:
`scripts/run_r1e0a_periodic_build_only_dc.py`

## Frozen periodic metadata

- Xmin/Xmax = unit cell
- Ymin/Ymax = unit cell
- Zmin/Zmax = expanded open
- OpenAddSpaceFactor = 0.5
- UnitCellFitToBoundingBox = True
- structure x/y span expected = 94 mm
- theta = 0 deg
- phi = 45 deg
- direction = outward
- no Floquet ports
- retained discrete differential port count = 1
- HF Frequency Domain selected
- no solver start

## Formal execution

Host:
NW / DESKTOP-GBTI6Q4

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work`

Fresh evidence:
`evidence/r1e0a_dc_nw_20260924_build01/`

Expected CST:
`D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst`

One formal invocation only.
No silent retry.

## PASS gate

`PASS_R1E0A_PERIODIC_CONFIG_BUILD_ONLY` requires:

- source/copy hash locked;
- geometry identical to R1A5F Pol-A;
- port count remains 1;
- fresh reopen succeeds;
- x/y boundaries read back as unit cell;
- z boundaries read back as expanded open;
- structure x/y spans read back as 94 mm;
- GetUnitCellScanAngle returns valid;
- theta=0, phi=45, direction=outward;
- no solver output.

## Stop boundary

Stop after metadata persistence qualification.

Do not run R1E0B broadside periodic solver in this task.
