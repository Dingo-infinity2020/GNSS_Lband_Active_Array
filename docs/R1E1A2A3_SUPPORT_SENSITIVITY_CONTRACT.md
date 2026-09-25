# R1E1A2/A3 Mechanical Support Build + Sensitivity Contract

Status: SCIENTIFIC FREEZE — BUILD AND SOLVE AUTHORIZED BY USER, EXECUTION PENDING

## Frozen source

Bare P094 source:
`D:\GNSS_Lband_Active_Array\_r1e1a1_six_pitch_fr4_work\R1E1A1_P094_PITCH_BUILD_ONLY_V01.cst`

SHA256:
`fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e`

Frequency range: 1.0–1.8 GHz solver, science gate 1.15–1.65 GHz.
Port / periodic setup / radiator geometry / pitch remain unchanged.

## Frozen S1 bonded-support geometry

Four identical supports at `(x,y)=(±30,±30) mm`.

- support post: 4 x 4 mm;
- bottom bond pad: 5 x 5 x 0.10 mm;
- top bond pad: 5 x 5 x 0.10 mm;
- foam body: z=0.10 mm to `height_ground-0.10 mm`;
- no PCB holes;
- no metal above the ground plane.

ROHACELL 31 HF baseline: epsilon_r=1.05, tan_delta=0.0002.
The loss tangent is a conservative use of Evonik's `<0.0002` representative value at 2.5 GHz; use at L band is an explicit project extrapolation.

Adhesive surrogate: epsilon_r=4.0, tan_delta=0.03, provenance `ASSUMPTION_CONSERVATIVE`, not a product claim.

## Frozen S4 metal sentinel

Four grounded PEC posts with the same 4 x 4 mm lateral envelope at `(±30,±30) mm`, z=0 to `height_ground`.

Purpose: high-risk conductive reference only. It is not a preferred assembly candidate.

## Build matrix

- S1_BONDED_B0: theta=0, phi=45 deg;
- S1_BONDED_C60P45: theta=60, phi=45 deg;
- S1_BONDED_C60P135: theta=60, phi=135 deg;
- S4_PEC_B0: theta=0, phi=45 deg.

R1E1A2 build must fresh-reopen all four, preserve one port / 94-mm unit cell, verify support shape counts, and contain zero solver results.

## Solve matrix and numerical contract

Exactly four independent one-shot NW solves, in the build-matrix order. No silent retry.

Reuse frozen R1E0C solver formulation:
- HF Frequency Domain;
- second-order tetrahedral;
- HighFrequencyTet / ExpertSystem;
- MinPasses 3, MaxPasses 8;
- MaxDeltaS 0.02 with two checks;
- broadband 1.0–1.8 GHz.

Each solve must use a fresh work/evidence directory and the exact build-source hash.

Numerical PASS requires periodic S11, finite results, final two Delta-S <=0.02, desired-accuracy termination, broadband convergence, and no solver error lines.

## Pre-frozen scientific gate

S1 is `EM_BENIGN` only if ALL three S1 scan states satisfy across 1.15–1.65 GHz:

- numerical PASS;
- max complex `|Delta S11| <= 0.05` versus the matching bare S0 state;
- max `|Delta Z_active| <= 10 ohm` versus the matching bare S0 state;
- no new severe alert: |S11|>=0.90, Re(Z_active)<=0, or |Z_active|>=1000 ohm.

These are project-owned engineering thresholds frozen before support results are viewed. They are intentionally much smaller than the previously observed ~209-ohm 60-deg scan-plane separation.

S4 is a diagnostic sentinel; it is classified by the same metrics but does not need to pass the S1 benign gate.

If S1 fails any state, close `HOLD_R1E1A3_SUPPORT_SCIENCE_GATE` and do not start R1E1B.
If S1 passes all three, it may be frozen as the passive support baseline before propagation to all pitch candidates.
