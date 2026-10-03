# R0.1A TOPOLOGY BUILD-ONLY — Host Return Report

**FINAL_STATUS = PASS_R0_TOPOLOGY_BUILD_ONLY**

- Task ID: `R0.1A-TOPOLOGY-BUILD-ONLY-H01`
- Host: H01 (DESKTOP-GBTI6Q4)
- Date: 2026-09-22
- Host start commit: `cd91035893a6a3ad23dcd13a55f9b7c1a176a9e1`
- Scope: CST 2022 build-only runtime validation + fresh-reopen audit
- Solver / optimization / ports: **not run / not used / none created**

## 1. Toolchain

- CST Studio Suite 2022.5 (build 2022-06-03, change 981760)
- Automation: CST bundled Python 3.6 + `cst.interface` API (DesignEnvironment)
- Bundled Python path: `D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python\python.exe`
- Python gate scripts: Miniconda CPython 3.13.9

## 2. Preflight (from `preflight.txt`)

```text
$ python scripts/r0_manifest_gate.py --stage topology
PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY
exit=0

$ python scripts/audit_r0_topology_macro.py
PASS_R0_TOPOLOGY_MACRO_STATIC_AUDIT
EXPECTED_SOLIDS=9
EXPECTED_PORTS=0
SOLVER_RUN=NO
exit=0
```

Both required checks PASS before any CST action.

## 3. Method

`run_harness.py` drives CST through the documented Python API:

1. **Session A** — new MWS project; the `Sub Main()` body of the committed
   `source/cst/R0_CHARTS_TOPOLOGY_BUILD_ONLY_V01.mcr` (193 lines) was read,
   unwrapped, and executed verbatim via `Modeler.add_to_history`. Project saved
   and closed. No macro content was modified.
2. **Session B** — fresh open of the saved project; view-controlled screenshots
   and object inventory.
3. **Session C** — second fresh open (fresh-reopen audit); inventory + screenshot.

View control uses `Plot.RestoreView` with reserved names. In this CST build the
reserved name `"Front"` yields the view along the model Z axis (plan/top view),
`"Bottom"` yields the in-plane elevation exposing the 200 mm ground gap, and
`"Perspective"` the oblique view. Exact commands and per-file SHA-256 are in
`harness_log.txt` / `harness_summary.json`.

The CST API applies `Plot.RestoreView` reliably only in a session that has
freshly opened a saved project, so all screenshots were taken from the saved
artifact in Sessions B/C rather than in the unsaved build session.

## 4. Build result

- Macro body length: 193 lines
- `add_to_history`: no error
- Project saved: `D:\GNSS_Lband_Active_Array\_r0_1a_h01_work\R0_1A_TOPOLOGY_BUILD_ONLY_H01.cst`
- Project SHA-256: `100A8563ADE4A9B341338D2698AABC7C71D68633B7F6133F6403E384F8499518`
- No solver started; `Result\output.txt` contains no solver/port/mesh/S-parameter
  activity (only a cosmetic non-ASCII warning, see Findings).

## 5. Object inventory

`object_inventory.txt` (Session B) and `reopen_inventory.txt` (Session C) both
report all nine expected objects present (`SelectTreeItem` = `-1` = True):

| Component | Solids | Present |
|---|---|---|
| ReferenceGround | GROUND_REFERENCE | yes |
| Radiator | PETAL_N / E / S / W | yes |
| PassiveRing | RING_N / S / E / W | yes |

Total = 9 solids. 0 ports, 0 lumped elements (none are created by the macro; the
static audit forbids port/lumped-element tokens).

## 6. Parameter snapshot (Candidate A)

From both inventories (`PARAM_COUNT=18`):

