# AR0-B1R-T0 RF-Tenon Solder Interface Freeze V0.1

Status: FROZEN FOR AUTHORIZED BUILD-ONLY
SimulationOps: 0.2.8

## 1. Purpose

Replace the B0/B1 signal-feedthrough-via interface with a directly solderable RF tenon.

This stage changes only the radiator-to-stalk signal joint.
The B1M mechanical support structure remains authoritative and unchanged.

No RF optimization is claimed.

## 2. Parent

Parent artifact:
R1E1A4A_AR0_B1M_FULL_MECHANICAL_STALK_BUILD_ONLY_V01.cst

SHA256:
6b2e3edc230b54eef54bdd427e8585a9fee1f0ef0235c747aa1b0ef6571b1dbe

Parent status:
PASS_R1E1A4A_AR0_B1M_FULL_MECHANICAL_STALK_BUILD_ONLY

## 3. Stalk thickness

The current stalk FR4 thickness is 1.00 mm.

B1R-T0 does not change it.

A future 0.80-mm stalk may be evaluated as a separate electro-mechanical sensitivity case, because stalk thickness changes:
- microstrip impedance for a fixed width;
- ground coupling;
- tenon strength;
- interlock clearance;
- assembly stiffness.

Thickness is therefore not bundled into the RF-tenon interface change.

## 4. RF tenon geometry

Per radiator terminal:
- one FR4 RF tenon;
- center local u = +3.0 mm or -3.0 mm;
- width along local u = 2.20 mm;
- stalk thickness local n = -1.0 to 0.0 mm;
- bottom = radiator/stalk interface z=57.1428571428 mm;
- top = 58.7428571428 mm.

The tenon therefore passes through the 1.0-mm radiator PCB and protrudes 0.60 mm above the radiator substrate top.

The top copper thickness is 0.035 mm, so the tenon remains approximately 0.565 mm above the top-copper surface.

Four tenons total.

## 5. Radiator RF mortise

Per RF tenon, cut a signal mortise centered on the terminal:
- width local u = 2.50 mm;
- local n = -1.125 to +0.125 mm;
- through the radiator substrate;
- matching clearance is cut through radiator top copper where the FR4 tenon passes.

Nominal clearance:
- 0.15 mm each side along u;
- 0.125 mm each side through board thickness.

The four RF mortises are distinct from the outer load-bearing B1M mechanical mortises.

## 6. Stalk signal copper

The existing B0 1.90-mm signal trace remains unchanged below z=57.1428571428 mm.

At each terminal, add a vertical copper extension on the RF tenon:
- width = 1.90 mm;
- local n = 0 to +0.035 mm;
- z = 57.1428571428 to 58.7428571428 mm;
- material = B0_COPPER.

The copper extension face-connects to the existing MSL at the stalk/radiator interface.

No backside ground is added to the tenon.

## 7. Solder interface

The old B0 plated feedthrough barrel is removed.

A first-cut solder bridge is represented explicitly between:
- the exposed stalk-tenon copper;
- the edge of the radiator top copper surrounding the RF mortise.

Per terminal the solder bridge runs toward the radiator arm, not across the stalk-thickness direction.

For the +u terminal:
- local u = +3.95 to +4.25 mm.

For the -u terminal:
- local u = -4.25 to -3.95 mm.

For both:
- local n = +0.035 to +0.125 mm;
- z = 58.1428571428 to 58.4278571428 mm;
- material = engineering solder proxy, sigma=7e6 S/m.

Thus the bridge spans the 0.30-mm clearance from the 1.90-mm vertical tongue-copper edge to the outward edge of the 2.50-mm radiator mortise.

This is a manufacturability proxy, not a final solder-fillet shape.

The exposed vertical stalk copper above the radiator remains visible and solderable.

## 8. Electrical ownership

Hard rules:
- one radiator terminal connects only to its corresponding RF-tenon copper;
- no RF-tenon ground exists;
- no stalk backside ground reaches the radiator PCB;
- no mechanical tenon is used as an electrical return;
- no PTH signal feedthrough remains;
- no radiator arm is redefined as ground.

## 9. Mechanical ownership

B1M remains unchanged:
- outer radiator/stalk load-bearing tenons stay at local u≈±12 mm;
- X/Y stalk half-depth interlock remains unchanged;
- bottom stalk/reflector tenons remain unchanged.

RF tenons are not primary load-bearing members.
They are signal/solder alignment features.

## 10. Static pre-build checks

The frozen first-cut geometry has been checked analytically:
- four 2.20-mm RF tenons do not cross each other between polarizations;
- four 2.50-mm RF mortises do not cross each other;
- RF tenons remain inside the B0 fork-prong u extent;
- no RF-tenon ground exists;
- outer B1M mechanical tenons remain well separated.

## 11. Build-only acceptance

Required:
- exact B1M parent hash;
- B1M mechanical component volumes unchanged;
- B0 MSL, B0 ground, B0 LNA-envelope volumes unchanged;
- B0 signal-feedthrough component absent after build;
- exactly four RF tenons;
- exactly four RF-tenon copper extensions;
- exactly four solder proxies;
- exactly four RF mortise openings in radiator substrate/top copper;
- all new solids positive-volume;
- no new tool solids remain;
- no cross-pol RF-tenon collision;
- no RF-tenon/ground intersection;
- fresh reopen;
- zero ports;
- zero solver results.

## 12. Status of RF matching

B1R-T0 does not qualify impedance matching.

The region remains:
balanced radiator
-> RF tenon / solder joint
-> short balanced throat
-> future symmetric ground-acquisition taper
-> twin MSL
-> twin LNA.

The existing abrupt B0 3-mm ground onset remains a placeholder.

Next RF stage after geometry acceptance:
AR0-B1R-T1_BALANCED_GROUND_ACQUISITION_TRANSITION.

No solver is authorized here.
