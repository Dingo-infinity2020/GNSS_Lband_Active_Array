# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1E0A_PERIODIC_CONFIG_BUILD_ONLY

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Host/toolchain

Host: NW / DESKTOP-GBTI6Q4
CST: 2022.5
Runtime: CST bundled Python 3.6 / cst.interface
Mode: BUILD_ONLY / configuration-only

## Immutable source

D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst

SHA256:
74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce

## R1E0A periodic configuration

- square unit cell
- nominal pitch = 94 mm via UnitCellFitToBoundingBox
- Xmin/Xmax/Ymin/Ymax = unit cell
- Zmin/Zmax = expanded open
- OpenAddSpaceFactor = 0.5
- PeriodicUseConstantAngles = False
- theta = 0 deg
- phi = 45 deg
- direction = outward
- UnitCellAngle = 90 deg
- no explicit UnitCellOrigin override
- no Floquet ports
- existing differential discrete port retained
- HF Frequency Domain selected
- no solver start

## Verified CST API source

Installed CST macro:
D:\Program Files (x86)\CST Studio Suite 2022\Library\Macros\Solver\F-Solver\Change settings from Full Array to Unitcell^+MWS.mcr

R1E0 copies only the boundary/scan metadata relevant to a discrete-port-driven antenna. The Floquet-port and parameter-sweep sections of the installed macro are intentionally not copied.

## Paths

Work:
D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work

Evidence:
evidence/r1e0a_dc_nw_20260924_build01/

Expected CST:
D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

## Stop boundary

Fresh reopen + periodic metadata verification only.

No solver.
No R1E0B broadside solve.
No scan sweep.
No pitch/material/LNA work.
