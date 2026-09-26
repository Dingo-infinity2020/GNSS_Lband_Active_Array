# CHARTS Figure Extraction — R0.0 / R0.1A3

Status: **PHOTO-CONSTRAINED TOPOLOGY; DIMENSIONS STILL PARTLY UNRESOLVED**

Primary source:
- Lau et al., "Active Planar Antenna Design for CHARTS Array", ISAP 2025
- Fig. 1(a): simulation model
- Fig. 2(a): fabricated active antenna

## Paper-explicit constraints

The paper explicitly states:
- square PCB layout,
- "4-petal" square antenna concept,
- passive ring structure around the antenna,
- center low-field region may accommodate feed/electronics,
- antenna height over ground = 200 mm,
- balanced output directly feeding a pair of LNAs,
- local ground beneath feed points and clip-on shield in the active implementation.

These facts do not uniquely define the slot dimensions.

## Visible Fig. 1 labels

The figure visibly contains:
- 227.5 mm,
- 247.5 mm,
- 40 mm.

All remain `FIGURE_DERIVED_UNVERIFIED`.

Current semantic interpretation:
- 247.5 mm -> square board/aperture span hypothesis,
- 227.5 mm -> opposing outer-slot centerline-frame span hypothesis,
- 40 mm -> **SEMANTICS_UNRESOLVED**.

The 40 mm label is deliberately not used as a V0.3 center-clear dimension.

## Direct Fig. 2 topology review

The fabricated board visibly contains **12 disconnected elongated slot segments**:

### Outer slot family
- 8 total,
- two segments per board side,
- a conductor bridge remains at every side midpoint,
- conductor remains at the four corners.

### Inner slot family
- 4 total,
- one radial segment along each +/-X and +/-Y direction,
- inner slots stop before the center electronics region,
- inner slots stop before the outer slots.

Therefore:
- V0.1 four-separate-petal model is rejected,
- V0.2 one-outer-slot-per-side model is also rejected,
- V0.3 is the current photo-constrained topology.

## V0.3 figure-derived metric hypothesis

See `PHOTO_GEOMETRY_ESTIMATE.md`.

Current topology-only values:
- board span: 247.5 mm,
- outer slot frame span: 227.5 mm,
- outer slot width: ~5 mm,
- 8 outer slot segment lengths: ~94.125 mm each,
- midpoint conductor bridge: ~18 mm,
- inner slot width: ~9 mm,
- inner slot length: ~73 mm,
- visible center clear span: ~60 mm,
- total slot count: 12,
- no large central through-hole.

The slot-width/length values are photo-derived estimates with finite uncertainty and are not solver-ready literature truth.

## Still unresolved

- exact meaning of the 40 mm Fig.1 label,
- exact active-feed cutout/copper geometry under the electronics,
- substrate material and thickness,
- copper thickness,
- detailed feed terminal geometry.

## Gate consequence

Allowed:
- V0.3 12-slot BUILD-ONLY,
- visual/replay review.

Not allowed:
- materialized dielectric model,
- ports,
- solver,
- optimization,
- L-band scaling,
- LNA integration.
