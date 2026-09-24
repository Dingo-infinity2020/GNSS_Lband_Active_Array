# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

DESIGN_R1E1A0_R1_PITCH_READY_CANONICAL_SOURCE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false

## Last formal execution

R1E1A0 endpoint pitch-parameterization BUILD-ONLY proof

Formal status:
HOLD_R1E1A0_SOURCE_HISTORY_PARAMETER_DECLARATION

Formal source commit:
750a036761c3b10a37830c95415b96c1436f3d29

Formal invocation count:
1

Runtime:
99.32 s

Solver:
NOT RUN

Endpoint artifacts:
- P088 SHA256: 65b649a28e148c8c373f06357caff36a8a4a65b06b898bf8abb96c196a3c688a
- P100 SHA256: 3746c521ffc628eddd257f96323980ac60b5183a36f536dc77876d99b1e5f779

Passed:
- pitch persistence
- structure span / UnitCellDs1/Ds2
- non-ground geometry invariance
- one-port / broadside periodic metadata
- fresh reopen
- no solver markers / results

Sole failed predicate:
no_pitch_history_warning

Root cause:
historical R1A3 model history contains StoreParameter for unit_cell_pitch_nominal=94, so CST emits a protected-parameter warning during parametric rebuild even though the requested pitch persists correctly.

Classification:
source-history/tooling HOLD; not a geometry or physics failure

Evidence:
evidence/r1e1a0_dc_nw_20260924_build01/

## Current recovery stage

Task:
R1E1A0-R1 pitch-ready 94-mm canonical source

Contract:
docs/R1E1A0R1_PITCH_READY_CANONICAL_SOURCE_CONTRACT.md

Runbook:
em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E1A0R1_PITCH_READY_SOURCE_BUILD_ONLY.md

Generator:
scripts/generate_r1e1a0r1_pitch_ready_macros.py

Harness:
scripts/run_r1e1a0r1_pitch_ready_source_build_only_dc.py

Static audit:
PASS_R1E1A0R1_STATIC_AUDIT

Recovery architecture:
derived pitch-ready R1A3 geometry macro + frozen R1A5F Pol-A single-port macro + derived parameter-ready periodic broadside macro

## Stop

R1 recovery build is not yet authorized in this closeout state.
No endpoint rerun.
No solver.
No material A/B.
No LNA integration.
