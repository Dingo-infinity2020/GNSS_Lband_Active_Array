# CST R0 — CHARTS 300–500 MHz Passive Reconstruction

## Current status

**NO MODEL COMMITTED YET. BUILD-ONLY PLAN.**

The first executable model must be generated from the parameter manifest rather than hand-edited without provenance.

## Intended model contents

- finite ground plane,
- 200 mm support height,
- four-petal planar conductor,
- passive surrounding ring,
- center differential feed gap,
- ideal differential port,
- open/free-space boundaries suitable for isolated-element characterization.

Explicitly excluded:
- QPL9547,
- active PCB,
- Bias-Tee,
- RF shield,
- periodic boundaries,
- array scan,
- L-band scaling.

## Proposed CST workflow

1. create parameterized geometry only;
2. save a build report with object count, materials, bounding boxes and feed-gap checks;
3. export geometry snapshot / parameter manifest;
4. STOP;
5. human visual review;
6. only then enable the passive solver.

## Build-only acceptance

- no solver run,
- fourfold intended geometry symmetry documented,
- no metal short across the differential feed,
- ring and petals are separate conductive objects where intended,
- ground plane is parallel to radiator plane,
- radiator-to-ground distance = 200 mm,
- every nontrivial dimension has provenance,
- no inferred dimension is labeled PAPER_EXPLICIT.

## Solver acceptance (later)

The first solver run is a reconstruction sanity check, not an optimization.

Published comparison anchors:
- S11 trend at 300/400/500 MHz,
- E/H beamwidth trend,
- broad hemispherical response,
- published gain trend.

Failure to reproduce the paper triggers an uncertainty review; it does not permit silent geometry fitting.
