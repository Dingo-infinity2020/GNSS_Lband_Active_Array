# R1E1A0 Pitch Parameterization BUILD-ONLY Runbook

Status: DESIGN ONLY — BUILD NOT AUTHORIZED

## Source

`D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst`

Source SHA256:
`48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223`

## Endpoint variants

- P088: 88.0 mm
- P100: 100.0 mm

## Mutation path

Use `project.schematic.execute_vba_code` with direct VBA `StoreParameter` for `unit_cell_pitch_nominal`.

Then call CST `RebuildForParametricChange` in the direct VBA snippet.

Do not insert the pitch mutation into modeler history.

## Future fresh paths

Work:
`D:\GNSS_Lband_Active_Array\_r1e1a0_pitch_parameterization_work`

Evidence:
`evidence/r1e1a0_dc_nw_20260924_build01/`

These paths are placeholders until a formal build authorization freezes the exact invocation.

## Runtime invariants

- shape count remains 3;
- non-ground shape inventory unchanged;
- structure X/Y span equals target pitch;
- UnitCellDs1/Ds2 equal target pitch;
- UnitCellAngle = 90 deg;
- X/Y boundaries = unit cell;
- Z boundaries = expanded open;
- port count = 1;
- broadside theta=0, phi=45, outward;
- no solver execution;
- no prevented-parameter warning for `unit_cell_pitch_nominal` or `ground_reference_span`;
- fresh reopen repeats all checks.

## PASS

`PASS_R1E1A0_PITCH_PARAMETERIZATION_BUILD_ONLY`

## Stop

No solver.
No material A/B.
No optimization.
No LNA integration.
