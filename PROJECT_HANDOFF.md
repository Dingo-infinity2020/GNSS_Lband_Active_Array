# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=31
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1E0B-BROADSIDE-PERIODIC-SMOKE-RECOVERY
CURRENT_TASK_ID=R1E0B-R1-READONLY-RESULT-RECOVERY
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_READONLY_QUALIFICATION
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=NO
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO
CST251_PERMISSION=NO
```

## Long-horizon authority

Read `PROJECT_MAINLINE.md` first.

R1E0B solver authorization has been consumed by exactly one formal invocation.

No solver rerun is authorized.

## Original formal R1E0B invocation

Source HEAD:
`10b50b0102cd50a4f21ed2d5ee07da80e9c01a63`

Formal status:
`HOLD_R1E0B_RESULT_PATH_QUALIFICATION`

Invocation count:
1

Exit code:
1

Runtime:
99.99 s

Solved artifact:
`D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work\R1E0B_POLA_PERIODIC_BROADSIDE_SMOKE_V01.cst`

SHA256:
`339021e580efa6aae6dfcfa229e4194b4dcf0bbef854398d44a0efed65aac7ad`

## Solver evidence already established

Periodic adaptation:
- 0.0453805
- 0.0552784
- 0.0530417
- 0.0204615
- 0.0179226
- 0.0185901

Final two Delta-S values are below 0.02.

CST termination:
desired accuracy limit reached.

Broadband sweep:
converged after 7 frequency samples.

The solver recognized:
Theta=0, Phi=45.

Pre-solver periodic metadata remained valid.

## HOLD classification

The formal harness expected isolated result path:

`1D Results\S-Parameters\S1,1`

The periodic result tree uses:

`1D Results\S-Parameters\S1(1),1(1)`

Classification:
`PERIODIC_RESULT_PATH_NAMING_MISMATCH`

This is a post-solve qualification HOLD, not a solver/physics failure.

## R1E0B-R1 recovery

Mode:
READ ONLY.

Qualifier:
`scripts/qualify_r1e0b_existing_periodic_result.py`

Allowed:
- read solved CST through cst.results;
- verify solved artifact hash;
- read the actual periodic S11 path;
- export compact S11/Z_active CSV;
- re-parse existing native convergence;
- compare against isolated clean Pol-A context;
- preserve result-tree/warning evidence.

Forbidden:
- DesignEnvironment/modeler use;
- CST modification;
- rebuild;
- solver rerun;
- scan/pitch/material/LNA work.

The future R1E0B harness has been corrected to recognize periodic and isolated driven-port result names, but it will not be rerun in this stage.

## Stop boundary

If read-only recovery PASS:
- close R1E0B broadside periodic smoke as canonical PASS;
- open R1E0C first-scan DESIGN only.

If recovery HOLD:
- return to DESIGN.

No solver is currently authorized.
