# M6 Frequency-Shape Mechanism Discrimination V0.1

Status: **PASS_M6_FREQUENCY_SHAPE_DISCRIMINATION**

Classification: **GROUND_SEPARATE_OR_SECONDARY_MECHANISM**

This is read-only analysis of existing S-parameter evidence. No CST launch, BUILD, or SOLVE was used.

## D2 versus full-E2C frequency shape

- raw_max_delta correlation: -0.6154
- frobenius_delta correlation: -0.3277
- mode_complex_delta correlation: 0.1898
- branch_imbalance correlation: -0.4723
- D2 complex perturbation-direction median alignment to full E2C: 0.9405
- full-E2C raw peak: 1.3432 GHz
- D2 raw peak: 1.6496 GHz
- raw peak separation: 0.3064 GHz

## Interpretation

- D2 ground/via perturbation does not closely track the full-E2C differential/common-mode frequency shape.
- D2 does not reproduce the full-E2C broadband raw source-side deviation shape.
- D2 and full-E2C raw-deviation peaks are separated by more than 100 MHz, arguing against a simple scaled copy of one mechanism.

The result strengthens the existing M6 conclusion: the ground/backside/via network is an important contributor, especially to common-mode conversion, but the full severe coexistence state is not a simple scaled copy of the ground-only perturbation.

The most defensible present mechanism is therefore a composite return-path / signal-ground interaction. Pre-CIN signal metal alone remains ruled out as a strong standalone cause.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
