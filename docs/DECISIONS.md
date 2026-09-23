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


## D0006 — Do not invent unpublished CHARTS center feed; use REF-CUI for exact passive-EM validation

Decision:
- Keep the CHARTS-inspired V0.3 visible topology as MAINLINE inspiration.
- Do not claim or fabricate an exact CHARTS center/feed geometry from the two-page ISAP source.
- Use Cui 2023 as the exact, fully specified passive-EM reference to validate CST geometry/material/dual-port/solver workflow.
- After REF-CUI validation, return to CHARTS-inspired GNSS development with a project-owned feed architecture whose assumptions are explicit.

Evidence:
- official IEICE CHARTS paper accessed design-side and audited,
- `docs/R0_1B2_DESIGN_SIDE_PRIMARY_SOURCE_AUDIT_20260923.md`,
- `refs/charts2025/CENTER_FEED_EXTRACTION.md`,
- open-access Cui 2023 paper with complete material and geometry table.

Reason:
- repeated access attempts do not solve missing public geometry,
- exact differential terminal pads, center copper removal, local-ground dimensions, and material stack are not uniquely published,
- continuing to tune guesses would violate reproduction-before-optimization and provenance rules,
- Cui 2023 provides a closely related square-loop dual-polarized structure with enough information to validate the EM workflow honestly.

Mainline impact:
- NONE. CHARTS-inspired active planar element remains MAINLINE.
- Cui remains REFERENCE_ONLY.

Reversal condition:
- author-provided CAD/layout, a higher-detail CHARTS publication, or another primary source resolves the exact center/feed geometry.


## D0007 — REF-CUI 26/26 source geometry mapping frozen; BUILD-ONLY authorized

Decision:
- Accept the user-supplied publisher PDF as the primary source for completing Figure 7 / Table-1 symbol mapping.
- Freeze all 26 Table-1 symbols to their Figure 7(a)/(b)/(c) geometric arrow meanings in `refs/cui2023/GEOMETRY_MAP.md`.
- Authorize a deterministic REF-CUI CST BUILD-ONLY model.
- Keep solver permission disabled until build/reopen and design-side visual review pass.

Evidence:
- user-supplied publisher PDF, Cui et al. 2023, DOI 10.1049/mia2.12343,
- `refs/cui2023/GEOMETRY_MAP.md`,
- `refs/cui2023/parameters.csv`,
- `docs/figures/REF_CUI_GEOMETRY_SCHEMATIC.svg`.

Reason:
- Figure 7(b)/(c) is sufficiently legible at high-resolution render to identify each Table-1 dimension arrow without relying on symbol-name guessing.
- The paper text explicitly ties Figure 7(c) to the two broadband baluns and Table 1 to the proposed antenna geometry.
- A build-only gate is appropriate before any solver or EM-performance comparison.

Mainline impact:
- NONE.
- CHARTS-inspired active planar element remains MAINLINE.
- REF-CUI remains REFERENCE_ONLY.

Reversal condition:
- a contradiction is found during build-only visual comparison against the primary PDF.


## D0008 — Stop REF-CUI before solver; return operational focus to CHARTS MAINLINE

Decision:
- Reclassify `PASS_REF_CUI_R0B_BUILD_ONLY` as an execution/replay PASS only.
- Scientific geometry fidelity is HOLD after comparison against the user-supplied primary PDF.
- Do not authorize a REF-CUI solver gate.
- Return operational project focus to the CHARTS-inspired MAINLINE.

Evidence:
- user-supplied Cui 2023 publisher PDF, especially Figure 7(b)/(c),
- `evidence/ref_cui_r0b_h01_20260923_1341/`,
- `evidence/REF_CUI_R0B_DESIGN_REVIEW_SCIENTIFIC_HOLD.md`.

Reason:
- V01 used independent proxy cuts for the four arm/slot regions instead of generating all arms by exact 90-degree rotation from one source-faithful master sector,
- open-slot geometry and balun metal were explicitly proxy constructions,
- visual symmetry / shape fidelity is not adequate for literature-solver validation,
- REF-CUI was introduced only as REFERENCE_ONLY workflow validation and should not consume the MAINLINE schedule.

If REF-CUI is revisited:
- create one canonical arm + slot and rotate by 90/180/270 degrees,
- enforce rotational geometry audit,
- source-lock the balun polygon before solver.

Mainline impact:
- CHARTS-inspired active planar element remains MAINLINE and becomes the next operational focus.

Reversal condition:
- only if a later CHARTS-specific blocker requires a reference solver benchmark that cannot be resolved directly.
