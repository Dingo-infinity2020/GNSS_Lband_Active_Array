# SIM_EXECUTION

## Current stage
R1E1A4A_MIXEDMODE_BUILD_CONTRACT_READY

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Last closed EM gate
HOLD_R1E1A3_SUPPORT_SCIENCE_GATE_S1_C60P135_DELTA_Z

## R1E1A4A design/circuit closeout
PASS_R1E1A4A_INTERFACE_GATE_AUDIT

Frozen:
- Gate T unchanged;
- Gate R V0.1 frozen;
- H0 backside active-hub/local-ground interface;
- P1A/P1B two-single-ended-port receiver reference-plane concept;
- QPL9547 G0 noise and S-parameter reference data;
- carrier decomposition C0/C1/C2/C3.

Not yet qualified:
- the real P1 differential-to-branch mapping;
- mixed-mode Sdd/Scc/Sdc/Scd with H0 local ground;
- physical package/feed trace/shield;
- any new mechanical carrier.

## Next execution ticket
Draft:
docs/R1E1A4A_MIXEDMODE_BUILD_ONLY_CONTRACT_DRAFT.md

Planned first CST action after separate BUILD authorization:
- parent = qualified bare P094;
- add 10x10-mm underside H0 local ground;
- replace one 100-ohm Pol-A differential port by two 50-ohm P1A/P1B ports;
- no support, package, shield, transistor, solver or optimization;
- fresh-reopen BUILD-ONLY audit.

## Stop boundary
Await explicit BUILD authorization.
No CST execution is currently authorized.
No solve.
No S4 sentinel.
No R1E1B pitch screen.
No material A/B.
