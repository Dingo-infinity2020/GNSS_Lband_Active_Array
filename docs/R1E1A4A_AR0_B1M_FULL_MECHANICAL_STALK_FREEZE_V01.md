# AR0-B1M Full Mechanical Stalk Integration Freeze V0.1

Status: FROZEN FOR AUTHORIZED BUILD-ONLY
SimulationOps: 0.2.8

## 1. Purpose

B1M turns the proven B0G feed-head into the first complete load-bearing element.

The final mechanical chain is frozen as:

radiator PCB
-> radiator/stalk mortise-tenon
-> two mutually orthogonal vertical stalk PCBs
-> complementary half-depth stalk/stalk interlock
-> stalk/reflector mortise-tenon
-> reflector plane.

B1M is a mechanical integration gate. It does not qualify RF matching.

## 2. Parent authority

Protected B0G artifact:
R1E1A4A_AR0_B0G_FEED_HEAD_BUILD_ONLY_V01.cst

SHA256:
6b027162dd93d8613a0943df0fd96d6bf65d6721893e49c8d8bdc17f8f5eb698

B0G status:
PASS_R1E1A4A_AR0_B0G_FEED_HEAD_BUILD_ONLY

The following B0G geometry is immutable in B1M:
- four signal-only feedthroughs;
- four front-face 1.90-mm first-cut signal traces;
- four fork prongs;
- 2.0-mm central feed-head clear slot;
- four QPL9547 visual envelopes;
- 3.0-mm no-ground setback and existing B0G ground rails.

Important: the B0G abrupt ground onset is a build placeholder only. It is NOT RF-qualified and must be replaced/optimized in the later balanced-throat/ground-acquisition stage before any passive EM solve.

## 3. Coordinate convention

Use the B0 polarization coordinates.

For each stalk:
- local u = polarization axis in the radiator plane;
- local n = board-thickness normal;
- z = global vertical coordinate.

Radiator/stalk interface:
z = 57.1428571428 mm.

Reflector upper surface:
z = 0 mm.

Stalk dielectric:
local n = -1.0 to 0.0 mm.

## 4. Full stalk lower body

For each polarization, add a physical FR4 lower body:

- local u = -15 to +15 mm;
- local n = -1.0 to 0.0 mm;
- z = 0 to 45.1428571428 mm.

This body face-joins the B0G fork-head at z=45.1428571428 mm.

No lower-body RF copper is frozen by B1M.

The region below the LNA/feed head is therefore a mechanical carrier in B1M. Broad ground extension, post-LNA routing, bias and service routing remain deferred.

## 5. Upper mechanical rails

The RF fork alone is not the structural attachment to the radiator.

Each stalk receives two outer FR4 mechanical rails:
- rail centers local u = +/-12 mm;
- rail width = 3.0 mm;
- local n = -1.0 to 0.0 mm;
- z = 45.1428571428 to 57.1428571428 mm.

Therefore the upper structure contains:
- two inner RF prongs at |u| = 1..5 mm;
- a clear center slot;
- a clear RF/mechanical separation region;
- two outer mechanical rails at |u| = 10.5..13.5 mm.

No copper or solder land is added to the upper mechanical rails in B1M.

## 6. Radiator/stalk mortise-tenon

Each outer rail continues into one FR4 tenon through the radiator PCB.

Per stalk:
- two top tenons;
- local u = [-13.5,-10.5] and [10.5,13.5] mm;
- local n = -1.0 to 0.0 mm;
- z = 57.1428571428 to 58.1428571428 mm.

Each radiator mortise uses nominal assembly clearance:
- local u width = 3.30 mm;
- local n width = 1.25 mm;
- through the full 1.0-mm radiator substrate.

A matching copper-clearance window is cut in the top radiator copper over each mortise.

Hard rule:
the FR4 tenon is mechanically connected to the radiator board but is NOT galvanically connected to radiator copper.

This copper clearance is a deliberate mechanical integration modification and must later receive a passive-EM perturbation test. B1M itself does not claim the slots are electromagnetically harmless.

