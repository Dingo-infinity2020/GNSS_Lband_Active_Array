# R1E1A0-R1 Pitch-Ready Canonical Source BUILD-ONLY Runbook

Status: DESIGN ONLY — BUILD NOT AUTHORIZED

## Host / tool

Host: NW
CST: 2022.5
Mode: BUILD_ONLY

## Inputs

Derived geometry macro:
`source/cst/R1E1A0R1_PITCH_READY_R1A3_GEOMETRY_V01.mcr`

Frozen Pol-A port macro:
`source/cst/R1A5F_POLA_SINGLE_PORT_BUILD_ONLY_V01.mcr`

Derived periodic macro:
`source/cst/R1E1A0R1_PARAMETER_READY_PERIODIC_BROADSIDE_V01.mcr`

Generator:
`scripts/generate_r1e1a0r1_pitch_ready_macros.py`

## Candidate future fresh paths

Work:
`D:\GNSS_Lband_Active_Array\_r1e1a0r1_pitch_ready_source_work`

Evidence:
`evidence/r1e1a0r1_dc_nw_20260924_build01/`

Expected CST:
`D:\GNSS_Lband_Active_Array\_r1e1a0r1_pitch_ready_source_work\R1E1A0R1_POLA_PERIODIC_PITCH_READY_94MM_V01.cst`

## Required preflight

- repository clean and on canonical branch;
- generator `--check` PASS;
- static audit PASS;
- future work/evidence paths absent;
- no residual modeler;
- historical source hashes exact;
- derived macro hashes exact.

## Formal execution

Exactly one formal build-only invocation after a separate authorization.

No silent retry.

## Stop

No endpoint mutation.
No solver.
No material A/B.
No LNA integration.
