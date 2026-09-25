# SIM_EXECUTION

## Current stage
R1E1A4A_H1R_NUMERICAL_RECOVERY_DESIGN

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## H1A closed solve
Canonical status:
HOLD_R1E1A4A_H1A_BROADSIDE_NUMERICAL_MAXPASSES

Formal solve invocation count: 1
Solver rerun: NO

Solved artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h1a_b0_solve_work\R1E1A4A_H1A_BROADSIDE_SOLVE_V01.cst

SHA256:
5960efbfe85a1f27ae29be987dc397a57c52d75129f9134a49372d898b64e930

Numerical status: HOLD.
- final Delta-S = 0.0213176;
- MaxPasses=12 reached;
- desired-accuracy termination = false;
- broadband sweep converged after 6 samples;
- no solver errors.

Provisional diagnostics only:
- mixed-mode symmetry would pass;
- max |Sdc| about -68.32 dB;
- branch magnitude imbalance about 0.0108 dB;
- QPL9547 R-NF0 provisional max about 0.421 dB;
- provisional exceedance only near 1.1504-1.1736 GHz.

These are NOT authoritative because the numerical gate failed.

## Next design
Plan:
docs/R1E1A4A_H1R_NUMERICAL_RECOVERY_PLAN.md

Frozen future recovery:
- H1A geometry unchanged;
- broadside unchanged;
- all Gate-R thresholds unchanged;
- sole solver change: MaxPasses 12 -> 16.

## Stop boundary
DESIGN ONLY.
Await fresh explicit H1R solve authorization.
No H1B/H1C, scan continuation, carrier, shield/package or transistor work.
