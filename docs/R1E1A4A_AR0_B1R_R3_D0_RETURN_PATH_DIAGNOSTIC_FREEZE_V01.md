# AR0-B1R-R3-D0 Return-Path Diagnostic Fixtures Freeze V0.1

Status: BUILD AUTHORIZED; SOLVE FORBIDDEN
SimulationOps: 0.2.8

## 1. Purpose

Diagnose whether the severe capacitive input seen in T2S-R2 is caused primarily by the local balanced-to-grounded transition itself or by the fact that the two local backside ground rails are still electrically separate inside the truncated feed-head fixture.

No T1 signal, substrate or ground-taper geometry is changed.

This stage creates two complementary diagnostic fixtures from the same clean T1 parent.

## 2. Parent geometry authority

Parent:
R1E1A4A_AR0_B1R_T1_GROUND_ACQUISITION_BUILD_ONLY_V01.cst

SHA256:
3144672323cbd4123d6413e7d9ae8f4842b78707d3a71b641748c7250ca2a8f6

Retain exactly:
- B0_Stalk:A_P_PRONG
- B0_Stalk:A_N_PRONG
- B0_MSL:A_P_MSL
- B0_MSL:A_N_MSL
- B1RT1_BackGround:A_P_GROUND_TAPER
- B1RT1_BackGround:A_N_GROUND_TAPER

Retained material and volume must match T1 exactly.

## 3. D0-A — differential control

Purpose:
measure the odd/differential transition without asking the two separated local grounds to serve as independent single-ended references.

Geometry:
the exact six retained T1 solids only.

Ports:
- Port 1: 100-ohm differential input at v=0, between + and - signal conductors.
- Port 2: 100-ohm differential output at v=10 mm, between + and - signal conductors.
- both differential-port endpoints use the signal outer/front surface, local n=+0.035 mm.
- the two backside grounds are passive EM structures and remain electrically separate.

No single-ended branch port exists in D0-A.

Diagnostic question:
Does the accepted T1 transition behave reasonably for differential/odd mode when no artificial single-ended return closure is demanded?

## 4. D0-B — ideal common-ground closure control

Purpose:
keep the accepted R2 three-port topology but explicitly close G+ and G- downstream of the output reference plane.

Geometry:
the exact six retained T1 solids plus one diagnostic copper bridge.

Ports:
- Port 1: identical to T2F-R2, 100-ohm differential input at v=0.
- Port 2: 50-ohm + branch output at v=10 mm, signal n=0 to ground n=-1.0 mm.
- Port 3: 50-ohm - branch output at v=10 mm, signal n=0 to ground n=-1.0 mm.

Diagnostic common-ground bridge:
- local u = -1.20 to +1.20 mm;
- local n = -1.035 to -1.000 mm;
- local v = 11.0 to 12.0 mm;
- material = B0_COPPER;
- exact face contact with the inner edges of the two 3.60-mm full-ground rails at u=+/-1.20 mm.

The bridge is intentionally below the v=10-mm output reference plane.

This bridge spans the central air slot and is a diagnostic idealization only.
It is NOT a manufacturable product-ground merge and does not modify the frozen B0/B1 mechanical architecture.

Diagnostic question:
Does providing a true common return path collapse the large capacitive input mismatch while preserving the excellent branch balance?

## 5. D0-C is deferred

A real manufacturable stalk-ground merge below the sensitive feed/LNA region is NOT part of D0 build-only.

D0-C becomes relevant only after D0-A/B solve results identify which return-path interpretation is correct.

## 6. Build-only acceptance — D0-A

Required:
- exact T1 parent hash;
- exactly six retained solids;
- retained material/volume exact;
- exactly two ports build + fresh reopen;
- both ports exactly 100 ohm;
- Port 1 at v=0;
- Port 2 at v=10 mm;
- both span +signal to -signal;
- no geometry edits;
- no result tree;
- zero solver invocations.

## 7. Build-only acceptance — D0-B

Required:
- exact T1 parent hash;
- exactly six retained T1 solids plus one bridge solid;
- retained six-solid material/volume exact;
- bridge positive volume;
- bridge dimensions exactly 2.40 mm x 0.035 mm x 1.00 mm;
- bridge face-connects both full-ground inner edges at u=+/-1.20 mm;
- bridge lies entirely at v=11..12 mm and backside n=-1.035..-1.0 mm;
- exactly three ports build + fresh reopen;
- P1 identical to T2F-R2;
- P2/P3 identical to T2F-R2;
- no result tree;
- zero solver invocations.

## 8. Stop boundary

D0 build-only PASS
-> human/analytic fixture review
-> separate solve authorization is still required.

No solver is authorized by this freeze.
