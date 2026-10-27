# R4-A0-E2A Pol-A Build HOLD Handoff — 2026-09-28

Status: `HOLD_R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_ONLY`

Classification: `HOLD_BUILD_AUDIT_CRITERION`

## Formal execution

- formal build invocations: 1
- solver invocations: 0
- automatic retries: 0
- silent retry: none

Artifact:

`D:\GNSS_R4A0E2A_20260928_BUILD\R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_INTEGRATED_BUILD_ONLY_V01.cst`

SHA256:

`573e21e893a5b8fa9a76ae3c8d5dce641c672607c2747aa1ca39f9879b63c7fc`

Lifecycle:
`PROTECTED_HOLD_PENDING_RECOVERY`

## What passed

- exact canonical parent SHA and complete companion project;
- 107 solids after fresh reopen;
- exact 107-name set and exact component counts;
- preserved parent signatures except the two intentionally drilled Pol-A prongs;
- 12 discrete ports with exact 50-ohm properties and coordinates;
- persistent History List through port 12;
- eight plated vias with expected CST volumes;
- eight drill tools consumed;
- empty solver result tree;
- fresh-reopen artifact hash stable;
- CDCheckModelIntersections returned with Err=0;
- 14/14 complete-project-copy Solid.Intersect checks returned Err=0 and zero positive-volume overlap;
- all eight via barrels have zero positive-volume overlap with their drilled FR4;
- both local backside grounds have zero positive-volume overlap with Pol-B prongs and Pol-B lower body;
- analytic cross-pol envelope also predicts zero positive-area overlap.

## Sole HOLD predicate

Frozen runner required the volume removed from each Pol-A prong by four 0.35-mm drills to equal the analytic cylinder value

`4*pi*(0.175 mm)^2*(1.0 mm) = 0.3848451000647496 mm^3`

within `1e-7 mm^3`.

Measured CST/ACIS losses:

- A_P: `0.38483724205539716 mm^3`
- A_N: `0.3848372420552977 mm^3`

The two branches agree to approximately `1e-13 mm^3`, but differ from the analytic formula by about `7.858e-6 mm^3` (20.4 ppm), so the frozen gate correctly forced HOLD.

## Attribution evidence

Previously accepted E1-V03 used the same 0.175-mm CST cylinder drill semantics.

Its 4 x 10 x 1 mm FR4 coupon changed from 40 mm^3 to 39.6151607557998 mm^3, corresponding to a CST Boolean drill loss of:

`0.3848392442002009 mm^3`

This already differs from the same analytic four-cylinder volume by about `5.856e-6 mm^3` (15.2 ppm).

Therefore an exact analytic `pi*r^2*h` equality at `1e-7 mm^3` is not a qualified CST/ACIS Boolean predicate.

This does **not** retroactively convert the formal E2A result to PASS. SimulationOps forbids changing a frozen gate after seeing the result.

## Recovery boundary

Recovery must be `NO_GEOMETRY_REDESIGN`.

Do not change:
- parent;
- E2A macro geometry;
- via radius / inner radius / locations;
- ports;
- local-ground topology;
- 107-solid inventory;
- interference pair registry.

Only the drill-volume audit semantics may be replaced with a pre-frozen kernel-aware / structural qualification.

A new formal build, if required for PASS, needs a new explicit BUILD authorization.

No solve is authorized.
