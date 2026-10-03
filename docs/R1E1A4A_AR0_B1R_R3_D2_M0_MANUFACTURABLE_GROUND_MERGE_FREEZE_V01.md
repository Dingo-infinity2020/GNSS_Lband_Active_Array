# AR0-B1R-R3-D2-M0 Manufacturable Ground-Merge Freeze V0.1

Status: BUILD AUTHORIZED; SOLVE FORBIDDEN
SimulationOps: 0.2.8

## 1. Purpose

Continue Architecture B from the corrected T1R1 geometry and replace the diagnostic unsupported D1R1-B ground bridge with a manufacturable single-layer backside ground merge that is fully supported by stalk FR4 and compatible with the existing orthogonal half-lap mechanical interlock.

This stage does not optimize impedance.
It creates the first physically manufacturable common-return topology.

## 2. Parent authority

Canonical corrected T1R1:
R1E1A4A_AR0_B1R_T1R1_GROUND_PLACEMENT_CORRECTED_BUILD_ONLY_V01.cst

SHA256:
fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e

Hard parent facts:
- Pol-A backside ground extrusion = -0.035 mm;
- Pol-B backside ground extrusion = +0.035 mm;
- all four T1R1 ground/prong volumetric overlaps = 0;
- B1M mechanical chain is retained:
  radiator mortise/tenon -> orthogonal stalks -> half-depth interlock -> reflector mortise/tenon.

## 3. Mechanical constraint from the half-lap interlock

B1M lower-body top:
z = 45.1428571428 mm, equivalent to v = 12.0 mm.

Interlock split:
z = 22.5714285714 mm.

Stalk A central slot:
z = -0.02 .. 22.5914285714 mm,
local u = -0.125 .. +1.125 mm.

Stalk B central slot:
z = 22.5514285714 .. 45.1628571428 mm,
local u = -1.125 .. +0.125 mm.

Therefore:
- A has intact center FR4 immediately ABOVE the split;
- B has intact center FR4 immediately BELOW the split;
- there is no common z-band near the split where both stalks simultaneously have intact center FR4.

The product merge must respect this rather than bridging an air slot.

## 4. Lower ground rails

The existing T1R1 feed-head grounds end at v = 12.0 mm with width 3.60 mm.

For each branch add a supported backside lower-ground extension.

Transition:
- v = 12.0 .. 13.0 mm;
- width tapers symmetrically from 3.60 mm to 3.20 mm.

Established lower rail:
- v = 13.0 .. 40.0 mm;
- width = 3.20 mm;
- centered at u = +3.0 / -3.0 mm.

Thus lower-rail intervals are:
- positive: u = +1.40 .. +4.60 mm;
- negative: u = -4.60 .. -1.40 mm.

Reason for 3.20-mm lower width:
the closest half-lap slot edge is |u| = 1.125 mm, leaving a minimum planar copper-to-slot clearance:

0.275 mm.

This is a manufacturability/mechanical-clearance choice, not an RF optimum.

## 5. Manufacturable common-ground merge

No via is introduced.
No copper spans unsupported air.
No copper crosses through the orthogonal stalk.

### Pol-A bridge

A central FR4 is intact above the split.

Bridge:
- local u = -1.40 .. +1.40 mm;
- v = 33.80 .. 34.30 mm;
- local backside copper only;
- thickness = 0.035 mm;
- B0_COPPER.

The A slot starts below at v ~= 34.55143 mm, so nominal longitudinal bridge-to-slot-end clearance is about 0.25143 mm.

### Pol-B bridge

B central FR4 is intact below the split.

Bridge:
- local u = -1.40 .. +1.40 mm;
- v = 34.85 .. 35.35 mm;
- local backside copper only;
- thickness = 0.035 mm;
- B0_COPPER.

The B slot ends above at v ~= 34.59143 mm, so nominal longitudinal bridge-to-slot-end clearance is about 0.25857 mm.

Each bridge face-connects the two 3.20-mm lower rails.

## 6. Why A/B bridge heights differ

The difference is imposed by the physical complementary half-lap interlock.

The two polarizations remain branch-symmetric internally, but their common-ground merge planes are separated by about 1.05 mm in v.

This is explicitly NOT claimed to be electromagnetically negligible.

A later passive qualification must compare the two polarizations or equivalent fixtures and decide whether this mechanical asymmetry is acceptable.

We do not hide this compromise by forcing a geometrically impossible C4-symmetric bridge.

## 7. Electrical ownership

Hard rules:
- radiator copper unchanged;
- RF tenons/tongues unchanged;
- T1R1 balanced throat/taper unchanged;
- no common ground in the feed/LNA head;
- lower rail and bridge exist only on stalk backside;
- no stalk ground bonds to reflector in M0;
- no via;
- no post-LNA signal routing added;
- no actual QPL9547 footprint/pads/bias network added.

## 8. D2-M0 build products

Product 1:
full dual-pol canonical
R1E1A4A_AR0_B1R_R3_D2_M0_MANUFACTURABLE_GROUND_MERGE_BUILD_ONLY_V01.cst

Product 2:
single-Pol-A diagnostic fixture
R1E1A4A_AR0_B1R_R3_D2_M0A_RF_FIXTURE_BUILD_ONLY_V01.cst

The fixture retains:
- corrected Pol-A T1R1 six-solid transition;
- Pol-A lower-ground extensions and supported common-ground bridge;
- P1 = 100-ohm differential at v=0;
- P2/P3 = 50-ohm signal-to-ground at v=10 using corrected conductor-interface endpoints.

The fixture is build-only in D2-M0.

## 9. Build acceptance

Canonical full dual-pol:
- exact T1R1 parent SHA;
- all parent non-D2 geometry/material/volume preserved;
- 4 lower rail-extension solids;
- 2 supported common-ground bridge solids;
- A/B corrected backside extrusion signs retained;
- all D2 copper positive-volume;
- every D2 copper solid has zero positive-volume overlap with its own FR4;
- conservative new-copper-to-interlock clearance >= 0.25 mm;
- no analytically predicted opposite-stalk collision;
- no ground/radiator contact;
- no ground/reflector contact;
- no via;
- fresh reopen;
- zero RF ports;
- zero result tree.

D2-M0A fixture:
- corrected Pol-A transition retained exactly;
- Pol-A M0 lower-ground extension/bridge retained exactly;
- exactly 3 ports;
- fresh reopen;
- zero result tree;
- zero solver invocation.

## 10. Human review

Mandatory:
1. full dual-pol stalk assembly with new lower-ground copper only highlighted;
2. A interlock/bridge region;
3. B interlock/bridge region;
4. orthogonal stalk crossing with copper visible;
5. top feed/LNA head to prove it is unchanged;
6. bottom tenon/reflector region to prove no ground bond was introduced.

Confirm:
- both bridges sit on real FR4;
- neither bridge spans the half-lap slot;
- 3.20-mm lower rails do not clip slot edges;
- no bridge intersects the orthogonal board;
- ordinary PCB manufacturing is plausible.

## 11. Stop boundary

BUILD-ONLY only.

After PASS:
human/analytic review
-> separate D2 solve authorization.

No solve and no matching sweep are authorized by this freeze.
