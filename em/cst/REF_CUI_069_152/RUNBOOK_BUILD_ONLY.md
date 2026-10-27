# REF-CUI-R0B BUILD-ONLY Runbook

Status: **READY FOR HOST BUILD-ONLY REVIEW**

## Preflight

```bash
python scripts/audit_ref_cui_r0b_macro.py
```

Expected:

```text
PASS_REF_CUI_R0B_MACRO_STATIC_AUDIT
EXPECTED_SOURCE_PARAMETERS=26
EXPECTED_PORTS=0
EXPECTED_SOLVER_RUN=NO
```

## CST execution

Fresh MWS project; run
`source/cst/REF_CUI_R0B_BUILD_ONLY_V01.mcr` (the `.bas` is a backup copy).

## Model contents

Components / solids expected:

- `MainGround:GROUND` — 260 mm square PEC reflector at z <= 0.
- `RadiatorBoard:RADIATOR_SUB` — Rogers 4350B board, top at z = 80 mm.
- `Radiator:LOOP` — square loop 115 mm outer, 5.9 mm trace.
- `Radiator:ARMS` — crossed-dipole arm plate (97 mm envelope) after the tapered
  cross gap, four open slots and four diagonal tapers.
- `Balun1:BALUN1_SUB` + balun-1 metal strips (`B1_*`).
- `Balun2:BALUN2_SUB` + balun-2 metal strips (`B2_*`).

0 ports, 0 lumped elements, 0 solver results.

## Source-locked values

All 26 Table-1 symbols are parameters in the macro. Do not tune them.

## CAD construction assumptions (NOT source-explicit)

These are project CAD choices, not paper dimensions:

| Item | Value | Reason |
|---|---:|---|
| copper_t | 0.035 mm | copper proxy thickness (Table 1 omits it) |
| ground_t | 0.5 mm | solid-metal proxy for the reflector |
| rad_margin | 5.0 mm | radiator dielectric lateral margin beyond the loop (not published) |
| balun_w | 30.0 mm | balun board lateral width (not published) |
| balun_off | 1.0 mm | lateral offset to keep the two orthogonal baluns from shorting |
| eps | 0.01 mm | infinitesimal through-cut overlap |
| open-slot shape | L-bend proxy (Ls/Lp1/Lp2/Lp3) | exact U-bend vertices not source-defined |
| balun metal | strip proxy | exact balun metal polygon not source-defined |

The pattern is a schematic strip proxy built from Wb1..Wb8 / Lb1..Lb5; it is not
claimed to be the exact published layout.

## Visual review

- 260 mm square ground,
- radiator board 80 mm above ground,
- square loop around the crossed dipoles,
- four open slots, fourfold symmetry where expected,
- two orthogonal vertical balun boards beneath the radiator,
- distinct balun-1 / balun-2 metal patterns,
- no accidental loop-to-dipole short,
- no accidental short between the two baluns.

## Save / close / fresh reopen

Save, close CST, reopen fresh; verify the geometry persists, 0 ports, and no
solver result tree.

## Prohibitions

No solver, no ports, no monitors, no optimizer, no GNSS scaling, no LNA/QPL9547,
no CHARTS geometry edits, no S11 tuning, no claim that REF-CUI is mainline.
