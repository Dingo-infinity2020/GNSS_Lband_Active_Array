# AR0-B1R-R3-D1R1 Diagnostic Interpretation V0.1

Status: BASELINE CHARACTERIZED; REVIEW REQUIRED BEFORE OPTIMIZATION

## Canonical geometry correction

The original T1 Pol-A backside ground tapers were fully embedded in FR4. Pol-B was already exterior because of the opposite local-frame handedness.

New canonical T1R1:
- Pol-A extrusion height = -0.035 mm
- Pol-B extrusion height = +0.035 mm
- all four own-prong volumetric intersections = 0
- corrected T1R1 SHA256 = fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e

The original T1 remains historical evidence and is superseded for future geometry work.

## D1R1-A: corrected differential control

Source SHA256:
5aa3dd603607a70f7ac190c746e25af550f6cfcb81a9b1bb45846d9c776b6bcd

Solved SHA256:
4f3cde7d98bb84ecc9294271bc6a98e230eaa678100d6e8e7bc2f4bb80d67cb4

Numerically qualified:
PASS, final Delta-S = 6.55134e-4 and 9.55589e-6.

Decision band 1.15-1.65 GHz:
- worst S11 = -4.003 dB
- worst S22 = -4.005 dB
- minimum S21 = -2.220 dB
- worst reciprocity error = 9.1e-6 dB
- worst mismatch-normalized excess loss = 0.01737 dB
- power closure = 0.99760 to 0.99821
- Zin real = 124.68 to 158.87 ohm
- Zin imag = +133.93 to +196.26 ohm

At L5/L2/L1 the imaginary impedance is approximately proportional to frequency, corresponding to an effective series-inductive heuristic of about 18.6-18.9 nH.

Scientific interpretation:
The corrected transition is very low-loss and reciprocal but remains significantly inductive and not yet matched to 100 ohm differential.

## D1R1-B: corrected common-ground closure control

Source SHA256:
93d97b06bc2a739f84f88454a7efa76b27731e7bbdb2714214118a3ec0bafb35

Solved SHA256:
284453ae96f6bb3a0c2cb14e39c644547a4d66edbca119b61c9ddd27e8e8aa35

Numerically qualified:
PASS, final Delta-S = 1.21702e-3 and 3.48919e-5.

Decision band 1.15-1.65 GHz:
- worst S11 = -5.661 dB
- worst amplitude imbalance = 0.00198 dB
- worst phase error = 0.04196 deg
- worst CMR = -68.324 dB
- worst mismatch-normalized excess loss = 0.01838 dB
- power closure = 0.99692 to 0.99766
- Zin real = 111.00 to 120.52 ohm
- Zin imag = +94.22 to +132.49 ohm

At L5/L2/L1 the imaginary impedance corresponds to an effective series-inductive heuristic of about 12.8-13.0 nH.

Scientific interpretation:
Providing a true downstream common return path materially improves both the resistive and reactive part of the input impedance while preserving excellent symmetry and very low excess loss.

## Causal conclusion

The prior R2 result of roughly 40 - j(250-400) ohm must not be treated as the physical impedance of the intended transition.

The corrected evidence shows:
1. the embedded Pol-A ground geometry was a dominant modeling defect;
2. after correcting copper placement, the transition changes from strongly capacitive to clearly inductive;
3. separated versus common downstream return path is a secondary but material effect;
4. common-ground closure moves the network toward the 100-ohm differential target;
5. the remaining problem is predominantly distributed/loop inductance rather than dissipation or balance.

## Recommended next stage

Do NOT start a blind multi-dimensional sweep.

Next:
AR0-B1R-R3-D2_MANUFACTURABLE_GROUND_MERGE_AND_INDUCTANCE_REDUCTION

First create a manufacturable lower-stalk continuation in which the fork slot closes below the sensitive/LNA region and the two backside ground rails merge on supported FR4.

Then qualify that real merge.

Only after the real merge is frozen should matching variables be released in this order:
1. shorten balanced throat / move ground acquisition earlier;
2. reshape or shorten the ground-acquisition taper;
3. widen/reshape signal locally if required;
4. ground width as a secondary variable.

The optimization direction is now toward reducing effective series inductance and moving Zin toward 100+j0 ohm.

No optimization is authorized by this document.
