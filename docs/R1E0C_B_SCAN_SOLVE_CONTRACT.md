# R1E0C-B First Scan Solve Contract

Status: DESIGN FROZEN — SOLVER NOT AUTHORIZED

## Mainline role

R1E0C-B is the first scan-dependent active-impedance solve gate for the 94-mm infinite periodic array.

R1E0C-A has already produced four qualified, immutable scan-state CST inputs. R1E0C-B must solve them without changing geometry, materials, ports, pitch, or periodic boundary metadata.

## Immutable scan-state inputs

Work root:
`D:\GNSS_Lband_Active_Array\_r1e0c_scanstate_build_only_recovery01`

- C30P45: theta=30 deg, phi=45 deg
  SHA256 `e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2`
- C45P45: theta=45 deg, phi=45 deg
  SHA256 `ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed`
- C60P45: theta=60 deg, phi=45 deg
  SHA256 `94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01`
- C60P135: theta=60 deg, phi=135 deg
  SHA256 `c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1`

Broadside reference:
`evidence/r1e0b_dc_nw_20260924_smoke01/active_s11_and_zactive.csv`

Broadside scan state:
theta=0 deg, phi=45 deg.

## Solve sequencing

Each scan state is a separate formal one-shot solve ticket.

Do not solve all four states inside one formal invocation.

Each state requires:
- immutable source hash;
- fresh work directory;
- fresh evidence directory;
- exact invocation record;
- no silent retry;
- independent PASS/HOLD classification.

Suggested order:
C30P45 -> C45P45 -> C60P45 -> C60P135.

## Numerical formulation

Reuse the numerically proven periodic broadside formulation, but omit the nonessential YZ-matrix postprocessor.

- CST 2022.5
- HF Frequency Domain
- tetrahedral second order
- curvature order 3
- General purpose method
- HighFrequencyTet adaptive mesh
- ExpertSystem
- MinPasses 3
- MaxPasses 8
- MaxDeltaS 0.02
- NumberOfDeltaSChecks 2
- LinearGrowthLimitation 40
- 1.0-1.8 GHz

The solver config must contain zero Boundary commands.

It must not change:
- theta/phi;
- unit-cell boundary type;
- pitch/cell size;
- geometry;
- material;
- port definition.

## Periodic driven result

Expected result path:
`1D Results\S-Parameters\S1(1),1(1)`

Reference impedance:
100 ohm differential.

`Z_active = 100 * (1 + S11) / (1 - S11)`

## Required outputs per state

- complex active S11 over 1.0-1.8 GHz;
- complex Z_active;
- native adaptation Delta-S sequence;
- native termination reason;
- broadband sweep convergence;
- warning/error extraction;
- anchor-frequency active impedance;
- comparison versus R1E0B broadside over 1.15-1.65 GHz.

Required movement metrics:
- max complex Delta S11 versus broadside;
- max |Delta Z_active| versus broadside;
- Re/Im/|Z_active| ranges;
- max |S11|;
- science-band anchor values.

## Numerical PASS

`PASS_R1E0C_B_<STATE>_SCAN_SOLVE` requires:
- source hash match;
- pre-solver scan metadata matches the intended state;
- geometry unchanged;
- port count = 1;
- solver completes;
- periodic S11 path exists;
- S11 and Z_active are finite;
- final two adaptive Delta-S values <= 0.02;
- CST terminates by desired accuracy;
- no max-pass termination;
- broadband sweep convergence is satisfied;
- no solver error lines.

## Physics-alert flags

These are scientific alerts, not numerical solver failures:

- |S11| >= 0.90 anywhere in 1.15-1.65 GHz;
- Re(Z_active) <= 0 anywhere in 1.15-1.65 GHz;
- |Z_active| >= 1000 ohm anywhere in 1.15-1.65 GHz;
- obvious sharp/discontinuous active-impedance behavior;
- strong 60-deg principal-plane versus orthogonal-plane divergence after both 60-deg cases are available.

Do not optimize the radiator inside R1E0C-B.

## Resource routing

R1E0B broadside solved in about 100 s on NW. R1E0C-B therefore defaults to NW one state at a time.

If any state becomes unexpectedly heavy or unstable:
- classify HOLD;
- do not automatically migrate to CST251;
- return to DESIGN for explicit routing.

## Stop boundary

R1E0C-B does not authorize:
- pitch sweep;
- material A/B;
- geometry optimization;
- LNA integration;
- CST251 production scan.

After all four scan states are qualified, summarize the scan-dependent active-impedance locus and decide whether the 94-mm architecture proceeds to R1E1/R1E2.
