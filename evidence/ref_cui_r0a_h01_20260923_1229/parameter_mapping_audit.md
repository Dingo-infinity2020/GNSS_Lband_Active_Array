# REF-CUI-R0A — Parameter Mapping Audit

Task: `REF-CUI-R0A-SOURCE-GEOMETRY-FREEZE-H01`
Date: 2026-09-23
Status: **BLOCKED — publisher Figure 7 / Table 1 not accessible to H01**

## Audit method

1. Read the repository transcription of Table 1 (`refs/cui2023/PROVENANCE.md`).
2. Attempt to open the publisher article/figures (Wiley / IET / DOAJ) to map each
   symbol to its physical feature and panel.
3. If a symbol cannot be mapped unambiguously, mark `MAPPING_UNRESOLVED` and do not
   guess.

## Result

Step 2 failed: every publisher/aggregator route returned HTTP 403 behind a
Cloudflare JS challenge, and all open-access aggregators (Unpaywall, OpenAlex,
Semantic Scholar) point back to the blocked publisher DOI with no repository
mirror. See `source_access_log.txt`.

Therefore **no symbol could be mapped to a physical feature**, so all 26 Table-1
symbols are recorded as `MAPPING_UNRESOLVED`. This is a *figure-access* failure,
not a parameter ambiguity in the source.

## Per-symbol status

| Symbol | Value (mm) | Mapping | Deterministic CAD |
|---|---:|---|---|
| Lg | 260 | MAPPING_UNRESOLVED | NO |
| H | 80 | MAPPING_UNRESOLVED | NO |
| Lr | 115 | MAPPING_UNRESOLVED | NO |
| Wr | 5.9 | MAPPING_UNRESOLVED | NO |
| Ld | 97 | MAPPING_UNRESOLVED | NO |
| Ws | 2.2 | MAPPING_UNRESOLVED | NO |
| Ls | 26.6 | MAPPING_UNRESOLVED | NO |
| Wg1 | 1.7 | MAPPING_UNRESOLVED | NO |
| Wg2 | 3.9 | MAPPING_UNRESOLVED | NO |
| Wp | 8.4 | MAPPING_UNRESOLVED | NO |
| Lp1 | 36.3 | MAPPING_UNRESOLVED | NO |
| Lp2 | 8.2 | MAPPING_UNRESOLVED | NO |
| Lp3 | 36.8 | MAPPING_UNRESOLVED | NO |
| Lb1 | 21 | MAPPING_UNRESOLVED | NO |
| Lb2 | 10 | MAPPING_UNRESOLVED | NO |
| Lb3 | 20.5 | MAPPING_UNRESOLVED | NO |
| Lb4 | 24.5 | MAPPING_UNRESOLVED | NO |
| Lb5 | 73 | MAPPING_UNRESOLVED | NO |
| Wb1 | 1.5 | MAPPING_UNRESOLVED | NO |
| Wb2 | 0.65 | MAPPING_UNRESOLVED | NO |
| Wb3 | 0.95 | MAPPING_UNRESOLVED | NO |
| Wb4 | 13 | MAPPING_UNRESOLVED | NO |
| Wb5 | 28.5 | MAPPING_UNRESOLVED | NO |
| Wb6 | 3.6 | MAPPING_UNRESOLVED | NO |
| Wb7 | 4.8 | MAPPING_UNRESOLVED | NO |
| Wb8 | 3.6 | MAPPING_UNRESOLVED | NO |

Values are the design-side transcription (treated as `PAPER_EXPLICIT`); H01 did
not independently verify them against the publisher.

## Material facts (from transcript; not re-verified by H01)

Rogers 4350B, er = 3.48, substrate thickness 0.76 mm, H = 80 mm, dual +/-45-degree
polarizations, two orthogonal broadband baluns, square loop not attached to the
dipoles, 0.69–1.52 GHz for RL > 15 dB, isolation > 35 dB.

## Deterministic-CAD verdict

`DETERMINISTIC_CAD_READY = NO`. A CST macro cannot be written for REF-CUI without
inventing the symbol-to-feature mapping, which the task forbids.

## Unblock options

- supply the Cui 2023 PDF to H01 as a git-ignored local file, or
- supply a project-owned Figure 7 coordinate description, or
- perform the symbol mapping design-side and issue H01 a consolidation task.
