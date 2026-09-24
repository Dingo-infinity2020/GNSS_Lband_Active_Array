# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=15
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A5-DIAGNOSTIC-SMOKE-SOLVE-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_SOLVE
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES_COPY_AND_CONFIG_ONLY
SOLVER_PERMISSION=YES_R1A5_SMOKE_ONLY
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
CST251_PERMISSION=NO
```

## Prerequisites

R1A4:
PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY

R1A4Q:
PASS_R1A4Q_NO_HARD_SHORT_WITH_PARASITIC_COUPLING

R1A4 hash-locked input:
`D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst`

Required SHA256:
`4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364`

## R1A5 frozen contract

Authoritative design:
`docs/R1A5_SMOKE_SOLVE_CONTRACT.md`

Solver configuration:
`source/cst/R1A5_SMOKE_SOLVER_CONFIG_V01.mcr`

Static audit:
`PASS_R1A5_STATIC_AUDIT`

Configuration:
- HF Frequency Domain
- tetrahedral first order
- mesh adaptation OFF
- 1.0–1.8 GHz
- all six boundaries open
- 50 mm background space in all six directions
- existing two 100 ohm differential ports unchanged
- no far-field monitors
- no optimization
- no parameter sweep

## Port-model interpretation limit

R1A4Q showed that crossed discrete-edge ports do not hard-short in the qualified FD/tetra solver, but add an artificial coupling floor.

Therefore:
- S11/S22, resonance and Pol-A/B symmetry are primary smoke diagnostics;
- S21/S12 are qualitative only;
- coupling around/below roughly -50 dB is PORT_MODEL_LIMITED;
- no production polarization-isolation claim is allowed.

## Authorized execution

Host:
NW / DESKTOP-GBTI6Q4

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1a5_diagnostic_smoke_work`

Fresh evidence:
`evidence/r1a5_dc_nw_20260924_smoke01/`

Expected CST:
`D:\GNSS_Lband_Active_Array\_r1a5_diagnostic_smoke_work\R1A5_DIAGNOSTIC_SMOKE_V01.cst`

Formal invocation:
one shot only.

Silent retry:
NO.

## PASS gate

PASS_R1A5_DIAGNOSTIC_SMOKE requires:
- exact input hash;
- byte-identical copy before config;
- geometry unchanged;
- port count remains 2;
- all four S curves exist;
- no NaN/Inf;
- max complex reciprocity error <= 1e-3;
- max |S11_dB - S22_dB| <= 1.0 dB.

Return-loss magnitude itself is diagnostic, not a PASS threshold.

## Hard stop

After smoke result interpretation:
- no automatic geometry edit;
- no second smoke invocation;
- no material A/B;
- no production solve;
- no CST251 staging.

Return baton to DESIGN.
