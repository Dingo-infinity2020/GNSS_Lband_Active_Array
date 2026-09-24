# R1E1A0 Pitch Parameterization Contract

Status: DESIGN FROZEN — BUILD NOT AUTHORIZED

## Question

Can CST 2022.5 change the existing periodic pitch parameter through the Parameter List, rebuild the dependent model, and persist the new pitch without inserting a parameter-changing history step?

## Source

Use the clean R1E0A broadside periodic model:

`D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst`

Required SHA256:
`48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223`

Reason:
- clean broadside periodic boundary setup;
- no solver result;
- qualified one-port clean feed;
- existing pitch chain is already parameterized.

## Parameter chain

`unit_cell_pitch_nominal -> ground_reference_span -> UnitCellGround:UNITCELL_GROUND_REFERENCE X/Y span`

`Boundary.UnitCellFitToBoundingBox=True` then makes the periodic X/Y cell follow the resulting structure bounding box.

## Mutation method under test

Do not use `modeler.add_to_history` for the pitch change.

Use:
`project.schematic.execute_vba_code(...)`

with direct VBA:
`StoreParameter "unit_cell_pitch_nominal", <pitch_mm>`

then invoke CST `RebuildForParametricChange` in the same direct VBA transaction

and save/fresh-reopen.

This is specifically intended to avoid the R1E0C parameter-history warning pattern.

## Endpoint proof

Only two build-only variants are needed for A0:
- 88 mm;
- 100 mm.

These bracket the entire planned R1E1 pitch range.

## Invariants

The only intended physical model change is the periodic ground-tile/cell X/Y footprint.

Must remain unchanged:
- top radiator/copper shape;
- substrate shape;
- slots and feed geometry;
- substrate thickness/material;
- vertical ground-to-radiator spacing;
- port count and port definition;
- periodic boundary types;
- broadside scan metadata;
- solver state = never started.

## Required runtime checks per endpoint

- source SHA match before mutation;
- direct-VBA parameter mutation completes;
- `RebuildForParametricChange` completes;
- shape count remains 3;
- non-ground shape inventory equals the 94-mm source;
- structure X span = target pitch;
- structure Y span = target pitch;
- UnitCellDs1 = target pitch;
- UnitCellDs2 = target pitch;
- UnitCellAngle = 90 deg;
- X/Y boundaries remain unit cell;
- Z boundaries remain expanded open;
- port count remains 1;
- theta=0, phi=45, outward;
- `unit_cell_pitch_nominal` persisted value = target;
- fresh-reopen repeats all checks;
- no solver-execution markers;
- no new warning that `unit_cell_pitch_nominal` or `ground_reference_span` was prevented from changing inside history rebuild.

## PASS

`PASS_R1E1A0_PITCH_PARAMETERIZATION_BUILD_ONLY`

requires both 88-mm and 100-mm endpoint variants to pass all checks.

## HOLD examples

- parameter reverts to 94 mm after parametric rebuild;
- ground tile changes but periodic cell does not;
- radiator/substrate/feed changes;
- new parameter-history warning prevents pitch persistence;
- solver starts;
- build/reopen mismatch.

A HOLD is a tooling/model-parameterization result, not a physics failure.

## Stop boundary

Build-only endpoint proof.

No pitch screen solver.
No material A/B.
No optimization.
No LNA integration.

No solver is authorized.
