# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=12
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1A4Q-CROSSED-DISCRETE-PORT-QUALIFICATION
CURRENT_TASK_ID=R1A4Q-ATTEMPT2-TOY-PORT-TOPOLOGY-SOLVE-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_FRESH_ATTEMPT2
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES_TOY_ONLY
SOLVER_PERMISSION=YES_TOY_ONLY
PRODUCTION_MODEL_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
CST251_PERMISSION=NO
```

## Attempt-1 record

Attempt-1 source:
cc76c1c3d18b3e54df9267e6bdddb6f3269fe9ea

Status:
HOLD_R1A4Q_HARNESS_RUNTIME_BEFORE_SOLVER

Reason:
unsupported Python API call `modeler.evaluate()`.

Important:
- CROSS toy model was saved;
- failure occurred before `run_solver()`;
- solver_run=NO;
- no electromagnetic conclusion was produced;
- no silent retry was performed.

Evidence:
`evidence/r1a4q_dc_nw_20260924/`

Attempt-1 work is preserved:
`D:\GNSS_Lband_Active_Array\_r1a4q_crossed_port_test`

## Attempt-2 correction

Only harness-control code changes:
- replace unsupported Python `modeler.evaluate()`;
- use a CST VBA history command to write `Solver.GetNumberOfPorts()` to a text file;
- require port count = 2 before solver.

The frozen A/B geometry, port coordinates, solver type, frequency range, boundaries, and diagnostic logic are unchanged.

## Attempt-2 fresh paths

Work:
`D:\GNSS_Lband_Active_Array\_r1a4q_crossed_port_test_attempt2`

Evidence:
`evidence/r1a4q_dc_nw_20260924_attempt2/`

## Scope

Authorized only:
- CROSS toy model;
- LIFTED_REFERENCE toy model;
- HF Frequency Domain 0.5–2.0 GHz on NW;
- no adaptive mesh.

Forbidden:
- GNSS R1A4 CST solver;
- modification of GNSS R1A4 CST;
- R1A5 antenna solve;
- CST251;
- optimization.

Attempt-2 is a new explicit invocation, not a silent retry.
