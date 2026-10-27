# H3B-T01A Freeze V0.1

Status: PASS_R1E1A4A_H3B_T01A_FREEZE

Nominal geometry:
- line Wsig = 1.50 mm
- line Gcpw = 0.40 mm
- transition signal-pad width = 2.00 mm
- transition pad gap = 0.30 mm
- transition extension = 0.30 mm
- O2C nominal tuning closed; contingency only
- T01-C remains deferred

Physical-fidelity O3:
- copper sigma = 5.8e7 S/m engineering model
- solder proxy sigma = 7.0e6 S/m
- worst core return = -14.5073 dB
- core S21 minimum = -0.33484 dB
- junction excess maximum = 0.06215 dB
- nominal final DeltaS = 0.0192088 / 0.0145830
- paired straight-reference final DeltaS = 0.0174087 / 0.0128955
- nominal solved SHA256 = 5a3ec0b2a9eca4bc0253d0e1fd5ab5f512d6d0fb63944bbd7b932505c1f5f82f
- straight-reference solved SHA256 = 421c4951a122749aacf36254b8bb5a156547a22dd6ab9e465139c44207d6519b

O4:
All six deterministic sentinels passed the frozen acceptable gates. FAB_LOWZ is the limiting return-loss case at -12.4942 dB.

Reusable outputs:
- evidence/r1e1a4a_h3b_t01a_o3_o4_nw_20260926_run01/T01A_P20_G30_E30_FINITE_CONDUCTIVITY.s2p
- evidence/r1e1a4a_h3b_t01a_o3_o4_nw_20260926_run01/T01A_W15_G40_STRAIGHT_FINITE_CONDUCTIVITY.s2p

Next boundary:
H3B_COMPLETE_PASSIVE_UNIT_FREEZE. No build or solve authorization is open.
