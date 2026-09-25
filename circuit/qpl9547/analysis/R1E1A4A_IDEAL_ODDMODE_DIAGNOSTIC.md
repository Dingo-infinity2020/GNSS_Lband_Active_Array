# R1E1A4A Ideal-Odd-Mode QPL9547 Noise Diagnostic

Status: ASSUMPTION DIAGNOSTIC ONLY — NOT GATE R

Assumption used only to estimate scale:
- ideal odd-mode virtual ground;
- each QPL9547 input sees `Z_branch = Z_diff / 2` directly at the device-lead plane;
- no intervening feed transformation or pre-LNA passive loss;
- QPL9547 Rev-D noise parameters interpolated across frequency.

This assumption has NOT been qualified by a local-ground / two-port mixed-mode EM model.

Results over 1.15–1.65 GHz:

| State | Bare branch NF range | S1 branch NF range | max |Delta NF| | max |Delta Te| |
| --- | --- | --- | --- | --- |
| B0 | 0.278–0.326 dB | 0.269–0.331 dB | 0.01447 dB | 1.03 K |
| C60P45 | 0.246–0.289 dB | 0.244–0.289 dB | 0.00205 dB | 0.146 K |
| C60P135 | 0.269–0.336 dB | 0.273–0.330 dB | 0.00787 dB | 0.564 K |

For C60P135, the largest support-induced NF change in this illustrative model is negative (slightly improved NF), despite the support failing Gate T with max |Delta Z_diff|=15.09 ohm.

Interpretation:
- the result demonstrates that a support-induced impedance movement need not map monotonically to worse LNA noise;
- it strengthens the case for a receiver-level Gate R in addition to Gate T;
- it does NOT validate S1 as a production support because common mode, real local ground, branch imbalance, feed loss, gain and stability are absent from this diagnostic.

Generated data:
- `R1E1A4A_B0_IDEAL_ODDMODE_QPL9547_NOISE_SHADOW.csv`
- `R1E1A4A_C60P45_IDEAL_ODDMODE_QPL9547_NOISE_SHADOW.csv`
- `R1E1A4A_C60P135_IDEAL_ODDMODE_QPL9547_NOISE_SHADOW.csv`
- `R1E1A4A_IDEAL_ODDMODE_QPL9547_NOISE_SHADOW_SUMMARY.json`

Next authority:
`docs/R1E1A4A_REFERENCE_PLANE_AND_COSIM_SPEC.md`.
