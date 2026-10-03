# R0.1A3 CHARTS 12-Slot BUILD-ONLY Runbook

Status: **READY FOR HOST BUILD-ONLY REVIEW**

## Scientific context

V0.1 and V0.2 remain preserved as execution evidence but are scientifically superseded.

V0.3 is constrained by direct Fig.2 review:

- one continuous square plate,
- 8 outer slot segments (2 per side),
- 4 inner radial slots,
- 12 disconnected slot apertures total,
- no large central through-hole.

The Fig.1 40 mm label remains semantics-unresolved and is not used to define the center clear span.

## Preflight

Run:

```bash
python scripts/r0_manifest_gate.py --stage topology
python scripts/audit_r0_12slot_v03.py
```

Expected:

```text
PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY
PASS_R0_V03_STATIC_AUDIT
EXPECTED_FINAL_SOLIDS=2
EXPECTED_OUTER_SLOT_SEGMENTS=8
EXPECTED_INNER_SLOT_SEGMENTS=4
EXPECTED_SLOT_SUBTRACTIONS=12
EXPECTED_PORTS=0
CENTER_THROUGH_HOLE=NO
FIG40_SEMANTICS=UNRESOLVED
SOLVER_RUN=NO
```

## CST execution

Use a fresh MWS project.

Run:

`source/cst/R0_CHARTS_12SLOT_BUILD_ONLY_V03.mcr`

Do not run V0.1 or V0.2.

## Expected final inventory

- `ReferenceGround:GROUND_REFERENCE`
- `Radiator:ANTENNA_PLATE`

Expected:
- 2 final solids,
- 12 consumed slot cutters,
- 0 ports,
- 0 lumped elements,
- 0 solver results.

## Geometry values under review

- board span = 247.5 mm
- outer slot-frame centerline span = 227.5 mm
- outer slot width = 5 mm
- each outer slot segment length = 94.125 mm
- side-midpoint bridge = 18 mm
- inner slot width = 9 mm
- inner slot length = 73 mm
- visible center clear span = 60 mm
- height above ground = 200 mm

Reference schematic:
`docs/figures/R0_V03_12SLOT_TOPOLOGY_SCHEMATIC.svg`

## Mandatory build checks

1. one connected antenna solid,
2. eight outer slot apertures,
3. exactly two outer slots on each side,
4. midpoint conductor bridge on each side,
5. conductor remains at all four corners,
6. four inner radial slots,
7. inner slots stop before center,
8. inner slots stop before outer slots,
9. no slot overlaps another,
10. no large central through-hole,
11. 200 mm height over ground,
12. build resembles the repository V0.3 schematic.

Do not tune dimensions.

## Save / close / reopen

Save, close CST, reopen fresh and verify:
- 2 final solids,
- 0 ports,
- no solver result tree.

## Required evidence

Create:

`evidence/r0_1a3_h01_<YYYYMMDD_HHMM>/`

Include:
- `RETURN_REPORT.md`
- `preflight.txt`
- `object_inventory.txt`
- `reopen_inventory.txt`
- top-view screenshot
- oblique/side screenshot
- fresh-reopen screenshot
- project path + SHA-256 if CST project remains git-ignored

Allowed final statuses:

- `PASS_R0_V03_12SLOT_TOPOLOGY_BUILD_ONLY`
- `HOLD_R0_V03_VISUAL_MISMATCH`
- `HOLD_R0_V03_CST_RUNTIME_SYNTAX`
- `FAIL_R0_V03_REPLAY`

## Prohibitions

No solver, ports, monitors, dielectric/material stack, LNA, shield, Bias-Tee, L-band scaling, parameter optimization, or reinterpretation of the 40 mm label.
