# R1E0C-A Scan-State BUILD-ONLY Runbook

Status: DESIGN ONLY — BUILD NOT AUTHORIZED

## Purpose

Create four immutable scan-state CST variants from the qualified clean periodic source.

No solver.

## Source

D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

## States

- C30P45: theta=30, phi=45
- C45P45: theta=45, phi=45
- C60P45: theta=60, phi=45
- C60P135: theta=60, phi=135

Direction:
outward

## Allowed change

Only:
- R1E0_scan_theta_deg
- R1E0_scan_phi_deg
- SetPeriodicBoundaryAngles using those parameters
- scan direction remains outward

Forbidden:
- boundary type changes
- pitch/cell-size changes
- geometry/material/port changes
- solver settings
- solver start
- Floquet-port changes

## Future fresh paths

Work:
D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_work

Evidence:
evidence/r1e0c_dc_nw_20260924_build01/

## Runtime acceptance per state

- pre-copy SHA equals R1E0A source SHA
- geometry inventory equals R1E0A
- port count = 1
- X/Y = unit cell
- Z = expanded open
- UnitCellDs1/2 = 94 mm
- UnitCellAngle = 90 deg
- scan query succeeds
- scan valid = nonzero
- theta/phi exactly match state
- direction = outward
- no solver output
- fresh reopen repeats the same result

## PASS

PASS_R1E0C_SCANSTATE_BUILD_ONLY

## Stop

Build/fresh-reopen only.

No scan solver is included in this runbook.
