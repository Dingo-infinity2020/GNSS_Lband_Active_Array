# CHARTS 2025 — Center / Feed Provenance Extraction (R0.1B)

Task: `R0.1B-CENTER-FEED-PROVENANCE-H01`
Date: 2026-09-22
Host: H01 (DESKTOP-GBTI6Q4)

Status (R0.1B, 2026-09-22): **EXTRACTION CONSOLIDATED FROM REPOSITORY PROVENANCE; PRIMARY FIGURES NOT AVAILABLE TO H01**
Status (R0.1B2, 2026-09-23): **OFFICIAL PDF ACCESS ATTEMPTED; BLOCKED BY PUBLISHER WAF CAPTCHA — NO NEW FIGURE AUDIT**

## 0. Source availability (honest limitation)

The task asked for a high-resolution inspection of Fig. 1(a) (simulation model)
and Fig. 2(a) (fabricated antenna). **Those figures were not available to H01:**

- the repository intentionally stores **no** copyrighted figures/PDF
  (`refs/charts2025/` contains only `.md` files);
- a local-machine search found no CHARTS/ISAP source copy;
- the recorded DOI (`10.34385/proc.98.1571143655`) resolves only to
  **bibliographic metadata** (title/authors/publisher), with no open full text
  or figure link; the Crossref and DataCite APIs returned 404 for this DOI.

Therefore H01 could not perform a new pixel-level figure audit. Everything below
is consolidated **only** from the repository's existing source-traceable records.
No new figure measurement was made and no figure was reinterpreted.

Relevant repository sources:

- `refs/charts2025/PROVENANCE.md`
- `refs/charts2025/FIGURE_EXTRACTION.md`
- `refs/charts2025/PHOTO_GEOMETRY_ESTIMATE.md`
- `docs/R0_RECONSTRUCTION_ASSUMPTIONS.md`
- `docs/R0_1A3_DESIGN_REVIEW_20260922.md`

## 0b. R0.1B2 update (2026-09-23) — official source access attempted

The design side recovered the official IEICE publisher links and issued
`R0.1B2-CENTER-FEED-SOURCE-RECOVERY-H01` to repeat the figure audit against the
primary PDF.

H01 attempted to download the official PDF and was blocked by the publisher's
**AWS WAF "Human Verification" CAPTCHA**:

- the landing/summary URL and the direct PDF URL both returned HTTP 405 with a
  2144-byte WAF challenge page for `curl.exe` / webfetch, and HTTP 403 for
  `Invoke-WebRequest`;
- the challenge requires JavaScript plus a human CAPTCHA; H01 did not attempt to
  bypass it.

Conclusion: the primary PDF is inaccessible to H01 via an automated,
rule-compliant path, so **no new Fig.1(a)/Fig.2(a) inspection was performed** and
no value below was re-measured or upgraded. The R0.1B content is preserved
unchanged as the best available provenance record.

Evidence: `evidence/r0_1b2_h01_20260923_1211/` (`source_access_log.txt`,
`figure_measurements.md`). Final status: `HOLD_R0_PRIMARY_SOURCE_ACCESS_FAILED`.

## 1. Text-supported central/feed statements (`PAPER_EXPLICIT`)

Only directly stated facts are listed; no dimensions are inferred from them.

- the antenna is a square PCB-based **"4-petal"** planar structure with a
  surrounding passive ring;
- a **small central low-field area may be removed** to accommodate feed
  points / electronics;
- the output is **balanced (differential)** and directly feeds **a pair of LNAs**;
- the active implementation uses a **small local ground plane beneath the feed
  points** plus a clip-on metallic shield;
- the LNA circuitry is mounted **at the feed region**;
- center/near-center impedance design region: **`(100 +/- 40) + j(0 +/- 40) ohm`**;
- height over the reference ground: **200 mm**.

None of these statements supply a numerical central-cutout or feed-terminal
dimension.

## 2. Required extraction table

Provenance classes used: `PAPER_EXPLICIT`, `FIGURE_DERIVED_UNVERIFIED`,
`SEMANTICS_UNRESOLVED`.

