# R1E1A4A H0/P1 Broadside Mixed-Mode Qualification

Formal harness status: `HOLD_R1E1A4A_H0_P1_BROADSIDE_POSTPROCESS_RESULT_PATH`.
Canonical science status: `HOLD_R1E1A4A_H0_P1_GATE_R_RNF0`.

The one authorized solver invocation completed successfully. The formal harness then failed only because it expected ordinary two-port result paths (`S1,1`, etc.) whereas the periodic CST model stored the four traces as `S1(1),1(1)`, `S1(1),2(1)`, `S2(1),1(1)`, `S2(1),2(1)`.

No solver rerun was performed. The completed artifact was qualified read-only.

## Numerical qualification

PASS.

Final adaptive sequence at the accepted 1.4-GHz adaptation sample:
- pass 2: 0.0451233;
- pass 3: 0.0194908;
- pass 4: 0.010365.

CST terminated mesh adaptation by desired accuracy, not MaxPasses. Broadband sweep converged after 11 samples. All four periodic two-port S-parameter traces are present and nonempty; no solver error lines were found.

## Frozen mixed-mode Gate-R subchecks

PASS.

Over 1.15–1.65 GHz:
- max |Sdc| = -42.3768 dB;
- max |Scd| = -42.3671 dB;
- max branch magnitude imbalance = 0.14287 dB;
- max odd-mode branch phase error = 0.37636 deg;
- max numerical residual `|Zdd - 2*Zavg|` = 0.00359 ohm.

Thus the H0/P1 nominal model validates the intended differential/common-mode decomposition and supports use of the actual P1A/P1B branch impedances in the receiver shadow.

## Differential loading versus old P0

The H0 V0.1 continuous 10x10-mm ground island materially changes the broadside differential source environment:
- max |Delta Sdd| vs old P0 = 0.41099;
- max |Delta Zdd| vs old P0 = 199.97 ohm;
- RMS |Delta Zdd| = 142.42 ohm.

Representative Zdd values:
- 1.15 GHz: H0 ~182.7+j80.7 ohm vs P0 ~108.6+j136.0 ohm;
- 1.30 GHz: H0 ~175.3-j103.6 ohm vs P0 ~250.3+j81.7 ohm;
- 1.40 GHz: H0 ~99.7-j111.2 ohm vs P0 ~243.8-j37.5 ohm;
- 1.60 GHz: H0 ~42.7-j70.5 ohm vs P0 ~105.2-j73.7 ohm.

The upper-band branch source impedance becomes strongly lower-resistance / capacitive.

## Gate R R-NF0

FAIL.

Using the traceable QPL9547 G0 noise-parameter shadow and the now-qualified actual branch impedances:
- P1A NF range = 0.2480 to 0.5646 dB;
- P1B NF range = 0.2485 to 0.5684 dB;
- frozen R-NF0 limit = 0.40 dB;
- P1A exceeds 0.40 dB for 329/625 samples (52.64%), approximately 1.3872–1.6496 GHz;
- P1B exceeds 0.40 dB for 330/625 samples (52.80%), approximately 1.3864–1.6496 GHz.

R-LOSS and the integrated R-NF1 gate are not evaluated because this reference-plane model still contains no physical signal via/feed trace/package network. R-NF0 failure alone is sufficient to stop H0 V0.1.

## Interpretation

The P1 mixed-mode reference-plane concept is retained: mode conversion and branch symmetry are good.

The failed object is the H0 V0.1 local-ground geometry: a continuous 10x10-mm ground island directly on the underside of the 1-mm radiator substrate places too much grounded conductor beneath the center feed/petal region and drives the upper-band source impedance away from the QPL9547 G0 low-noise region.

Common-mode reflection |Scc| is approximately 0 dB across the band, while differential-to-common conversion remains small. This is recorded for later shield/common-mode stability work but is not itself a frozen Gate-R failure.

Solved artifact:
`D:\GNSS_Lband_Active_Array\_r1e1a4a_h0_p1_b0_solve_work\R1E1A4A_H0_P1_BROADSIDE_SOLVE_V01.cst`

SHA256:
`a95e18b66d5000b034807455c368abdf9b831e2c1395427edb33bd6de73fafab`

Artifact state: PROTECTED_IN_PLACE.

Per the frozen stop rule, no C60P45/C60P135 solve and no carrier study was started.
