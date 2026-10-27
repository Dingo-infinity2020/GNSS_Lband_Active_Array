# AR0-B1R-R3-D2-M1 Dual-Polarization Characterization Interpretation V0.1

Status: PARTIAL NUMERICAL QUALIFICATION; MECHANISM REVIEW REQUIRED
SimulationOps: 0.2.8

## 1. Execution status

Pol-A:
PASS_R1E1A4A_AR0_B1R_R3_D2_M1A_CHARACTERIZED

Pol-B:
HOLD_R1E1A4A_AR0_B1R_R3_D2_M1B_QUALIFICATION

Formal solver invocations:
- Pol-A: 1
- Pol-B: 1

Automatic retries:
0

No further solver launch is authorized.

## 2. Numerical qualification

Pol-A final Delta-S:
- 7.798894e-6
- 7.276578e-6
PASS.

Pol-B final Delta-S:
- 0.02920479
- 6.563163e-6

Pol-B does not satisfy the frozen requirement that the final two consecutive Delta-S values are both <= 0.02.
Therefore B remains numerically unqualified and its RF values are diagnostic, not final qualification evidence.

No retry is permitted by the one-shot authorization.

## 3. Pol-A result

Decision band 1.15..1.65 GHz:
- worst S11 = -0.2891 dB
- worst amplitude imbalance = 0.02760 dB
- worst phase error = 0.02152 deg
- worst CMR = -55.97 dB
- worst mismatch-normalized excess loss = 1.2923 dB
- power closure = 0.98343 .. 0.99300

Equivalent 100-ohm-reference Zin:
- real = 152.3 .. 5981.8 ohm
- imag = -409.9 .. +2479.3 ohm

Representative:
L5 1.1768 GHz:
157.69 + j347.67 ohm

L2 1.2272 GHz:
170.29 + j391.32 ohm

L1 1.5752 GHz:
1111.70 + j1798.08 ohm

The structure is strongly mismatched despite excellent branch symmetry.

## 4. Pol-B one-shot diagnostic result

Decision band:
- worst S11 = -0.3167 dB
- worst amplitude imbalance = 0.02134 dB
- worst phase error = 0.2652 deg
- worst CMR = -52.64 dB
- worst mismatch-normalized excess loss = 1.1726 dB
- power closure = 0.98336 .. 0.99281

Representative:
L5:
157.34 + j349.81 ohm

L2:
169.76 + j393.02 ohm

L1:
943.49 + j1643.58 ohm

These values are diagnostic only because numerical qualification did not pass.

## 5. A/B comparison

The comparison measures the full manufacturable lower-stalk asymmetry:
- complementary half-lap slot orientation;
- supported common-ground merge position;
- associated return-current path.

It is not a pure 1.05-mm bridge-height experiment.

Over 1.15..1.65 GHz:
- max abs delta S11 = 0.02761 dB
- max abs delta amplitude imbalance = 0.02230 dB
- max abs delta phase error = 0.25699 deg
- max abs delta normalized excess loss = 0.11976 dB

At L5:
- delta S11 = +0.02014 dB
- delta Zin = -0.35 + j2.14 ohm

At L2:
- delta S11 = +0.01435 dB
- delta Zin = -0.53 + j1.70 ohm

At L1:
- delta S11 = -0.02397 dB
- delta Zin = -168.21 - j154.50 ohm

The very large maximum absolute delta-Z values over the full decision band are not a good standalone asymmetry metric because the impedance transform becomes ill-conditioned when |Gamma| approaches 1.
The much smaller delta-S11 and the close L5/L2 impedances show that both polarizations share essentially the same dominant mismatch mechanism.

Pol-B's qualification HOLD prevents claiming final A/B equivalence, but the current evidence does not identify the mechanical A/B asymmetry as the primary problem.

## 6. Comparison with local diagnostic closure

Earlier corrected D1R1-B with a diagnostic common-ground closure immediately downstream of the output reference plane gave:
- worst S11 about -5.66 dB;
- Zin about 111..121 + j(94..132) ohm over the decision band;
- excellent symmetry and very low normalized excess loss.

M1 with the manufacturable remote lower-stalk merge instead gives approximately:
- worst S11 about -0.3 dB;
- very high reactive/high-resistance input over much of the band.

Therefore moving from a local return closure to the long lower-stalk return network produces a major RF change.

## 7. Physical interpretation

The current evidence is consistent with a distributed return-path / loop-inductance / resonance problem associated with the long lower-ground continuation and remote common-ground closure.

However this must not yet be treated as a final product-ground conclusion.

The passive fixture has:
- 50-ohm branch output ports at v=10 mm;
- signal conductors ending near the feed-head region;
- ground rails continuing far down the mechanical stalk before common closure;
- no actual LNA package ground network, bias decoupling, post-LNA routing or shield structure.

Thus M1 may contain a real return-path problem, a passive-fixture artifact, or both.

## 8. Recommended next stage

Do not release W_MSL / L_bal / taper-width matching sweeps.

Next proposed stage:
AR0_B1R_R3_D2_M2_RETURN_PATH_FIXTURE_MECHANISM_PROBE

Its purpose should be to separate:
1. local return closure effect;
2. long-ground continuation effect;
3. remote common-ground merge effect;
4. passive output-port / missing-active-network effect.

Only after this mechanism is understood should the physical stalk topology or impedance-matching variables be changed.

No M2 build or solve is authorized by this document.
