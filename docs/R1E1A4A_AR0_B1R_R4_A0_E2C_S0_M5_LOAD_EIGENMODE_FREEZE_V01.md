# R4-A0-E2C-S0 M5 Load-Sensitivity and Eigenmode Freeze V0.1

Status: FROZEN_OFFLINE_M5
Date: 2026-10-02

M5 uses only the already solved E2C S0 S-parameter data.

## M5-A — Passive E_UP load-sensitivity

Scan a frequency-independent, identical passive reflection coefficient Gamma on the opposite-polarization E_UP +/- pair.

Grid:
- magnitude |Gamma| = 0.00..1.00 in 0.05 steps;
- phase = 0..350 deg in 10 deg steps;
- Gamma=0 evaluated once.

For each load state and each polarization, analytically reterminate the existing 8-source S-subnetwork and evaluate:
1. maximum same-pol 4x4 complex deviation versus isolated E2A/E2B baseline;
2. E_UP differential-to-common degradation versus isolated baseline;
3. E_UP +/- return imbalance.

This is a constant-Gamma passive-load sensitivity study, not a claim that a real broadband component has frequency-independent Gamma.

A second per-frequency optimum is calculated only as an optimistic mathematical lower bound and is not treated as a realizable broadband termination.

## M5-B — E_UP eigen/singular modes

Transform the four E_UP ports into [A_diff, A_common, B_diff, B_common].

At L5, L2, the worst balanced cross-pol region near 1.3384 GHz, and L1:
- compute the full 4x4 modal S matrix;
- compute eigenvectors/eigenvalues;
- compute singular vectors/singular values;
- report A/B participation and differential/common participation;
- compute the 2x2 A-to-B cross-modal coupling block singular values.

Interpretation:
- A/B participation near 1/0 means nominal polarizations remain eigenlike;
- A/B participation near 0.5/0.5 means the physical eigenchannels are strongly mixed A/B combinations;
- large cross-block singular value means no choice of a single nominal A/B basis removes the coupling.

## Gate

M5 may recommend the next physical sentinel, but it cannot authorize BUILD or SOLVE.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
