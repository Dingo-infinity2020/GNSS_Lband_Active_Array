# R1A5M Adaptive Mesh Convergence Contract

Status: FROZEN FOR NW ADAPTIVE CONVERGENCE QUALIFICATION

## Purpose

R1A5R established that second-order tetrahedral basis restores the expected Pol-A/Pol-B symmetry, but first-order and second-order absolute S-parameter curves differ materially.

R1A5M tests absolute numerical convergence while holding the physical model and polynomial order fixed.

## Immutable source

Use the original hash-locked R1A4 CST:

D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

Required SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

## Fixed physical/solver variables

Unchanged:
- geometry
- materials
- two differential ports
- port reference = 100 ohm
- HF Frequency Domain solver family
- 1.0–1.8 GHz
- open boundaries on all six faces
- 50 mm background in all directions
- tetrahedral mesh family
- second-order basis
- curvature order 3
- General purpose method
- no far-field monitors
- no optimization
- no material A/B

## Single convergence variable

Enable CST native tetrahedral adaptive mesh refinement.

Settings are based on CST 2022.5 installed examples:

With MeshAdaption3D:
- SetType = HighFrequencyTet
- SetAdaptionStrategy = ExpertSystem
- MinPasses = 3
- MaxPasses = 6
- MaxDeltaS = 0.02
- NumberOfDeltaSChecks = 2
- SetLinearGrowthLimitation = 40

FDSolver.MeshAdaptionTet = True

## Baseline for comparison

R1A5R non-adaptive second-order result:
D:\GNSS_Lband_Active_Array\_r1a5r_second_order_work\R1A5R_SECOND_ORDER_V01.cst

R1A5R SHA256:
f2254cffe07312270d115e95f5526d5841411a865571dfc22c8a3321a98e24e0

Compact baseline:
evidence/r1a5r_dc_nw_20260924_second01/sparameters_and_zin.csv

## Required outputs

- final S11/S12/S21/S22 curves
- derived Zin1/Zin2
- GNSS anchor samples
- Pol-A/B symmetry
- reciprocity
- final mesh/log evidence
- adaptation-pass evidence if exposed by CST logs/results
- comparison to R1A5R second-order baseline

## Scientific convergence metrics

Primary native criterion:
- CST adaptive mesh configured for MaxDeltaS = 0.02;
- two consecutive Delta-S checks requested;
- at least 3 passes, no more than 6.

External final-vs-baseline criteria over the science band 1.15–1.65 GHz:
1. max complex |S11_adapt - S11_R1A5R| <= 0.05;
2. max complex |S22_adapt - S22_R1A5R| <= 0.05;
3. max final |S11_dB-S22_dB| <= 1.0 dB;
4. max complex reciprocity error |S21-S12| <= 1e-3;
5. no NaN/Inf and complete equal-length result grids.

Diagnostic-only:
- S21/S12 remain limited by the crossed discrete-edge-port model;
- isolation around/below roughly -50 dB must not be interpreted as physical polarization isolation.

## Classification

PASS_R1A5M_ABSOLUTE_MESH_CONVERGED:
- solver completes;
- provenance gates pass;
- final result gates pass;
- external final-vs-second-order baseline criteria pass;
- no adaptation failure is indicated by CST logs.

HOLD_R1A5M_ADAPTIVE_NOT_CONVERGED:
- solver completes but final-vs-baseline criteria fail materially or CST hits max passes without convergence.

HOLD_R1A5M_RUNTIME:
- solver/API/runtime failure.

## Resource boundary

NW is authorized because the current model is small and previous solves completed in tens of seconds.

If adaptive mesh expands unexpectedly or becomes a heavy production-scale solve:
- stop/classify HOLD;
- do not migrate to CST251 automatically;
- return to DESIGN for explicit host escalation.

## Stop boundary

After exactly one adaptive run:
- return to DESIGN;
- no further mesh refinement automatically;
- no material A/B automatically;
- no geometry optimization;
- no CST251 staging.
