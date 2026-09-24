# PROJECT_HANDOFF.md

> Canonical operational handoff for GNSS L-band Active Array.

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=9
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A4-DIFFERENTIAL-PORT-BUILD-ONLY-DC-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_BUILD_ONLY
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES
SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO
HARDWARE_PERMISSION=NO
```

## Prerequisite closure

R1A3 human CST review: PASS.
Record: `docs/R1A3_HUMAN_REVIEW_20260924.md`.

Immutable reviewed source:
`D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst`

Required SHA256:
`b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa`

## R1A4 frozen contract

Design:
`docs/R1A4_DIFFERENTIAL_PORT_DESIGN.md`

Manifest:
`em/cst/R1_CHARTS_LBAND/parameters_r1a4_ports.csv`

Port 1 / Pol-A:
- NE -> SW
- 100 ohm differential reference

Port 2 / Pol-B:
- NW -> SE
- exact +90 degree rotation of Port 1
- 100 ohm differential reference

Both endpoints use R1A2 terminal_r=3.00 mm and the R1A3 top-copper surface.
No ground reference is used.

Static audit:
`PASS_R1A4_STATIC_AUDIT`

The R1A4 macro is PORT-ONLY:
- 2 DiscretePort blocks
- 0 geometry commands
- 0 solver commands

## Authorized task

Host:
NW / DESKTOP-GBTI6Q4

Source bundle:
- source/cst/R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.mcr
- scripts/audit_r1a4_differential_ports.py
- scripts/run_r1a4_port_build_only_dc.py
- em/cst/R1_CHARTS_LBAND/parameters_r1a4_ports.csv
- em/cst/R1_CHARTS_LBAND/RUNBOOK_R1A4_PORT_BUILD_ONLY.md

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work`

Expected CST:
`D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst`

Evidence:
`evidence/r1a4_dc_nw_20260924_build01/`

## PASS gate

Required:
- source R1A3 hash exact match;
- fresh copied CST initially has identical hash;
- exactly 2 ports after build;
- exactly 2 ports after fresh reopen;
- shape inventory exactly matches R1A3;
- no solver.

Allowed final status:
`PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY`

On any formal runtime failure:
- preserve evidence;
- classify HOLD;
- no silent retry;
- do not alter port coordinates or invent ground reference.

## Stop boundary

Build authorization applies only to this port qualification.
No smoke solve is authorized by this handoff.
