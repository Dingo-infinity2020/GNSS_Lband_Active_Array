# H3B-T01A MaxPass16 Numerical Recovery Qualification

Canonical status: PASS_R1E1A4A_H3B_T01A_NUMERICALLY_CONVERGED_MAXPASS16.

Recovery changed only adaptive MaxPasses from 8 to 16. Geometry, ports, frequency range, mesh formulation and DeltaS threshold remained frozen.

Native CST adaptive convergence:
- pass 11 All-S DeltaS = 0.01971590799;
- pass 12 All-S DeltaS = 0.01570656518;
- threshold = 0.02, two consecutive checks required;
- CST terminated adaptation because desired accuracy was reached;
- actual passes executed = 12.

Numerically qualified core-band diagnostics (1.15–1.65 GHz):
- S11 range approximately -15.37 to -9.77 dB;
- S22 range approximately -15.37 to -9.77 dB;
- S21 range approximately -0.240 to -0.639 dB;
- S12 range approximately -0.240 to -0.639 dB;
- S21/S12 reciprocity max difference approximately 6.5e-5 dB;
- max core-band S21 change versus maxpass8 result = 0.0686 dB.

Interpretation:
- no evidence of a sharp destructive transition resonance in the core band;
- the baseline is not yet at the preferred return-loss/insertion-loss targets;
- measured RP1-to-RP2 loss includes both FR4 GCPW line sections and the 90-degree junction; it is not junction-only loss.

Solved artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h3b_t01a_recovery16_work\R1E1A4A_H3B_T01A_RECOVERY_MAXPASS16_V01.cst

SHA256:
928400031803e62665df0a17890b2158b8d56b2673e9af1a9e0c7a7d171266df

Next node: H3B_T01A_LOCAL_RF_OPTIMIZATION_FREEZE. No optimization is authorized by this closeout.