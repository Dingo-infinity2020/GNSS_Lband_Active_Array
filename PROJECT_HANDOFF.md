# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=88
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1E1A4-SUPPORT-RECEIVER-CODESIGN
CURRENT_TASK_ID=R1E1-A4A-H3B-T01A-O0-REFERENCE-LINE-AWAIT-AUTH
TASK_OWNER=DESIGN_CONTROL
TASK_STATUS=MASTERPLAN_FROZEN_AWAIT_O0_AUTH
SIMULATIONOPS_PROTOCOL=0.2.6
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
R1E0 scan qualification -> R1E1A support/mechanical gate -> R1E1A4A receiver-shadow + interface freeze -> targeted support/hub co-design -> support/hub-inclusive pitch/material trade -> R1E2 authoritative active-impedance atlas -> active-front-end co-design.

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

## Original R1E0C-A formal invocation

Status:
`HOLD_R1E0C_A_HARNESS_MACRO_PATH_FORMAT`

Source commit:
`746b34d35e6ae4ee948a6fc510bc6c072584e654`

Invocation count:
1

Exit code:
1

Runtime:
24.23 s

Failure class:
pre-build harness path-format bug; no scan metadata applied and no solver run.

Original failed work/evidence are preserved and are not reused.

## R1E0C-A-R1 recovery invocation

Status:
`HOLD_R1E0C_A_RECOVERY_NO_SOLVER_PREDICATE`

Source commit:
`cde5f8827d82473750c1a6e92510ac617d3835ab`

Invocation count:
1

Exit code:
0

Runtime:
197.31 s

All four scan-state CSTs were generated, fresh-reopened, and passed geometry/boundary/scan metadata checks.

Formal artifact hashes:
- C30P45: `e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2`
- C45P45: `ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed`
- C60P45: `94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01`
- C60P135: `c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1`

HOLD classification:
`NO_SOLVER_PREDICATE_FILE_EXISTENCE_MISMATCH`

CST created `Result\output.txt` as a message log containing parameter-history warnings. Read-only inspection found no solver execution markers and zero S-Parameter/Adaptive-Meshing/Power-Excitation result-tree items.

## R1E0C-A canonical closeout

Read-only qualification:
`PASS_R1E0C_SCANSTATE_BUILD_ONLY_READONLY_QUALIFICATION`

Canonical stage conclusion:
`PASS_R1E0C_SCANSTATE_BUILD_ONLY`

Qualified artifact root:
`D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_recovery01`

Immutable scan-state hashes:
- C30P45: `e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2`
- C45P45: `ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed`
- C60P45: `94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01`
- C60P135: `c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1`

All four artifacts are PROTECTED_IN_PLACE and are the only authorized R1E0C-B scan inputs.

Parameter-history warnings are preserved in evidence. They are accepted because project parameters and fresh-reopen Boundary scan metadata agree exactly, and no solver-generated results exist in the build artifacts.

## Current R1E0C-B design

Contract:
`docs/R1E0C_B_SCAN_SOLVE_CONTRACT.md`

Solver config:
`source/cst/R1E0C_B_SCAN_SOLVER_CONFIG_V01.mcr`

Static audit:
`PASS_R1E0C_B_SCAN_SOLVER_STATIC_AUDIT`

Harness:
`scripts/run_r1e0c_scan_solve_dc.py`

Runbook:
`em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E0C_B_SCAN_SOLVE.md`

Critical solver-config invariants:
- Boundary commands = 0;
- geometry/material/port changes = 0;
- YZ-matrix postprocessor = 0;
- solver-start commands inside config = 0.

Each scan state must be a separate formal one-shot solve with fresh work/evidence.

Suggested order:
C30P45 -> C45P45 -> C60P45 -> C60P135.

## R1E0C-B C30P45 closed stage

Status:
`PASS_R1E0C_B_C30P45_SCAN_SOLVE`

Formal source commit:
`046ccc660e70f4ab4c9ddfd6026111c6a140ad24`

Formal invocation count:
1

Runtime:
112.60 s

Solved artifact:
`D:\GNSS_Lband_Active_Array\_r1e0c_b_c30p45_scan_solve_work\R1E0C_B_C30P45_SCAN_SMOKE_V01.cst`

