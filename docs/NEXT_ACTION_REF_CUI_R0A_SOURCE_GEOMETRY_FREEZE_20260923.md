# NEXT ACTION — REF-CUI-R0A Source/Geometry Freeze

Task ID: **REF-CUI-R0A-SOURCE-GEOMETRY-FREEZE-H01**

Status: **SOURCE/PROVENANCE ONLY — NO CST**

## Why this task exists

The public CHARTS proceeding does not uniquely publish the hidden center/feed geometry.

The project therefore uses the fully specified, open-access Cui 2023 antenna as the exact passive-EM reference for validating:
- geometry construction,
- substrate/material handling,
- dual-polarized ports,
- square-loop/open-slot resonance physics,
- later solver/post-processing workflow.

This does **not** replace the CHARTS-inspired mainline.

## Primary source

Publisher:
https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/mia2.12343

DOI:
10.1049/mia2.12343

## Required reading

- `docs/PROJECT_RULES.md`
- `docs/DECISIONS.md`
- `refs/cui2023/PROVENANCE.md`
- `PROJECT_HANDOFF.md`

## Objective

Create a source-locked geometry map for Cui 2023 Figure 7 / Table 1.

The current provenance file already contains the complete published parameter table.

The host must now determine, from the publisher article/figures, what each symbol physically means.

## Required deliverables

Create/update:

1. `refs/cui2023/GEOMETRY_MAP.md`
2. `refs/cui2023/parameters.csv`
3. `docs/figures/REF_CUI_GEOMETRY_SCHEMATIC.svg` — project-owned redraw only
4. evidence directory:
   `evidence/ref_cui_r0a_h01_<YYYYMMDD_HHMM>/`

Evidence should include:
- `RETURN_REPORT.md`
- `source_access_log.txt`
- `parameter_mapping_audit.md`
- hashes if local source files are used

Do not commit publisher PDF or raw source figures.

## Parameter mapping requirement

For every Table-1 symbol:

`Lg, H, Lr, Wr, Ld, Ws, Ls, Wg1, Wg2, Wp, Lp1, Lp2, Lp3, Lb1..Lb5, Wb1..Wb8`

record:

- numeric value,
- unit,
- physical feature,
- figure/panel used for mapping,
- provenance = `PAPER_EXPLICIT`,
- confidence = HIGH/MEDIUM/LOW,
- whether the mapping is sufficient for deterministic CAD.

If a symbol cannot be mapped unambiguously:
- mark `MAPPING_UNRESOLVED`,
- do not guess,
- return HOLD if it blocks deterministic geometry.

## Material/source facts to verify

Verify from the publisher source:

- Rogers 4350B,
- er = 3.48,
- substrate thickness = 0.76 mm,
- ground-plane height H = 80 mm,
- dual +/-45-degree polarizations,
- two orthogonal broadband baluns,
- square loop is not electrically attached to the dipoles,
- reported band 0.69–1.52 GHz for RL >15 dB,
- reported isolation >35 dB.

## Strict prohibitions

- NO CST.
- NO solver.
- NO optimization.
- NO CHARTS geometry edits.
- NO L-band GNSS scaling.
- NO QPL9547/LNA work.
- NO copying source figures/PDF into Git.

## Final status

Return exactly one:

- `PASS_REF_CUI_SOURCE_GEOMETRY_FROZEN`
- `HOLD_REF_CUI_FIGURE_ACCESS_FAILED`
- `HOLD_REF_CUI_PARAMETER_MAPPING_AMBIGUOUS`

Then update `PROJECT_HANDOFF.md`, commit, push, and stop.
