# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=20
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1A5M2-ADAPTIVE-CONVERGENCE-RECOVERY
CURRENT_TASK_ID=R1A5M2-MAXPASS8-RECOVERY-SOLVE-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_SOLVE
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES_COPY_AND_CONFIG_ONLY
SOLVER_PERMISSION=YES_R1A5M2_ONLY
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
CST251_PERMISSION=NO
```

## Trigger

R1A5M:
HOLD_R1A5M_ADAPTIVE_NOT_CONVERGED

Native Delta-S:
0.0673917 -> 0.0497934 -> 0.0274924 -> 0.0203932 -> 0.0173369

CST stopped because MaxPasses=6 was reached before two consecutive checks were below 0.02.

## R1A5M2 scientific freeze

Contract:
`docs/R1A5M2_MAXPASS_RECOVERY_CONTRACT.md`

Config:
`source/cst/R1A5M2_ADAPTIVE_MAXPASS8_CONFIG_V01.mcr`

Harness:
`scripts/run_r1a5m2_maxpass_recovery_dc.py`

Static audit:
`PASS_R1A5M2_STATIC_AUDIT`

Exactly one permitted solver-setting change:
- MaxPasses: 6 -> 8

Everything else remains identical to R1A5M:
- HF Frequency Domain
- tetrahedral second order
- curvature order 3
- General purpose
- HighFrequencyTet / ExpertSystem
- MinPasses 3
- MaxDeltaS 0.02
- NumberOfDeltaSChecks 2
- LinearGrowthLimitation 40
- 1.0–1.8 GHz
- open boundaries
- 50 mm background
- unchanged geometry/materials/ports

## Immutable physical source

R1A4:
`D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst`

SHA256:
`4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364`

## Incremental baseline

R1A5M pass-6 final compact result:
`evidence/r1a5m_dc_nw_20260924_adapt01/sparameters_and_zin.csv`

R1A5M CST SHA256:
`67b44e77aa88709287caf194c8e89cc2535951e1fab66b7c679df9e398a62c9b`

## PASS gate

Native:
- final two consecutive Delta-S values <= 0.02;
- no max-pass termination;
- broadband sweep converged;
- no solver error lines.

External over 1.15–1.65 GHz:
- max complex delta S11 vs R1A5M pass6 <= 0.03;
- max complex delta S22 vs R1A5M pass6 <= 0.03;
- max Pol-A/B dB asymmetry <= 1.0;
- reciprocity <= 1e-3;
- complete finite curves.

PASS:
`PASS_R1A5M2_NATIVE_AND_ABSOLUTE_CONVERGED`

## Execution

Host:
NW / DESKTOP-GBTI6Q4

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1a5m2_maxpass8_work`

Fresh evidence:
`evidence/r1a5m2_dc_nw_20260924_recovery01/`

Exactly one formal invocation.
No silent retry.

## Stop boundary

After this recovery solve:
- return to DESIGN;
- no further automatic pass extension;
- no material A/B;
- no geometry optimization;
- no CST251 staging.
