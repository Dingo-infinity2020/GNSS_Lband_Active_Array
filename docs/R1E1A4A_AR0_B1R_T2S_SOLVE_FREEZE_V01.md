# AR0-B1R-T2S Transition EM Qualification Freeze V0.1

Status: SOLVE AUTHORIZED
SimulationOps: 0.2.8

## 1. Source identity

Canonical fixture:
R1E1A4A_AR0_B1R_T2F_CANONICAL_TRANSITION_FIXTURE_V01.cst

SHA256:
f0184b638b5af6c5c752804fd5570a5e4178e52bc6bdd62e31e72c281c03de90

T2F human review:
PASS_USER_CONFIRMED_20260927

Geometry changes in T2S:
FORBIDDEN.

Port changes in T2S:
FORBIDDEN.

## 2. Solver formulation

Frequency range:
1.0 to 1.8 GHz.

Decision band:
1.15 to 1.65 GHz.

Reference GNSS frequencies:
- L5: 1.17645 GHz
- L2: 1.22760 GHz
- L1: 1.57542 GHz

Boundary:
open on all six sides.

Background spacing:
30 mm on all six sides.

Solver:
HF Frequency Domain.

Mesh:
tetrahedral, second order.

Adaptive convergence:
- MinPasses = 3
- MaxPasses = 12
- MaxDeltaS = 0.02
- NumberOfDeltaSChecks = 2
- LinearGrowthLimitation = 40

No symmetry plane.

## 3. Formal execution

Execution host:
CST251 / mowei / container cst2022.

NW is control/staging/evidence only.

Exactly one formal solver launch is authorized.
No automatic solver retry.

A tooling/result-reader recovery that does not start the solver may be authorized by the same stage only if it does not alter geometry, ports, solver formulation, or completed solver products.

## 4. Three-port interpretation

Physical ports:
- Port 1: 100-ohm balanced input
- Port 2: 50-ohm + branch output
- Port 3: 50-ohm - branch output

For Port-1 excitation define:
A = S21
B = S31

Differential output proxy:
D = (A - B)/sqrt(2)

Common-mode output proxy:
C = (A + B)/sqrt(2)

Common-mode ratio:
CMR_dB = 20 log10(|C|/|D|)

Ideal balanced conversion has:
- equal |A| and |B|;
- phase(A)-phase(B) = 180 deg;
- C -> 0.

## 5. Metrics

For every sampled frequency report:
- S11 magnitude / dB;
- S21 and S31 magnitude / phase;
- amplitude imbalance abs(20log10(|S21|/|S31|));
- phase error from 180 deg;
- CMR_dB;
- raw power closure P = |S11|^2+|S21|^2+|S31|^2;
- delivered transmission T = |S21|^2+|S31|^2;
- mismatch-normalized transmission eta = T/(1-|S11|^2), where denominator is positive;
- normalized excess loss = -10log10(eta).

Primary summaries are over 1.15–1.65 GHz and at L5/L2/L1.

## 6. Frozen diagnostic gates

Numerical qualification:
- last two adaptive Delta-S values <= 0.02.

Return loss:
- preferred: S11 <= -15 dB over decision band;
- acceptable: S11 <= -10 dB over decision band;
- strong concern: any decision-band S11 > -3 dB.

Amplitude balance:
- preferred: <=0.25 dB;
- acceptable: <=0.50 dB.

Phase balance:
- preferred: error <=5 deg from 180 deg;
- acceptable: <=10 deg.

Common-mode suppression:
- preferred: CMR <= -20 dB;
- acceptable: CMR <= -15 dB.

Mismatch-normalized transition loss:
- preferred: <=0.20 dB;
- acceptable: <=0.50 dB;
- concern: >1.0 dB.

These are diagnostics for the T1 first-cut transition, not a product-level antenna acceptance specification.

## 7. Outcome logic

PASS_T2S_BASELINE_CHARACTERIZED requires:
- one formal solver invocation completed;
- result tree contains all nine Sij terms needed for the 3-port matrix;
- numerical convergence is qualified;
- passive power behavior is physically consistent within numerical tolerance;
- metrics are extracted reproducibly.

Scientific geometry verdict is reported separately:
- PREFERRED
- ACCEPTABLE
- NEEDS_OPTIMIZATION
- STRONG_CONCERN

A NEEDS_OPTIMIZATION verdict is still a successful T2S characterization.

## 8. Stop boundary

After the one-shot solve and read-only qualification:
- close SOLVE authority;
- preserve solved artifact in place on CST251;
- push compact evidence only;
- stop before any L_bal/L_taper/W_ground sweep.
