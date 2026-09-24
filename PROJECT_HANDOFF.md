# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=25
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1A5FQ-CLEAN-FEED-EQUIVALENCE
CURRENT_TASK_ID=R1A5FQ-CLEAN-FEED-EQUIVALENCE-SOLVE-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_SOLVE
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=YES_R1A5FQ_ONLY
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
CST251_PERMISSION=NO
```

## Long-horizon authority

Read `PROJECT_MAINLINE.md` first.

R1A5FQ is the final isolated-element equivalence gate.

On PASS:
- close isolated passive element qualification;
- next primary physics gate = R1E0 94-mm periodic unit cell.

No isolated optimization is permitted.

## Inputs

Model A:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst`

SHA256:
`74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce`

Model B:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLB_SINGLE_PORT_V01.cst`

SHA256:
`11ca4ae06baa1d3f18376789c90717f28aee2b02480d7eba88d2f5155d51a1bf`

Baseline:
`evidence/r1a5m2_dc_nw_20260924_recovery01/sparameters_and_zin.csv`

## Frozen contract

`docs/R1A5FQ_ISOLATED_EQUIVALENCE_CONTRACT.md`

Static audit:
`PASS_R1A5FQ_STATIC_AUDIT`

Solver config:
`source/cst/R1A5FQ_EQUIVALENCE_SOLVER_CONFIG_V01.mcr`

Harness:
`scripts/run_r1a5fq_clean_feed_equivalence_dc.py`

## Numerical formulation

Identical to converged R1A5M2:
- HF Frequency Domain
- tetrahedral second order
- curvature order 3
- General purpose
- HighFrequencyTet adaptive
- ExpertSystem
- MinPasses 3
- MaxPasses 8
- MaxDeltaS 0.02
- two Delta-S checks
- 1.0–1.8 GHz
- open all six faces
- 50 mm background

No geometry, material, or port changes.

## PASS gate over 1.15–1.65 GHz

`PASS_R1A5FQ_CLEAN_FEED_EQUIVALENT` requires:

- A and B native adaptive convergence by desired accuracy;
- no max-pass termination;
- complete finite curves;
- max complex delta A vs R1A5M2 S11 <= 0.03;
- max complex delta B vs R1A5M2 S22 <= 0.03;
- max complex delta A vs B <= 0.02;
- max A/B dB difference <= 0.5 dB.

## Execution

Host:
NW / DESKTOP-GBTI6Q4

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1a5fq_equivalence_work`

Fresh evidence:
`evidence/r1a5fq_dc_nw_20260924_equiv01/`

One formal harness invocation only.
The harness solves A then B sequentially.

Silent retry:
NO.

## Stop boundary

After equivalence interpretation:
- return to DESIGN;
- no isolated optimization;
- no material A/B;
- no far-field production study;
- no periodic solve inside this task;
- no CST251 staging.

If PASS, open R1E0 periodic unit-cell DESIGN.
