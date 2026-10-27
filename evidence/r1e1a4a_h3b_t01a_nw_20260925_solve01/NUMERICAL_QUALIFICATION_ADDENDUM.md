# H3B-T01A Numerical Qualification Addendum

Formal solver invocation completed and produced a full reciprocal 2-port result set, but the frozen adaptive-mesh convergence requirement was NOT satisfied.

Native CST adaptive-mesh result tree proves eight passes:
- mesh cells: 43,521 -> 51,980 -> 61,554 -> 74,117 -> 78,237 -> 82,457 -> 88,182 -> 98,391;
- All-S ΔS at pass 7 = 0.0320727160;
- All-S ΔS at pass 8 = 0.0309454700;
- frozen threshold = 0.02 with two consecutive checks required;
- maximum frozen pass count = 8.

Therefore canonical numerical status:
`HOLD_R1E1A4A_H3B_T01A_ADAPTIVE_MAXPASS8_NOT_CONVERGED`.

The original summary.json is retained unchanged as raw execution evidence. Its `numerical_pass=true` field only meant the solver returned S-parameter data; it is superseded for qualification by this addendum and native_adaptation.json.

Provisional diagnostic observations only:
- no sharp S21 notch in 1.15–1.65 GHz;
- S11/S22 approximately -14.7 to -10.3 dB across the core band;
- S21 approximately -0.257 to -0.570 dB across the core band;
- S21/S12 reciprocity difference approximately 4e-5 dB.

These values are NOT science-qualified until adaptive convergence is recovered.

No silent retry is allowed. A new explicit solve authorization is required for numerical recovery.