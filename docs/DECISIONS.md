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

## D0009 — Freeze a mechanical-support EM gate before the R1E1B pitch screen

Decision:
- Treat the radiator standoff/frame as a first-class electromagnetic object rather than a post-simulation mechanical detail.
- Insert R1E1A2 mechanical-support design and a later small P094 support-sensitivity qualification before the 18-case R1E1B pitch screen.
- Preserve the six R1E1A1 support-free pitch models as immutable bare-array references.
- Prefer a minimal-volume low-density RF-foam concept for first evaluation; do not assume it is perfectly transparent.
- Treat aluminium/metal supports as high-risk RF structures requiring explicit modelling, grounding and symmetry.

Evidence/reason:
- current radiator PCB span is 70.714 mm and it is suspended about 57.143 mm above the ground/backplane;
- the missing support therefore occupies the antenna/array near-field volume;
- adding support only after pitch screening could change active impedance and invalidate pitch comparisons;
- the project requirements already call for a ground/backplane and simple mechanical support.

Reversal condition:
- a mechanically credible support is demonstrated by frozen full-wave sensitivity criteria to be electromagnetically negligible across the required band/scan set, or a later integrated active-hub mechanical architecture supersedes it with quantified evidence.

## D0010 — Qualify the support joint/fastener assembly together with the support body

Decision:
- The support is defined as `radiator PCB -> upper joint -> support body -> lower joint -> ground/backplane`.
- Adhesive, screws, mounting holes, clips, soldered features and bond-line thickness are electromagnetic geometry, not invisible mechanical details.
- First-pass preferred assembly is four symmetric minimal-section low-density foam/low-permittivity posts with small bonded interfaces and no metal hardware above the ground plane.
- A serviceable dielectric-standoff / dielectric-fastener architecture is the second candidate, not the default baseline.
- Soldered metal legs and exposed metal standoffs are not accepted as neutral support methods.
- Assembly height, tilt, warp and registration are later tolerance variables because they alter the radiator-to-ground geometry.

Reason:
- a low-perturbation support material can be invalidated by conductive fasteners or a large/high-permittivity adhesive region;
- through-holes or mounting pads change the already-qualified radiator geometry;
- the support assembly sets the approximately 57.143-mm radiator-to-ground spacing and therefore also controls an RF-critical geometric dimension.

Reference:
`docs/R1E1A2_ASSEMBLY_INTERFACE_PLAN.md`

Reversal condition:
- later mechanical/EM evidence demonstrates a different joint architecture provides equal or lower RF perturbation with superior repeatability, serviceability or environmental robustness.

## D0011 — Do not relax the support-transparency gate after C60P135; enter support co-design

Decision:
- Keep the pre-frozen support benign thresholds unchanged after observing the R1E1A3 results.
- Do not freeze the current four-post S1 bonded assembly because C60P135 reaches max |Delta Z_active| = 15.09084 ohm versus the 10-ohm gate.
- Treat this as a support science-gate HOLD, not a numerical failure and not a radiator failure.
- Do not run the queued S4 metal sentinel after this HOLD.
- Insert R1E1A4 support co-design diagnostics before any R1E1B pitch screen.

Reason:
- broadside and C60P45 support perturbations are small, but C60P135 shows a broad upper-band loading effect rather than a single-point outlier;
- changing the threshold after viewing results would invalidate the scientific gate;
- the efficient next question is attribution of foam body / adhesive bond volume / support placement, not pitch optimization.

Reference:
`docs/R1E1A4_SUPPORT_CO_DESIGN_DIAGNOSTIC_PLAN.md`

Reversal condition:
- a mechanically credible revised support assembly passes the unchanged three-state support gate with qualified numerics.

## D0012 — Reframe support selection as mechanical/receiver co-design; introduce receiver shadow before more CST solves

