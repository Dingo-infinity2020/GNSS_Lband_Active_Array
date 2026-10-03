# R1E0C-B Scan Solve Runbook

Status: DESIGN ONLY — SOLVER NOT AUTHORIZED

## Purpose

Solve one qualified periodic scan-state CST per formal invocation and extract scan-dependent active S11/Z_active.

## Qualified source states

- C30P45: `e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2`
- C45P45: `ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed`
- C60P45: `94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01`
- C60P135: `c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1`

Source root:
`D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_recovery01`

## Solver config

`source/cst/R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr`

Static audit:
`PASS_R1E0C_B_SCAN_SOLVER_STATIC_AUDIT`

Invariants:
- no Boundary commands;
- no geometry/material/port commands;
- no YZ-matrix postprocessor;
- no solver-start command inside the config.

## Harness

`scripts/run_r1e0c_scan_solve_dc.py`

CLI inputs:
- repo
- evidence
- work
- source-cst
- state

Each state has an internal frozen theta/phi/source SHA registry.

## Formal execution discipline

One state = one formal invocation.

Fresh work/evidence per state.

No silent retry.

Any infrastructure/tooling failure => HOLD before retry.

Do not automatically continue to the next state after a HOLD.

## Suggested solve order

1. C30P45
2. C45P45
3. C60P45
4. C60P135

Broadside reference:
`evidence/r1e0b_dc_nw_20260924_smoke01/active_s11_and_zactive.csv`

## Outputs

- solved CST + SHA256
- active_s11_and_zactive.csv
- summary.json
- native_adaptation.json
- pre_solver_object_inventory.txt
- pre_solver_periodic_status.txt

## Stop

No solve is authorized by this runbook alone.

Future authorization must name the state(s) and retain one-shot per-state invocation semantics.
