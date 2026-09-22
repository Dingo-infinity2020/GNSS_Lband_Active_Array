# R0 Reconstruction Assumptions

Status: **PROPOSED, EXPLICIT, REVERSIBLE**

This file defines assumptions permitted for the first topology-only build.
They are not literature facts.

## A. Split R0 build into two permissions

### R0.1A — TOPOLOGY_BUILD

Purpose:
- validate scripts, symmetry, conductor connectivity, feed gap, object naming and geometry bookkeeping.

Allowed simplifications:
- zero-thickness PEC sheets,
- no dielectric substrate,
- finite ground plane represented by a simple PEC sheet,
- no active PCB,
- no shield,
- no solver.

Required:
- 200 mm height over ground,
- four-petal topology,
- passive surrounding square ring,
- explicit central feed/electronics opening,
- all ambiguous dimensions remain parameters.

### R0.1B — MATERIALIZED_BUILD

Purpose:
- instantiate dielectric/copper thickness and prepare the passive EM model.

Requires additional approved assumptions or source evidence for:
- substrate,
- substrate thickness,
- copper thickness,
- ground-plane extent.

Still no solver until a separate SOLVER permission.

## B. Primary reconstruction hypothesis

Candidate A from `FIGURE_EXTRACTION.md` is the preferred first topology hypothesis:

- smaller 227.5 mm characteristic span -> active petal envelope,
- larger 247.5 mm characteristic span -> surrounding passive ring,
- 40 mm -> central removed/feed-region characteristic span.

This is tagged `ASSUMPTION_FROM_FIGURE` in discussion and remains
`FIGURE_DERIVED_UNVERIFIED` in the parameter manifest.

Candidate B must remain reproducible by a single configuration switch.

## C. Geometry family, not a single hidden drawing

The topology generator must expose at least:

- `petal_span`
- `ring_span`
- `center_opening`
- `petal_slit`
- `ring_trace_width`
- `pcb_span`
- `ground_span`
- `height_ground`

The exact petal polygon must be represented by named vertices/ratios, not a hand-edited opaque sketch.

## D. No performance fitting

No value may be adjusted to improve S11/beamwidth during R0.1A.

If the topology build looks unlike the publication, record HOLD and revise provenance/interpretation before any solver work.
