# R1A5M2 Adaptive Convergence Recovery Contract

Status: FROZEN FOR STATIC AUDIT / NW RECOVERY SOLVE

## Trigger

R1A5M ended with:
HOLD_R1A5M_ADAPTIVE_NOT_CONVERGED

Native CST Delta-S sequence:
- pass 2: 0.0673917
- pass 3: 0.0497934
- pass 4: 0.0274924
- pass 5: 0.0203932
- pass 6: 0.0173369

The trend is monotonic and pass 6 is below the configured 0.02 threshold, but pass 5 is slightly above. With two consecutive checks required, MaxPasses=6 was reached before native convergence could be declared.

## Scientific question

Does the identical second-order adaptive formulation formally converge if the maximum allowed pass count is extended from 6 to 8?

## Immutable source

Use the original R1A4 CST:

D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

Required SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

## Exactly one allowed configuration change

R1A5M:
MaxPasses = 6

R1A5M2:
MaxPasses = 8

Everything else remains identical:
- HF Frequency Domain
- tetrahedral second order
- curvature order 3
- General purpose method
- HighFrequencyTet
- ExpertSystem
- MinPasses 3
- MaxDeltaS 0.02
- NumberOfDeltaSChecks 2
- LinearGrowthLimitation 40
- 1.0–1.8 GHz
- open all six faces
- 50 mm background
- unchanged geometry/materials/ports
- no far-field monitors
- no optimization

## Baseline for incremental convergence

R1A5M pass-6 final compact result:
evidence/r1a5m_dc_nw_20260924_adapt01/sparameters_and_zin.csv

R1A5M CST SHA256:
67b44e77aa88709287caf194c8e89cc2535951e1fab66b7c679df9e398a62c9b

## Required native convergence evidence

Parse CST Result/output.txt.

PASS requires:
- at least two final consecutive Delta-S values <= 0.02;
- native termination is not "maximum number of passes is reached";
- no adaptation/solver error.

## External incremental convergence gate

Over 1.15–1.65 GHz compare R1A5M2 final against R1A5M pass-6 result.

Require:
- max complex delta S11 <= 0.03;
- max complex delta S22 <= 0.03;
- final max |S11_dB-S22_dB| <= 1.0 dB;
- reciprocity <= 1e-3;
- complete finite curves.

The 0.03 criterion is an incremental convergence check against the already-refined pass-6 state, not against the coarse non-adaptive baseline.

## Classification

PASS_R1A5M2_NATIVE_AND_ABSOLUTE_CONVERGED:
- native consecutive Delta-S gate passes;
- no max-pass termination;
- incremental external convergence gates pass.

HOLD_R1A5M2_NATIVE_NOT_CONVERGED:
- max passes reached again or final two Delta-S checks do not both pass.

HOLD_R1A5M2_ABSOLUTE_NOT_CONVERGED:
- native convergence occurs but final-vs-pass6 S11/S22 delta exceeds 0.03.

HOLD_R1A5M2_RUNTIME:
- runtime/API/solver failure.

## Resource boundary

NW only.
If the run expands unexpectedly into a heavy workload, stop and return to DESIGN.
No automatic CST251 migration.

## Stop boundary

Exactly one R1A5M2 recovery solve.
No automatic further pass extension.
No material A/B.
No geometry optimization.
No production solver.
