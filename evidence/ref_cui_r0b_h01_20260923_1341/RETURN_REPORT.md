# REF-CUI-R0B DETERMINISTIC BUILD-ONLY — Host Return Report

**FINAL_STATUS = PASS_REF_CUI_R0B_BUILD_ONLY**

- Task ID: `REF-CUI-R0B-BUILD-ONLY-H01`
- Host: H01 (DESKTOP-GBTI6Q4)
- Date: 2026-09-23
- Host start commit: `3db2a75`
- Scope: CST 2022 deterministic build-only + fresh-reopen audit
- Solver / ports / monitors / optimization: **none**

## 1. Preflight (from `preflight.txt`)

```text
$ python scripts/audit_ref_cui_r0b_macro.py
PASS_REF_CUI_R0B_MACRO_STATIC_AUDIT
EXPECTED_SOURCE_PARAMETERS=26
EXPECTED_PORTS=0
EXPECTED_SOLVER_RUN=NO
exit=0
```

## 2. Build result

- Macro executed verbatim via the CST Python API in a fresh MWS; no error.
- Saved: `D:\GNSS_Lband_Active_Array\_ref_cui_r0b_work\REF_CUI_R0B_BUILD_ONLY_V01.cst`
- Macro SHA-256: `5df1aa152d38e67293536b38ddf51e2b5fb7df5d10f3c01d500502ec99a4ae90`
- Project SHA-256: see `harness_summary.json`.
- 0 ports, 0 lumped elements, 0 monitors; `Result` contains no solver output.

## 3. Definitive shape inventory (Session B; identical after reopen)

`SHAPE_COUNT=22`, all `isSolid=TRUE`:

- `MainGround:GROUND` — volume 33800 mm^3 (= 260*260*0.5).
- `RadiatorBoard:RADIATOR_SUB` — 11875 mm^3 (= 125*125*0.76).
- `Radiator:LOOP` — 90.1166 mm^3 (= (115^2 - 103.2^2)*0.035).
- `Radiator:ARMS` — 286.191 mm^3 (envelope Ld=97 minus cross gap, 4 slots, 4 tapers).
- `Balun1:BALUN1_SUB` + `Balun1:B1_{F1,F2,F3,STUB,UL,UR,TABR,TABL}`.
- `Balun2:BALUN2_SUB` + `Balun2:B2_{F1,F2,F3,STUB,UL,UR,TABR,TABL}`.

No `Tools` cutters remain (all consumed by boolean subtraction).

## 4. Parameter inventory

`PARAM_COUNT=47`: all 26 source symbols with their frozen values, plus material
(er=3.48, sub_t=0.76) and 19 documented CAD/derived parameters.

## 5. Visual build checks

| Check | Result | Evidence |
|---|---|---|
| 260 mm square ground | PASS | `top_view.png` (volume confirmed) |
| radiator board 80 mm above ground | PASS | `oblique_view.png`, `side_view.png` |
| square loop around crossed dipoles | PASS | `top_view.png` |
| four open slots | PASS | `top_view.png` |
| two orthogonal vertical balun boards | PASS | `underside_balun.png` |
| distinct Balun1 / Balun2 metal patterns | PASS | `underside_balun.png` |
| no loop-to-dipole short (3.1 mm gap) | PASS | `top_view.png` |
| no short between orthogonal baluns | PASS | `underside_balun.png` (offset balun_off) |
| fourfold radiator symmetry | PASS | `top_view.png` |

## 6. Save / close / fresh reopen

Saved, closed, reopened fresh: `reopen_inventory.txt` identical to
`object_inventory.txt` (22 solids, 0 ports, no solver result tree);
`view_after_reopen.png` captured.

## 7. Deliverables

- `source/cst/REF_CUI_R0B_BUILD_ONLY_V01.mcr` + identical `.bas`
- `scripts/audit_ref_cui_r0b_macro.py`
- `em/cst/REF_CUI_069_152/README.md`, `RUNBOOK_BUILD_ONLY.md`
- Evidence: `RETURN_REPORT.md`, `preflight.txt`, `object_inventory.txt`,
  `parameter_inventory.txt`, `construction_assumptions.md`, `reopen_inventory.txt`,
  `reopen_parameter_inventory.txt`, screenshots
  (`top_view.png`, `oblique_view.png`, `underside_balun.png`, `side_view.png`,
  `view_after_reopen.png`), `harness_log.txt`, `harness_summary.json`,
  `run_harness.py`, `hashes.txt`.

## 8. CAD assumptions and design action required

All source dimensions are exact. The arm/open-slot bend shape and the balun metal
polygon are **project CAD proxies** (see `construction_assumptions.md`); they are
the only non-source-explicit shape choices. Per the handoff stop rule, **design
must compare these screenshots against the user-supplied primary PDF** before any
passive solver gate is authorized.

## 9. Prohibitions honored

No solver, no ports, no monitors, no optimizer, no GNSS scaling, no LNA/QPL9547,
no CHARTS geometry edits, no S11 tuning, no mainline promotion. No source-frozen
dimension was changed. No publisher PDF/figure committed.

## 10. Next action

None issued. H01 stops; the design side reviews visually. No solver is
authorized.