Solved artifact SHA256:
`068665b01c0cdea5338662a43fd70f1675e623ef205dbf0b910f45b40526823c`

Native convergence:
0.0534035 -> 0.0428105 -> 0.0459950 -> 0.0447652 -> 0.0130888 -> 0.0198328

Termination:
desired accuracy limit reached

Broadband sweep:
PASS after 8 frequency samples

Physics alerts:
NONE

Science-band active-impedance range:
- Re(Z_active): 93.21 to 191.35 ohm
- Im(Z_active): -30.20 to +103.55 ohm
- max |Z_active|: 195.49 ohm

Movement versus broadside:
- max complex Delta S11 = 0.22935
- max |Delta Z_active| = 73.84 ohm

The solved C30P45 artifact is PROTECTED_IN_PLACE.

## R1E0C-B C45P45 closed stage

Status:
`PASS_R1E0C_B_C45P45_SCAN_SOLVE`

Formal source commit:
`8b45ac4aad13d61cf8cb9494fb232f0eca22db41`

Formal invocation count:
1

Runtime:
114.18 s

Solved artifact:
`D:\GNSS_Lband_Active_Array\_r1e0c_b_c45p45_scan_solve_work\R1E0C_B_C45P45_SCAN_SMOKE_V01.cst`

Solved artifact SHA256:
`c36861d616af18d06ad3dddba11ef50112646bc77181aeb54e7a23a1052eb7f1`

Native convergence:
0.0451306 -> 0.0302095 -> 0.0382559 -> 0.0277872 -> 0.0182843 -> 0.0148265

Termination:
desired accuracy limit reached

Broadband sweep:
PASS after 8 frequency samples

Physics alerts:
NONE

Science-band active-impedance range:
- Re(Z_active): 100.78 to 123.59 ohm
- Im(Z_active): +29.23 to +58.09 ohm
- max |Z_active|: 129.84 ohm

Movement versus broadside:
- max complex Delta S11 = 0.49334
- max |Delta Z_active| = 143.69 ohm

The solved C45P45 artifact is PROTECTED_IN_PLACE.

## R1E0C-B C60P45 closed stage

Status:
`PASS_R1E0C_B_C60P45_SCAN_SOLVE`

Formal source commit:
`4df0ac815b4b0c4134634a3e540ff3c48f2061e0`

Formal invocation count:
1

Runtime:
76.68 s

Solved artifact:
`D:\GNSS_Lband_Active_Array\_r1e0c_b_c60p45_scan_solve_work\R1E0C_B_C60P45_SCAN_SMOKE_V01.cst`

Solved artifact SHA256:
`58018c0ffa058c46a16fdca92948a6477ff77124960b027f0a2d071b4f368828`

Native convergence:
0.0500864 -> 0.0284443 -> 0.0175831 -> 0.0157380

Termination:
desired accuracy limit reached

Broadband sweep:
PASS after 8 frequency samples

Physics alerts:
NONE

Science-band active-impedance range:
- Re(Z_active): 55.42 to 77.84 ohm
- Im(Z_active): -13.42 to +103.03 ohm
- max |Z_active|: 129.13 ohm

Movement versus broadside:
- max complex Delta S11 = 0.82410
- max |Delta Z_active| = 209.36 ohm

The solved C60P45 artifact is PROTECTED_IN_PLACE.

## R1E0C-B C60P135 closed stage

Status:
`PASS_R1E0C_B_C60P135_SCAN_SOLVE`

Formal source commit:
`b7768b99848da9053a52ac1b1a7cefe2fe782c59`

Formal invocation count:
1

Runtime:
115.29 s

Solved artifact:
`D:\GNSS_Lband_Active_Array\_r1e0c_b_c60p135_scan_solve_work\R1E0C_B_C60P135_SCAN_SMOKE_V01.cst`

Solved artifact SHA256:
`8107aff4f656c5013e9d6cf422f7d258ee4e045affa0311b7273c2889918d16c`

Native convergence:
0.0678618 -> 0.0451358 -> 0.0260878 -> 0.0274831 -> 0.0165357 -> 0.0145798

Termination:
desired accuracy limit reached

Broadband sweep:
PASS after 9 frequency samples

