# R0.1A3 Design Review — 12-slot topology build-only

Date: 2026-09-22
Branch: `project/r0-charts-scaffold`
Reviewed host return: `0054b52a09b435336e4e4ca1812e35724b313ff1`
Evidence commit: `20303c587061c29a23d76da590b132df60a85c4e`

## Decision

`FINAL_REVIEW_STATUS=ACCEPT_R0_V03_12SLOT_TOPOLOGY_BUILD_ONLY`

The H01 return for `R0.1A3-12SLOT-BUILD-ONLY-H01` is accepted as valid build-only evidence.

Accepted evidence includes:

- preflight manifest gate PASS;
- V0.3 static audit PASS;
- exact committed V0.3 macro replayed without geometry edits;
- 2 final solids after boolean operations;
- all 12 slot cutters consumed;
- 8 outer slot segments + 4 inner radial slots;
- no solver, port, lumped element, monitor, mesh or result output;
- save/close/fresh-reopen inventory preserved;
- plate volume equals full plate minus the twelve independent slot volumes;
- top/side/oblique visual checks PASS;
- 200 mm radiator-to-ground spacing preserved;
- `fig40_unresolved=40` preserved without reinterpretation.

The rejected first Save-As path entry noted by the host is operational only and does not affect the scientific acceptance of the saved/reopened model.

## What is now frozen

The following is accepted as the current **visible V0.3 topology baseline**:

- square plate span hypothesis: 247.5 mm;
- outer-slot frame span hypothesis: 227.5 mm;
- 8 outer slot segments, 2 per side;
- side-midpoint conductor bridge on all 4 sides;
- corner conductor bridges retained;
- 4 inner radial slots;
- inner slots stop before the centre and before the outer family;
- no large central through-hole;
- radiator plane 200 mm above the reference ground.

This freezes the topology for the next provenance step. It does **not** upgrade figure-derived dimensions to paper-explicit truth.

## Why solver is still blocked

R0.1A3 proves deterministic construction of the visible slot topology only. It does not yet define a physically defensible balanced feed model.

The primary source explicitly says that:

- the antenna is a printed/PCB planar dipole-derived structure;
- a small central area may be removed to accommodate feed points/electronics;
- the output is naturally balanced and directly feeds a pair of LNAs;
- the height over ground is 200 mm.

But the repository still lacks a resolved, source-traceable definition of:

- the exact central removed/feed-region topology;
- the geometric meaning of the visible Fig.1 `40 mm` label;
- the terminal locations and differential gap geometry;
- substrate material/thickness and copper thickness;
- the full-scale ground-plane lateral size.

Therefore a solver run now would force an unreviewed feed topology or material assumption. That would violate the R0 provenance rules.

## Next gate

Proceed to:

`R0.1B-CENTER-FEED-PROVENANCE-H01`

Purpose: perform a source/figure extraction focused only on the central feed region and the Fig.1 40 mm label, without CST solver/build changes.

The next task is defined in:

`docs/NEXT_ACTION_R0_1B_CENTER_FEED_PROVENANCE_20260922.md`

## Permissions after this review

- literature/provenance extraction: YES
- figure-derived measurement with explicit uncertainty: YES
- CST geometry modification: NO for the next task
- CST solver: NO
- optimization: NO
- L-band scaling: NO
- LNA integration: NO
- hardware: NO
