# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=26
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1E0-PERIODIC-UNIT-CELL-BASELINE
CURRENT_TASK_ID=R1E0-DESIGN-PERIODIC-UNIT-CELL-94MM
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

The isolated-element passive qualification is now CLOSED.

The active-array mainline has moved to:
R1E0 periodic unit cell -> R1E1 pitch/material array trade -> R1E2 active-impedance atlas.

Do not reopen isolated-element S11 optimization unless a later array result demonstrates a quantified need.

## Closed R1A5FQ stage

Final status:
`PASS_R1A5FQ_CLEAN_FEED_EQUIVALENT`

Formal source HEAD:
`9d4d7dbf0741df2776298c2be51fa8df26ff3427`

Formal invocation count:
1

Exit:
0

Runtime:
180.64 s

Key equivalence:
- A vs R1A5M2 max complex delta = 0.008537500
- B vs R1A5M2 max complex delta = 0.008399949
- clean A vs clean B max complex delta = 0.012309052
- clean A vs clean B max dB difference = 0.456468929 dB

All frozen equivalence gates PASS.

## Clean passive feed basis

Canonical periodic-array starting sources remain the clean R1A5F no-result CSTs:

Pol-A:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst`

SHA256:
`74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce`

Pol-B:
`D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLB_SINGLE_PORT_V01.cst`

SHA256:
`11ca4ae06baa1d3f18376789c90717f28aee2b02480d7eba88d2f5155d51a1bf`

R1A5FQ result CSTs and compact evidence remain checkpointed/protected for provenance, but periodic design should derive from the clean R1A5F source models rather than solver-result-bearing copies.

## Current task: R1E0 design

Scientific goal:
establish the first periodic/unit-cell workflow for the actual array environment.

Initial baseline from PROJECT_MAINLINE.md:
- square lattice
- pitch = 94 mm
- FR4 baseline
- clean single differential polarization per model
- x/y periodic or unit-cell phase boundaries
- radiating/open z direction
- scan-dependent active differential impedance
- no LNA yet

First R1E0 qualification set should remain small:
- broadside
- theta = 30 deg
- theta = 45 deg
- theta = 60 deg
- representative low/mid/high L-band frequencies

Before authorizing a solver:
- verify CST 2022.5 boundary/scan API from installed examples/documented macros;
- freeze exact phase/sign convention;
- freeze whether model A alone is sufficient for first workflow proof or whether A/B both are required;
- define broadside sanity relation to the clean isolated baseline;
- define scan-blindness/anomaly metrics;
- define lightweight NW versus CST251 routing.

No periodic build or solver is currently authorized.
