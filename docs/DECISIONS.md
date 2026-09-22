# Design Decision Log

## D0001 — Preserve two independent linear polarizations

Decision:
- Generation 1 outputs X and Y independently.
- No analog 90-degree hybrid before digitization.

Reason:
- preserve calibration freedom,
- enable digital RHCP/LHCP,
- preserve polarization/multipath information,
- avoid unnecessary pre-LNA loss.

Reversal condition:
- a later system-level study demonstrates a compelling cost/power advantage that outweighs the scientific and calibration loss.

## D0002 — Treat QPL9547 as reference, not final selection

Decision:
- QPL9547 remains the reference LNA through early circuit modeling.
- Production selection remains open.

Reason:
- strong noise parameters,
- relevant differential-radio-astronomy precedent,
- good linearity.

Reversal condition:
- another device demonstrates equal or lower receiver noise over the actual source-impedance locus with better cost/power/integration.

## D0003 — CHARTS-inspired balanced planar element is current mainline

Decision:
- use CHARTS-inspired planar petal/ring architecture as the current reconstruction/mainline research path.
- keep PUMA / unbalanced TCDA as first backup.

Reason:
- planar/low-cost construction,
- feed-point active electronics,
- no required pre-LNA balun,
- strong alignment with project manufacturability goals.

Reversal condition:
- R1/R2/R3 evidence shows unacceptable bandwidth, scan, polarization, or integration behavior that a competing architecture solves with comparable cost/complexity.

## D0004 — R0 is reconstruction, not optimization

Decision:
- R0 remains 300–500 MHz passive CHARTS reconstruction.
- no L-band scaling, LNA, array optimization, or solver fitting until provenance/build gates pass.

Reason:
- prevent source ambiguity from contaminating later optimization.

Reversal condition:
- none; this is a methodological rule for R0.


## D0005 — Accept V0.3 visible 12-slot topology; keep centre/feed unresolved

Decision:
- Accept R0.1A3 as the current visible CHARTS topology baseline: 8 outer slot segments + 4 inner radial slots, one connected plate, no large central through-hole, 200 mm height over ground.
- Preserve all V0.3 photo-derived dimensions as `FIGURE_DERIVED_UNVERIFIED`; do not promote them to paper-explicit truth.
- Keep the central removed/feed region and the Fig.1 `40 mm` label unresolved.
- Do not authorize a passive solver until a balanced feed topology can be defined without inventing hidden conductor geometry.

Evidence:
- `evidence/r0_1a3_h01_20260922_2158/`
- `docs/R0_1A3_DESIGN_REVIEW_20260922.md`

Reason:
- deterministic CST build/reopen and exact volume accounting validate the visible 12-slot topology,
- but the primary paper states that a central area is removed for feed/electronics while not publishing enough detail to reconstruct the hidden feed region unambiguously.

Reversal condition:
- a higher-quality primary source, author clarification, or independent geometry evidence contradicts the 12-slot topology or resolves the central/feed geometry more precisely.
