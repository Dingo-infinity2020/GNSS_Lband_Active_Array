# R0.1B Center/Feed Measurement Table (project-owned)

Task: `R0.1B-CENTER-FEED-PROVENANCE-H01`
Status: **CONSOLIDATED FROM REPOSITORY PROVENANCE — PRIMARY FIGURES NOT AVAILABLE TO H01**

Provenance classes: `PAPER_EXPLICIT` / `FIGURE_DERIVED_UNVERIFIED` / `SEMANTICS_UNRESOLVED`.
No figure-derived item was independently re-measured by H01 in this task.

| Feature | Observation | Value/range | Provenance | Confidence | Solver consequence |
|---|---|---|---|---|---|
| Central region usage | Paper states a small central low-field area may be removed for feed/electronics | not dimensioned | PAPER_EXPLICIT | High (text) | central opening/cutout expected; port boundary not definable |
| Balanced output | Output is balanced and directly feeds a pair of LNAs | n/a | PAPER_EXPLICIT | High (text) | differential/balanced excitation is the correct model |
| Feed-region local ground | Small ground plane beneath the feed points | not dimensioned | PAPER_EXPLICIT | High (text) | local feed ground exists, distinct from reference ground; geometry unpublished |
| LNA location | LNA circuits mounted at the feed region | n/a | PAPER_EXPLICIT | High (text) | center occupied by electronics, not a simple aperture |
| Center impedance target | Near-center design impedance region | (100 +/- 40) + j(0 +/- 40) ohm | PAPER_EXPLICIT | High (text) | later matching target; not a geometry |
| Fig.1 `40 mm` label | Central-region dimension annotation; spanned points ambiguous | 40 mm value; endpoints unresolved | SEMANTICS_UNRESOLVED | Low | cannot size central cutout or terminal gap |
| Differential terminal geometry | No published terminal coordinates/gap | UNKNOWN | SEMANTICS_UNRESOLVED | None | excitation cannot be placed without invention |
| Central removed/cutout shape | Removal implied by text; shape/size not resolved | UNKNOWN | SEMANTICS_UNRESOLVED | None | materialized/feed model blocked |
| Visible central clear span (prior photo estimate) | Inner-slot slot-to-slot clear span | ~60 mm (+/- 5) | FIGURE_DERIVED_UNVERIFIED | Low-Medium | topology estimate, not feed-terminal geometry; not equal to 40 mm |
| No large central through-hole | Prior design review recorded none; V0.3 center solid | n/a | FIGURE_DERIVED_UNVERIFIED | Low-Medium | consistent with solid-center build-only model |
| Substrate / copper stack at the feed | Not published | UNKNOWN | SEMANTICS_UNRESOLVED | None | materialized build remains HOLD |

Decision fields: `FIG40_SEMANTICS=UNRESOLVED`, `DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED`,
`CENTRAL_REMOVED_REGION=PARTIAL`, `SOLVER_READY=NO`.

Full narrative: `refs/charts2025/CENTER_FEED_EXTRACTION.md`.
