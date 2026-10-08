# AR0-B1R-T2F-R2 Output-Port Endpoint Fix Freeze V0.1

Status: BUILD AUTHORIZED; CONDITIONAL SOLVE AUTHORIZED AFTER BUILD PASS
SimulationOps: 0.2.8

## Purpose

Correct only the grounded output-port endpoints of the accepted T2F transition fixture.

Native CST evidence from the prior NW solve showed:
- Ports 2 and 3: endpoint(s) not connected to a good conductor;
- mesh corruption near lumped element 2;
- the old P2/P3 segment traversed finite-thickness lossy copper.

No T1 geometry is changed.

## Parent

T1 product artifact:
R1E1A4A_AR0_B1R_T1_GROUND_ACQUISITION_BUILD_ONLY_V01.cst

SHA256:
3144672323cbd4123d6413e7d9ae8f4842b78707d3a71b641748c7250ca2a8f6

The R2 fixture is rebuilt from this clean T1 parent, not from the failed solve copy.

## Retained geometry

Exactly the same six solids as T2F:
- B0_Stalk:A_P_PRONG
- B0_Stalk:A_N_PRONG
- B0_MSL:A_P_MSL
- B0_MSL:A_N_MSL
- B1RT1_BackGround:A_P_GROUND_TAPER
- B1RT1_BackGround:A_N_GROUND_TAPER

Every retained solid must match the original T2F/T1 material and volume exactly.

## Ports

Port 1 is unchanged:
- 100 ohm balanced input;
- endpoints remain on the outer/front surfaces of the two signal conductors at v=0;
- local n=+0.035 mm.

Ports 2 and 3 retain:
- 50 ohm impedance;
- v=10.0 mm reference plane;
- u=+3.0 / -3.0 mm branch centers.

Only their n coordinates change:

Old:
- signal n=+0.035 mm;
- ground n=-1.035 mm.

R2:
- signal endpoint n=0.0 mm;
- ground endpoint n=-1.0 mm.

Thus the P2/P3 discrete-port segment spans only the 1.0-mm FR4 dielectric and terminates on the copper/FR4 interfaces. It does not traverse either lossy copper sheet.

## Build-only acceptance

Required:
- exact T1 parent hash;
- exactly six retained solids;
- retained geometry/material/volume exact;
- exactly three ports build + fresh reopen;
- P1 coordinates identical to accepted T2F;
- P2/P3 u,z,impedance unchanged;
- P2/P3 n exactly 0.0 to -1.0 mm;
- P2/P3 mirror symmetry exact;
- no result tree;
- zero solver invocations.

## Conditional downstream authorization

The user explicitly authorized the complete recovery chain.

If and only if R2 build-only passes all gates:
- solver config may be applied without another user prompt;
- exactly one new NW formal solve is authorized;
- no retry;
- no parameter sweep.

Any HOLD stops the chain.
