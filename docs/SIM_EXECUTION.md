# SIM_EXECUTION

## Current stage
R1E1A4A_H0_P1_BROADSIDE_MIXEDMODE_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true — ONE BROADSIDE INVOCATION ONLY
PRODUCTION_SOLVE_AUTHORIZED: true — R1E1A4A BROADSIDE ONLY
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Locked source
Artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h0_p1_build_work\R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_V01.cst

SHA256:
d1ebb6f4a6e8b48f3484cc5459790dd5c9bbd29482832c491076c84f783b3deb

Canonical build status:
PASS_R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_READONLY_RECOVERY

## Solve scope
- broadside only;
- 2x50-ohm P1A/P1B source-facing ports;
- extract S11/S12/S21/S22;
- transform to Sdd/Sdc/Scd/Scc with frozen orthonormal mixed-mode convention;
- compare Sdd/Zdd against old P0 100-ohm differential broadside reference;
- apply frozen Gate-R mode-conversion and branch-symmetry limits;
- no carrier, shield, package, transistor or optimization.

Solver config:
source/cst/R1E1A4A_H0_P1_BROADSIDE_SOLVER_CONFIG_V01.mcr

Numerical configuration is identical to the qualified MaxPasses=12 recovery baseline.

## Stop boundary
Any HOLD stops.
No silent retry or MaxPasses increase.
After broadside qualification, do not continue to C60P45/C60P135 or any carrier study without new authorization.
