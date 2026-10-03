# NEXT ACTION — REF-CUI-R0B Deterministic CST BUILD-ONLY

Task ID: **REF-CUI-R0B-BUILD-ONLY-H01**

Status: **BUILD-ONLY AUTHORIZED / SOLVER FORBIDDEN**

## Purpose

Build a deterministic CST 2022 reference model of Cui et al. 2023 using the now-frozen 26/26 source-to-geometry mapping.

This reference validates the project's CST geometry/material/dual-polarization workflow.

It does **not** replace the CHARTS-inspired mainline.

## Authoritative project inputs

Read in order:

1. `docs/PROJECT_RULES.md`
2. `docs/DECISIONS.md`
3. `refs/cui2023/PROVENANCE.md`
4. `refs/cui2023/GEOMETRY_MAP.md`
5. `refs/cui2023/parameters.csv`
6. `docs/figures/REF_CUI_GEOMETRY_SCHEMATIC.svg`

The original publisher PDF is intentionally not required on H01.

## Source-locked facts

Material:
- Rogers 4350B
- er = 3.48
- thickness = 0.76 mm

Major geometry:
- main ground plane = 260 mm square
- radiator-to-ground height = 80 mm
- square-loop outer side = 115 mm
- square-loop width = 5.9 mm
- crossed-dipole envelope span = 97 mm

All remaining Table-1 values and their geometric arrow meanings are frozen in `GEOMETRY_MAP.md`.

## Objective

Create a parameterized CST Structure Macro and run it in BUILD-ONLY mode.

The task answers only:

> Can the source-frozen Cui geometry be represented deterministically in CST 2022 without hidden manual edits or solver activity?

## Required repository artifacts

Create:

- `source/cst/REF_CUI_R0B_BUILD_ONLY_V01.mcr`
- `source/cst/REF_CUI_R0B_BUILD_ONLY_V01.bas`
- `scripts/audit_ref_cui_r0b_macro.py`
- `em/cst/REF_CUI_069_152/README.md`
- `em/cst/REF_CUI_069_152/RUNBOOK_BUILD_ONLY.md`

The macro must be fully parameterized from `refs/cui2023/parameters.csv`.

No source-frozen numeric dimension may be silently replaced.

## Geometry scope

Build at minimum:

1. square main PEC ground plane,
2. horizontal Rogers 4350B radiator substrate at z = 80 mm,
3. surrounding square loop,
4. four crossed/tapered dipole-arm sectors,
5. four open-slot cuts,
6. two orthogonal vertical Rogers 4350B balun boards,
7. Port-1 balun metal pattern,
8. Port-2 balun metal pattern.

### Important

Ports are **not** created in this task.

Do not create discrete/waveguide/lumped ports merely because the source labels Port 1/Port 2.

The red port markers in the source are geometric feed reference locations only for this gate.

## Source-to-CAD discipline

If the source map defines a dimension arrow but a remaining CAD construction choice is not source-unique, do not hide the choice.

Record it as:
- `CAD_CONSTRUCTION_ASSUMPTION`
- with exact reason,
- in a build manifest/change report.

Examples:
- dielectric-board lateral margin if not source-explicit,
- exact copper thickness if not source-explicit,
- boolean construction order,
- infinitesimal separation used only to prevent accidental overlap.

Do not change any source-mapped radiator or balun dimension.

## Copper thickness

The paper gives substrate thickness but not copper thickness in Table 1.

For BUILD-ONLY, either:
- use zero-thickness PEC sheets, preferred, or
- use a clearly documented `CAD_CONSTRUCTION_ASSUMPTION`.

Do not promote copper thickness to `PAPER_EXPLICIT`.

## Required static checks before CST

The audit must verify:

- all 26 source parameters are present,
- Rogers 4350B / er 3.48 / 0.76 mm are present,
- no solver command,
- no optimizer/sweep command,
- no port object,
- no LNA,
- no CHARTS geometry,
- no GNSS scaling.

Expected static terminal status:

`PASS_REF_CUI_R0B_MACRO_STATIC_AUDIT`

## CST runtime review

Use a fresh MWS project.

Run only the V01 build macro.

Verify visually:

- 260 mm square ground,
- radiator board 80 mm above ground,
- square loop around crossed dipoles,
- four symmetric open slots,
- two orthogonal vertical balun boards beneath the radiator,
- balun metal patterns are distinct and correspond to Port 1 / Port 2 mapping,
- no accidental loop-to-dipole short,
- no accidental short between orthogonal baluns,
- fourfold radiator symmetry is preserved where expected.

## Save / close / fresh reopen

After successful build:

1. save,
2. close CST,
3. reopen fresh,
4. verify geometry persists,
5. verify no port objects,
6. verify no solver result tree.

## Required evidence

Create:

`evidence/ref_cui_r0b_h01_<YYYYMMDD_HHMM>/`

At minimum:

- `RETURN_REPORT.md`
- `preflight.txt`
- `object_inventory.txt`
- `parameter_inventory.txt`
- `construction_assumptions.md`
- `reopen_inventory.txt`
- top-view screenshot
- oblique screenshot
- underside/balun screenshot
- fresh-reopen screenshot
- CST project local path + SHA-256 if not committed

## Allowed final status

Exactly one:

- `PASS_REF_CUI_R0B_BUILD_ONLY`
- `HOLD_REF_CUI_R0B_CAD_AMBIGUITY`
- `HOLD_REF_CUI_R0B_CST_RUNTIME_SYNTAX`
- `HOLD_REF_CUI_R0B_VISUAL_MISMATCH`
- `FAIL_REF_CUI_R0B_REPLAY`

## Strict prohibitions

- NO solver.
- NO ports.
- NO monitors.
- NO optimizer.
- NO GNSS scaling.
- NO LNA/QPL9547.
- NO CHARTS geometry edits.
- NO tuning to match S11.
- NO claim that REF-CUI is the project mainline.

After commit/push, stop.
