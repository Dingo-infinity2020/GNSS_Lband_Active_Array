# R0.1A2 SLOTTED-PLATE BUILD-ONLY — Host Return Report

**FINAL_STATUS = PASS_R0_V02_SLOTTED_TOPOLOGY_BUILD_ONLY**

- Task ID: `R0.1A2-SLOTTED-PLATE-BUILD-ONLY-H01`
- Host: H01 (DESKTOP-GBTI6Q4)
- Date: 2026-09-22
- Host start commit: `a3671b5afff0a0661b53d2de53db9697afcb5b17`
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

$ python scripts/audit_r0_slotted_plate_v02.py
PASS_R0_V02_STATIC_AUDIT
EXPECTED_FINAL_SOLIDS=2
EXPECTED_SLOT_SUBTRACTIONS=8
EXPECTED_PORTS=0
CENTER_THROUGH_HOLE=NO
SOLVER_RUN=NO
exit=0
```

Both required gates PASS before any CST action.

## 3. Method

`run_harness.py` drives CST through the Python API:

1. **Session A** — new MWS; the `Sub Main()` body (185 lines) of the committed
   `source/cst/R0_CHARTS_SLOTTED_PLATE_BUILD_ONLY_V02.mcr` was read, unwrapped,
   and executed verbatim via `Modeler.add_to_history`. The macro was not
   modified. Project saved and closed.
2. **Session B** — fresh open; screenshots + object/shape inventory.
3. **Session C** — second fresh open (fresh-reopen audit); inventory + screenshot.

Macro SHA-256: `2a5be60afa58b096888fd08588c5696c6a2733622678b0f9904690228f6bb398`
Unchanged from the repository copy. The V0.1 macro was not run.

## 4. Build result

- `add_to_history`: no error
- Saved: `D:\GNSS_Lband_Active_Array\_r0_1a2_h01_work\R0_1A2_SLOTTED_PLATE_BUILD_ONLY_H01.cst`
- Project SHA-256: `F429A52B784CECFA2F1ED123CD6FF7450DC91AB6FFA848E670892DB9E290C1CA`
- `Result\output.txt` is empty: no solver, port, mesh or excitation activity.

## 5. Definitive shape inventory

Enumerated with the CST `Solid` query API (`GetNumberOfShapes`,
`GetNameOfShapeFromIndex`, `GetVolume`, `IsSolidShape`) in both sessions:

```text
SHAPE_COUNT=2
ReferenceGround:GROUND_REFERENCE  volume=1000000        isSolid=TRUE
Radiator:ANTENNA_PLATE            volume=5347.225000... isSolid=TRUE
```

- All eight `SlotTools:CUT_*` cutters are absent (`SelectTreeItem` = 0 = False),
  i.e. consumed by boolean subtraction.
- `Components\SlotTools` still exists as an empty component (CST retains the
  component after subtraction); it contains no solids.
- 0 ports, 0 lumped elements, 0 solver results.

## 6. Connectivity / slot-independence proof

Volume arithmetic confirms one connected plate with eight non-overlapping cuts:

```text
full plate        247.5 * 247.5 * 0.1                       = 6125.625 mm^3
outer cuts (4)    4 * (2*83.75) * 8 * 0.1                   =  536.000 mm^3
inner cuts (4)    4 * (95.75 - 20) * 8 * 0.1                =  242.400 mm^3
expected remaining 6125.625 - 536.000 - 242.400             = 5347.225 mm^3
measured ANTENNA_PLATE volume                               = 5347.225 mm^3
```

The exact match proves the eight slot volumes are independent (no slot overlaps
another) and each lies fully within the plate; the plate therefore remains one
connected solid, matching reconstruction invariant D.

## 7. Mandatory visual review (top view vs Fig. 2(a))

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | One continuous square antenna/PCB silhouette | PASS | `top_view_plate.png` |
| 2 | Four outer slots near the perimeter | PASS | `top_view_plate.png` |
| 3 | Outer slots stop before corners | PASS | `top_view_plate.png` |
| 4 | Four inner slots form a cross / "田"-like partition | PASS | `top_view_plate.png` |
| 5 | Inner slots stop before the centre | PASS | `top_view_plate.png` |
| 6 | Inner slots stop before the outer slots | PASS | `top_view_plate.png` |
| 7 | All eight slot apertures mutually disconnected | PASS | `top_view_plate.png` + §6 |
| 8 | Central region remains solid (no through-hole) | PASS | `top_view_plate.png` |
| 9 | The plate remains one connected CST solid | PASS | §5/§6 (`SHAPE_COUNT=2`, `isSolid=TRUE`) |
| 10 | Topology materially closer to Fig. 2 than V0.1 | PASS | `top_view_plate.png` vs superseded V0.1 |

Side / oblique:

- antenna plate plane is 200 mm above the reference ground — PASS
  (`side_view_ground_gap.png`, `oblique_view.png`).

Note on item 10: the repository intentionally does not contain the copyrighted
Fig. 2(a). The comparison was made against the repository's documented Fig. 2
topology description in `refs/charts2025/FIGURE_EXTRACTION.md` (continuous board,
four outer + four inner disconnected slots, no central through-hole). The build
matches that description. A human with the paper should re-confirm the final
visual judgement. No dimensions were tuned; placeholders are unchanged.

## 8. Save / close / reopen audit

- Saved under the R0 build-only name above; closed; reopened fresh.
- Reopen inventory identical to Session B: 2 solids, 0 ports, no solver results.
- Reopen screenshot: `view_after_reopen.png`.

## 9. Prohibitions honored

No solver, no ports, no monitors, no dielectric/material stack, no LNA/shield/
Bias-Tee, no L-band scaling, no optimization, no numeric geometry change. The V0.1
petal/ring topology was not resurrected. Candidate C mapping was not altered.

## 10. Findings / notes

1. **Corrected topology rebuilt cleanly.** One continuous plate + eight
   disconnected slots; the V0.1 scientific error is not reproduced.
2. **View-control quirk (as before).** `Plot.View` is invalid in this CST build;
   standard views require `Plot.RestoreView`, and reserved name `"Front"` yields
   the model Z-axis plan view, `"Bottom"` the in-plane elevation.
3. **View-controlled screenshots** are taken from freshly opened saved projects
   (the API only applies `Plot.RestoreView` reliably then).
4. **Benign CST startup messages.** `Access is denied.` twice on DE startup
   (configuration/cache); no effect on the model.
5. **CST project size** ~1 MB (folder project), git-ignored (`*.cst`); only path
   and SHA-256 are committed.

## 11. Hashes

```text
macro  source/cst/R0_CHARTS_SLOTTED_PLATE_BUILD_ONLY_V02.mcr
       2a5be60afa58b096888fd08588c5696c6a2733622678b0f9904690228f6bb398
project R0_1A2_SLOTTED_PLATE_BUILD_ONLY_H01.cst
       F429A52B784CECFA2F1ED123CD6FF7450DC91AB6FFA848E670892DB9E290C1CA
top_view_full.png         65b717dfc2ed8b93d8e7d99397d929730cc98fef083bbf11002764d18f1dd96b
top_view_plate.png        63e23de4ce83c4132139d5b0543ca45366d2c6136d3d0265319ec7da764f2264
side_view_ground_gap.png  5278afd6b07d2e18dbf548fd2c9c146e168ae427aec9eca0cb7a6bf0a85524f7
oblique_view.png          9d77877271f676b591dcb4c8c5d872e6225068acd19864570e7c85284c6b86d8
view_after_reopen.png     dfa950f1535f3fd5d09fb698c86de3fe4b4672ccb186f88390799192ac97c5bc
```

## 12. Next action

None issued. Per `PROJECT_HANDOFF.md` §4 the execution host stops here and the
design side reviews the outcome. No solver or further work is authorized.
