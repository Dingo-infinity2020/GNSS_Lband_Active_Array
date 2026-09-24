# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=21
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A5F-DESIGN-SPLIT-SINGLE-PORT-FEED
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

## Closed numerical qualification

R1A5M2 final status:
`PASS_R1A5M2_NATIVE_AND_ABSOLUTE_CONVERGED`

Source HEAD:
`165707fe2da53e5c5ccf9b7e8d775f45017ec8b2`

R1A5M2 CST:
`D:\GNSS_Lband_Active_Array\_r1a5m2_maxpass8_work\R1A5M2_ADAPTIVE_MAXPASS8_V01.cst`

SHA256:
`1f904290293b49d4ad39d71cf3d3ddda86c81c2c202305e95f43b50ed477428e`

Runtime:
108.72 s

Native adaptation:
- pass 6 Delta-S = 0.0173367
- pass 7 Delta-S = 0.0175890
- two consecutive checks below 0.02
- termination by desired accuracy, not max passes
- broadband sweep convergence PASS

Incremental convergence versus R1A5M pass6:
- max complex delta S11 = 0.015124122
- max complex delta S22 = 0.015189754
- frozen threshold = 0.03

Symmetry:
- max Pol-A/B dB asymmetry = 0.013107094 dB

Reciprocity:
- max complex error = 7.96678e-05

## Converged diagnostic FR4 baseline

Sampled -10 dB matching:
- Pol-A: 1.1600 GHz through 1.8000 GHz sweep limit
- Pol-B: 1.1600 GHz through 1.8000 GHz sweep limit

At 1.15 GHz:
approximately -9.09 dB for both polarizations.

The current crossed two-port model remains diagnostic-only for S21/isolation.

## Current next task

R1A5F is DESIGN only.

Plan:
`docs/R1A5F_SPLIT_SINGLE_PORT_FEED_PLAN.md`

Direction:
create two separate single-port differential models from the human-reviewed R1A3 geometry:
- Model A: NE -> SW only
- Model B: NW -> SE only

This removes the central port-port crossing while preserving the exact polarization basis and 90-degree symmetry.

Direct two-port isolation is deferred to a future physically meaningful multi-conductor/active feed model.

No build or solver is currently authorized.

## Protected/checkpointed artifacts

Keep:
- R1A3 reviewed geometry
- R1A5M2 converged CST and compact evidence

Earlier R1A5/R1A5R/R1A5M workspaces remain checkpointed until a later dedicated host-hygiene closeout decides purge eligibility.
