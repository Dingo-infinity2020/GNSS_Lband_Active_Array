# R0.1A3 12-SLOT BUILD-ONLY — Host Return Report

**FINAL_STATUS = PASS_R0_V03_12SLOT_TOPOLOGY_BUILD_ONLY**

- Task ID: `R0.1A3-12SLOT-BUILD-ONLY-H01`
- Host: H01 (DESKTOP-GBTI6Q4)
- Date: 2026-09-22
- Host start commit: `1ea38af92b4350261adc2598e9c3bb897ae89905`
- Scope: CST 2022 build-only runtime validation + fresh-reopen audit
- Solver / optimization / ports: **not run / not used / none created**

## 1. Toolchain

- CST Studio Suite 2022.5 (build 2022-06-03, change 981760)
- Automation: CST bundled Python 3.6 + `cst.interface` API
- Bundled Python: `D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python\python.exe`
- Gate scripts: Miniconda CPython 3.13.9

## 2. Preflight (from `preflight.txt`)

```text
$ python scripts/r0_manifest_gate.py --stage topology
PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY
exit=0

$ python scripts/audit_r0_12slot_v03.py
PASS_R0_V03_STATIC_AUDIT
EXPECTED_FINAL_SOLIDS=2
EXPECTED_OUTER_SLOT_SEGMENTS=8
EXPECTED_INNER_SLOT_SEGMENTS=4
EXPECTED_SLOT_SUBTRACTIONS=12
EXPECTED_PORTS=0
CENTER_THROUGH_HOLE=NO
FIG40_SEMANTICS=UNRESOLVED
SOLVER_RUN=NO
exit=0
```

Both required gates PASS before any CST action.

## 3. Method

`run_harness.py` drives CST through the Python API:

1. **Session A** — new MWS; the `Sub Main()` body (253 lines) of the committed
   `source/cst/R0_CHARTS_12SLOT_BUILD_ONLY_V03.mcr` was read, unwrapped, and
   executed verbatim via `Modeler.add_to_history`. The macro was not modified.
   Project saved and closed.
2. **Session B** — fresh open; screenshots + object/shape inventory.
3. **Session C** — second fresh open (fresh-reopen audit); inventory + screenshot.

Macro SHA-256: `08943e4208e3d852f38d154fb082bbc7fb734581a0ef4788c20a50e8f69d9e6d`
(unchanged from the repository copy). V0.1 and V0.2 macros were not run.

## 4. Build result

- `add_to_history`: no error
- Saved: `D:\GNSS_Lband_Active_Array\_r0_1a3_h01_work\R0_1A3_12SLOT_BUILD_ONLY_H01.cst`
- Project SHA-256: `8502C38DA8EB66FE57D96C6A8DCECF449744618CA76E7B35044CD4E47581B491`
- `Result\output.txt` is absent: no solver, port, mesh or excitation activity.

## 5. Definitive shape inventory

Enumerated with the CST `Solid` query API in both sessions:

```text
SHAPE_COUNT=2
ReferenceGround:GROUND_REFERENCE  volume=1000000          isSolid=TRUE
Radiator:ANTENNA_PLATE            volume=5486.325000...  isSolid=TRUE
```

- All twelve `SlotTools:CUT_*` cutters are absent (`SelectTreeItem` = 0 = False),
  i.e. consumed by boolean subtraction.
- `Components\SlotTools` still exists as an empty component (CST retains the
  component after subtraction); it contains no solids.
- 0 ports, 0 lumped elements, 0 solver results.

## 6. Connectivity / slot-independence proof

Volume arithmetic confirms one connected plate with twelve non-overlapping cuts:

```text
full plate        247.5 * 247.5 * 0.1                         = 6125.625 mm^3
outer cuts (8)    8 * 94.125 * 5 * 0.1                        =  376.500 mm^3
inner cuts (4)    4 * 73 * 9 * 0.1                            =  262.800 mm^3
expected remaining 6125.625 - 376.5 - 262.8                   = 5486.325 mm^3
measured ANTENNA_PLATE volume                                 = 5486.325 mm^3
```

The exact match proves the twelve slot volumes are independent (no slot overlaps
another) and each lies fully within the plate; the plate therefore remains one
connected solid.

Bridge margins (from the macro parameters, geometric, no fitting):

```text
mid-side conductor bridge          = 18.0 mm
corner margin (per corner)         = (247.5 - 2*94.125 - 18)/2 = 20.625 mm
inner-to-outer solid bridge        = 113.75 - 2.5 - 103        =   8.25 mm
central clear span (inner radius)  = 60 mm (inner_start_radius = 30)
```

