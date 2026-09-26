# R1A5M Adaptive Mesh Convergence — Return Report

**FINAL_STATUS = HOLD_R1A5M_ADAPTIVE_NOT_CONVERGED**

Source HEAD:
1563c64bc55b9c72e23b61d7be110d334a34cf71

Formal invocation count:
1

Exit code:
0

Runtime:
81.54 s

R1A5M CST:
D:\GNSS_Lband_Active_Array\_r1a5m_adaptive_work\R1A5M_ADAPTIVE_SECOND_ORDER_V01.cst

SHA256:
67b44e77aa88709287caf194c8e89cc2535951e1fab66b7c679df9e398a62c9b

## Provenance and result integrity

PASS:
- immutable R1A4 source hash
- byte-identical pre-config copy
- unchanged shape inventory
- port count = 2
- complete 1001-point S11/S12/S21/S22 curves
- no NaN/Inf
- reciprocity
- Pol-A/B symmetry

Final max Pol-A/B dB asymmetry:
0.179711978 dB

Final max complex reciprocity error:
6.95296e-05

## Native adaptive convergence

CST output.txt reports:

- pass 2: Delta-S 0.0673917
- pass 3: Delta-S 0.0497934
- pass 4: Delta-S 0.0274924
- pass 5: Delta-S 0.0203932
- pass 6: Delta-S 0.0173369

Configured threshold:
0.02

Configured consecutive checks:
2

Pass 6 is below threshold, but pass 5 is slightly above threshold.

CST explicitly reports:
`Mesh adaptation terminated because the maximum number of passes is reached.`

Therefore the native adaptive sequence is trending monotonically toward convergence but has not satisfied the frozen two-consecutive-check condition.

## External baseline comparison

Compared with the non-adaptive second-order R1A5R baseline over 1.15–1.65 GHz:

- max complex delta S11 = 0.148757667
- max complex delta S22 = 0.147259378

This fails the frozen <=0.05 external baseline criterion.

Interpretation:
the non-adaptive R1A5R baseline is itself too coarse to serve as a converged absolute reference.

## Engineering conclusion

- no numerical divergence observed;
- symmetry and reciprocity improve strongly;
- absolute response is still not formally mesh-converged;
- current adaptive run stopped because MaxPasses=6 was too restrictive for two consecutive Delta-S checks.

Recommended recovery:
R1A5M2 with identical model/solver/adaptation settings except MaxPasses increased from 6 to 8.

No geometry/material/port changes are justified.
No production science or material A/B is authorized yet.