Frozen severe-mismatch alerts:
NONE

Science-band active-impedance range:
- Re(Z_active): 73.43 to 263.32 ohm
- Im(Z_active): -63.82 to +137.07 ohm
- max |Z_active|: 266.40 ohm

The solved C60P135 artifact is PROTECTED_IN_PLACE.

## R1E0C canonical closeout

Status:
`PASS_R1E0C_SCAN_QUALIFICATION`

Qualified periodic states:
- broadside reference;
- C30P45;
- C45P45;
- C60P45;
- C60P135.

Principal-plane core scan through 60 deg:
`PASS_NO_FROZEN_SEVERE_ALERT`

Orthogonal 60-deg sentinel:
`PASS_NO_FROZEN_SEVERE_ALERT`

Read-only 60-deg plane comparison:
- max complex Delta S11 = 0.67023;
- RMS complex Delta S11 = 0.64286;
- max |Delta Z_active| = 208.98 ohm;
- RMS |Delta Z_active| = 173.71 ohm.

No plane-divergence PASS/FAIL threshold was frozen before results, so no post-hoc threshold is applied.

Scientific conclusion:
the 94-mm baseline is numerically viable through the required 0-60 deg scan gate, but its active source impedance is strongly dependent on scan angle and scan plane.

System consequence:
final LNA input matching remains blocked.

Closeout evidence:
`evidence/r1e0c_closeout_20260924/`

## R1E1A0 endpoint-proof formal HOLD

Status:
`HOLD_R1E1A0_SOURCE_HISTORY_PARAMETER_DECLARATION`

Formal source commit:
`750a036761c3b10a37830c95415b96c1436f3d29`

Formal invocation count:
1

Runtime:
99.32 s

Solver:
NOT RUN

Endpoint artifacts:
- P088: `65b649a28e148c8c373f06357caff36a8a4a65b06b898bf8abb96c196a3c688a`;
- P100: `3746c521ffc628eddd257f96323980ac60b5183a36f536dc77876d99b1e5f779`.

All geometry / periodic metadata / pitch persistence checks passed for both endpoints.

Sole failed predicate:
`no_pitch_history_warning`.

Root cause:
the historical R1A3 lineage still contains `StoreParameter "unit_cell_pitch_nominal", 94.0` in model history, so parametric rebuild correctly preserves the user-updated pitch but emits CST's protected-parameter warning.

Classification:
source-history/tooling HOLD; not a geometry or physics failure.

Evidence:
`evidence/r1e1a0_dc_nw_20260924_build01/`

## R1E1A0-R1 closed stage

Status:
`PASS_R1E1A0R1_PITCH_READY_CANONICAL_SOURCE_BUILD_ONLY`

Formal source commit:
`0241a840819847b1b8e9332d4436eb17e58e3307`

Formal invocation count:
1

Runtime:
42.93 s

Solver:
NOT RUN

## H3B-to-active-array masterplan integration

Master plan:
docs/R1E1A4A_H3B_TO_ACTIVE_ARRAY_MASTERPLAN_V01.md

Key correction:
- close T01-A locally before H3B-I01;
- after H3B-I01, return to support/hub-inclusive R1E1B pitch/material trade and R1E2 active-impedance atlas;
- H3C-LNA0 device qualification may proceed in parallel when separately authorized;
- H3C-C01 final antenna/LNA co-design is blocked until R1E2 exists;
- T01-C remains deferred.

Immediate next node:
H3B_T01A_O0_REFERENCE_LINE_FREEZE.

No BUILD/SOLVE permission is open.

## H3B-to-active-array masterplan integration

Master plan:
docs/R1E1A4A_H3B_TO_ACTIVE_ARRAY_MASTERPLAN_V01.md

Key correction:
- close T01-A locally before H3B-I01;
- after H3B-I01, return to support/hub-inclusive R1E1B pitch/material trade and R1E2 active-impedance atlas;
- H3C-LNA0 device qualification may proceed in parallel when separately authorized;
- H3C-C01 final antenna/LNA co-design is blocked until R1E2 exists;
- T01-C remains deferred.

Immediate next node:
H3B_T01A_O0_REFERENCE_LINE_FREEZE.

No BUILD/SOLVE permission is open.