## 7. Mandatory build/visual review

| # | Check | Result | Basis |
|---|---|---|---|
| 1 | Antenna plate remains one connected solid | PASS | `SHAPE_COUNT=2`, `isSolid=TRUE`, volume exact |
| 2 | 8 outer slots total | PASS | `top_view_plate.png`, §6 |
| 3 | Exactly 2 outer slots per side | PASS | `top_view_plate.png` |
| 4 | Midpoint conductor bridge on all 4 sides | PASS | `top_view_plate.png` (18 mm) |
| 5 | Conductor remains at all 4 corners | PASS | `top_view_plate.png` (20.625 mm) |
| 6 | 4 inner radial slots | PASS | `top_view_plate.png` |
| 7 | Inner slots stop before centre | PASS | central 60 mm clear span |
| 8 | Inner slots stop before outer slots | PASS | 8.25 mm bridge |
| 9 | All 12 slots mutually disconnected | PASS | §6 volume additivity |
| 10 | No large central through-hole | PASS | `top_view_plate.png` |
| 11 | Antenna plane 200 mm above ground | PASS | `side_view_ground_gap.png`, `oblique_view.png` |
| 12 | Top view matches V0.3 schematic | PASS | `top_view_plate.png` vs `docs/figures/R0_V03_12SLOT_TOPOLOGY_SCHEMATIC.svg` |

Item 12: the CST top view reproduces the repository schematic — a continuous
square plate with corner bridges, a mid-side bridge per side splitting the outer
family into two segments, and four inner radial slots stopping short of both the
centre and the outer family. No dimension was tuned.

## 8. Save / close / reopen audit

- Saved under the R0 build-only name above; closed; reopened fresh.
- Reopen inventory identical to Session B: 2 solids, 0 ports, no solver results.
- Reopen screenshot: `view_after_reopen.png`.

## 9. Prohibitions honored

No solver, no ports, no monitors, no dielectric/material stack, no QPL9547/LNA,
no shield/Bias-Tee, no L-band scaling, no dimension optimization, no V0.1/V0.2
geometry revival. The Fig.1 40 mm label was not reinterpreted: it is retained as
`fig40_unresolved = 40` and was **not** used to cut a centre hole or to force the
inner-slot spacing.

## 10. Findings / notes

1. **Corrected 12-slot topology built cleanly**; V0.2's single-per-side outer
   slot error is resolved into two segments per side.
2. **Fig.1 40 mm label** remains `SEMANTICS_UNRESOLVED`; the V0.3 centre clear
   span (60 mm) is a photo-derived estimate and is deliberately distinct.
3. **View-control quirk (as before).** `Plot.View` is invalid in this CST build;
   standard views require `Plot.RestoreView`, and reserved name `"Front"` yields
   the model Z-axis plan view, `"Bottom"` the in-plane elevation.
4. **Documentation nit for design side:** `PROJECT_HANDOFF.md` line 144 merges the
   tail of the CURRENT BASELINE section into the `# HOST TASK` heading
   (`... docs/R0_RECONSTRUCT# HOST TASK`); the task itself is unambiguous but the
   baseline paragraph is truncated.
5. **Benign CST startup messages.** `Access is denied.` twice on DE startup
   (configuration/cache); no effect on the model.
6. **CST project size** ~1 MB (folder project), git-ignored (`*.cst`); only path
   and SHA-256 are committed.

## 11. Hashes

```text
macro  source/cst/R0_CHARTS_12SLOT_BUILD_ONLY_V03.mcr
       08943e4208e3d852f38d154fb082bbc7fb734581a0ef4788c20a50e8f69d9e6d
project R0_1A3_12SLOT_BUILD_ONLY_H01.cst
       8502C38DA8EB66FE57D96C6A8DCECF449744618CA76E7B35044CD4E47581B491
top_view_full.png         22b09b2cc1cd852f667a84de505a884799748eac73fbb6cbe600741557fcf48c
top_view_plate.png        2cafeda201889f2ef819d4b61edad0969a3fe56b23724b1a8b2371404353ab3b
side_view_ground_gap.png  8b14fde9d60b32755b123f8a6fd3a4ed36391a2ef70ee98c14d1e47d8bd8c1bc
oblique_view.png          1d0dc87ad5c94460a5cfa224fbd8a0f8c60987ede83c3553697c4ed7c1418257
view_after_reopen.png     9f35ed31daf0e8617cd9f28842d2f5f8141b8fc507040d9eddccdc69e704d7fb
```

## 12. Next action

None issued. Per `PROJECT_HANDOFF.md` §4 the execution host stops here and the
design side reviews the outcome. No solver or further work is authorized.