## 7. Stalk/stalk orthogonal interlock

The two full stalks remain mutually perpendicular.

The interlock is below the B0 feed/LNA head.

Let:
- lower-body top = 45.1428571428 mm;
- interlock split plane = 22.5714285714 mm.

Stalk A:
- central slot local |u| <= 0.625 mm;
- cut from z=-0.02 to z=22.5914285714 mm.

Stalk B:
- central slot local |u| <= 0.625 mm;
- cut from z=22.5514285714 to z=45.1628571428 mm.

The 1.25-mm slot width provides 0.25-mm total clearance around the 1.0-mm other-board thickness.

The two cuts overlap by 0.04 mm in z to avoid a knife-edge interference at the split plane.

No copper bridge across this interlock is authorized in B1M.

## 8. Stalk/reflector mortise-tenon

Each stalk also receives two lower FR4 tenons:
- local u = [-13.5,-10.5] and [10.5,13.5] mm;
- local n = -1.0 to 0.0 mm;
- z = -0.5 to 0 mm.

The existing reflector/ground-reference metal receives matching slots:
- local u width = 3.30 mm;
- local n width = 1.25 mm;
- through z=-0.52 to +0.02 mm.

B1M treats this as a mechanical slot only.

No stalk-ground-to-reflector galvanic bond is implied. That electrical decision is deferred.

## 9. Mechanical/RF separation

Hard keepout rules:
- no mechanical tenon/mortise enters local |u| < 10.35 mm at the radiator interface;
- no mechanical metal/solder is added in the feed head;
- no mechanical feature may intersect the four signal feedthroughs, signal traces, B0 ground rails or QPL9547 envelopes;
- no lower-body interlock cut may enter the B0 feed head;
- the B0 signal/ground geometry is not modified by B1M.

## 10. RF transition status

The pre-LNA feed is now formally partitioned into:

Zone I — balanced throat:
radiator terminal to future ground-acquisition region.

Zone II — symmetric ground-acquisition transition:
future gradual conversion from balanced two-conductor fields to two ground-referenced microstrip modes.

Zone III — twin microstrip / twin LNA.

B1M does NOT freeze the final Zone-I/II dimensions.

The B0G 3-mm abrupt ground setback remains a geometry placeholder only.

Next RF stage after B1M mechanical acceptance:
AR0-B1R_BALANCED_TO_TWIN_MSL_TRANSITION_FREEZE

That stage must replace the abrupt ground onset with an explicitly modeled symmetric taper before any integrated passive solve.

## 11. B1M build-only acceptance

Required:
- parent B0G SHA exact;
- B0G feed-head component inventory preserved;
- exactly two full lower bodies;
- exactly four upper mechanical rails;
- exactly four top tenons;
- exactly four bottom tenons;
- four radiator mortises/copper clearances;
- four reflector mortises;
- complementary A/B half-depth interlock;
- top and bottom tenons face-connected to their stalk bodies/rails;
- no unexplained positive-volume cross-polarization collision;
- no mechanical feature intersects B0 signal/LNA/ground geometry;
- fresh reopen;
- zero RF ports;
- zero solver results.

## 12. Human review

Mandatory views:
1. radiator + top mortise clearances;
2. top tenons / outer rails only;
3. B0 RF fork-head only;
4. full stalk FR4 with center interlock;
5. reflector slots / bottom tenons;
6. full dual-pol assembly.

Review questions:
- does the assembly now look like a real support structure?
- are RF prongs clearly separated from mechanical rails?
- do the two vertical boards genuinely interlock rather than overlap?
- are top tenons mechanically plausible without touching radiator copper?
- are bottom tenons visibly seated through the reflector slots?
- is the B0 feed/LNA region untouched?

## 13. Route after B1M

B1M PASS + human review
-> B1R balanced-throat / ground-acquisition transition design
-> transition coupon / mode-conversion qualification
-> B2 passive integrated element
-> LNA package/bias integration
-> realistic periodic active-impedance atlas.

No solver is authorized by B1M.
