# SIM_EXECUTION

## Current stage
R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY

BUILD_AUTHORIZED: true — ONE FORMAL INVOCATION ONLY
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Frozen source
Parent: qualified bare P094 periodic source.
SHA256: fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e

## Authorized mutation
- remove existing one 100-ohm Pol-A differential discrete port;
- add one centered 10x10-mm underside H0 local-ground island;
- add exactly two 50-ohm single-ended P1A/P1B ports referenced to H0 ground;
- preserve 94-mm periodic geometry, radiator, substrate, top copper, boundaries and broadside scan;
- no support, shield, package, bias, output, transistor, solver or optimization.

## Formal build rules
- one invocation only;
- source hash lock before copy;
- fresh work/evidence directories;
- CST 2022 official `DiscretePort.GetProperties` and `GetCoordinates` used for port audit;
- fresh reopen must reproduce shape/port/periodic predicates;
- prior P094 evidence is byte-snapshotted and restored if CST history replay touches it;
- no solver markers or solver result tree.

## Stop boundary
After build closeout, BUILD authorization is consumed.
Broadside mixed-mode solve requires separate explicit authorization.
