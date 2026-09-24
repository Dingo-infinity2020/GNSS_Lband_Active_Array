# R1E1A1 Six-Pitch FR4 Source Set Contract

Status: DESIGN FROZEN — BUILD NOT YET AUTHORIZED

## Source

`D:\GNSS_Lband_Active_Array\_r1e1a0r1_pitch_ready_source_work\R1E1A0R1_POLA_PERIODIC_PITCH_READY_94MM_V01.cst`

SHA256:
`585929d5bf9cbf46c4a6d0ae40b42baa8e2efff673f79c1026dcff33cb014fc2`

R1E1A0 canonical status:
`PASS_R1E1A0_PITCH_PARAMETERIZATION_MECHANISM`

## Pitch set

- 88 mm
- 90 mm
- 92 mm
- 94 mm
- 96 mm
- 100 mm

All variants remain:
- FR4 1.00-mm baseline;
- same radiator/substrate/feed;
- same one-port Pol-A definition;
- broadside theta=0, phi=45;
- same boundary types;
- no solver results.

## Required checks per source

- target pitch persists build/reopen;
- structure X/Y span = target pitch;
- UnitCellDs1/Ds2 = target pitch;
- non-ground geometry unchanged;
- no pitch-history warning;
- no solver markers/results;
- all six CST hashes unique.

## PASS

`PASS_R1E1A1_SIX_PITCH_FR4_SOURCE_SET_BUILD_ONLY`

## Stop

No solver.
No material A/B.
No LNA integration.