Decision:
- Preserve the R1E1A3 10-ohm Delta-Z transparency gate as Gate T. The current S1 four-post bonded foam assembly remains a Gate-T FAIL at C60P135.
- Do not interpret Gate-T failure as automatic rejection from the final active antenna.
- Introduce Gate R for receiver/system acceptability using a frozen balanced antenna-to-LNA reference plane, QPL9547 reference noise/stability data, and scan-dependent active source impedance.
- Make R1E1A4A receiver-shadow / interface freeze the next task before any additional support solve.
- Reclassify low-density foam as a valid low-epsilon reference/possible architecture, but not the assumed production default.
- Decompose the architecture into mandatory H0 active-hub / local-ground interface plus carrier families: C0 bonded low-density foam reference, C1 central dielectric tube/serviceable standoff, and C2 structural PCB/printed frame.
- Treat grounded aluminium/metal carrier C3 as an intentional RF structure if pursued, not as neutral mechanics.
- Require passive active-hub PCB/local-ground/shield geometry to enter full-wave EM on the final shortlist before the array baseline is frozen; the transistor itself remains a circuit/noise model until later co-design.

Reason:
- receiver-array literature shows that active impedance and LNA noise match are coupled system quantities;
- QPL9547 publishes in-band noise parameters, so a receiver shadow can be built now without adding a physical transistor model to CST;
- CHARTS-inspired architecture already assumes balanced feed-point LNAs and a local active hub/shield;
- literature confirms Rohacell/foam + bonding is used in antenna construction, but usually as sheets/sandwich cores rather than the project's four discrete bonded posts;
- a mechanically robust structure that predictably shifts Z_active can be a valid co-designed RF structure even when it is not electromagnetically transparent.

Reference:
`docs/R1E1A4_SYSTEM_CO_DESIGN_REVIEW_20260925.md`

Reversal condition:
- system-level modeling or hardware evidence shows that enforcing near-transparent support is required for noise/stability/manufacturability, or that a different architecture dominates the Pareto trade.

## D0013 — Freeze H0/P1 mixed-mode receiver interface and Gate R before new support solves

Decision:
- Freeze H0 as a centered backside active-hub/local-ground interface; mechanical carrier families are C0/C1/C2/C3 beneath H0 rather than alternatives to the hub itself.
- Freeze the first source-facing H0 envelope at 11 x 11 mm and the initial local-ground island at 10 x 10 mm, centered beneath the existing radiator terminal region.
- Replace the next-generation Pol-A one-port abstraction with two 50-ohm single-ended P1A/P1B ports referenced to the same local ground; their mixed-mode differential reference is 100 ohm.
- Keep the active QPL9547 transistor outside CST; CST owns the passive EM multiport, while Python/ADS owns device noise/gain/stability.
- Freeze Gate R V0.1 before any new R1E1A4B carrier result: device-noise shadow <=0.40 dB, pre-LNA passive loss <=0.05 dB, nominal integrated first-stage estimate <=0.45 dB, structure-induced Delta-NF <=+0.05 dB, plus explicit mixed-mode/stability gates.
- Do not assume `Z_branch=Z_diff/2` until the H0 two-port model qualifies the nominal virtual-ground condition.

Reason:
- current S1_BONDED Gate-T failure does not map monotonically to LNA noise in the preliminary ideal-odd-mode diagnostic;
- QPL9547 reference data show strong in-band standalone 2-port stability, while real shield/ground feedback can still destabilize an assembly;
- a two-port local-ground model is the smallest EM object that exposes differential/common mode, branch imbalance and a physical receiver reference plane.

Reference:
- `docs/R1E1A4A_ACTIVE_HUB_INTERFACE_V01.md`
- `docs/R1E1A4A_GATE_R_RECEIVER_FREEZE_V01.md`
- `docs/R1E1A4A_MIXEDMODE_BUILD_ONLY_CONTRACT_DRAFT.md`

Reversal condition:
- build/solve evidence shows the H0 reference-plane abstraction is ill-posed or cannot produce a stable, reproducible mixed-mode mapping.

## D0014 — Retain P1 mixed-mode interface; reject H0 V0.1 continuous same-board local ground

Decision:
- retain the two-single-ended P1A/P1B mixed-mode receiver-interface architecture;
- retain Gate R V0.1 unchanged;
- classify the H0 V0.1 broadside solver as numerically qualified and mixed-mode qualified but receiver-noise unacceptable;
- reject the continuous 10x10-mm local ground directly on the radiator underside as the next physical active-hub baseline;
- do not continue H0 V0.1 to scan states or carrier studies;
- next design stage is H1 local-ground/feed-transition redesign, beginning with the H1A 2.0-mm offset-ground diagnostic after separate authorization.

