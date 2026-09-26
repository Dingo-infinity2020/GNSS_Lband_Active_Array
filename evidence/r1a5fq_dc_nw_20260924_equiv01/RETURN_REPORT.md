# R1A5FQ Clean-Feed Isolated Equivalence — Final Report

**FINAL_STATUS = PASS_R1A5FQ_CLEAN_FEED_EQUIVALENT**

Mainline authority:
PROJECT_MAINLINE.md

Source HEAD:
9d4d7dbf0741df2776298c2be51fa8df26ff3427

Formal invocation count:
1

Exit code:
0

Runtime:
180.64 s

## Input models

A source:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst

A source SHA256:
74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce

B source:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLB_SINGLE_PORT_V01.cst

B source SHA256:
11ca4ae06baa1d3f18376789c90717f28aee2b02480d7eba88d2f5155d51a1bf

R1A5M2 baseline CSV SHA256:
e4413cf91a986006bc922611fb8e5a493fea260741d58a373a9d387151c888aa

## Native adaptive convergence

Model A Delta-S:
0.0993532 -> 0.0268758 -> 0.0225950 -> 0.0230506 -> 0.0212685 -> 0.0164832 -> 0.0145415

A termination:
desired accuracy reached

A broadband sweep:
PASS

Model B Delta-S:
0.0661009 -> 0.0383940 -> 0.0272181 -> 0.0232756 -> 0.0179865 -> 0.0139052

B termination:
desired accuracy reached

B broadband sweep:
PASS

Neither model terminated by maximum pass count.

## Equivalence metrics over 1.15–1.65 GHz

A clean S11 vs R1A5M2 S11:
- max complex delta = 0.008537500
- frozen threshold = 0.03
- PASS

B clean S11 vs R1A5M2 S22:
- max complex delta = 0.008399949
- frozen threshold = 0.03
- PASS

Clean A vs clean B:
- max complex delta = 0.012309052
- frozen threshold = 0.02
- PASS
- max dB difference = 0.456468929 dB
- frozen threshold = 0.5 dB
- PASS

## Result artifacts

A result CST:
D:\GNSS_Lband_Active_Array\_r1a5fq_equivalence_work\R1A5FQ_A_EQUIVALENCE_V01.cst

SHA256:
0afc37b65b65d6f17746b7e04a7d4aec239f395ec38351fbfaa1502a4ec87e2a

B result CST:
D:\GNSS_Lband_Active_Array\_r1a5fq_equivalence_work\R1A5FQ_B_EQUIVALENCE_V01.cst

SHA256:
f78d87dda909af55844ce645c4593cea2d2e9d0f5de4e492a5bd66d42fed5c0f

## Scientific conclusion

Removing the simultaneous crossed second discrete port does not materially change the converged passive self-response.

The R1A5F clean single-port representations are accepted as the passive feed basis for subsequent periodic/unit-cell array work.

The isolated-element passive qualification is now CLOSED.

No isolated-element geometry optimization is justified or authorized.

## Mainline transition

Next primary physics gate:
R1E0 — 94-mm periodic unit-cell baseline.

R1E0 must move the project from isolated input impedance toward scan-dependent active impedance.

No periodic solver is authorized by this report alone.
