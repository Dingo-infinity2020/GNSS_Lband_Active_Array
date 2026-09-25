# SIM_EXECUTION

## Current stage
R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY

BUILD_AUTHORIZED: true — ONE H1A BUILD-ONLY INVOCATION
SOLVE_AUTHORIZED: false during build
SOLVE_AUTHORIZED_AFTER_BUILD_PASS: true — ONE H1A BROADSIDE INVOCATION
PRODUCTION_SOLVE_AUTHORIZED: conditional on H1A build PASS
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## H1A frozen geometry
- parent = qualified bare P094;
- 10x10x0.035-mm centered local ground;
- ground top = 2.000 mm below radiator substrate underside;
- two 50-ohm P1A/P1B ports at unchanged terminal x/y coordinates;
- no carrier, daughterboard dielectric, package, shield, bias, output or active transistor.

## Sequence
1. one formal BUILD-ONLY invocation with fresh reopen;
2. if and only if build canonical PASS, transition to one authorized broadside solve;
3. apply unchanged numerical/mixed-mode gates and R-NF0 <= 0.40 dB;
4. stop after H1A broadside closeout.

No C60P45/C60P135, H1B, carrier, shield/package or transistor work is authorized.
