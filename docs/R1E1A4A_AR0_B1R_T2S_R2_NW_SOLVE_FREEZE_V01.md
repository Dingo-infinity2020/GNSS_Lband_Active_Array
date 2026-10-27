# AR0-B1R-T2S-R2 NW Qualification Freeze V0.1

Status: SOLVE AUTHORIZED BY CONDITIONAL CHAIN
SimulationOps: 0.2.8

Source fixture:
R1E1A4A_AR0_B1R_T2F_R2_CANONICAL_TRANSITION_FIXTURE_V01.cst

SHA256:
ae3bc705fea01e3a8f1c4a52458f447726843ba32a22d247c085c62b8bb83a7b

Parent build status:
PASS_R1E1A4A_AR0_B1R_T2F_R2_FIXTURE_BUILD_ONLY

Port correction:
- P1 unchanged, 100 ohm balanced.
- P2/P3 signal endpoint n=0.0 mm.
- P2/P3 ground endpoint n=-1.0 mm.
- P2/P3 port segment spans FR4 only.

Geometry changes during solve:
FORBIDDEN.

Port changes during solve:
FORBIDDEN.

Solver configuration:
unchanged from T2S V0.1:
- 1.0-1.8 GHz
- HF Frequency Domain
- second-order tetrahedral
- MinPasses 3
- MaxPasses 12
- MaxDeltaS 0.02
- two consecutive checks
- open boundaries
- 30 mm background spacing

Execution host:
NW / Windows CST 2022.

Exactly one formal run_solver() invocation.
No retry.
No sweep.

Qualification:
- require 9 Sij result terms;
- require final two Delta-S <=0.02;
- require passive closure max <=1.02;
- report S11, S21/S31, amplitude balance, phase balance, CMR and mismatch-normalized loss over 1.15-1.65 GHz and at L5/L2/L1.

A scientifically NEEDS_OPTIMIZATION geometry is still a successful characterization if numerical qualification and physical result integrity pass.
