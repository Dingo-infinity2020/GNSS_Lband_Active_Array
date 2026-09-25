# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=61
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1E1-PITCH-MATERIAL-TRADE
CURRENT_TASK_ID=R1E1-A4-SUPPORT-CO-DESIGN-DIAGNOSTIC-DESIGN
TASK_OWNER=DESIGN
TASK_STATUS=HOLD_SCIENCE_GATE
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

Canonical source:
`D:\GNSS_Lband_Active_Array\_r1e1a0r1_pitch_ready_source_work\R1E1A0R1_POLA_PERIODIC_PITCH_READY_94MM_V01.cst`

SHA256:
`585929d5bf9cbf46c4a6d0ae40b42baa8e2efff673f79c1026dcff33cb014fc2`

Qualification:
- R1A3 geometry exact;
- frozen R1A5F Pol-A port exact;
- 94-mm broadside periodic metadata exact;
- pitch/span dependent expressions preserved;
- no sweep-parameter history warning;
- no solver markers/results;
- fresh reopen PASS.

The canonical source is PROTECTED_IN_PLACE.

Evidence:
`evidence/r1e1a0r1_dc_nw_20260924_build01/`

## R1E1A0-R2 closed stage

Status:
`PASS_R1E1A0R2_PITCH_PARAMETERIZATION_BUILD_ONLY`

Canonical R1E1A0 status:
`PASS_R1E1A0_PITCH_PARAMETERIZATION_MECHANISM`

Formal source commit:
`063d3b467c5b149e1a818daf0a0e585a1ea1b5c9`

Formal invocation count:
1

Runtime:
91.57 s

Solver:
NOT RUN

P088 SHA256:
`089fdcfd7a2339a3504b8fb3b9542a586265549773e7c13ac4b20ef483e37b3a`

P100 SHA256:
`8ffd74b176ad2f139770afbb5aa2201ae60e1a4f0e1fb38cf05a2254966e5a03`

Both endpoints passed pitch persistence, periodic span, non-ground geometry invariance, fresh reopen and zero protected-parameter warning.

Evidence:
`evidence/r1e1a0r2_dc_nw_20260924_build01/`

## R1E1A1 six-pitch FR4 BUILD-ONLY closeout

Task:
`R1E1-A1-SIX-PITCH-FR4-SOURCE-SET-BUILD-ONLY-NW`

Source:
`D:\GNSS_Lband_Active_Array\_r1e1a0r1_pitch_ready_source_work\R1E1A0R1_POLA_PERIODIC_PITCH_READY_94MM_V01.cst`

Source SHA256:
`585929d5bf9cbf46c4a6d0ae40b42baa8e2efff673f79c1026dcff33cb014fc2`

Harness SHA256:
`e42e05e150222fc4b04fa64edd63baa9c19cc41604a1fe93ce783b90cbca1b6b`

Audit SHA256:
`2b7fc77446d38fec4b669143d934009b3d6f22399252f947225d41ca6ea740f2`

Contract SHA256:
`192e76a2e7c9bdb370dac4206f753fe65788d22abfe12c66275c3f2ab6a68733`

Runbook SHA256:
`98470c45e3de7b2f018f3d1ccce533389f972f43d6bf1de36bbfbaecd4e86ca4`

