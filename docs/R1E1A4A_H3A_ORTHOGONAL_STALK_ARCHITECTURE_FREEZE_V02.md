# H3A Orthogonal PCB Stalk Architecture Freeze V0.2

Status: FROZEN FOR ONE BUILD-ONLY INVOCATION — NO SOLVE

V0.2 retains H3A V0.1 except for one mechanical correction discovered in human 3D review.

## V0.1 finding

The four top tenon centers at +/-12 mm lie inside the parent radiator INNER_N/S/E/W through-slots. Those slots remove both FR4 substrate and top copper from radius 8.57142857142 to 29.428571428542 mm with width 2.571428571426 mm.

Therefore the V0.1 top mortise was cut in already-empty FR4 and did not form a true tenon/mortise joint.

V0.1 remains immutable evidence and is not overwritten.

## V0.2 local FR4 bridge

At each of the four top tenon locations, add one local FR4 bridge inside the existing inner through-slot:
- bridge material: same FR4 as radiator substrate;
- bridge thickness: 1.0 mm, z = 57.1428571428 ... 58.1428571428 mm;
- bridge center: +/-12.0 mm on the relevant X or Y axis;
- bridge length along original slot axis: 5.50 mm;
- bridge width across original slot: 2.571428571426 mm;
- bridge is united with Substrate:FR4_BOARD.

Do NOT restore top copper in the bridge region. The accepted top-copper slot remains unchanged.

## True mortise after bridge

After the FR4 bridge is united with the parent substrate, cut the original frozen mortise:
- mortise length = 3.30 mm;
- mortise width = 1.25 mm;
- through the full 1.0-mm radiator FR4.

Resulting nominal FR4 wall:
- along slot axis: (5.50 - 3.30)/2 = 1.10 mm per end;
- across slot: (2.571428571426 - 1.25)/2 = 0.660714285713 mm per side.

The stalk tenon remains 3.0 x 1.0 x 1.0 mm, preserving 0.15-mm end clearance and 0.125-mm side clearance in the mortise.

## Electromagnetic interpretation

This is a dielectric-only mechanical bridge. It intentionally changes the local dielectric occupancy of the original inner slot but does not bridge the radiating copper.

No RF performance claim is made in build-only. The effect of the four dielectric bridges on active impedance must be evaluated in a later explicitly authorized passive RF solve.

## All other H3A V0.1 geometry remains frozen

- X/Y stalk orientation;
- 1.0-mm stalk thickness;
- half-depth stalk-to-stalk interlock;
- 17 x 17 x 7-mm electronics cavity;
- radiator-backside LNA envelopes;
- +/-9.4-mm post-LNA RF transitions;
- +/-12-mm mechanical tenons;
- bottom tenons/backplane mortises;
- shield/service routing topology.

## BUILD gate

V0.2 must satisfy SimulationOps >=0.2.6:
- fresh reopen;
- CST EM auto-intersection checking;
- CST full-model CDCheckModelIntersections;
- positive critical-clearance audit;
- zero unresolved/unclassified geometry interference;
- zero RF ports;
- no solver results.

Stop after human 3D review. No solve.
