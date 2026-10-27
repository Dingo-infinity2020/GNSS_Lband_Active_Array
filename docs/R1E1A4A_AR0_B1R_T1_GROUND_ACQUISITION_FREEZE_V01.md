# AR0-B1R-T1 Balanced-Throat / Ground-Acquisition Geometry Freeze V0.1

Status: FROZEN FOR AUTHORIZED BUILD-ONLY
SimulationOps: 0.2.8

## 1. Purpose

Replace the B0/B1R-T0 abrupt 3.0-mm no-ground then full-ground step with a continuous symmetric first-cut transition:

balanced radiator
-> RF tenon / solder joint
-> balanced throat
-> symmetric ground-acquisition taper
-> twin grounded microstrip
-> twin LNA reserve.

This stage is geometry-only.
It does not claim impedance, noise-match, common-mode or radiation qualification.

## 2. Parent

Parent artifact:
R1E1A4A_AR0_B1R_T0_RF_TENON_BUILD_ONLY_V01.cst

SHA256:
f4c51b603fc01e8c3cec095de0ca641a3a671dc1e2449a95a123af6a8b902bb9

Parent status:
PASS_R1E1A4A_AR0_B1R_T0_RF_TENON_BUILD_ONLY

Immutable in T1:
- radiator RF mortises;
- four FR4 RF tenons;
- four RF-tenon copper extensions;
- four solder-interface proxies;
- all 1.90-mm front signal traces;
- all QPL9547 visual envelopes;
- B1M load-bearing mechanics;
- stalk thickness = 1.00 mm.

Only the four B0 backside-ground rails are replaced.

## 3. Transmission-line zoning

Let v be distance downward from the radiator/stalk interface.

### Zone I — balanced throat

v = 0 to 1.50 mm.

- no backside ground;
- two same-polarization signal traces form the local balanced two-conductor field;
- RF tenon is included in this balanced signal region;
- no claim that its differential impedance is already optimized.

Nominal balanced-throat length:
L_bal = 1.50 mm.

### Zone II — ground acquisition

v = 1.50 to 4.50 mm.

Each signal branch receives a backside copper flare.

At v=1.50 mm:
- ground width tends to zero at the signal-trace centerline.

At v=4.50 mm:
- ground width reaches 3.60 mm, centered on the 1.90-mm signal trace.

The flare is linear in the u-z plane.

Nominal taper length:
L_taper = 3.00 mm.

### Zone III — established local microstrip ground

v = 4.50 to 12.00 mm.

- backside ground width = 3.60 mm;
- centered under the associated 1.90-mm signal trace;
- same copper conductivity as the B0 engineering copper.

At the nominal QPL9547 center v=7.0 mm, the ground is fully established.

## 4. Ground width correction

The earlier B0 ground occupied the full 4.00-mm RF-prong width.

Static dual-polarization preflight shows that retaining a full 4.00-mm backside rail causes one cross-polarization backside-copper intersection because the two stalk PCBs use one-sided n=-1..0-mm board references.

T1 therefore freezes:
W_gnd = 3.60 mm.

For a trace center at u=+3.0 mm:
ground full-width interval = +1.20 to +4.80 mm.

For a trace center at u=-3.0 mm:
ground full-width interval = -4.80 to -1.20 mm.

Consequences:
- 0.20-mm copper-to-prong-edge margin;
- conservative cross-polarization ground-to-ground clearance about 0.23 mm;
- no cross-polarization ground-to-stalk collision in static transformed geometry.

This is a geometry/manufacturability correction, not a final RF optimum.

## 5. Ground-taper geometry

For each branch, one continuous backside-copper solid is used.

Local u-z polygon for + branch:
- tip: (u=+3.0, v=1.50);
- outer upper corner: (u=+4.80, v=4.50);
- outer lower corner: (u=+4.80, v=12.00);
- inner lower corner: (u=+1.20, v=12.00);
- inner upper corner: (u=+1.20, v=4.50);
- back to tip.

The - branch is the exact mirror about u=0.

Backside copper thickness:
0.035 mm outside the n=-1.0-mm stalk backside.

Pol-B is the exact +90-degree rotated counterpart of Pol-A.

## 6. Electrical ownership

Hard rules:
- no ground reaches the radiator PCB;
- no ground exists on RF tenons;
- no ground exists in v<1.50 mm;
- all ground-acquisition geometry remains on the stalk backside;
- + and - branches use mirror-identical taper laws;
- Pol-A and Pol-B use exact rotationally equivalent taper laws;
- no common ground bridge is introduced between branches in the feed head;
- no stalk-ground-to-reflector bond is introduced in T1.

## 7. What T1 does not optimize

T1 does not freeze as final:
- L_bal = 1.50 mm;
- L_taper = 3.00 mm;
- W_gnd = 3.60 mm;
- MSL width = 1.90 mm;
- differential impedance;
- odd/even-mode impedance;
- QPL9547 source/noise match.

These are nominal first-cut variables for the next EM qualification stage.

## 8. Build-only acceptance

Required:
- exact T0 parent hash;
- all non-ground T0/B1M/B0 component volumes unchanged;
- old B0_BackGround count = 0;
- exactly four new T1 ground-taper solids;
- all new ground solids positive-volume;
- no ground in v<1.50 mm;
- full ground reached exactly at v=4.50 mm;
- full ground width exactly 3.60 mm;
- four taper laws mirror/rotate exactly;
- conservative transformed ground-ground collision count = 0;
- conservative transformed ground-vs-opposite-stalk collision count = 0;
- no ground reaches RF tenon or radiator;
- fresh reopen;
- zero ports;
- zero solver results.

## 9. Next stage

After T1 build PASS + human 3D review:
AR0-B1R-T2_TRANSITION_EM_QUALIFICATION

T2 will introduce ports/reference planes and quantify:
- differential return;
- odd/even-mode behavior;
- differential-to-common-mode conversion;
- branch balance;
- sensitivity to L_bal/L_taper/W_gnd.

T1 itself authorizes no solver.
