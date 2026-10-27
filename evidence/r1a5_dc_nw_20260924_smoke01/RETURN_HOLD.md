# R1A5 Diagnostic Smoke — Attempt-1 Return

**FINAL_STATUS = HOLD_R1A5_DIAGNOSTIC_INTEGRITY**

Source HEAD:
f8cda7b8366047e28fbce2c3370546d38605d9cc

Formal invocation count:
1

Exit code:
0

Runtime:
27.92 s

Solver:
COMPLETED

Result curves:
- S11: present, 1001 points
- S12: present, 1001 points
- S21: present, 1001 points
- S22: present, 1001 points
- NaN/Inf: none

Provenance:
- source hash match: PASS
- byte-identical pre-config copy: PASS
- geometry unchanged: PASS
- port count = 2: PASS
- reciprocity: PASS

Only failed frozen gate:
max |S11_dB - S22_dB| <= 1.0 dB

Observed:
max asymmetry = 1.504024537 dB at 1.4136 GHz.

Best match:
- Pol-A S11 = -18.593128 dB at 1.3976 GHz
- Pol-B S22 = -17.137847 dB at 1.3936 GHz

Resonance frequency separation:
approximately 4 MHz.

At GNSS anchor frequencies the S11/S22 difference is substantially smaller, approximately 0.26–0.85 dB.

Interpretation:
- the actual antenna model clearly resonates around 1.4 GHz;
- no gross feed/model failure is present;
- the HOLD is a narrow polarization-symmetry convergence issue near the deep resonance;
- first-order tetrahedral discretization is a plausible numerical cause and must be tested before modifying geometry.

No automatic retry was performed.

Recovery:
authorize a fresh R1A5R numerical-convergence check from the original hash-locked R1A4 CST, changing only tetrahedral basis/solver accuracy while preserving geometry, ports, boundaries and frequency range.
