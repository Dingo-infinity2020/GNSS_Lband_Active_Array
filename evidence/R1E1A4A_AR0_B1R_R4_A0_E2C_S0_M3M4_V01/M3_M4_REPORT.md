# E2C S0 M3/M4 Offline Mechanism Classification V0.1

Status: **PASS_M3M4_OFFLINE_MECHANISM_CLASSIFICATION**

No CST launch, BUILD, or SOLVE was used.

## A/B balanced modal coupling at E_UP

- A_diff_to_B_diff: -9.858 dB at 1.3384 GHz
- A_diff_to_B_common: -8.936 dB at 1.3464 GHz
- A_common_to_B_diff: -8.926 dB at 1.3448 GHz
- A_common_to_B_common: -5.971 dB at 1.6496 GHz
- B_diff_to_A_diff: -9.858 dB at 1.3384 GHz
- B_diff_to_A_common: -8.926 dB at 1.3448 GHz
- B_common_to_A_diff: -8.936 dB at 1.3464 GHz
- B_common_to_A_common: -5.971 dB at 1.6496 GHz

## Analytical opposite-polarization retermination

### PolA
- matched: max delta=0.703793; E diff->common peak=-8.915 dB; E_UP imbalance=11.374 dB
- opp_EUP_open: max delta=0.451125; E diff->common peak=-11.986 dB; E_UP imbalance=3.114 dB
- opp_PIN_open: max delta=0.703678; E diff->common peak=-8.915 dB; E_UP imbalance=11.368 dB
- opp_all_open: max delta=0.448124; E diff->common peak=-12.040 dB; E_UP imbalance=3.077 dB

### PolB
- matched: max delta=0.700675; E diff->common peak=-8.972 dB; E_UP imbalance=11.237 dB
- opp_EUP_open: max delta=0.436643; E diff->common peak=-12.330 dB; E_UP imbalance=2.844 dB
- opp_PIN_open: max delta=0.700577; E diff->common peak=-8.972 dB; E_UP imbalance=11.232 dB
- opp_all_open: max delta=0.433690; E diff->common peak=-12.385 dB; E_UP imbalance=2.810 dB

## Band decomposition

### LOW 1.15-1.25 GHz
- PolA: max raw delta=0.674446; E diff->common peak=-9.348 dB
- PolB: max raw delta=0.673313; E diff->common peak=-9.376 dB

### MID 1.28-1.4 GHz
- PolA: max raw delta=0.703793; E diff->common peak=-8.915 dB
- PolB: max raw delta=0.700675; E diff->common peak=-8.972 dB

### HIGH 1.5-1.65 GHz
- PolA: max raw delta=0.681263; E diff->common peak=-9.134 dB
- PolB: max raw delta=0.678174; E diff->common peak=-9.203 dB

## Evidence-based classification

- **HIGH — ANALYSIS_SEMANTICS_NOT_PRIMARY**: M1 semantic integrity PASS
- **HIGH — OPPOSITE_POL_EUP_50OHM_TERMINATION_NOT_SUFFICIENT_TO_EXPLAIN_HOLD**: open retermination leaves >50% of matched delta
- **HIGH — TRUE_BALANCED_CROSSPOL_COUPLING_IS_STRONG**: A/B differential-to-differential E_UP coupling exceeds -20 dB
- **HIGH — NARROW_RESONANCE_NOT_PRIMARY**: previous 50 MHz resonance gate remained below 10 dB

## Decision boundary

Do not BUILD yet. A geometry change is justified only if the residual after physically relevant retermination still points to a named geometric/ground mechanism.
The next offline task, if needed, is to convert the retermination result into a concrete physical circuit interpretation and define the minimum future sentinel that separates loading from geometry.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
