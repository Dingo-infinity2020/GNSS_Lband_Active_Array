# SIM_EXECUTION

## Current stage
R1E1A4A_H1_LOCAL_GROUND_REDESIGN_DESIGN

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Closed H0/P1 broadside solve
Formal harness status:
HOLD_R1E1A4A_H0_P1_BROADSIDE_POSTPROCESS_RESULT_PATH

Canonical science status:
HOLD_R1E1A4A_H0_P1_GATE_R_RNF0

Formal solve invocation count: 1
Solver rerun: NO

Solved artifact SHA256:
a95e18b66d5000b034807455c368abdf9b831e2c1395427edb33bd6de73fafab

Numerical qualification: PASS.
Mixed-mode Gate-R subchecks: PASS.
- max |Sdc| = -42.3768 dB;
- max |Scd| = -42.3671 dB;
- max branch magnitude imbalance = 0.14287 dB;
- max branch phase error = 0.37636 deg.

Receiver R-NF0: FAIL.
- P1A max source-conditioned QPL9547 NF = 0.5646 dB;
- P1B max = 0.5684 dB;
- frozen limit = 0.40 dB;
- failure begins near 1.386–1.387 GHz and persists through 1.6496 GHz.

The H0/P1 reference-plane concept is retained; the continuous same-board 10x10-mm local ground is rejected as the next physical baseline.

## Next design
Primary plan:
docs/R1E1A4A_H1_LOCAL_GROUND_REDESIGN_PLAN.md

First proposed candidate:
H1A_OFFSET_GROUND_G2P0
- same 10x10-mm local-ground footprint;
- move local-ground top surface 2.0 mm below the radiator-substrate underside;
- preserve two 50-ohm P1A/P1B reference ports;
- no support, daughterboard dielectric, package, shield or transistor;
- BUILD-ONLY first after separate authorization.

## Stop boundary
DESIGN ONLY.
No H1A build or solve.
No follow-on scan solve.
No carrier/shield/package/transistor.
No R1E1B pitch screen.
