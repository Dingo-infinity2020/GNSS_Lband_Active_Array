# SIM_EXECUTION

## Current stage
R1E1A4A_H2A_UNIVERSAL_CENTER_STRUCTURE_BUILD_ONLY

BUILD_AUTHORIZED: true — ONE H2A BUILD-ONLY INVOCATION
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

## H2A V0.1 build scope
- same-board backside patterned local ground;
- 20x20-mm outer ground envelope with 8x8-mm center clearance;
- four 0.90-mm square signal landing pads;
- four 0.30-mm square RF pin/via proxies at exact terminal centers;
- four 2x2x0.6-mm dummy LNA package envelopes at radius 6.2 mm;
- 18x18-mm shield-can envelope, 6-mm depth;
- hollow PEEK visual-surrogate carrier, 30-mm outer / 21-mm inner square span;
- existing main backplane remains the parent `UNITCELL_GROUND_REFERENCE`.

H2A intentionally contains:
- no RF ports;
- no feed traces/matching network;
- no bias/output network;
- no transistor/LNA device model;
- no solver or optimization.

Build macro:
source/cst/R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY_V01.mcr

Design freeze:
docs/R1E1A4A_H2A_UNIVERSAL_CENTER_STRUCTURE_V01.md

## Stop boundary
After fresh-reopen BUILD qualification, stop for human 3D review.
No H2A solve and no H2B/H2C build.
