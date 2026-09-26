# R1E1A3-R1 S1 Bonded Broadside Qualification

Status: `PASS_R1E1A3R1_S1_BONDED_B0_SOLVE_AND_BENIGN_GATE`

Recovery sole solver change: MaxPasses 8 -> 12.

Adaptive Delta-S ended with pass 10 = 0.0164063 and pass 11 = 0.0144292; CST terminated by desired accuracy, not MaxPasses. Broadband convergence passed and no solver error line was found.

Versus qualified bare broadside over 1.15–1.65 GHz:
- max complex |Delta S11| = 0.02950756;
- RMS complex |Delta S11| = 0.01361627;
- max |Delta Z_active| = 5.58606 ohm;
- RMS |Delta Z_active| = 4.40921 ohm;
- no severe mismatch alerts.

Frozen benign gate 0.05 / 10 ohm: PASS.

Versus the prior MaxPasses=8 HOLD solution:
- max complex |Delta S11| = 0.02741071;
- max |Delta Z_active| = 6.36602 ohm.

The recovery remains physically consistent in scale while providing strict numerical qualification.

Provenance protection worked: CST history replay attempted to rewrite the two historical R1E1A2 B0 build-audit files; the recovery harness detected the rewrites, restored the byte-level snapshots, and verified restoration.

Solved artifact:
`D:\GNSS_Lband_Active_Array\_r1e1a3r1_s1_b0_recovery_work\R1E1A3R1_S1_BONDED_B0_SOLVE_V02.cst`

SHA256:
`9ca14907abb5a839c399452ef88a7f949dd3df4476992918d1bba5b7c33b71a9`

Artifact is PROTECTED_IN_PLACE.
