# R4-A0-E2C-S0 M6 D1/D2 Diagnostic SOLVE Freeze V0.1

Status: FROZEN_READY_AWAIT_SOLVE_AUTH

This node freezes the diagnostic solve semantics only. No solver has been run.

## Common observer semantics

D1 and D2 use the exact E2A-S0L six-port observer network:

1. A_E_UP — source
2. A_P_IN — source/device-input plane
3. A_P_OUT — 50-ohm passive load only
4. B_E_UP — source
5. B_P_IN — source/device-input plane
6. B_P_OUT — 50-ohm passive load only

Ports 1,2,4,5 are the only selected sources. Ports 3,6 are never excited.

Frequency/solver fidelity is inherited from E2A-S0L: 1.0-1.8 GHz HF Frequency Domain, second-order tetrahedral adaptive mesh, MaxDeltaS 0.02, two consecutive checks, MaxPasses 16.

## Surface-current evidence

Three H-field monitors are frozen at:
- L2 1.2276 GHz
- mixed-mode diagnostic frequency 1.3384 GHz
- L1 1.57542 GHz

CST's high-frequency monitor workflow uses H-field monitor results for H-field/surface-current inspection on conducting surfaces. These field maps are supporting mechanism evidence; numerical convergence remains governed by the S-parameter hard gates.

For current-path review, compare source excitations 1 and 4 with identical display scale and inspect:
- observer radiator/feed;
- passive diagnostic entities;
- branch symmetry/antisymmetry;
- localization on signal metal versus ground/vias.

## Attribution metrics

Every variant is compared to the immutable isolated E2A baseline and normalized to the already-solved full-E2C Pol-A endpoint.

Metrics:
1. maximum complex delta of the 4x4 source-side S block;
2. E_UP differential-to-common peak degradation in dB;
3. E_UP plus/minus self-return imbalance in dB.

Effect fractions are defined against the full-E2C effect.

Variant classification:
- STRONG: at least two of three fractions >= 0.60;
- WEAK: all three fractions <= 0.30;
- INTERMEDIATE: otherwise.

Cross-variant interpretation:
- D1 STRONG / D2 WEAK -> pre-CIN signal path primary;
- D1 WEAK / D2 STRONG -> ground-return path primary;
- D1 WEAK / D2 WEAK while full E2C remains severe -> signal-ground interaction/composite mixed mode primary;
- D1 STRONG / D2 STRONG -> both classes independently strong;
- all other cases -> mixed/inconclusive and field-current review is required before geometry optimization.

## Execution order

Default future order is D1 solve first, close its grant and qualify it, then D2 under a separate SOLVE grant. There is no automatic continuation and no retry.

No geometry optimization, C1 promotion, or active-LNA integration is authorized by a diagnostic result.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
