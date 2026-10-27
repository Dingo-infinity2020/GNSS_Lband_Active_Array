# R4-A0-E2A Pol-A Build Audit Recovery Freeze V0.1

Status: RECOVERY READY — AWAIT NEW BUILD AUTHORIZATION  
Date: 2026-09-28  
Recovery class: `NO_GEOMETRY_REDESIGN`

## 1. Formal HOLD being recovered

Formal attempt 1:

`HOLD_R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_ONLY`

Artifact:

`D:\GNSS_R4A0E2A_20260928_BUILD\R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_INTEGRATED_BUILD_ONLY_V01.cst`

SHA256:

`573e21e893a5b8fa9a76ae3c8d5dce641c672607c2747aa1ca39f9879b63c7fc`

Formal build attempt 1 remains HOLD and is not retroactively reclassified.

## 2. Sole failed predicate

Attempt 1 required each Pol-A prong to lose exactly the analytic four-cylinder volume:

`4*pi*(0.175 mm)^2*(1.0 mm) = 0.3848451000647496 mm^3`

within `1e-7 mm^3`.

CST measured:

- A_P: `0.38483724205539716 mm^3`
- A_N: `0.3848372420552977 mm^3`

All other automated gates passed.

## 3. Root cause proof

A disposable **complete project copy** of the canonical T1R1 parent was modified with only the exact eight frozen drill primitives, with no E2 copper, ports, local ground, or other production geometry.

Reference source:

`source/cst/R1E1A4A_AR0_B1R_R4_A0_E2A_DRILL_KERNEL_REFERENCE_V01.mcr`

Git blob:

`e7fe96e2e763fcc025ce45e874162d9c8a771f77`

Result:

`PASS_R4_A0_E2A_DRILL_KERNEL_REFERENCE`

The CST/ACIS-native reference produced:

- A_P final prong volume: `47.6151627579446 mm^3`
- A_N final prong volume: `47.6151627579447 mm^3`

Those values are **exactly identical** to the formal HOLD artifact.

Therefore:
- no drill is missing;
- no drill is partial;
- no drill is displaced by the integrated E2 geometry;
- the two branches are symmetric at the Boolean-volume level;
- the discrepancy is between analytic `pi*r^2*h` and the CST/ACIS Boolean-kernel volume representation.

Historical E1-V03 independently showed the same phenomenon for the same 0.175-mm drill primitive.

## 4. Frozen recovery rule

Do **not** loosen an analytic tolerance after seeing the result.

Instead, V02 uses a pre-production CST-native kernel reference:

1. verify canonical parent SHA;
2. create a disposable complete-project copy;
3. apply exactly the eight frozen drill primitives only;
4. fresh-reopen and measure A_P/A_N prong losses;
5. require reference integrity and branch symmetry;
6. clean the disposable reference project;
7. only then execute the unchanged formal E2 production macro;
8. require each production prong loss to match its CST-native reference within `1e-7 mm^3`.

The analytic `4*pi*r^2*h` value remains reported as diagnostic only.

If the kernel-reference preflight fails, production E2 History must not run and the formal build budget is not consumed.

## 5. Frozen production geometry remains unchanged

Production macro remains:

`source/cst/R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_ONLY_V01.mcr`

Git blob:

`9931736f1129624d94aee1c9e983a1eaabca5f24`

Inventory remains:

`execution/R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_INVENTORY_V01.json`

Git blob:

`e10886a4c01d9aafd55a16d8126418b7e22025fd`

Unchanged:
- canonical parent and SHA;
- 45 - 12 + 74 = 107 solid accounting;
- all coordinates;
- all 12 ports;
- four device-plane ports 2/3/8/9;
- all 8 via drill centers/radii;
- all 8 plated barrels;
- G-L0 local-ground topology;
- inactive Pol-B open-stub condition;
- 14 pairwise interference registry;
- whole-model intersection gate;
- History persistence;
- no solver.

## 6. Recovery runner

`scripts/run_r1e1a4a_ar0_b1r_r4_a0_e2a_pola_build_only_v02_recovery.py`

Git blob:

`a8f9183d7e4bb635ece3a5cc9e0edd30fb230502`

Static audit:
- `run_solver()` count = 0;
- complete-project copy used for both kernel reference and production artifact;
- kernel-reference gate executes before production History;
- old analytic hard gate absent;
- new CST-native hard gate present;
- comparison tolerance remains `1e-7 mm^3`;
- production macro and inventory unchanged.

## 7. Authorization boundary

`BUILD_AUTHORIZED = false`

`SOLVE_AUTHORIZED = false`

`LNA_INTEGRATION_AUTHORIZED = false`

A future V02 recovery build requires one new explicit BUILD authorization.

No solve follows automatically.
