# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=29
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1E0B-BROADSIDE-PERIODIC-SMOKE
CURRENT_TASK_ID=R1E0B-DESIGN-BROADSIDE-PERIODIC-SMOKE
TASK_OWNER=DESIGN
TASK_STATUS=READY_FOR_DESIGN
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

The isolated-element passive stage is closed.

The project is now on the array-first mainline:
R1E0 periodic unit cell -> R1E1 pitch/material trade -> R1E2 active-impedance atlas -> active-front-end co-design.

## R1E0A closed stage

Original formal status:
`HOLD_R1E0A_PERIODIC_CONFIG_AUDIT`

Original HOLD classification:
`AUDIT_BOOLEAN_ENCODING_MISMATCH`

Read-only recovery status:
`PASS_R1E0A_PERIODIC_CONFIG_BUILD_ONLY_READONLY_RECOVERY`

Canonical stage conclusion:
`PASS_R1E0A_PERIODIC_CONFIG_BUILD_ONLY`

No CST rerun was performed during recovery.

No solver was run.

## Qualified periodic artifact

`D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst`

SHA256:
`48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223`

Qualified persisted metadata:
- one clean Pol-A differential port
- Xmin/Xmax = unit cell
- Ymin/Ymax = unit cell
- Zmin/Zmax = expanded open
- 94 x 94 mm unit-cell metadata
- theta = 0 deg
- phi = 45 deg
- outward scan direction
- geometry unchanged from clean R1A5F Pol-A
- no solver output

This artifact is PROTECTED_IN_PLACE because R1E0B consumes it.

## Current R1E0B design

Contract:
`docs/R1E0B_BROADSIDE_PERIODIC_SMOKE_CONTRACT.md`

Solver config:
`source/cst/R1E0B_PERIODIC_BROADSIDE_SOLVER_CONFIG_V01.mcr`

Static audit:
`PASS_R1E0B_STATIC_AUDIT`

Harness:
`scripts/run_r1e0b_broadside_periodic_smoke_dc.py`

Critical design rule:
R1E0B solver config contains no Boundary commands.

The qualified R1E0A periodic metadata must remain untouched.

Numerical formulation:
- HF Frequency Domain
- tetrahedral second order
- curvature order 3
- General purpose
- HighFrequencyTet / ExpertSystem adaptive
- MinPasses 3
- MaxPasses 8
- MaxDeltaS 0.02
- two Delta-S checks
- 1.0–1.8 GHz

Primary output:
broadside active differential impedance

Z_active = 100 * (1 + S11) / (1 - S11)

Broadside periodic Z_active is not required to equal isolated Zin.

## Current authorization

R1E0B is DESIGN ONLY.

No solver is currently authorized.

A future R1E0B solver authorization must freeze:
- exact source HEAD;
- fresh work/evidence paths;
- one-shot invocation;
- NW resource boundary;
- PASS/HOLD gate from the current contract.

## Next stage after R1E0B PASS

R1E0C first scan qualification:
- theta = 0, 30, 45, 60 deg
- primary Pol-A scan plane phi=45 deg
- orthogonal sentinel at theta=60 deg, phi=135 deg

No scan solver is authorized yet.
