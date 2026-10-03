# R4-A0-E1 Build HOLD Recovery Freeze V0.2

Status: ROOT CAUSE CONFIRMED / RECOVERY PREBUILD READY — NO BUILD / NO SOLVE AUTHORIZATION
Date: 2026-09-28
SimulationOps minimum: 0.2.10

Supersedes:
- docs/R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_HOLD_RECOVERY_FREEZE_V01.md

## 1. Formal V02 HOLD remains authoritative

The first formal V02 build is retained as:
HOLD_R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_ONLY

Protected artifact SHA256:
f5ee6fceab2c26db5d4d63365e37abec65b87698633c577e1ca87613b86a9745

It is not solve-eligible and will not be overwritten.

## 2. Root cause A — port/build persistence CONFIRMED

V02 production construction used direct schematic.execute_vba_code.

Evidence:
- the saved V02 Model/3D/Model.mod contains only the CST header and no geometry/port history;
- a full-project temporary copy plus direct execute_vba_code Port 99 fresh-reopens with PORT_COUNT=0;
- the same full-project temporary copy plus modeler.add_to_history Port 99 fresh-reopens with PORT_COUNT=1;
- the History case Model.mod explicitly contains TOOLING_DIAG_ADD_PORT_99 and the DiscretePort definition;
- historical R1A4 History-built artifacts likewise contain persistent DiscretePort commands.

Conclusion:
production geometry/ports must enter the 3D History List. Direct execute_vba_code is not an accepted production builder for this stage.

## 3. Root cause B — pairwise temporary-copy failure CONFIRMED

The V02 formal pairwise audit copied only the .cst file.

In that temporary project:
- target volume read as zero;
- Solid.Intersect returned -2147418113.

When the tooling probe copied the complete CST project state:
- .cst file plus same-stem companion directory;
- PIN2_RFIN volume before Boolean = 0.0037625 mm^3;
- Solid.Intersect(PIN2_RFIN, EXPOSED_PADDLE) returned Err.Number=0;
- the no-overlap result removed the target intersection object, so subsequent GetVolume object-not-found is interpreted as zero intersection volume only because the Boolean itself succeeded.

Conclusion:
pairwise audit copies must be complete project copies unless a .cst-only copy has separately proven self-contained reopen equivalence.

## 4. CST 2022.5 non-destructive query finding

On NW CST 2022.5 VBA automation:
Solid.DoTheseGeometricallyIntersect is not exposed; the probe returns Method or property not found.

Therefore V03 qualification uses:
1. CDCheckModelIntersections whole-model command;
2. complete-project-copy Solid.Intersect fallback for frozen forbidden pairs.

A Boolean Err.Number != 0 remains a tooling HOLD and cannot be interpreted as zero overlap.

## 5. V03 no-geometry-redesign source

Source:
source/cst/R1E1A4A_AR0_B1R_R4_A0_E1_ONE_LNA_LANDING_ZONE_BUILD_ONLY_V03.mcr

Static status:
PASS_R4_A0_E1_V03_STATIC_NO_GEOMETRY_REDESIGN

Macro blob:
8066f693f7a3ba980cf015ef5d9554fd31dc7549

V03 changes only build persistence semantics.
Frozen geometry, materials, vias, pads, routing and six port coordinates are unchanged from V02.

## 6. Recovery runner

Runner:
scripts/run_r1e1a4a_ar0_b1r_r4_a0_e1_v03_recovery_build.py

Runner blob:
a3e7bd8b9ce585f268d4cfbae834b01ed73ee5a1

Static status:
PASS_R4_A0_E1_V03_RECOVERY_RUNNER_STATIC_AUDIT

The runner:
- builds V03 through modeler.add_to_history;
- fresh-reopens;
- requires persistent Model.mod history;
- requires exactly 36 solids;
- requires six discrete ports plus properties/coordinates;
- runs CDCheckModelIntersections;
- uses complete project copies for ten destructive pairwise zero-positive-volume checks;
- verifies empty result tree and stable artifact hash;
- never starts a solver.

## 7. Recovery acceptance

A recovery build may PASS only if all of the following pass:
- persistent History List;
- exact 36-solid inventory/component/material set;
- exactly six ports;
- expected port properties and coordinates;
- drill tools consumed / four plated vias retained;
- whole-model intersection command returns;
- all ten forbidden pairwise positive-volume overlaps are zero;
- result tree empty;
- solver invocations = 0;
- fresh-reopen artifact hash stable.

## 8. Authorization boundary

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
LNA_INTEGRATION_AUTHORIZED = false

The V03 recovery build is ready to request a new one-shot BUILD-ONLY authorization.
No solve follows automatically.
