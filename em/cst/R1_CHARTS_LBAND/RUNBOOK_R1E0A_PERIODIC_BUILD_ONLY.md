# R1E0A Periodic Unit-Cell BUILD-ONLY Runbook

## Scope

Host:
NW

CST:
2022.5

Mode:
BUILD_ONLY / configuration-only

No solver is authorized.

## Input

Clean Pol-A R1A5F CST:

D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst

Required SHA256:
74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce

## Configuration

source/cst/R1E0A_PERIODIC_BROADSIDE_BUILD_ONLY_V01.mcr

Static audit:
scripts/audit_r1e0a_periodic_config.py

## Fresh work/evidence

Work:
D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work

Evidence:
evidence/r1e0a_dc_nw_20260924_build01/

Expected CST:
D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

## Runtime acceptance

After save and fresh reopen:

- port count = 1
- shape inventory exactly equals clean R1A5F Pol-A
- Xmin/Xmax/Ymin/Ymax = unit cell
- Zmin/Zmax = expanded open
- structure x span = 94 mm
- structure y span = 94 mm
- GetUnitCellScanAngle returns valid
- theta = 0 deg
- phi = 45 deg
- direction = +1 / outward
- no solver output exists
- no geometry or port changes

## PASS

PASS_R1E0A_PERIODIC_CONFIG_BUILD_ONLY

## Stop

Stop after fresh-reopen metadata verification.

Do not run R1E0B broadside solver in this gate.
