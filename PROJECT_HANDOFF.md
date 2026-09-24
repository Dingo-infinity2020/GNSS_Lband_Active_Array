# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=24
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1A5FQ-CLEAN-FEED-EQUIVALENCE
CURRENT_TASK_ID=R1A5FQ-DESIGN-ISOLATED-EQUIVALENCE
TASK_OWNER=DESIGN
TASK_STATUS=READY_FOR_DESIGN
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=NO
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
CST251_PERMISSION=NO
```

## Long-horizon authority

Read `PROJECT_MAINLINE.md` first.

The array-first route is:
R1A5FQ short isolated equivalence -> R1E0 periodic unit cell -> R1E1 pitch/material trade -> R1E2 active-impedance atlas.

Do not expand R1A5FQ into isolated-element optimization.

## R1A5F closed stage

Final status:
`PASS_R1A5F_SPLIT_SINGLE_PORT_BUILD_ONLY`

Formal source HEAD:
`b914822134ca6d3e2cc4cdca9de801e38d13863a`

Formal invocation count:
1

Exit:
0

Runtime:
113.17 s

Solver:
NOT RUN

## Protected clean-feed artifacts

Model A / Pol-A / NE->SW:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst`

SHA256:
`74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce`

Model B / Pol-B / NW->SE:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLB_SINGLE_PORT_V01.cst`

SHA256:
`11ca4ae06baa1d3f18376789c90717f28aee2b02480d7eba88d2f5155d51a1bf`

R1A5F checks:
- one port per model after fresh reopen: PASS
- A/B geometry identical to R1A3: PASS
- exact runtime +90 deg endpoint relation: PASS
- same 100 ohm differential normalization: PASS
- no simultaneous port crossing: PASS

Evidence:
`evidence/r1a5f_dc_nw_20260924_build01/`

Both CST artifacts are retained and purge is forbidden while R1A5FQ/R1E0 may consume them.

## Current R1A5FQ design

Contract:
`docs/R1A5FQ_ISOLATED_EQUIVALENCE_CONTRACT.md`

Scientific question:
confirm that the two clean single-port models reproduce the already converged R1A5M2 passive self-response.

This gate is the final isolated-element equivalence check.

No solver is currently authorized.

## Next mainline gate after R1A5FQ PASS

R1E0:
94-mm periodic unit-cell baseline.

The project must move to scan-dependent active impedance after equivalence closure rather than continue isolated S11 optimization.
