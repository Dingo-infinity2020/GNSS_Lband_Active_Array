# REF-CUI 0.69–1.52 GHz — CST Reference Module

Status: **BUILD-ONLY MODEL**

This module holds the deterministic CST reference build of:

- Yuehui Cui, Zhenxing Tu, Yue Qin, RongLin Li,
  "A compact broadband antenna for ultra high frequency and L band on 5G new
  radio base stations", IET Microw. Antennas Propag. 17(5), 361–368 (2023),
  DOI `10.1049/mia2.12343`.

REF-CUI is **REFERENCE_ONLY** (Decision D0006/D0007). It validates the project's
CST geometry/material/dual-polarization workflow and does not replace the
CHARTS-inspired mainline.

## Source lock

- 26 Table-1 symbols frozen in `refs/cui2023/GEOMETRY_MAP.md` and
  `refs/cui2023/parameters.csv` (all `PAPER_EXPLICIT`).
- Material: Rogers 4350B, er = 3.48, substrate thickness = 0.76 mm.
- Main ground = 260 mm square; radiator height = 80 mm; square loop = 115 mm
  outer, 5.9 mm trace; crossed-dipole envelope = 97 mm.
- Project-owned schematic: `docs/figures/REF_CUI_GEOMETRY_SCHEMATIC.svg`.

## Files

- `source/cst/REF_CUI_R0B_BUILD_ONLY_V01.mcr` — parameterized Structure Macro.
- `source/cst/REF_CUI_R0B_BUILD_ONLY_V01.bas` — identical source backup copy.
- `scripts/audit_ref_cui_r0b_macro.py` — static build-only audit.
- `RUNBOOK_BUILD_ONLY.md` — execution and acceptance steps.

## Permissions

- BUILD_ONLY: YES.
- ports / monitors / solver / optimization: NO.
- GNSS scaling / LNA / CHARTS edits: NO.
