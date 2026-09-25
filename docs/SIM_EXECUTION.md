# SIM_EXECUTION

## Current stage
R1E1A4A_H2A_V02_SERVICE_ARCHITECTURE_BUILD_ONLY

BUILD_AUTHORIZED: true — ONE H2A V0.2 BUILD-ONLY INVOCATION
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Source
Parent artifact:
D:\GNSS_Lband_Active_Array\_r1e1a1_six_pitch_fr4_work\R1E1A1_P094_PITCH_BUILD_ONLY_V01.cst

SHA256:
fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e

## V0.2 build scope
- retain V0.1 patterned ground / feed pins / dummy LNA envelopes;
- replace old PEEK carrier concept with four hollow copper service tubes;
- add four MHF4/U.FL-class board-side connector envelopes;
- add four 0.81-mm micro-coax service paths;
- add four top and four bottom insulating tube-interface spacers;
- add four backplane feedthroughs;
- add four MMCX-class lower connector envelopes;
- shield receives corner service egress paths;
- tube electrical bond state remains unfrozen for later T0/T1/T2 study.

No RF port, solver, active transistor, matching network, bias network or optimization is allowed.

Design freeze:
docs/R1E1A4A_H2A_V02_SERVICE_ARCHITECTURE.md

Build macro:
source/cst/R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY_V01.mcr

## Stop boundary
Stop after fresh-reopen BUILD qualification for human 3D review.
No H2A V0.2 solve and no H2B/T0/T1/T2 execution.
