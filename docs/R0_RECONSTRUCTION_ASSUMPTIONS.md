# R0 Reconstruction Assumptions

Status: **V0.2 PROPOSED / EXPLICIT / REVERSIBLE**

## A. Gate split

### R0.1A2 — SLOTTED_TOPOLOGY_BUILD

Purpose:
- validate the corrected Fig. 2 topology only.

Allowed:
- PEC proxy plate,
- simple reference ground,
- eight rectangular slot cutters,
- boolean subtraction,
- topology placeholders,
- build-only and fresh-reopen audit.

Forbidden:
- ports,
- solver,
- substrate/material claims,
- LNA/shield/Bias-Tee,
- L-band scaling,
- optimization.

### R0.1B — MATERIALIZED_BUILD

Still requires approved source/assumptions for:
- substrate material,
- substrate thickness,
- copper thickness,
- detailed center feed/copper implementation.

## B. Candidate C topology

The next build uses:
- square continuous plate span: 247.5 mm,
- outer-slot frame characteristic span: 227.5 mm,
- central retained solid/electronics region: 40 mm,
- 200 mm height above ground.

The plate is cut by:
- four disconnected perimeter slots,
- four disconnected inner slots.

The central region stays solid in the topology build.

## C. Topology-only placeholders

The following are not literature dimensions and must not be used for solver claims:

- slot width,
- outer-slot end/corner bridge,
- inner-to-outer slot bridge,
- PEC proxy thickness,
- visualization ground span.

They exist only to produce a Fig. 2-like connected topology for human review.

## D. Connectivity invariant

A valid V0.2 topology must satisfy:

1. antenna plate remains one connected solid after all eight cuts,
2. no slot touches another slot,
3. no outer slot reaches a board edge/corner,
4. no inner slot reaches the central solid region,
5. no inner slot reaches an outer slot,
6. no central through-hole exists.

If any invariant fails, return HOLD before any solver work.

## E. No performance fitting

No parameter may be adjusted to improve S11/gain/beamwidth during R0.1A2.

Visual/topological correction is allowed only against the published figure and must be documented.
