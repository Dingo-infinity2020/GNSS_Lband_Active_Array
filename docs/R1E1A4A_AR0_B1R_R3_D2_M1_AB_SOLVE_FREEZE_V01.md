# AR0-B1R-R3-D2-M1 Dual-Polarization Fixture / A-B Solve Freeze V0.1

Status: POL-B BUILD AUTHORIZED; CONDITIONAL A/B SOLVES AUTHORIZED
SimulationOps: 0.2.8

## 1. Purpose

Quantify whether the mechanically required ~1.05-mm difference in common-ground merge height between Pol-A and Pol-B produces a material RF difference.

No matching optimization is released in M1.

## 2. Parent authority

Canonical D2-M0R1:
SHA256
4ec39ab9965dd9ec6b416d801ded0ee6e56d910d2ffc2ba405cb9dec978cd91e

Existing Pol-A fixture:
SHA256
33294aa6200264135582ec0c0742a1b4e6ca7b2148e1adece2f64388d81d3dd6

Pol-A merge:
v = 33.80..34.30 mm

Pol-B merge:
v = 34.85..35.35 mm

Merge-height offset:
1.05 mm.

## 3. Pol-B fixture

Create a fresh-copy Pol-B diagnostic fixture from the canonical D2-M0R1 artifact.

Keep exactly:
- B0_Stalk:B_P_PRONG
- B0_Stalk:B_N_PRONG
- B0_MSL:B_P_MSL
- B0_MSL:B_N_MSL
- B1RT1R1_BackGround:B_P_GROUND_TAPER
- B1RT1R1_BackGround:B_N_GROUND_TAPER
- B1M_LowerStalk:B_LOWER_BODY
- D2M0R1_BackGround:B_P_LOWER_RAIL
- D2M0R1_BackGround:B_N_LOWER_RAIL
- D2M0R1_BackGround:B_COMMON_BRIDGE

Port geometry uses the Pol-B local frame:
u = (-1/sqrt(2), +1/sqrt(2))
n = (-1/sqrt(2), -1/sqrt(2))

Thus:
x = -(u+n)/sqrt(2)
y = +(u-n)/sqrt(2)

Ports:
- P1 = 100 ohm differential between + and - signal conductors at v=0;
- P2 = 50 ohm + signal-to-ground at v=10 mm;
- P3 = 50 ohm - signal-to-ground at v=10 mm.

Conductor-interface local n values remain:
- top signal n=+0.035 mm;
- output signal n=0;
- output ground n=-1.0 mm.

## 4. Pol-B build acceptance

- exact canonical parent SHA;
- exactly 10 retained solids;
- exact retained-name set;
- exact retained material/volume signature from canonical;
- exactly 3 ports;
- port endpoints match the frozen Pol-B coordinate transform;
- fresh reopen hash stable;
- result tree empty;
- zero solver invocations.

If any build gate fails, stop and do not solve.

## 5. Conditional A/B solve authority

If Pol-B fixture build PASSes, the user's authorization permits:

- exactly one formal NW solve of existing Pol-A fixture;
- exactly one formal NW solve of new Pol-B fixture;
- same solver macro and numerical settings for both;
- no retry;
- no sweep.

Solver:
- HF Frequency Domain;
- 1.0..1.8 GHz;
- tetrahedral second order;
- MinPasses 3;
- MaxPasses 12;
- MaxDeltaS 0.02;
- 2 consecutive checks;
- open boundaries;
- 30-mm background spacing.

## 6. Per-polarization metrics

Over 1.15..1.65 GHz and at L5/L2/L1:
- S11;
- S21 / S31;
- branch amplitude imbalance;
- phase error from 180 deg;
- common-mode ratio;
- power closure;
- mismatch-normalized excess loss;
- equivalent 100-ohm-reference input impedance.

Numerical qualification:
final two Delta-S <= 0.02.

## 7. A/B comparison

Compare on the same sampled frequencies:
- delta S11_dB = B - A;
- delta Zin real;
- delta Zin imaginary;
- delta amplitude imbalance;
- delta phase error;
- delta CMR;
- delta normalized excess loss.

Report max absolute differences over 1.15..1.65 GHz and values at L5/L2/L1.

This stage asks whether the 1.05-mm merge-height asymmetry is materially important.
It does not optimize either polarization.

## 8. Stop boundary

After two one-shot solves and comparison:
close BUILD/SOLVE authority
and stop at D2 matching-strategy review.
