# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=30
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1E0B-BROADSIDE-PERIODIC-SMOKE
CURRENT_TASK_ID=R1E0B-BROADSIDE-PERIODIC-SMOKE-SOLVE-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_SOLVE
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=YES_R1E0B_ONLY
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO
CST251_PERMISSION=NO
```

## Long-horizon authority

Read `PROJECT_MAINLINE.md` first.

R1E0B is the first actual solve of the infinite periodic array environment.

The authorization in this handoff is limited to one NW broadside periodic smoke solve.

It does not authorize:
- R1E0C scan sweep;
- pitch/material variation;
- LNA integration;
- geometry optimization;
- CST251 production solve.

## Qualified periodic source

`D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst`

Required SHA256:
`48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223`

Persisted periodic metadata:
- one clean Pol-A differential port
- X/Y = unit cell
- Z = expanded open
- 94 x 94 mm cell
- theta = 0 deg
- phi = 45 deg
- direction = outward

## R1E0B frozen contract

Contract:
`docs/R1E0B_BROADSIDE_PERIODIC_SMOKE_CONTRACT.md`

Solver config:
`source/cst/R1E0B_PERIODIC_BROADSIDE_SOLVER_CONFIG_V01.mcr`

Static audit:
`PASS_R1E0B_STATIC_AUDIT`

Harness:
`scripts/run_r1e0b_broadside_periodic_smoke_dc.py`

Critical invariant:
the solver config contains zero Boundary commands.

## Authorized numerical formulation

- HF Frequency Domain
- tetrahedral second order
- curvature order 3
- General purpose
- HighFrequencyTet / ExpertSystem adaptive
- MinPasses 3
- MaxPasses 8
- MaxDeltaS 0.02
- NumberOfDeltaSChecks 2
- LinearGrowthLimitation 40
- 1.0–1.8 GHz

## Formal execution

Host:
NW / DESKTOP-GBTI6Q4

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work`

Fresh evidence:
`evidence/r1e0b_dc_nw_20260924_smoke01/`

Expected result CST:
`D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work\R1E0B_POLA_PERIODIC_BROADSIDE_SMOKE_V01.cst`

Formal invocation count:
1

Silent retry:
NO

## PASS gate

`PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE` requires:
- source/copy hash gates pass;
- pre-solver periodic metadata remains valid;
- geometry remains unchanged;
- one discrete port remains;
- solver completes;
- non-empty finite S11;
- finite derived Z_active;
- final two native Delta-S <= 0.02;
- desired-accuracy termination;
- no max-pass termination;
- broadband sweep converged;
- no solver error lines.

The isolated clean Pol-A curve is contextual only and has no equality threshold.

## Stop boundary

After this one broadside periodic smoke:
- return to DESIGN;
- do not launch theta sweep;
- do not change pitch/material;
- do not integrate LNA;
- do not migrate to CST251 automatically.

On PASS, open R1E0C first-scan DESIGN only.
