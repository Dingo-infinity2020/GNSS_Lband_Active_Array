# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=18
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1A5M-ABSOLUTE-MESH-CONVERGENCE
CURRENT_TASK_ID=R1A5M-ADAPTIVE-SECOND-ORDER-SOLVE-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_SOLVE
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES_COPY_AND_CONFIG_ONLY
SOLVER_PERMISSION=YES_R1A5M_ONLY
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
CST251_PERMISSION=NO
```

## Background

R1A5 first-order diagnostic smoke:
- solver completed;
- symmetry gate HOLD at 1.504 dB max S11/S22 difference.

R1A5R second-order:
- PASS_R1A5R_SYMMETRY_CONVERGED;
- max S11/S22 difference reduced to 0.558 dB;
- reciprocity PASS;
- absolute first-vs-second S-parameter agreement still insufficient.

Therefore R1A5M fixes the second-order formulation and tests native h-refinement convergence.

## Immutable physical source

R1A4 CST:
`D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst`

Required SHA256:
`4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364`

## R1A5M frozen contract

Contract:
`docs/R1A5M_ADAPTIVE_MESH_CONVERGENCE_CONTRACT.md`

Config:
`source/cst/R1A5M_ADAPTIVE_SECOND_ORDER_CONFIG_V01.mcr`

Harness:
`scripts/run_r1a5m_adaptive_convergence_dc.py`

Static audit:
`PASS_R1A5M_STATIC_AUDIT`

Fixed:
- HF Frequency Domain
- second-order tetrahedral
- curvature order 3
- General purpose method
- 1.0–1.8 GHz
- open all six boundaries
- 50 mm background all directions
- unchanged geometry/materials/ports

Adaptive settings:
- HighFrequencyTet
- ExpertSystem
- MinPasses 3
- MaxPasses 6
- MaxDeltaS 0.02
- NumberOfDeltaSChecks 2
- LinearGrowthLimitation 40
- FDSolver.MeshAdaptionTet=True

## Baseline comparison

R1A5R compact baseline:
`evidence/r1a5r_dc_nw_20260924_second01/sparameters_and_zin.csv`

External convergence gate over 1.15–1.65 GHz:
- max complex delta S11 <= 0.05
- max complex delta S22 <= 0.05
- final max |S11_dB-S22_dB| <= 1.0 dB
- reciprocity <= 1e-3

## Authorized execution

Host:
NW / DESKTOP-GBTI6Q4

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1a5m_adaptive_work`

Fresh evidence:
`evidence/r1a5m_dc_nw_20260924_adapt01/`

Expected CST:
`D:\GNSS_Lband_Active_Array\_r1a5m_adaptive_work\R1A5M_ADAPTIVE_SECOND_ORDER_V01.cst`

Formal invocation:
exactly one.

Silent retry:
NO.

## Stop boundary

After this adaptive convergence qualification:
- return to DESIGN;
- no automatic second adaptive run;
- no material A/B;
- no geometry optimization;
- no CST251 staging.

If the adaptive run becomes unexpectedly heavy, classify HOLD and stop rather than silently migrating hosts.
