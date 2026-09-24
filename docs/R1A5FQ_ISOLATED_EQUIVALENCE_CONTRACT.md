# R1A5FQ Clean-Feed Isolated Equivalence Contract

Status: DESIGN FROZEN — SOLVER NOT AUTHORIZED

## Mainline role

This is the final isolated-element equivalence gate before the project moves to:
R1E0 periodic unit-cell array physics.

It must not become an isolated-element optimization loop.

## Scientific question

Do the clean, non-crossing single-port R1A5F models preserve the converged passive self-impedance / self-reflection behavior established by R1A5M2?

## Inputs

Model A:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst

SHA256:
74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce

Model B:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLB_SINGLE_PORT_V01.cst

SHA256:
11ca4ae06baa1d3f18376789c90717f28aee2b02480d7eba88d2f5155d51a1bf

Baseline:
R1A5M2 crossed-two-port converged diagnostic result.

Compact S baseline:
evidence/r1a5m2_dc_nw_20260924_recovery01/sparameters_and_zin.csv

Comparison:
- clean Pol-A S11 vs R1A5M2 S11
- clean Pol-B S11 vs R1A5M2 S22
- clean Pol-A vs clean Pol-B after exact polarization rotation

## Solver settings

When separately authorized, reuse the numerically converged R1A5M2 formulation:

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
- 1.0–1.8 GHz
- open all six faces
- 50 mm background
- no far-field monitors

Each A/B model is solved independently.

## Required outputs

For each model:
- one-port S11 complex curve
- derived Zin using Z0=100 ohm
- native adaptation Delta-S sequence / termination
- anchor-frequency samples
- mesh/log evidence

Comparisons over 1.15–1.65 GHz:
- max complex delta clean-A S11 vs R1A5M2 S11
- max complex delta clean-B S11 vs R1A5M2 S22
- max complex delta clean-A vs clean-B
- max A/B dB difference

## PASS gate

PASS_R1A5FQ_CLEAN_FEED_EQUIVALENT if:
- both native adaptive solves converge by desired accuracy rather than max-pass termination;
- complete finite S11 curves exist;
- max complex delta A vs R1A5M2 S11 <= 0.03;
- max complex delta B vs R1A5M2 S22 <= 0.03;
- max complex delta A vs B <= 0.02;
- max A/B dB difference <= 0.5 dB.

These thresholds test representation equivalence, not antenna optimization.

## HOLD interpretation

If clean-vs-crossed self-response differs materially:
- do not optimize the radiator;
- determine whether the removed crossed-port wire caused a meaningful self-loading artifact;
- treat the clean-feed result as potentially more physically meaningful, but require explicit design review before replacing the baseline.

## Stop boundary

On PASS:
- isolated-element passive baseline is closed;
- next primary physics gate is R1E0 94-mm periodic unit-cell baseline.

No geometry optimization, material A/B, or far-field production study is allowed inside R1A5FQ.
