# R0 Gate Check — Figure Extraction Update

Status:

- **PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY**
- **HOLD_R0_MATERIALIZED_PARAMETERS_UNRESOLVED**

## Newly extracted from CHARTS Fig. 1(a)

Visible dimension labels:

- 227.5 mm
- 247.5 mm
- 40 mm

They remain `FIGURE_DERIVED_UNVERIFIED`.

The primary reconstruction hypothesis (Candidate A) maps:
- 227.5 mm -> active petal-envelope characteristic span,
- 247.5 mm -> surrounding passive-ring characteristic span,
- 40 mm -> central feed/electronics opening.

Candidate B (the two large labels swapped) remains documented and must stay reproducible until better source evidence is found.

## Topology-only placeholders

For **build visualization only**, with no solver permission:

- petal slit: 5 mm
- ring trace width: 10 mm
- visualization ground span: 1000 mm
- conductor model: zero-thickness PEC

These are `ASSUMPTION / TOPOLOGY_PLACEHOLDER`, not CHARTS dimensions and not EM-ready values.

## Materialized HOLD items

Still unresolved:

- PCB outer size
- substrate material
- substrate thickness
- copper thickness

Therefore no materialized CST model and no solver run are authorized.

## Next allowed action

Create a deterministic, parameterized **TOPOLOGY_BUILD_ONLY** geometry generator supporting both Candidate A and Candidate B.

The generator must:
- not contain solver commands,
- expose all placeholder values,
- produce a geometry/change manifest,
- stop after build.
