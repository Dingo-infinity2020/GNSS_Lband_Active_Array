# R4-A0-E1 Build HOLD Recovery Freeze V0.1

Status: RECOVERY DESIGN FROZEN — NO BUILD / NO SOLVE AUTHORIZATION
Date: 2026-09-28
Parent HOLD:
- docs/R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_HOLD_HANDOFF_20260928.md
- execution/result_packets/R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_HOLD_20260928_result.json

## 1. Root-cause evidence

The first formal V02 build produced the exact 36-solid inventory, exact materials, consumed via drill tools, four plated vias, empty result tree, and a fresh-reopen-stable project hash.

However:
- expected discrete ports = 6;
- observed after fresh reopen = 0;
- all ten temporary-copy `Solid.Intersect` qualification calls returned the same CST automation error `-2147418113`.

The V02 saved project `Model/3D/Model.mod` contains only the nine-line CST header and no build history.
By contrast, the historical R1A4 artifact that fresh-reopened with two ports contains full geometry history plus explicit `DiscretePort` history entries.

Therefore the primary recovery hypothesis is:
**V02 used `prj.schematic.execute_vba_code(macro_text)` for production construction rather than the persistent 3D History List.**
The database state was saveable enough to preserve solids, but the build was not represented as replayable model history and discrete ports did not persist.

## 2. Boolean-audit evidence

The destructive temporary-copy `Solid.Intersect` technique is not globally invalid.
Historical D2-M0 recovery used the same technique and returned:
- `intersect_err=0` for genuine zero-overlap pairs;
- positive intersection volume (~0.049 mm^3) for two real ground/stalk interferences.

Therefore the uniform V02 `0x8000FFFF` response is a tooling/model-state HOLD, not proof of ten simultaneous geometry failures.

## 3. Recovery invariant: no geometry redesign

V03 SHALL NOT change:
- coupon dimensions;
- substrate/copper/material values;
- QPL9547 land geometry;
- paddle/spoke geometry;
- via drill/final-hole geometry;
- C_IN/C_OUT/L1/C_RF pad locations;
- signal/bias routing;
- six port coordinates/reference impedances;
- expected 36-solid inventory.

V03 changes only production-build persistence semantics.

## 4. V03 persistent source

Source:
`source/cst/R1E1A4A_AR0_B1R_R4_A0_E1_ONE_LNA_LANDING_ZONE_BUILD_ONLY_V03.mcr`

V03 is flattened: it contains no helper subroutines.
The body between `Sub Main()` and `End Sub` is suitable for one deterministic:

`project.modeler.add_to_history("R4-A0-E1 persistent V03 build", body)`

Direct `schematic.execute_vba_code` is prohibited for production construction.

## 5. Mandatory recovery qualification

Before a recovery build can PASS, fresh reopen must prove:
1. `Model/3D/Model.mod` contains the named V03 history entry / source commands;
2. exact 36-solid inventory and component counts;
3. exact material identities;
4. exactly six discrete ports;
5. `DiscretePort.GetProperties` succeeds for ports 1..6;
6. `DiscretePort.GetCoordinates` matches the frozen six endpoint pairs;
7. four drill tools consumed and four annular barrels remain;
8. result tree empty and solver launch count zero;
9. project hash stable after read-only reopen/audit.

## 6. Intersection qualification hierarchy

Use:
1. CST built-in `CDCheckModelIntersections` after fresh reopen;
2. a non-destructive pair query such as `Solid.DoTheseGeometricallyIntersect` / equivalent, **only after CST 2022 host-level API support is verified**;
3. temporary-copy destructive `Solid.Intersect` only as fallback.

For destructive fallback:
- `Err.Number != 0` is a tooling HOLD;
- reported zero volume after an errored Boolean is NOT zero-overlap evidence.

Intentional contacts remain separately allowlisted.
Forbidden signal-ground and via-FR4 positive-volume overlaps must be zero.

## 7. Authorization boundary

Current:
- BUILD_AUTHORIZED = false
- SOLVE_AUTHORIZED = false
- recovery retry authorized = false

The first formal build budget is consumed.
A V03 recovery build requires a new explicit user authorization after:
- V03 static equivalence audit;
- CST 2022 non-destructive intersection API probe, or a frozen fallback;
- recovery runner freeze.

No solve may follow automatically.
