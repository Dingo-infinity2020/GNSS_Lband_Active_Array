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
