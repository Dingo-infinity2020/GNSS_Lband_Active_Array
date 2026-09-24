# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=11
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1A4Q-CROSSED-DISCRETE-PORT-QUALIFICATION
CURRENT_TASK_ID=R1A4Q-TOY-PORT-TOPOLOGY-SOLVE-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_ISOLATED_DIAGNOSTIC
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES_TOY_ONLY
SOLVER_PERMISSION=YES_TOY_ONLY
PRODUCTION_MODEL_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
CST251_PERMISSION=NO
```

## Reason for reopening port qualification

The user identified a credible short-circuit risk in the R1A4 crossed diagonal discrete-port arrangement.

CST 2022.5 local documentation confirms that discrete edge ports are represented using perfect-conducting wire sections plus a central lumped/source element.

Therefore:
- R1A4 persistence/build PASS remains valid as a software-object result;
- R1A4 is NOT yet accepted as a solver-safe production feed model;
- R1A5 antenna smoke solve is suspended.

## Authorized diagnostic

Document:
`docs/R1A4Q_CROSSED_DISCRETE_PORT_TEST.md`

Host:
NW / DESKTOP-GBTI6Q4

Work:
`D:\GNSS_Lband_Active_Array\_r1a4q_crossed_port_test`

Models:
- CROSS.cst
- LIFTED_REFERENCE.cst

Frequency:
0.5–2.0 GHz

Solver:
HF Frequency Domain, first-order tetrahedral, mesh adaptation off.

Purpose:
compare crossed discrete-port behavior against a non-intersecting lifted reference.

## Hard stop

This authorization does NOT permit:
- opening the GNSS R1A4 CST in a solver;
- modifying GNSS R1A4 geometry;
- R1A5 smoke solve;
- CST251 staging;
- optimization.

After A/B diagnostics, return to DESIGN with results and recommendation.
