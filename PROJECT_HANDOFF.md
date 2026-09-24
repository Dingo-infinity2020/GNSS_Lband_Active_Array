# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=16
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1A5R-NUMERICAL-SYMMETRY-CONVERGENCE
CURRENT_TASK_ID=R1A5R-SECOND-ORDER-SOLVE-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_SOLVE
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES_COPY_AND_CONFIG_ONLY
SOLVER_PERMISSION=YES_R1A5R_ONLY
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
CST251_PERMISSION=NO
```

## R1A5 attempt-1

Status:
`HOLD_R1A5_DIAGNOSTIC_INTEGRITY`

Solver completed successfully.
Only failed gate:
max |S11_dB-S22_dB| <= 1.0 dB.

Observed:
- max asymmetry = 1.504024537 dB @ 1.4136 GHz
- best Pol-A = -18.593128 dB @ 1.3976 GHz
- best Pol-B = -17.137847 dB @ 1.3936 GHz
- reciprocity error = 1.71625e-4
- all four S curves complete, 1001 points
- geometry/ports/hash provenance PASS

Evidence:
`evidence/r1a5_dc_nw_20260924_smoke01/`

## R1A5R purpose

Test numerical convergence before any physical design change.

Immutable input remains the original R1A4 CST:
`D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst`

Required SHA256:
`4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364`

R1A5R changes only numerical tetrahedral settings:
- second-order basis
- curvature order 3
- General purpose tetrahedral method
- adaptation OFF

Unchanged:
- geometry
- ports
- boundary
- 50 mm background
- 1.0–1.8 GHz
- solver family
- materials

Authoritative contract:
`docs/R1A5R_SYMMETRY_CONVERGENCE_CONTRACT.md`

Static audit:
`PASS_R1A5R_STATIC_AUDIT`

## Authorized execution

Host:
NW

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1a5r_second_order_work`

Fresh evidence:
`evidence/r1a5r_dc_nw_20260924_second01/`

Formal invocation:
one shot only.

Silent retry:
NO.

## PASS/HOLD

PASS_R1A5R_SYMMETRY_CONVERGED if:
- normal provenance/result gates pass;
- max |S11_dB-S22_dB| <= 1.0 dB.

Otherwise classify the numerical trend and return to DESIGN.

No geometry change, adaptation follow-up, optimization, material A/B, production solve or CST251 is pre-authorized.
