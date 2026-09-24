# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=23
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1A5F-CLEAN-NONCROSSING-FEED
CURRENT_TASK_ID=R1A5F-SPLIT-SINGLE-PORT-BUILD-ONLY-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_BUILD_ONLY
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES_R1A5F_BUILD_ONLY
SOLVER_PERMISSION=NO
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
CST251_PERMISSION=NO
```

## Long-horizon authority

Read `PROJECT_MAINLINE.md` first.

This handoff executes M1 of the array-first mainline:
clean non-crossing passive feed -> short isolated equivalence -> R1E0 periodic unit cell.

Do not expand this gate into isolated-element optimization.

## Prerequisite

R1A5M2:
`PASS_R1A5M2_NATIVE_AND_ABSOLUTE_CONVERGED`

The crossed two-port model is a converged diagnostic baseline but is not the production feed representation for isolation.

## Immutable geometry source

Human-reviewed R1A3 CST:
`D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst`

Required SHA256:
`b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa`

## R1A5F frozen design

Plan:
`docs/R1A5F_SPLIT_SINGLE_PORT_FEED_PLAN.md`

Manifest:
`em/cst/R1_CHARTS_LBAND/parameters_r1a5f_single_ports.csv`

Canonical macro generator:
`scripts/generate_r1a5f_single_port_macros.py`

Static audit:
`PASS_R1A5F_STATIC_AUDIT`

Generated model A:
- Pol-A
- one 100 ohm differential discrete port
- NE -> SW
- no Pol-B port

Generated model B:
- Pol-B
- one 100 ohm differential discrete port
- NW -> SE
- exact Rz(+90 deg) rotation of model A
- no Pol-A port

Each model contains only one diagonal port, so no port-port crossing exists.

## Authorized build-only execution

Host:
NW / DESKTOP-GBTI6Q4

Runbook:
`em/cst/R1_CHARTS_LBAND/RUNBOOK_R1A5F_SPLIT_SINGLE_PORT_BUILD_ONLY.md`

Harness:
`scripts/run_r1a5f_split_single_port_build_only_dc.py`

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work`

Fresh evidence:
`evidence/r1a5f_dc_nw_20260924_build01/`

Expected CST A:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst`

Expected CST B:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLB_SINGLE_PORT_V01.cst`

## PASS gate

`PASS_R1A5F_SPLIT_SINGLE_PORT_BUILD_ONLY` requires:

For A and B:
- byte-identical R1A3 copy before port insertion;
- exactly one port after build;
- exactly one port after fresh reopen;
- shape inventory exactly equal to R1A3;
- no solver.

Cross-model:
- A/B geometry inventories identical;
- runtime endpoint parameters satisfy exact +90 degree rotation;
- both remain 100 ohm differential references.

## Formal execution discipline

- one formal harness invocation;
- no silent retry;
- preserve any HOLD evidence;
- no solver commands;
- no CST251 staging.

## Stop boundary

Stop after build/fresh-reopen qualification.

The next gate, if R1A5F passes, is a separately authorized **short isolated equivalence solve** only to confirm the clean single-port representation reproduces the converged passive baseline.

Do not begin periodic unit-cell solver work automatically in this task.
