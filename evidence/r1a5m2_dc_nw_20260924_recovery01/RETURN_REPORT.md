# R1A5M2 MaxPass Recovery — Final Report

**FINAL_STATUS = PASS_R1A5M2_NATIVE_AND_ABSOLUTE_CONVERGED**

Source HEAD:
165707fe2da53e5c5ccf9b7e8d775f45017ec8b2

Formal invocation count:
1

Exit code:
0

Runtime:
108.72 s

R1A5M2 CST:
D:\GNSS_Lband_Active_Array\_r1a5m2_maxpass8_work\R1A5M2_ADAPTIVE_MAXPASS8_V01.cst

SHA256:
1f904290293b49d4ad39d71cf3d3ddda86c81c2c202305e95f43b50ed477428e

Bytes:
48178

## Native CST adaptation

Delta-S sequence:
- pass 2: 0.0673917
- pass 3: 0.0497934
- pass 4: 0.0274924
- pass 5: 0.0203928
- pass 6: 0.0173367
- pass 7: 0.0175890

Configured threshold:
0.02

Required consecutive checks:
2

Pass 6 and pass 7 are both below threshold.

CST termination:
`Mesh adaptation terminated because the desired accuracy limit is reached.`

Max-pass termination:
NO

Broadband sweep:
converged after 8 frequency samples.

## Incremental absolute convergence

Compared with R1A5M pass-6 result over 1.15–1.65 GHz:

- max complex delta S11 = 0.015124122
- max complex delta S22 = 0.015189754

Frozen threshold:
0.03

PASS.

## Symmetry / reciprocity

- max |S11_dB-S22_dB| = 0.013107094 dB
- max complex |S21-S12| = 7.96678e-05

Both PASS.

## Converged diagnostic matching

Sampled -10 dB bandwidth over the 1.0–1.8 GHz sweep:

- Pol-A: 1.1600 GHz through 1.8000 GHz sweep limit
- Pol-B: 1.1600 GHz through 1.8000 GHz sweep limit

At 1.15 GHz:
- Pol-A S11 ~ -9.09 dB
- Pol-B S22 ~ -9.08 dB

Representative anchors:
- 1.1768 GHz: -11.62 / -11.61 dB
- 1.2272 GHz: -15.74 / -15.75 dB
- 1.2784 GHz: -15.67 / -15.68 dB
- 1.4000 GHz: -12.32 / -12.32 dB
- 1.5608 GHz: -12.29 / -12.29 dB
- 1.5752 GHz: -12.46 / -12.46 dB
- 1.6024 GHz: -12.84 / -12.85 dB
- 1.6496 GHz: -13.77 / -13.78 dB

## Important feed-model limitation

The crossed discrete-edge ports remain diagnostic-only.

R1A4Q showed a solver-dependent artificial coupling path caused by the crossed port representation.

Therefore:
- S11/S22 and passive matching baseline are accepted for diagnostic/convergence use;
- S21/S12 around/below approximately -50 dB are port-model-limited;
- no production polarization-isolation claim is allowed from this model;
- material A/B, efficiency/gain and production far-field work should use or cross-check a non-intersecting differential feed model.

## Scientific conclusion

The CHARTS-inspired FR4 passive element is numerically stable and mesh-converged for the current diagnostic model.

No physical geometry change is justified by the R1A5/R1A5R/R1A5M/R1A5M2 sequence.

Next recommended gate:
R1A5F non-crossing differential-feed design and qualification.

No solver is authorized by this conclusion.
