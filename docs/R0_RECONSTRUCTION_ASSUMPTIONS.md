# R0 Reconstruction Assumptions

Status: **V0.3 PHOTO-CONSTRAINED / EXPLICIT / REVERSIBLE**

## Current question

Can we construct a topology that matches the fabricated CHARTS board closely enough to justify moving toward a materialized passive model?

R0.1A3 does not answer any S-parameter or radiation question.

## V0.3 model

Build-only model consists of:
- one continuous square PEC proxy antenna plate,
- 8 disconnected outer slot segments,
- 4 disconnected inner radial slot segments,
- one reference ground,
- 200 mm vertical separation.

No central through-hole is introduced.

## Figure-derived topology values

- board span = 247.5 mm,
- outer-slot centerline frame = 227.5 mm,
- outer slot width = 5 mm,
- outer segment length = 94.125 mm,
- side-midpoint bridge = 18 mm,
- inner slot width = 9 mm,
- inner slot length = 73 mm,
- inner center-clear span = 60 mm.

The 40 mm Fig.1 label remains `SEMANTICS_UNRESOLVED`.

## Connectivity invariants

A valid build must satisfy all:

1. antenna remains one connected solid,
2. exactly 12 disconnected slot apertures are subtracted,
3. 8 outer slots = two per side,
4. every side has a midpoint conductor bridge,
5. corner conductor bridges remain,
6. 4 inner slots stop before center,
7. 4 inner slots stop before outer slots,
8. no slot aperture intersects another,
9. no large central through-hole,
10. height above ground remains 200 mm.

## Materials

R0.1A3 uses a PEC proxy only.

Materialized build remains HOLD pending:
- substrate material,
- substrate thickness,
- copper thickness,
- feed-region stack/geometry.

## No fitting

Photo-derived values may be revised only by a documented image/provenance review.

They may not be tuned to improve S11, beamwidth, gain, or any other solver quantity during R0.1A3.
