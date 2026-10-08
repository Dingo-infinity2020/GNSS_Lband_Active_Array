# R1E1A4A-H1A Broadside Mixed-Mode Solve Qualification

Canonical status: `HOLD_R1E1A4A_H1A_BROADSIDE_NUMERICAL_MAXPASSES`.

The one authorized H1A broadside solve was consumed. No retry was performed.

## Numerical gate

FAIL.

Adaptive Delta-S sequence:
`0.102059 -> 0.0449968 -> 0.0426612 -> 0.0414162 -> 0.0500126 -> 0.0495401 -> 0.0477349 -> 0.0433231 -> 0.0356251 -> 0.0288383 -> 0.0213176`.

CST terminated because MaxPasses=12 was reached. The frozen criterion requires the final two Delta-S values <=0.02 and desired-accuracy termination. Broadband sweep itself converged after 6 samples and no solver errors were recorded.

## Provisional mixed-mode trend — NOT A PASS CLAIM

The unqualified result is nevertheless retained for diagnostic scale only:
- max |Sdc| = -68.323 dB;
- max |Scd| = -68.372 dB;
- max branch magnitude imbalance = 0.01083 dB;
- max branch phase error = 0.1623 deg;
- mixed-mode symmetry predicates would pass if the numerical gate were qualified.

Versus old P0 over 1.15–1.65 GHz:
- max |Delta Sdd| = 0.39554;
- max |Delta Zdd| = 68.98 ohm;
- RMS |Delta Zdd| = 51.34 ohm.

Compared with H0 V0.1, the 2-mm offset ground produces a very large source-environment change, confirming that ground separation is a first-order design variable.

## Provisional QPL9547 receiver-shadow trend — NOT A PASS/FAIL CLAIM

If the unqualified H1A S-matrix is projected through the frozen QPL9547 noise model:
- P1A max NF = 0.42107 dB at 1.1504 GHz;
- P1B max NF = 0.42080 dB at 1.1504 GHz;
- only 30/625 samples per branch exceed 0.40 dB (4.8%);
- provisional exceedance range is about 1.1504–1.1736 GHz;
- upper-band NF falls far below the H0 V0.1 case, reaching about 0.183 dB near 1.65 GHz.

Because the numerical gate failed, these values are diagnostics only and do not establish Gate-R status.

## Artifact

Solved CST:
`D:\GNSS_Lband_Active_Array\_r1e1a4a_h1a_b0_solve_work\R1E1A4A_H1A_BROADSIDE_SOLVE_V01.cst`

SHA256:
`5960efbfe85a1f27ae29be987dc397a57c52d75129f9134a49372d898b64e930`

Artifact state: PROTECTED_IN_PLACE.

Historical build evidence touched by CST history replay was restored and verified by the harness.
