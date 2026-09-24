# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=32
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1E0C-FIRST-SCAN-QUALIFICATION
CURRENT_TASK_ID=R1E0C-A-DESIGN-SCANSTATE-BUILD-ONLY
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

The project is now in actual periodic-array physics.

Mainline:
R1E0 scan qualification -> R1E1 pitch/material trade -> R1E2 active-impedance atlas -> active-front-end co-design.

Do not return to isolated-element S11 optimization unless a later array result provides a quantified reason.

## R1E0B closed stage

Original formal status:
`HOLD_R1E0B_RESULT_PATH_QUALIFICATION`

Original HOLD classification:
`PERIODIC_RESULT_PATH_NAMING_MISMATCH`

Read-only recovery status:
`PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE_READONLY_RECOVERY`

Canonical stage conclusion:
`PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE`

Formal solver invocation count:
1

Solver rerun during recovery:
NO

## Protected solved broadside artifact

`D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work\R1E0B_POLA_PERIODIC_BROADSIDE_SMOKE_V01.cst`

SHA256:
`339021e580efa6aae6dfcfa229e4194b4dcf0bbef854398d44a0efed65aac7ad`

Periodic driven-port result path:
`1D Results\S-Parameters\S1(1),1(1)`

Native adaptation:
0.0453805 -> 0.0552784 -> 0.0530417 -> 0.0204615 -> 0.0179226 -> 0.0185901

Final two Delta-S values < 0.02:
PASS

Termination:
desired accuracy limit reached

Broadband sweep:
PASS after 7 frequency samples

## Broadside 94-mm array result

Science band:
1.15–1.65 GHz

Broadside active-impedance range:
- Re(Z_active): 85.05 to 264.39 ohm
- Im(Z_active): -84.19 to +141.95 ohm
- |Z_active|: 105.33 to 266.79 ohm

Broadside S11 range:
approximately -5.24 to -9.70 dB

Representative anchors:
- 1.1768 GHz: 132.0+j141.1 ohm
- 1.2272 GHz: 182.8+j136.5 ohm
- 1.2784 GHz: 234.1+j104.2 ohm
- 1.4000 GHz: 243.8-j37.5 ohm
- 1.5608 GHz: 125.3-j80.8 ohm
- 1.5752 GHz: 117.4-j78.5 ohm
- 1.6024 GHz: 104.1-j73.2 ohm

Maximum complex S11 difference versus clean isolated Pol-A over the science band:
0.70508

This is accepted as physical mutual-coupling evidence, not a failure.

## System implication

The array environment has already moved the antenna source impedance far away from a single nominal 100-ohm point.

Therefore:
- do not freeze LNA input matching now;
- do not force the radiator back toward isolated 100-ohm matching;
- continue scan-dependent active-impedance mapping first.

## Current R1E0C design

Plan:
`docs/R1E0C_FIRST_SCAN_QUALIFICATION_PLAN.md`

### R1E0C-A future BUILD-ONLY states

- C30P45: theta=30, phi=45
- C45P45: theta=45, phi=45
- C60P45: theta=60, phi=45
- C60P135: theta=60, phi=135

Broadside theta=0 reference is R1E0B and is not re-solved.

Canonical scan-state generator:
`scripts/generate_r1e0c_scan_state_macros.py`

Static audit:
`PASS_R1E0C_SCAN_MACRO_STATIC_AUDIT`

Build-only harness:
`scripts/run_r1e0c_scanstate_build_only_dc.py`

Runbook:
`em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E0C_SCANSTATE_BUILD_ONLY.md`

All four macros contain:
- zero boundary-type changes;
- zero geometry changes;
- zero material changes;
- zero port changes;
- zero solver commands.

## Current authorization

R1E0C-A remains DESIGN ONLY.

No build is authorized.
No scan solver is authorized.

A future build authorization must freeze fresh work/evidence paths and the exact source HEAD.

R1E0C-B scan solves require a separate later solver authorization.