| Feature | Observation | Value/range | Provenance | Confidence | Solver consequence |
|---|---|---|---|---|---|
| Central region usage | Paper states a small central low-field area may be removed for feed/electronics | not dimensioned | PAPER_EXPLICIT | High (text) | a central opening/cutout is expected; without dimensions a port boundary cannot be defined |
| Balanced output | Output is balanced and directly feeds a pair of LNAs | n/a | PAPER_EXPLICIT | High (text) | a differential/balanced excitation is the physically correct model |
| Feed-region local ground | Small ground plane beneath the feed points (active implementation) | not dimensioned | PAPER_EXPLICIT | High (text) | a local feed ground exists, distinct from the main reference ground; geometry unpublished |
| LNA location | LNA circuits mounted at the feed region | n/a | PAPER_EXPLICIT | High (text) | active electronics occupy the center; the region is not a simple aperture |
| Center impedance target | Design region for near-center impedance | `(100 +/- 40) + j(0 +/- 40) ohm` | PAPER_EXPLICIT | High (text) | later matching target; not a geometry |
| Fig.1 `40 mm` label | Visible central-region dimension annotation; which two points it spans is not unambiguous at available resolution | 40 mm value; endpoints unresolved | SEMANTICS_UNRESOLVED | Low | cannot be used to size the central cutout or the terminal gap |
| Differential terminal geometry (position, gap, orientation) | No published terminal coordinates or gap | UNKNOWN | SEMANTICS_UNRESOLVED | None | a solver excitation cannot be placed without inventing hidden conductor topology |
| Central removed/cutout shape | Text implies removal for feed/electronics; figure endpoint/shape not resolved; V0.3 keeps the center solid | UNKNOWN | SEMANTICS_UNRESOLVED | None | materialized/feed model remains blocked |
| Visible central clear span (previously recorded photo estimate) | Slot-to-slot clear span of the inner radial slots | ~60 mm (+/- 5) | FIGURE_DERIVED_UNVERIFIED | Low–Medium | this is a topology estimate, not feed-terminal geometry, and is not equal to 40 mm |
| No large central through-hole | Design-side review recorded no large through-hole; V0.3 keeps a solid center | n/a | FIGURE_DERIVED_UNVERIFIED | Low–Medium | consistent with a solid center in the current build-only model |
| Substrate / copper stack at the feed | Not published | UNKNOWN | SEMANTICS_UNRESOLVED | None | materialized build remains HOLD |

Note: the `FIGURE_DERIVED_UNVERIFIED` rows above were recorded earlier by the
design side; H01 did **not** independently re-measure them in this task and does
not upgrade them.

## 3. Fig.1 `40 mm` interpretation candidates (no winner selected)

The label endpoints are not unambiguous in the available record. All of the
following remain possible; none is accepted:

- **Candidate A — feed-terminal separation.** `40 mm` spans the gap between the
  two balanced feed terminals at the center (differential feed gap). No published
  terminal geometry supports this directly.
- **Candidate B — small central removed square.** `40 mm` is the side of a small
  central removed square for feed/electronics. This would be a sub-feature, since
  the previously recorded visible central clear span is ~60 mm and no large
  through-hole is recorded.
- **Candidate C — local feed ground extent.** `40 mm` is a dimension of the small
  local ground plane beneath the feed points.
- **Candidate D — inner-region spacing.** `40 mm` relates to an inner conductor
  or slot spacing other than the ~60 mm visible clear span.

A redrawn, project-owned schematic of these candidates is provided at
`docs/figures/R0_CENTER_FEED_INTERPRETATION.svg`. It contains no source imagery.

## 4. Decision fields

```text
FIG40_SEMANTICS=UNRESOLVED
DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED
CENTRAL_REMOVED_REGION=PARTIAL
SOLVER_READY=NO
```

Rationale:

- `FIG40_SEMANTICS=UNRESOLVED`: no source geometry makes the annotation endpoints
  unambiguous.
- `DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED`: only the existence of a balanced
  feed is source-supported; its geometry is not.
- `CENTRAL_REMOVED_REGION=PARTIAL`: the paper explicitly allows a central removal
  for feed/electronics, and a previous figure review recorded no large
  through-hole, but the removed shape/size is not resolved.
- `SOLVER_READY=NO`: a balanced excitation cannot be defined without inventing
  hidden terminal/cutout geometry.

## 5. What would unblock the solver

One of the following:

- a higher-resolution copy of Fig. 1(a) making the `40 mm` endpoints and the
  feed-terminal geometry unambiguous;
- an author-provided feed/electronics layout;
- independent measurement of the fabricated board center.

Until then, R0 remains build-only and no passive solver is authorized.

## 6. Provenance rules honored

- No figure-derived value was promoted to `PAPER_EXPLICIT`.
- The `40 mm` label was not silently decided.
- No copyrighted PDF/figure was copied into the repository.
- V0.3 geometry was not modified; no CST/solver was run.
