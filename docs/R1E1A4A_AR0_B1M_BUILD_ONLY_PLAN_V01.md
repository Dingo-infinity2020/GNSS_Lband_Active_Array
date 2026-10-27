# AR0-B1M Full Mechanical Stalk Build-Only Plan V0.1

Status: BUILD AUTHORIZED BY USER; SOLVE FORBIDDEN

Authority:
docs/R1E1A4A_AR0_B1M_FULL_MECHANICAL_STALK_FREEZE_V01.md

Parent:
B0G artifact SHA256 6b027162dd93d8613a0943df0fd96d6bf65d6721893e49c8d8bdc17f8f5eb698

Build actions:
1. verify B0G artifact hash;
2. preserve the full B0G feed head unchanged;
3. add two FR4 lower stalk bodies;
4. cut complementary half-depth center interlock;
5. add four upper mechanical rails;
6. add four top FR4 tenons and cut four radiator mortises plus copper-clearance windows;
7. add four bottom FR4 tenons and cut four reflector slots;
8. fresh reopen and inventory;
9. run deterministic coordinate/volume/collision audit;
10. stop.

No RF port.
No transistor model.
No matching network.
No solver.
No retry.

The B0 abrupt ground onset remains a placeholder and is not RF-qualified in this stage.

## Pre-build coordinate correction

Because B0 stalks use local n=-1..0 mm rather than a centered board thickness:
- A interlock slot u = -0.125..+1.125 mm;
- B interlock slot u = -1.125..+0.125 mm;
- top/bottom mortise n clearance = -1.125..+0.125 mm.

These corrections are frozen before the formal B1M build and do not change B0G RF geometry.
