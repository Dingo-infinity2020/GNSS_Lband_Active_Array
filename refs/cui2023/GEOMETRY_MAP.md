# Cui 2023 — Source-to-Geometry Map (REF-CUI-R0A)

Task: `REF-CUI-R0A-SOURCE-GEOMETRY-FREEZE-H01`
Date: 2026-09-23
Host: H01 (DESKTOP-GBTI6Q4)

Status: **MAPPING BLOCKED — PUBLISHER FIGURES NOT ACCESSIBLE TO H01**

## 1. Purpose

Map every Table-1 symbol of the open-access Cui 2023 antenna to its exact
physical feature/panel so a deterministic CST build can later be written without
guessing.

Source:
- Cui, Tu, Qin, Li, "A compact broadband antenna for ultra high frequency and L
  band on 5G new radio base stations", IET Microw. Antennas Propag. 17(5),
  361–368 (2023); DOI `10.1049/mia2.12343`.
- Publisher page: https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/mia2.12343

## 2. Access outcome (blocker)

The publisher full text and figures could **not** be accessed by H01:

- Wiley (`ietresearch.onlinelibrary.wiley.com`, landing / pdfdirect / pdf / epdf)
  returns HTTP 403 behind a **Cloudflare "Just a moment..." JS challenge**;
- IET Digital Library (`digital-library.theiet.org`) returns HTTP 403;
- DOAJ article page returns HTTP 403;
- Unpaywall / OpenAlex / Semantic Scholar list the item as GOLD OA but provide
  **only the publisher DOI** as the OA location (`url_for_pdf = null`,
  `has_fulltext = false`) — no accessible mirror.

Automated, rule-compliant access failed. H01 did **not** attempt to defeat the
Cloudflare challenge. Full details in
`evidence/ref_cui_r0a_h01_20260923_1229/source_access_log.txt`.

Consequence: the physical meaning of each Table-1 symbol cannot be established
from the publisher figures. Per the task rule ("do not guess"), every symbol is
marked `MAPPING_UNRESOLVED`.

## 3. Symbol map

Value provenance: the numeric values below are transcribed from Table 1 by the
design side (`refs/cui2023/PROVENANCE.md`) and are treated as `PAPER_EXPLICIT`
values. H01 did **not** independently verify them against the publisher (blocked).

| Symbol | Value (mm) | Physical feature | Figure/panel used | Provenance | Confidence | Deterministic CAD |
|---|---:|---|---|---|---|---|
| Lg | 260 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| H | 80 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Lr | 115 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wr | 5.9 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Ld | 97 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Ws | 2.2 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Ls | 26.6 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wg1 | 1.7 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wg2 | 3.9 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wp | 8.4 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Lp1 | 36.3 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Lp2 | 8.2 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Lp3 | 36.8 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Lb1 | 21 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Lb2 | 10 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Lb3 | 20.5 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Lb4 | 24.5 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Lb5 | 73 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wb1 | 1.5 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wb2 | 0.65 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wb3 | 0.95 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wb4 | 13 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wb5 | 28.5 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wb6 | 3.6 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wb7 | 4.8 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |
| Wb8 | 3.6 | MAPPING_UNRESOLVED | NOT_ACCESSED | PAPER_EXPLICIT | NONE | NO |

26 symbols; 0 deterministically mapped; mapping is blocked, not ambiguous, until
the publisher figures are accessible.

## 4. Material / source facts (from transcript; not re-verified by H01)

- Rogers 4350B, er = 3.48, substrate thickness 0.76 mm;
- ground-plane height H = 80 mm;
- dual +/-45-degree polarizations, two orthogonal broadband baluns;
- square loop tightly coupled but not electrically attached to the dipoles;
- reported band 0.69–1.52 GHz for RL > 15 dB; reported isolation > 35 dB.

These are the design-side transcription; H01 could not re-verify them against the
publisher because of the access block.

## 5. Why no redraw was produced

The task requested `docs/figures/REF_CUI_GEOMETRY_SCHEMATIC.svg`. Producing a
geometry redraw requires knowing Figure 7's layout. Since the figure is
inaccessible, any redraw would be fabricated, which the task forbids
("do not guess"). The schematic is therefore **deliberately not created**.

## 6. What would unblock the mapping

Either:

- provide the Cui 2023 PDF to H01 as a git-ignored local file (with permission to
  read it), or
- provide a project-owned coordinate description of Figure 7, or
- perform the Figure 7 symbol mapping design-side and issue H01 a consolidation
  task.

Until then, no symbol may be assigned a physical feature and no deterministic
REF-CUI CST build is authorized.
