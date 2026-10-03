# AR0-B1R-T2F Canonical Transition Fixture Freeze V0.1

Status: FROZEN FOR AUTHORIZED BUILD-ONLY
SimulationOps: 0.2.8

## 1. Purpose

Create a solver-ready but unsolved canonical fixture for the T1 balanced-throat / ground-acquisition transition.

T2F is deliberately isolated from the radiator and mechanical support so the later S-parameter solve measures the transition itself rather than a mixture of transition loss, antenna radiation, reflector coupling and support scattering.

No solver is authorized in T2F.

## 2. Parent

Parent product artifact:
R1E1A4A_AR0_B1R_T1_GROUND_ACQUISITION_BUILD_ONLY_V01.cst

SHA256:
3144672323cbd4123d6413e7d9ae8f4842b78707d3a71b641748c7250ca2a8f6

Parent status:
PASS_R1E1A4A_AR0_B1R_T1_GROUND_ACQUISITION_BUILD_ONLY

## 3. Canonical polarization

Pol-A is used as the canonical local transition fixture.

Reason:
- T1 geometry is exact C4/rotation-equivalent between Pol-A and Pol-B;
- T2F aims to qualify the local feed transition, not cross-polarization coupling;
- avoiding duplicate A/B fixtures reduces formal builds and keeps the first EM qualification minimal.

A later integrated dual-polarization sentinel will verify coupling in the real assembly.

## 4. Geometry extraction

Copy the exact T1 artifact and retain only these six solids:

- B0_Stalk:A_P_PRONG
- B0_Stalk:A_N_PRONG
- B0_MSL:A_P_MSL
- B0_MSL:A_N_MSL
- B1RT1_BackGround:A_P_GROUND_TAPER
- B1RT1_BackGround:A_N_GROUND_TAPER

All other solids are deleted in the fixture copy.

No retained geometry is re-created, moved, scaled, united or trimmed.

Therefore T2F preserves exactly:
- stalk FR4 thickness = 1.00 mm;
- prong width = 4.00 mm each;
- center clear slot = 2.00 mm;
- signal width = 1.90 mm;
- signal center positions local u=+/-3.00 mm;
- L_bal = 1.50 mm;
- L_taper = 3.00 mm;
- full-ground start v=4.50 mm;
- full-ground width = 3.60 mm;
- feed-head depth = 12.00 mm.

The RF tenon/solder joint is intentionally excluded from this local transition fixture. It remains a separate manufacturability interface already accepted at T0 and will be tested again in the later integrated antenna model.

## 5. Coordinate system

Use original global coordinates from Pol-A.

Pol-A local unit vectors:
- u = (+1/sqrt(2), +1/sqrt(2), 0)
- n = (-1/sqrt(2), +1/sqrt(2), 0)

Radiator/stalk interface:
z0 = 57.1428571428 mm.

The fixture runs downward to:
v = 12.0 mm
or
z = 45.1428571428 mm.

## 6. Port topology

Three discrete S-parameter ports are frozen.

### Port 1 — balanced input

Role:
canonical differential excitation of the two top signal conductors.

Reference impedance:
100 ohm.

Reference plane:
top end of retained signal traces at v=0 / z=z0.

Endpoints:
- P1: + branch signal outer/front surface, local (u=+3.0, n=+0.035, z=z0)
- P2: - branch signal outer/front surface, local (u=-3.0, n=+0.035, z=z0)

This is a lumped differential fixture port.
It is not an antenna port.

### Port 2 — + branch grounded output

Reference impedance:
50 ohm.

Reference plane:
v=10.0 mm, safely inside the established full-ground region and below the former LNA-envelope region.

Endpoints at local u=+3.0:
- signal outer/front surface n=+0.035;
- local ground outer/back surface n=-1.035;
- z=z0-10.0 mm.

### Port 3 — - branch grounded output

Identical to Port 2 under mirror symmetry.

Reference impedance:
50 ohm.

Endpoints at local u=-3.0:
- signal outer/front surface n=+0.035;
- local ground outer/back surface n=-1.035;
- z=z0-10.0 mm.

## 7. Future mixed-mode interpretation

T2F itself does not solve, but the later T2S qualification will interpret:
- Port 1 as the 100-ohm balanced input;
- Ports 2 and 3 as the two 50-ohm ground-referenced output branches.

The primary later observables will be:
- differential input return;
- total delivered power into Ports 2+3;
- branch amplitude imbalance;
- branch phase imbalance relative to 180 degrees;
- common-mode proxy from the coherent sum of output waves;
- excess loss after accounting for reflection.

No claim is made that the present dimensions are optimal.

## 8. Build-only acceptance

Required:
- exact T1 parent hash;
- exactly six retained geometry solids;
- every retained solid name/material/volume exactly preserved;
- no radiator, reflector, mechanical support, LNA envelope, RF-tenon or solder-proxy solid remains;
- Port 1 exists once at 100 ohm;
- Ports 2 and 3 exist once each at 50 ohm;
- exactly three ports after immediate build audit;
- exactly three ports after fresh reopen;
- no geometry change between immediate build and fresh reopen;
- no solver result tree;
- no solver invocation;
- endpoint parameters preserve exact Pol-A symmetry.

## 9. Stop boundary

T2F PASS
-> HUMAN FIXTURE REVIEW
-> later explicit T2S SOLVE authorization.

No solve is authorized by this freeze.
