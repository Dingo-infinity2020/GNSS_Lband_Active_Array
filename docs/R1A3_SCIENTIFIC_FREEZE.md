# R1A3 Scientific Freeze — Materialized Aperture

Status: FROZEN FOR NW BUILD-ONLY

## Scientific question

R1A3 asks one question only:

> Can the accepted scaled CHARTS-inspired topology be converted from proxy geometry into a deterministic physical PCB/copper structure without changing the architecture or introducing a solver-dependent feed model?

It does not compare materials, optimize dimensions, validate impedance, or claim antenna performance.

## Frozen physical interpretation

Mechanical topology:
- one 70.714285714 mm square substrate,
- 12 disconnected through-slots (8 outer + 4 inner),
- substrate remains mechanically connected through corner/midpoint/bridge regions,
- board height above the 94 mm ground-reference plane is 57.142857143 mm.

RF copper topology:
- 35 um top conductor,
- same 12 through-slots,
- one project-owned four-arm center isolation cross,
- one project-owned continuous square-ring isolation gap,
- intended topology after isolation: outer passive ring + four central petal conductor regions.

The center cross and ring are each authored from exactly one master and three exact 90-degree CST Transform copies.

## Material decision for this gate

Only FR4_COST_BASELINE is materialized:
- epsilon_r = 4.2
- tan_delta = 0.018
- thickness = 1.00 mm

This is a manufacturability/cost baseline, not a selected final laminate.

RO4350B_REFERENCE is intentionally deferred. A two-material comparison before the port/solver contract is frozen would mix the material-loss question into the geometry-materialization gate.

Top conductor uses PEC in R1A3 BUILD_ONLY while retaining physical copper thickness = 0.035 mm. Finite conductivity becomes a solver-contract parameter later.

## Terminal/feed decision
R1A2 terminal coordinates remain frozen metadata:
- terminal_r = 3.00 mm
- terminal_len = 2.00 mm
- terminal_w = 1.60 mm
- Pol-A = NE/SW
- Pol-B = NW/SE

R1A3 creates no terminal PEC overlay, no physical pad, and no port.

Reason: the current gate should show only the physical materialized structure. The first physical/differential port model belongs to the next reviewed gate after the user has inspected the R1A3 CST artifact.

## Human CST review

The user has explicitly required the canonical R1A3 CST file for manual review.

Therefore:
- BUILD_ONLY may PASS,
- the CST artifact must remain protected on NW,
- no staging to CST251 is allowed,
- no solver gate may be opened,
until explicit human review is complete.

## Acceptance
Required:
- static source audit PASS,
- fresh CST build on NW,
- fresh reopen PASS,
- ground + substrate + top-copper geometry present,
- no slot/gap tool residue,
- exact-rotation construction present in source,
- 0 ports,
- no solver,
- canonical CST path/hash/bytes recorded,
- artifact lifecycle purge_allowed=false.

Final build status before human review:
PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
