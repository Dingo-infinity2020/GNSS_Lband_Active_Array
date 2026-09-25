# R1E1A4A-H1A OFFSET_GROUND_G2P0 Build/Solve Contract

Status: BUILD AUTHORIZED; ONE BROADSIDE SOLVE CONDITIONALLY AUTHORIZED AFTER BUILD PASS

## Scientific question
Does moving the same 10x10-mm local ground 2.0 mm away from the radiator underside recover the source impedance/noise environment without breaking the already-qualified P1 mixed-mode symmetry?

## Frozen geometry
- parent: qualified bare P094, SHA256 `fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e`;
- local-ground footprint: 10.0 x 10.0 mm;
- local-ground thickness: 0.035 mm;
- local-ground top: z = 55.142857143 mm;
- radiator substrate underside: z = 57.142857143 mm;
- air gap: 2.000 mm;
- two 50-ohm P1A/P1B discrete ports at unchanged terminal x/y coordinates;
- no carrier, daughterboard dielectric, package, shield, bias/output network or active device.

## Build gate
One formal build-only invocation on NW.
Fresh reopen must prove geometry, exact port coordinates/impedances, 94-mm unit cell, broadside scan and zero solver products.
No silent retry.

## Conditional broadside solve gate
Only if build canonical PASS:
- one formal broadside solve;
- use the already-qualified MaxPasses=12 HF tetrahedral configuration;
- extract full periodic 2-port S matrix;
- derive Sdd/Sdc/Scd/Scc and actual branch source impedances;
- apply unchanged mixed-mode Gate R and R-NF0 <= 0.40 dB;
- compare against both H0 V0.1 and old P0.

Stop after H1A broadside closeout. No scan continuation or H1B under this contract.