| Parameter | Expression | Value |
|---|---|---|
| candidate_swap | 0 | 0 |
| fig227 | 227.5 | 227.5 mm |
| fig247 | 247.5 | 247.5 mm |
| center_opening | 40.0 | 40 mm |
| petal_span | fig227 + candidate_swap*(fig247-fig227) | 227.5 mm |
| ring_span | fig247 - candidate_swap*(fig247-fig227) | 247.5 mm |
| height_ground | 200.0 | 200 mm |
| petal_slit | 5.0 | 5 mm (placeholder) |
| ring_trace_width | 5.0 | 5 mm (placeholder) |
| ground_span | 1000.0 | 1000 mm (placeholder) |
| topology_t | 0.1 | 0.1 mm (placeholder) |

Candidate A mapping is materialized as intended.

## 7. Visual checks (Candidate A)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Fourfold rotational symmetry | PASS | `top_view_radiator.png` |
| 2 | Central square opening present | PASS | `top_view_radiator.png` |
| 3 | Four petal gaps electrically open | PASS | `top_view_radiator.png` |
| 4 | Passive ring surrounds petals, no contact | PASS | `top_view_radiator.png` |
| 5 | Radiator/ring plane 200 mm above ground | PASS | `side_view_ground_gap.png`, `oblique_view.png` |
| 6 | No malformed / self-crossing extruded polygon | PASS | `top_view_radiator.png` |
| 7 | Model tree names match runbook | PASS | `object_inventory.txt` |

`top_view_full.png` shows the radiator in context over the 1000 mm ground;
`top_view_radiator.png` hides the ground for topology detail. No geometry was
altered to resemble the paper.

## 8. Save / close / reopen audit

- Project saved under the R0 build-only name above.
- CST closed, then reopened fresh.
- Reopen inventory confirms the same 9 solids, 0 ports.
- No solver-result tree created by this task (`Result\output.txt` clean).
- Reopen screenshot: `view_after_reopen.png`.
- `reopen_inventory.txt` matches `object_inventory.txt`.

## 9. Prohibitions honored

No solver, no ports, no monitors, no substrate/dielectric, no QPL9547/LNA, no
Bias-Tee, no L-band scaling, no optimization, no geometry repair, no Candidate B
switch, no numeric geometry change. The committed macro was executed unmodified.

## 10. Findings / limitations

1. **Non-ASCII characters in the macro.** `output.txt` warns that history block 1
   contains non-ASCII characters. The macro contains two U+2014 em dashes
   (UTF-8 `E2 80 94`) at byte offsets 69–71 and 5072–5074; the second lies inside
   the `Sub Main()` body (a comment separator). No functional impact was
   observed, but for replay-safe portability the design side may wish to replace
   the em dashes with ASCII `-`.
2. **View control quirk.** The reserved view name `"Front"` yields the model
   Z-axis (plan) view in this CST build; `Plot.View` is not a valid command and
   silently aborts a history block. Recorded for future host runs.
3. **Build-session screenshots.** `Plot.RestoreView`/`Plot.ExportImage` are only
   reliable after a fresh open of a saved project, hence the three-session
   structure.
4. **Benign CST messages.** `Access is denied.` appears twice on DE startup
   (configuration/cache), and an initial collection run produced identical
   screenshots until the corrected view commands were used. No effect on the
   saved model.
5. **CST project size** is ~1 MB (folder project) and is git-ignored (`*.cst`);
   only its path and SHA-256 are committed here.

## 11. Commands and hashes

See `harness_log.txt` and `harness_summary.json`. Screenshot SHA-256:

```text
top_view_full.png         765c4f218e74c7024af7d14be4a4b403729cd71e65076d3073d415670bb4d1fc
top_view_radiator.png     1b3d1e7b54f8331cfed2026908c73f46716c14362898b5bac24756b29ad5272c
side_view_ground_gap.png  90511ad2de317c0eedbb01e546c9cbd937f3b34bdff777cab14c7ce1af8ea8b0
oblique_view.png          9a0151ff3902c391e455cb2cb61b0dadc7fa29f8962c64763372af0451d452b8
view_after_reopen.png     e35cf41f341cb018ce63ed15a33fb5c2c7f6586b6424ffff122b8dd479aecd1e
```

## 12. Next action

None issued. Per `PROJECT_HANDOFF.md` §4 the execution host stops here and the
design side reviews the outcome. No solver or further work is authorized.
