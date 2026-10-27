# E2C S0 M5 Load-Sensitivity and Eigenmode Analysis V0.1

Status: **PASS_M5_LOAD_SENSITIVITY_AND_EIGENMODE_ANALYSIS**

No CST launch, BUILD, or SOLVE was used.

## Passive E_UP load scan

- scanned constant passive Gamma states: 721
- passing states under all frozen thresholds: 0
- best constant-Gamma worst delta: 0.104756 at |Gamma|=1.00, phase=20.0 deg
- best constant-Gamma worst normalized score: 2.921 at |Gamma|=1.00, phase=20.0 deg
- optimistic per-frequency load lower-bound max delta across band: 0.104756

### Special states
- matched: worst delta=0.703793, worst mode degradation=23.461 dB, worst imbalance=11.374 dB
- open: worst delta=0.451125, worst mode degradation=20.103 dB, worst imbalance=3.114 dB
- short: worst delta=1.072644, worst mode degradation=27.211 dB, worst imbalance=34.365 dB

## E_UP modal/eigenmode results

- global A/B cross-modal principal coupling sigma: -2.700 dB at 1.6496 GHz
- second A/B cross-modal sigma there: -19.661 dB
- worst-region singular-mode A/B purity range: 0.503 .. 0.509

### L5 1.17680 GHz
- A/B cross-block singular values: -3.934 dB, -24.239 dB
- singular mode 1: sigma -0.008 dB; A 0.503 / B 0.497; diff 0.487 / common 0.513
- singular mode 2: sigma -0.013 dB; A 0.486 / B 0.514; diff 0.007 / common 0.993

### L2 1.22720 GHz
- A/B cross-block singular values: -3.116 dB, -23.280 dB
- singular mode 1: sigma -0.009 dB; A 0.496 / B 0.504; diff 0.497 / common 0.503
- singular mode 2: sigma -0.018 dB; A 0.493 / B 0.507; diff 0.007 / common 0.993

### WORST_REGION 1.33840 GHz
- A/B cross-block singular values: -2.702 dB, -21.733 dB
- singular mode 1: sigma -0.010 dB; A 0.494 / B 0.506; diff 0.521 / common 0.479
- singular mode 2: sigma -0.025 dB; A 0.494 / B 0.506; diff 0.007 / common 0.993

### L1 1.57520 GHz
- A/B cross-block singular values: -2.881 dB, -20.016 dB
- singular mode 1: sigma -0.017 dB; A 0.488 / B 0.512; diff 0.588 / common 0.412
- singular mode 2: sigma -0.057 dB; A 0.497 / B 0.503; diff 0.008 / common 0.992

## Evidence-based classification

- **HIGH — NO_CONSTANT_PASSIVE_EUP_LOAD_MEETS_FROZEN_SENTINEL_THRESHOLDS**: 0 scanned passive constant-Gamma states pass both polarizations
- **HIGH — A_B_MODAL_COUPLING_BLOCK_HAS_STRONG_PRINCIPAL_CHANNEL**: largest A-B modal cross-block singular value exceeds -20 dB
- **HIGH — WORST_REGION_SINGULAR_CHANNELS_ARE_STRONGLY_MIXED_AB_MODES**: at least one dominant orthogonal channel has A/B purity below 0.70

## Boundary

M5 does not authorize a geometry change. The next step is to use the M5 result to choose a minimum physical attribution sentinel, not to retune the full antenna blindly.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
