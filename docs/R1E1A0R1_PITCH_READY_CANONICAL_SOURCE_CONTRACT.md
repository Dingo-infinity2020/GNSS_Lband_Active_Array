# R1E1A0-R1 Pitch-Ready Canonical Source Contract

Status: DESIGN FROZEN — BUILD NOT AUTHORIZED

## Why this recovery exists

The first R1E1A0 endpoint proof generated correct 88-mm and 100-mm periodic models, but formally HOLD because the historical R1A3 lineage still stores `unit_cell_pitch_nominal = 94` inside model history.

CST therefore preserved the user-updated pitch correctly while emitting the protected-parameter warning that the frozen A0 contract explicitly prohibited.

Formal HOLD:
`HOLD_R1E1A0_SOURCE_HISTORY_PARAMETER_DECLARATION`

This is a tooling/source-history issue, not a geometry or physics failure.

## Recovery principle

Do not weaken the frozen A0 predicate after seeing results.

Do not modify historical R1A3/R1A5F/R1E0A macros or artifacts.

Instead, build a new 94-mm canonical periodic Pol-A source from deterministic derived macros whose only semantic changes are the declarations of parameters intended for future sweeps.

## Historical provenance

R1A3 geometry macro:
`source/cst/R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr`

SHA256:
`1e5bb3188c5d19146b673ec54372d0c35ae572abc775512529f71db71cfad5be`

Historical R1A3 CST:
`D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst`

SHA256:
`b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa`

R1A5F Pol-A clean single-port macro:
`source/cst/R1A5F_POLA_SINGLE_PORT_BUILD_ONLY_V01.mcr`

SHA256:
`f2b4555413005596f5fa8ceefacc64b7cadbba2cce1c430f0c9c713a6f7aead9`

Historical R1A5F Pol-A CST:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst`

SHA256:
`74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce`

R1E0A periodic broadside macro:
`source/cst/R1E0A_PERIODIC_BROADSIDE_BUILD_ONLY_V01.mcr`

SHA256:
`eaa9c714978c76381424747307d635397084078ddbf235103d54c3b51275f7ff`

Historical R1E0A CST:
`D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst`

SHA256:
`48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223`

## Derived macros

Generator:
`scripts/generate_r1e1a0r1_pitch_ready_macros.py`

Generated geometry macro:
`source/cst/R1E1A0R1_PITCH_READY_R1A3_GEOMETRY_V01.mcr`

SHA256:
`6f54dc6b7e73160f48a974e214fa481773f0d342a80bdb1242d0316fa39be6b7`

Allowed differences from historical R1A3 macro:
- `StoreParameter "unit_cell_pitch_nominal", 94.0` -> `MakeSureParameterExists "unit_cell_pitch_nominal", "94.0"`;
- `StoreParameter "ground_reference_span", "unit_cell_pitch_nominal"` -> `MakeSureParameterExists "ground_reference_span", "unit_cell_pitch_nominal"`;
- provenance comments only.

Generated periodic macro:
`source/cst/R1E1A0R1_PARAMETER_READY_PERIODIC_BROADSIDE_V01.mcr`

SHA256:
`b96469c62337f1dab9cb71a0bcdb7a7666e8ec558ee4f937c565d75a66e0de54`

Allowed differences from historical R1E0A macro:
- `R1E0_pitch_nominal_mm` becomes a `MakeSureParameterExists` expression tied to `unit_cell_pitch_nominal`;
- `R1E0_scan_theta_deg` becomes `MakeSureParameterExists` with default 0;
- `R1E0_scan_phi_deg` becomes `MakeSureParameterExists` with default 45;
- provenance comments only.

Boundary physics remains unchanged.

## Build sequence

Start in a fresh MWS.

1. Add the derived pitch-ready R1A3 geometry macro to model history.
2. Add the frozen historical R1A5F Pol-A single-port macro unchanged.
3. Add the derived parameter-ready periodic broadside macro.
4. Save one final 94-mm canonical CST.
5. Close and fresh-reopen.
6. Audit read-only/direct-VBA; do not add audit entries to model history.

## Required equivalence checks

Geometry:
- exactly 3 solids;
- shape inventory equals the human-reviewed historical R1A3 geometry;
- no SlotTools/CopperGapTools residue.

Feed:
- exactly one discrete port;
- 100-ohm differential reference;
- Pol-A endpoint parameters reproduce the frozen R1A5F values.

Periodic configuration:
- X/Y boundaries = unit cell;
- Z boundaries = expanded open;
- broadside theta=0, phi=45, outward;
- structure X/Y span = 94 mm;
- UnitCellDs1/Ds2 = 94 mm;
- UnitCellAngle = 90 deg.

Parameter readiness:
- `unit_cell_pitch_nominal = 94`;
- `ground_reference_span` remains expression-dependent on `unit_cell_pitch_nominal`;
- `R1E0_pitch_nominal_mm` remains expression-dependent on `unit_cell_pitch_nominal`;
- scan theta/phi parameters persist;
- no protected-parameter history warning for pitch/span/theta/phi;
- generated macro check passes.

Execution hygiene:
- no solver markers;
- zero solver-generated result-tree items;
- build/reopen metadata identical;
- final CST hash recorded and protected.

## PASS

`PASS_R1E1A0R1_PITCH_READY_CANONICAL_SOURCE_BUILD_ONLY`

## HOLD

Any geometry, port, boundary, parameter-readiness, history-warning or fresh-reopen mismatch => HOLD.

## Stop boundary

R1 only builds the 94-mm canonical source.

Do not perform 88/100 endpoint mutation in R1.
No solver.
No material A/B.
No optimization.
No LNA integration.

After R1 PASS, open a separate R1E1A0-R2 endpoint-proof authorization.