Pitch set:
88, 90, 92, 94, 96, 100 mm.

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1e1a1_six_pitch_fr4_work`

Fresh evidence:
`evidence/r1e1a1_dc_nw_20260924_build01/`

Formal invocation count:
1

Silent retry:
NO

Canonical status:
`PASS_R1E1A1_SIX_PITCH_FR4_SOURCE_SET_BUILD_ONLY`

Qualified hashes:
- P088 `c0af9163d6d3c176b773f0e731b3ce2e1821affc307033da06b4bae3394203c1`
- P090 `27b7aac39d3ca7952509a761a59823bc3bcd6a090879f7864b8f808431d36850`
- P092 `58609d126e6f1198da1d94528e9afca15c59236ed32e9807547b68a75d60c008`
- P094 `fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e`
- P096 `0e949b8940baa92ab88534f45442ecbef71ec54a299ad6df14fc3dff10a8e8f2`
- P100 `df8f1c52dd6406a068f699420c6c94c9c6692121329db2544efe608a7d8b1efd`

Closeout evidence:
`evidence/R1E1A1_CLOSEOUT_20260925.md`

The A1 build authorization is consumed.
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO

Current next task:
`R1E1-A2-MECHANICAL-SUPPORT-EM-BASELINE-DESIGN`

The missing standoff/frame occupies the near-field volume between the radiator PCB and ground/backplane. Mechanical support must therefore be defined and later sensitivity-qualified before R1E1B.

R1E1A2 explicitly includes the complete assembly interface:
`radiator PCB -> upper joint -> support body -> lower joint -> ground/backplane`.
Adhesive/bond-line, mounting holes, screws/clips/soldered features, stand-off height, tilt, warp and registration are part of the design state.

Preferred first assembly candidate:
four symmetric minimal-section low-density foam/low-permittivity supports with small bonded interfaces and no metal hardware projecting above the ground plane.

Second candidate:
serviceable dielectric standoff + dielectric fastener assembly.

Assembly plan:
`docs/R1E1A2_ASSEMBLY_INTERFACE_PLAN.md`

User authorization received for the frozen R1E1A2 build-only matrix and R1E1A3 support-sensitivity solves.

Authorized matrix only:
- S1_BONDED_B0;
- S1_BONDED_C60P45;
- S1_BONDED_C60P135;
- S4_PEC_B0.

Build must PASS before any solve. Each solve is an independent one-shot invocation with no silent retry.
Scientific gate and material/geometry freeze: `docs/R1E1A2A3_SUPPORT_SENSITIVITY_CONTRACT.md`.

No R1E1B pitch screen, material A/B, LNA integration or CST251 execution is authorized.

## R1E1A2 support build closeout / R1E1A3 solve baton

Formal build invocation count: 1.
Original formal status: `HOLD_R1E1A2_SUPPORT_BUILD_ONLY_IN_SESSION_AUDIT_PERSISTENCE`.
Canonical read-only recovery: `PASS_R1E1A2_SUPPORT_BUILD_ONLY_READONLY_RECOVERY`.
No build rerun occurred and no solver ran during recovery.

Immutable solve sources:
- S1_BONDED_B0: `addcd7a30fabdac49227b9f8ab8f05a6832266f0e00b58d288982abec13bae95`
- S1_BONDED_C60P45: `9c66bad44df42761aa09bacca835704dbc9d0e9eea458cd5088bb674d6ce8105`
- S1_BONDED_C60P135: `05ef5bb2ff7094072bae01895b2aa066d16abbf2213ef68e42202479745af789`
- S4_PEC_B0: `3962a20eb07c3db0f920304a9f3fc90d33e6946c03c753a9f43e99f4ede3223c`

Solve order is fixed as listed above. Each solve is an independent one-shot NW invocation. Build authorization is consumed; R1E1B remains forbidden.

## R1E1A3 first solve HOLD

Consumed solve: `S1_BONDED_B0` only.
Status: `HOLD_R1E1A3_S1_BONDED_B0_NUMERICAL_MAXPASSES`.
Result SHA256: `55a55f56ad4981fb30d31624cc656f2a6f4affc5438d3879176531b633480ce3`.

Adaptive Delta-S: 0.0344858 -> 0.0434797 -> 0.0306481 -> 0.0224755 -> 0.0130842 -> 0.0202292 -> 0.021505.
Broadband sweep converged, but desired-accuracy termination did not occur and MaxPasses=8 was reached.

Provisional physical movement stayed inside the frozen benign limits: max |Delta S11|=0.01111983 and max |Delta Z_active|=4.27463 ohm. This is not a PASS claim because numerical qualification failed.

Remaining three support solves were not started. Recovery design is `docs/R1E1A3R1_NUMERICAL_RECOVERY_PLAN.md`; no recovery solve is authorized.

## R1E1A3-R1 recovery authorization

User authorized solver continuation after the broadside numerical HOLD.
Scope is frozen as: first rerun only `S1_BONDED_B0` with `MaxPasses=12`; all other numerical/physical settings unchanged. If and only if this recovery PASSes, continue `S1_BONDED_C60P45`, `S1_BONDED_C60P135`, and `S4_PEC_B0` as independent one-shot solves under the same config. Any HOLD stops the sequence.

Recovery harness snapshots and restores immutable R1E1A2 build-evidence files to neutralize CST history replay of absolute audit paths.
No R1E1B, material A/B, LNA integration, or CST251 execution is authorized.

## R1E1A3-R1 broadside recovery PASS

`S1_BONDED_B0` recovery completed with strict numerical PASS and benign-gate PASS.
Adaptive final two Delta-S values: 0.0164063, 0.0144292; desired-accuracy termination; broadband convergence PASS.
Max support-vs-bare |Delta S11| = 0.02950756; max |Delta Z_active| = 5.58606 ohm.
Solved SHA256: `9ca14907abb5a839c399452ef88a7f949dd3df4476992918d1bba5b7c33b71a9`.

Conditional authorization now opens the remaining sequence:
`S1_BONDED_C60P45 -> S1_BONDED_C60P135 -> S4_PEC_B0`, each one-shot under the identical MaxPasses=12 recovery config. Any HOLD stops the sequence.

## R1E1A3-R1 S1 C60P45 PASS

`S1_BONDED_C60P45` completed with strict numerical PASS and benign-gate PASS.
Adaptive Delta-S final pair: 0.0116278, 0.00987295; desired-accuracy termination; broadband convergence PASS.
Support-vs-bare max |Delta S11| = 0.00697213; max |Delta Z_active| = 0.982821 ohm.
Solved SHA256: `9e26e2ef4222a91aeeda983bd8f96c5ebe78aaf49e6a9ad6c6e7747ca4d74c49`.
Next authorized one-shot state: `S1_BONDED_C60P135`.

## R1E1A3 support gate final closeout

S1 bonded support qualification:
- B0: numerical PASS, benign PASS; max |Delta S11|=0.02950756, max |Delta Z|=5.58606 ohm;
- C60P45: numerical PASS, benign PASS; max |Delta S11|=0.00697213, max |Delta Z|=0.982821 ohm;
- C60P135: numerical PASS, benign FAIL; max |Delta S11|=0.02868632, max |Delta Z|=15.09084 ohm.

C60P135 exceeds the frozen 10-ohm Delta-Z gate over 297/625 science-band samples from about 1.4128 to 1.6496 GHz. Peak occurs at 1.5520 GHz with Delta Z approximately -5.03-j14.23 ohm.

Canonical stage status: `HOLD_R1E1A3_SUPPORT_SCIENCE_GATE_S1_C60P135_DELTA_Z`.
S4_PEC_B0 was not started after the HOLD. R1E1B remains blocked.
Next task is DESIGN ONLY: `docs/R1E1A4_SUPPORT_CO_DESIGN_DIAGNOSTIC_PLAN.md`.
