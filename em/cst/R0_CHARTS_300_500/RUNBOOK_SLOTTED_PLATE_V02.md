# R0.1A2 CHARTS Slotted-Plate BUILD-ONLY Runbook

Status: **READY FOR HOST BUILD-ONLY REVIEW**

## Scientific correction

V0.1 separate petals/ring is superseded.

V0.2 models the Fig.2 topology as:
- one continuous square PEC proxy plate,
- four disconnected outer slots,
- four disconnected inner slots,
- no central through-hole,
- one reference ground.

This is still a reconstruction hypothesis, not an exact CHARTS replica.

## Preflight

Run:

```bash
python scripts/r0_manifest_gate.py --stage topology
python scripts/audit_r0_slotted_plate_v02.py
```

Expected:

```text
PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY
PASS_R0_V02_STATIC_AUDIT
EXPECTED_FINAL_SOLIDS=2
EXPECTED_SLOT_SUBTRACTIONS=8
EXPECTED_PORTS=0
CENTER_THROUGH_HOLE=NO
SOLVER_RUN=NO
```

## CST execution

Fresh MWS project.

Run:

`source/cst/R0_CHARTS_SLOTTED_PLATE_BUILD_ONLY_V02.mcr`

Do not run the old V0.1 macro.

## Expected final object inventory

- `ReferenceGround:GROUND_REFERENCE`
- `Radiator:ANTENNA_PLATE`

The eight slot cutter solids should be consumed by boolean subtraction.

Expected:
- 2 final solids,
- 0 ports,
- 0 lumped elements,
- 0 solver results.

## Visual topology checks

Top view must show:

1. one continuous square plate,
2. four outer elongated slots near the perimeter,
3. outer slots stop before corners,
4. four inner elongated slots forming a cross / "田"-like partition,
5. inner slots stop before the central region,
6. inner slots stop before outer slots,
7. all 8 slots are mutually disconnected,
8. no central square through-hole,
9. central solid region remains available for electronics/feed,
10. topology visually resembles CHARTS Fig.2(a) much more closely than V0.1.

Side/oblique view:
- plate is 200 mm above reference ground.

## Fresh-reopen audit

Save, close CST, reopen fresh, verify:
- same 2 final solids,
- 0 ports,
- no solver results.

## Allowed final statuses

- `PASS_R0_V02_SLOTTED_TOPOLOGY_BUILD_ONLY`
- `HOLD_R0_V02_VISUAL_MISMATCH`
- `HOLD_R0_V02_CST_RUNTIME_SYNTAX`
- `FAIL_R0_V02_REPLAY`

## Prohibitions

No solver, no port, no monitor, no dielectric, no LNA, no shield, no Bias-Tee, no L-band scaling, no optimization.
