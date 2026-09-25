# SIM_EXECUTION

## Current stage
R1E1A4A_H0_P1_BROADSIDE_SOLVE_DESIGN

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Closed build
Formal status:
HOLD_R1E1A4A_H0_P1_BUILD_AUDIT_VBA_RESERVED_WORD

Canonical status:
PASS_R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_READONLY_RECOVERY

Formal build invocation count: 1
Build rerun: NO
Solver run: NO

Qualified artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h0_p1_build_work\R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_V01.cst

SHA256:
d1ebb6f4a6e8b48f3484cc5459790dd5c9bbd29482832c491076c84f783b3deb

Qualified invariants:
- 4 solids including one 10x10x0.035-mm H0 local ground;
- exactly two 50-ohm SParameter ports;
- exact +/-180-degree P1A/P1B terminal symmetry;
- 94-mm periodic cell and broadside preserved;
- no solver markers or solver result tree.

## Next design ticket
Solve contract draft:
docs/R1E1A4A_H0_P1_BROADSIDE_SOLVE_CONTRACT_DRAFT.md

Solver config draft:
source/cst/R1E1A4A_H0_P1_BROADSIDE_SOLVER_CONFIG_V01.mcr

The future first solve is broadside only and must extract the complete 2-port S matrix before mixed-mode conversion.

## Stop boundary
Await explicit SOLVE authorization.
No build rerun.
No CST solve.
No support carrier.
No shield/package/transistor.
No R1E1B pitch screen.
