# R1E1A4A-H2A Universal Passive/Active Center Structure V0.1

Status: BUILD-ONLY AUTHORIZED; NO SOLVE AUTHORIZATION

Purpose:
Create a manufacturable, visually reviewable center assembly shared by future passive and active variants before any further RF optimization.

This stage supersedes H1A as the PRODUCT-ARCHITECTURE mainline. H1A remains diagnostic evidence that local-ground coupling is a first-order variable.

## Literature-derived architecture rules

The project adopts only broad engineering patterns, not unpublished dimensions:
- CHARTS: feed electronics and a small local ground belong at the center feed region; a metallic shield is part of the active implementation.
- SKALA-class aperture elements: LNA/feed hardware is treated as a dedicated feed-point assembly designed together with mechanics and testability.
- EMBRACE: the low-loss pre-LNA feed board is physically fixed to the radiator; assembly features are RF-relevant.

H2A dimensions below are PROJECT_DESIGN for review and are not claimed to reproduce any literature antenna.

## V0.1 shared PCB-side topology

Parent: immutable R1E1A1 P094 bare radiator source.

Backside feed-module geometry:
- no H1A 2-mm offset ground;
- copper is directly on the radiator-substrate underside;
- patterned local-ground frame outer span = 20.0 mm;
- central square RF clearance = 8.0 x 8.0 mm;
- copper thickness = existing 0.035 mm;
- four signal landing pads = 0.90 x 0.90 mm;
- four vertical RF pin/via proxies = 0.30 x 0.30 mm;
- signal centers inherit the exact four terminal centers at radius 3.0 mm.

The center clearance deliberately keeps continuous ground away from the four terminal projections. The surrounding ground frame provides the future shield/LNA/bias/output return region.

## Population envelope

H2A contains no active device model.

For mechanical review only:
- four dummy LNA package envelopes;
- each envelope = 2.0 x 2.0 x 0.60 mm;
- package centers lie on the four diagonal feed axes at radius 6.2 mm;
- package bodies extend downward from the backside copper plane;
- these are non-authoritative placeholders for a QPL9547-class package footprint.

Future passive variant: leave these positions unpopulated and use the same signal landing pads for probe/test fixtures.
Future active variant: populate the same mechanical positions after H2B feed-transition definition.

No RF trace geometry, matching network, package lead model, bias network, output network, transistor or optimization is introduced in H2A.

## Shield and carrier envelope

Shield-can envelope:
- square outer span = 18.0 mm;
- nominal wall thickness = 0.50 mm;
- wall depth below PCB = 6.0 mm;
- nominal lid thickness = 0.30 mm;
- PEC is used as a manufacturable metal-envelope proxy.

Mechanical carrier:
- material label = `PEEK_VISUAL_SURROGATE`;
- square hollow tube, outer span = 30.0 mm;
- inner opening = 21.0 mm;
- runs from the main backplane top plane to the radiator PCB underside;
- the shield fits inside the carrier opening with clearance;
- the hollow core is reserved for RF/DC service routing.

The carrier is intentionally outside the feed/shield volume rather than occupying the center field region.

## H2A build-only acceptance

Fresh reopen must verify:
- parent P094 radiator, substrate and main backplane remain present;
- old ideal differential port removed; total port count = 0;
- exactly one fourfold patterned-ground frame family;
- exactly four signal pads and four RF pin/via proxies;
- exactly four dummy package envelopes;
- shield = four walls plus one lid;
- carrier = four PEEK wall solids;
- exact 94-mm unit cell and broadside metadata remain unchanged;
- zero solver-generated S-parameter/adaptive-mesh results;
- no transistor, bias, matching-network or optimization geometry.

## Stop boundary

BUILD ONLY.
After PASS, stop for human 3D review.
No H2A solve.
No H2B/H2C build.
No H1R numerical recovery solve.
No carrier/material optimization.
