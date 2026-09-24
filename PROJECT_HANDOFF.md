# PROJECT_HANDOFF.md

> Canonical operational handoff for GNSS L-band Active Array.

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=10
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A5-DESIGN-SMOKE-SOLVE-CONTRACT
TASK_OWNER=DESIGN
TASK_STATUS=READY_FOR_DESIGN
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO
HARDWARE_PERMISSION=NO
```

## Closed stages

- R1A1: PASS_R1A1_SCALED_APERTURE_BUILD_ONLY
- R1A2: PASS_R1A2_FEED_REFERENCE_BUILD_ONLY
- R1A3: PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
- R1A3 human review: PASS
- R1A4: PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY

## R1A4 closeout

Formal source HEAD:
`80648b960d7d3ce91e6af99f52b9913637b1e820`

R1A4 CST:
`D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst`

SHA256:
`4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364`

Bytes:
`47220`

Port count:
- build = 2
- fresh reopen = 2

Geometry identity:
- exact shape-inventory match to reviewed R1A3 = PASS
- no geometry commands existed in the R1A4 port-only macro

Solver:
- NOT RUN

Evidence:
`evidence/r1a4_dc_nw_20260924_build01/`

## Current next stage

R1A5 is DESIGN only.

Goal:
freeze a lightweight isolated-element smoke-solve contract for the hash-locked R1A4 CST.

The smoke stage must define before authorization:
- solver family;
- boundary conditions;
- frequency window;
- mesh policy;
- excitation policy;
- diagnostic outputs;
- PASS/HOLD criteria;
- exact stop boundary.

No solver is authorized by this handoff.

The R1A4 CST remains checkpointed and purge_allowed=false because it is the candidate immutable source for R1A5.
