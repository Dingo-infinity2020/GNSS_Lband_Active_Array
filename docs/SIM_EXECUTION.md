# SIM_EXECUTION

## Current stage
R1E1A4A_H1A_BROADSIDE_MIXEDMODE_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true — ONE H1A BROADSIDE INVOCATION
PRODUCTION_SOLVE_AUTHORIZED: true — H1A BROADSIDE ONLY
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## H1A build closeout
Formal status:
HOLD_R1E1A4A_H1A_BUILD_IN_SESSION_AUDIT_PERSISTENCE

Canonical status:
PASS_R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY_READONLY_RECOVERY

Artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h1a_build_work\R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY_V01.cst

SHA256:
b903d678a7039105ad4d91bea2f82e9c1e5e9f8bbf5a5977360c85e34ced3b94

Fresh-reopen geometry:
- 10x10x0.035-mm centered offset local ground;
- exact 2.000-mm air gap below radiator substrate;
- two 50-ohm P1A/P1B ports;
- port length 3.035 mm;
- 94-mm broadside periodic cell;
- no solver results.

## Authorized solve
- broadside only;
- qualified MaxPasses=12 numerical baseline;
- extract complete periodic 2-port;
- compare H1A vs H0 V0.1 and old P0;
- apply frozen mixed-mode Gate R;
- calculate actual branch QPL9547 R-NF0;
- no carrier, daughterboard dielectric, package, shield or transistor.

## Stop boundary
Stop after H1A broadside qualification.
No C60P45/C60P135 or H1B without new authorization.