Evidence:
- mixed-mode conversion <= about -42.4 dB over the science band;
- branch imbalance <=0.143 dB / 0.376 deg;
- max |Delta Zdd| vs P0 about 200 ohm;
- QPL9547 source-conditioned NF exceeds the frozen 0.40-dB R-NF0 limit over roughly 53% of science-band samples and reaches about 0.568 dB.

Interpretation:
- the reference-plane decomposition is sound;
- the dominant current problem is local-ground electromagnetic loading, not differential/common-mode symmetry.

Reference:
`docs/R1E1A4A_H1_LOCAL_GROUND_REDESIGN_PLAN.md`

Reversal condition:
- none for H0 V0.1 as currently defined. A materially different local-ground/feed-transition geometry is a new candidate, not a threshold change.

## D0015 — H1A offset-ground is directionally promising but numerically unqualified; freeze a one-step numerical recovery

Decision:
- preserve H1A `OFFSET_GROUND_G2P0` geometry exactly as solved;
- do not classify H1A receiver performance from the MaxPasses=12 run;
- retain the provisional result only as a diagnostic trend showing that 2-mm local-ground separation strongly changes the source environment and largely removes the H0 upper-band QPL9547 NF penalty;
- freeze R1E1A4A-H1R as a numerical-only recovery with sole solver change MaxPasses 12 -> 16;
- do not change Gate R, geometry, ports, materials, scan state, or mixed-mode definitions;
- do not proceed to H1B/H1C or scan states until H1R is numerically qualified.

Reason:
- H1A final Delta-S = 0.0213176 at MaxPasses=12, narrowly above the frozen 0.02 criterion;
- the late-pass sequence is monotonically decreasing, making a bounded numerical recovery appropriate;
- provisional R-NF0 exceedance is confined to the low-band edge but cannot be treated as authoritative until numerical PASS.

Reference:
`docs/R1E1A4A_H1R_NUMERICAL_RECOVERY_PLAN.md`

Reversal condition:
- H1R numerical PASS followed by authoritative Gate-R classification, or H1R numerical HOLD.

## D0015 — Promote H2 universal center structure; demote H1A to diagnostic evidence

Decision:
- H1A 2-mm offset-ground remains valuable diagnostic evidence but is not the product mechanical architecture.
- Product-architecture mainline moves to H2: one passive/active-compatible center structure using the same radiator PCB, patterned same-board local ground, shared signal landing pads, shield envelope and mechanical carrier.
- H2A V0.1 is BUILD-ONLY for human mechanical/manufacturing review before any EM solve.
- Passive and active variants should preserve the same mechanical/RF interface; the active variant later populates LNA circuitry rather than requiring a different antenna-support architecture.

Rationale:
- H0 showed a continuous same-board 10x10-mm ground can over-load the source environment.
- H1A showed ground coupling strength is a first-order variable but introduced a mechanically awkward suspended-ground architecture.
- CHARTS, SKALA-class and EMBRACE implementations support integrating feed electronics, local ground/shield and mechanical assembly as a common feed-point module rather than treating support as a late add-on.

H2A V0.1 freezes topology only, not RF-optimal dimensions. No post-result optimization is allowed inside the build-only gate.

Reference:
`docs/R1E1A4A_H2A_UNIVERSAL_CENTER_STRUCTURE_V01.md`

## D0016 — RF service routing joins the universal-center structure gate

Decision:
- RF-output connector class, cable egress, service tubes and backplane service interface are part of H2 structural architecture, not a late packaging detail.
- H2A V0.2 therefore adds connector/cable/tube geometry before any passive RF solve.
- board-side interface is frozen only to MHF4/U.FL class envelope; backplane interface only to MMCX class envelope. Exact vendor parts remain unfrozen.
- four hollow copper service tubes replace the V0.1 PEEK carrier concept for this candidate.
- tube bonding is explicitly deferred to T0/T1/T2 passive RF qualification; V0.2 uses insulating top/bottom interfaces and makes no RF-performance claim.
