# R1A5R Second-Order Symmetry Convergence — Return Report

**FINAL_STATUS = PASS_R1A5R_SYMMETRY_CONVERGED**

Source HEAD:
73391ffa61cb1fb7f3b8cc5cb785b9c1a3d0ecc6

Formal invocation:
1

Exit code:
0

Runtime:
36.57 s

Input source:
R1A4 hash-locked two-port CST

Input SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

R1A5R CST:
D:\GNSS_Lband_Active_Array\_r1a5r_second_order_work\R1A5R_SECOND_ORDER_V01.cst

R1A5R CST SHA256:
f2254cffe07312270d115e95f5526d5841411a865571dfc22c8a3321a98e24e0

Config SHA256:
0f16ce84ef99778a6132530c89df9de7cd94504fc8633176782ef4187f717cb4

Harness SHA256:
512c1e2c9eb1e106ed0797787b1a20aa449c9467642bbcfbdfea84702b406294

## Integrity results

- all four S curves present: PASS
- 1001 frequency points: PASS
- no NaN/Inf: PASS
- geometry unchanged: PASS
- port count = 2: PASS
- reciprocity max complex error = 1.86209e-4: PASS
- max |S11_dB-S22_dB| = 0.558463159 dB: PASS

R1A5 first-order baseline asymmetry:
1.504024537 dB

Reduction:
approximately 62.9%.

Conclusion:
the R1A5 first-order polarization asymmetry is primarily numerical/discretization-related rather than evidence of broken fourfold antenna geometry.

## Second-order diagnostic response

At 1.4 GHz:
- S11 = -18.8685 dB
- S22 = -18.4264 dB
- S21 = -45.6379 dB qualitative only

The strong ~1.4 GHz matching feature remains present.

Global best over 1.0–1.8 GHz:
- S11 = -19.1452 dB @ 1.7520 GHz
- S22 = -19.7036 dB @ 1.7520 GHz

Second-order -10 dB sampled bandwidth:
- Pol-A: 1.1816 GHz through the 1.8 GHz upper sweep limit
- Pol-B: 1.1776 GHz through the 1.8 GHz upper sweep limit

## Important non-convergence finding

First-order -10 dB sampled bandwidth:
- Pol-A: 1.2144–1.6176 GHz
- Pol-B: 1.2248–1.5904 GHz

Maximum second-order minus first-order difference:
- S11 magnitude in dB: ~12.25 dB at 1.8 GHz
- S22 magnitude in dB: ~13.15 dB near 1.788 GHz
- S21 magnitude in dB: ~16.31 dB at 1.0 GHz

Therefore:
- polarization symmetry has converged enough for this gate;
- absolute S-parameter response is NOT yet declared mesh/order converged;
- material A/B and production science must wait for an explicit mesh-convergence gate.

## Mesh note

First-order generated approximately:
21452 tetrahedra.

Second-order generated approximately:
8545 tetrahedra with second-order basis / curvature order 3.

Different polynomial order and meshing behavior are sufficient to explain why direct first-vs-second absolute S-curve agreement cannot be assumed.

## Stop

Return to DESIGN.

Recommended next gate:
R1A5M mesh-convergence contract.

No automatic third solve.
No adaptation.
No geometry edit.
No material A/B.
No CST251.
