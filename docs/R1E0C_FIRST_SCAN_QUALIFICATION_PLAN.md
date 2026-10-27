# R1E0C First Scan Qualification Plan

Status: DESIGN BASELINE — NO BUILD OR SOLVER AUTHORIZATION

## Mainline role

R1E0C is the first scan-dependent active-impedance gate.

Prerequisites:
- R1A5F clean feed PASS
- R1A5FQ isolated equivalence PASS
- R1E0A periodic configuration PASS
- R1E0B broadside periodic smoke PASS

The objective is not to optimize S11.

The objective is to observe how the 94-mm infinite-array active impedance moves with scan angle and scan plane, and to identify any severe scan anomaly before pitch/material/LNA co-design.

## Canonical source

Use the clean qualified periodic-config source, not the solved R1E0B result-bearing copy:

D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

Reason:
- unit-cell boundary metadata already qualified;
- no pre-existing solve result;
- one clean Pol-A differential port;
- geometry provenance is clean.

## Scan basis

Pol-A feed axis:
+45 deg / NE-SW.

Primary scan plane:
phi = 45 deg.

Core scan states:
- theta = 30 deg, phi = 45 deg
- theta = 45 deg, phi = 45 deg
- theta = 60 deg, phi = 45 deg

Orthogonal-plane sentinel:
- theta = 60 deg, phi = 135 deg

Broadside reference:
R1E0B theta=0, phi=45.

No additional broadside solve is needed in R1E0C.

## R1E0C-A — scan-state BUILD-ONLY

Purpose:
create four immutable periodic CST variants with only scan-angle metadata changed.

For each variant:
- source is byte-identical R1E0A copy before angle change;
- X/Y boundaries remain unit cell;
- Z boundaries remain expanded open;
- UnitCellDs1/2 remain 94 mm;
- UnitCellAngle remains 90 deg;
- port count remains 1;
- geometry remains unchanged;
- only theta/phi metadata change;
- direction remains outward;
- no solver.

Suggested IDs:
- C30P45
- C45P45
- C60P45
- C60P135

Each build must fresh-reopen and verify the intended scan angle.

R1E0C-A may create all four variants in one build-only task only if:
- every variant gets its own CST hash;
- every variant gets separate runtime audit evidence;
- any one failure causes the build task to HOLD;
- no solver starts.

## R1E0C-B — scan solves

Separate later authorization.

Each scan state should be treated as its own one-shot solve case with:
- immutable scan-state CST source hash;
- fresh run directory;
- separate evidence directory;
- no silent retry.

Do not hide partial failures inside a batch aggregate.

The same periodic one-port driven result path is expected:

1D Results\S-Parameters\S1(1),1(1)

## Numerical formulation

Reuse the proven R1E0B numerical formulation, but omit the nonessential YZ-matrix postprocessor that generated a one-port periodic warning.

Required:
- HF Frequency Domain
- tetrahedral second order
- curvature order 3
- General purpose
- HighFrequencyTet / ExpertSystem
- MinPasses 3
- MaxPasses 8
- MaxDeltaS 0.02
- two consecutive Delta-S checks
- LinearGrowthLimitation 40
- 1.0–1.8 GHz

The solver config must contain zero Boundary commands.

## Required outputs per scan state

- complex active S11
- Z_active
- native adaptation Delta-S sequence
- solver termination reason
- broadband sweep convergence
- warning/error extraction
- comparison versus R1E0B broadside active S11/Z_active

Derived movement metrics:
- max |Delta Gamma_active| versus broadside over 1.15–1.65 GHz
- max |Delta Z_active| versus broadside
- Re/Im/|Z_active| ranges
- anchor-frequency Z_active values

## Numerical PASS

Each scan state passes numerically if:
- periodic metadata matches the intended theta/phi;
- S11 is complete and finite;
- Z_active is finite;
- final two Delta-S values <=0.02;
- desired-accuracy termination occurs;
- no max-pass termination;
- broadband sweep converges;
- no solver error lines.

## Physics-alert flags

The following are reported as PHYSICS_ALERT, not silently converted to numerical failure:

- |S11| >= 0.90 anywhere in 1.15–1.65 GHz
- Re(Z_active) <= 0 anywhere in 1.15–1.65 GHz
- |Z_active| >= 1000 ohm
- a sharp discontinuity/singularity relative to neighboring frequency points
- strong principal-plane vs orthogonal-plane divergence at 60 deg

These indicate possible scan blindness, severe active mismatch, or strong mutual-coupling behavior and should drive R1E1 decisions.

Do not optimize the radiator inside R1E0C.

## Grating-lobe context

94 mm is near the intended core-scan limit at the upper end of L-band.

The 1.0–1.8 GHz numerical sweep is retained for continuity, but the formal required science band is 1.15–1.65 GHz.

Any high-frequency behavior above 1.65 GHz is diagnostic and must not be confused with failure of the required band.

## Stop boundary

R1E0C does not:
- vary pitch;
- compare materials;
- integrate LNA;
- optimize geometry.

After R1E0C:
- summarize the scan-dependent active-impedance locus;
- proceed to R1E1 pitch/material trade if no architecture-level HOLD is found;
- begin parallel LNA circuit-model research if desired, but do not freeze the LNA input match until R1E2.
