# PROJECT_HANDOFF.md

> Canonical operational handoff for GNSS L-band Active Array.

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=8
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A4-DESIGN-DIFFERENTIAL-PORT-FREEZE
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
- R1A3 human CST review: PASS on 2026-09-24

Reviewed immutable R1A3 source:
`D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst`

SHA256:
`b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa`

Human-review record:
`docs/R1A3_HUMAN_REVIEW_20260924.md`

## R1A4 objective

Qualify an ideal balanced two-port excitation without changing the reviewed R1A3 geometry.

R1A4 shall:
- copy the reviewed R1A3 CST into a fresh R1A4 work directory;
- never overwrite the reviewed R1A3 artifact;
- add only two ideal discrete differential ports;
- save, close, fresh reopen, and audit port persistence;
- prove shape inventory remains identical to R1A3;
- stop before any solver.

Proposed port contract:
- Port 1 / Pol-A: NE -> SW;
- Port 2 / Pol-B: NW -> SE;
- Port 2 is exact +90 degree rotation of Port 1;
- terminal radius = 3.00 mm;
- terminal z = top-copper surface;
- differential reference impedance = 100 ohm;
- no ground-referenced single-ended feed.

## Current boundary

R1A4 is DESIGN only.

BUILD_AUTHORIZED=NO
SOLVE_AUTHORIZED=NO

Next authorized transition requires:
- port design document;
- port parameter manifest;
- port-only builder/macro;
- static audit PASS;
- updated stage contract explicitly setting BUILD_AUTHORIZED=YES.

No solver is pre-authorized.
