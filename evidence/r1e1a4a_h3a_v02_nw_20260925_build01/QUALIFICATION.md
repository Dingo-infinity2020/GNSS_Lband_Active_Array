# H3A V0.2 FR4-Bridged Mortise — BUILD-ONLY Qualification

Canonical status: PASS_R1E1A4A_H3A_V02_FR4_BRIDGED_MORTISE_BUILD_ONLY.

One formal V0.2 build-only invocation was consumed on NW. No solver was invoked.

## Mechanical correction proved

H3A V0.1 placed the top tenons inside the parent INNER_N/S/E/W through-slots. V0.2 locally restores radiator FR4 around those locations before cutting the true mortises.

Fresh reopen measured Substrate:FR4_BOARD volume = 4518.70408162357 mm^3.
Expected volume = 4518.704081623642 mm^3.
The agreement proves the four dielectric bridges were incorporated into the radiator substrate with the intended bridge-minus-mortise volume.

The temporary H3A_RadiatorBridge component was fully consumed by Solid.Add; no bridge helper solid remains.
TopCopper remains a single unchanged-shape family and no copper bridge was added.

## Geometry / intersection gate

CST electromagnetic auto-intersection checking was enabled during build.
After fresh reopen, CST built-in CDCheckModelIntersections was executed and returned control successfully.
All critical-clearance predicates remained positive.

Additional V0.2 mortise-wall margins:
- FR4 wall along original slot axis = 1.10 mm per end;
- FR4 wall across original slot = 0.660714285713 mm per side;
- tenon-to-mortise side clearance = 0.125 mm;
- tenon-to-mortise end clearance = 0.15 mm.

## Other qualification

- 126 positive-volume solids with exact component-family counts;
- zero RF ports;
- 94-mm unit cell / broadside metadata preserved;
- no solver result-tree items or solver markers;
- no residual H3A_Tools cutting solids;
- parent evidence unchanged;
- protected artifact unchanged by fresh-reopen qualification.

## Artifact

D:\GNSS_Lband_Active_Array\_r1e1a4a_h3a_v02_build_work\R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY_V02.cst

SHA256:
9e810560fc8fc759a88d4ac5fc39067863a1e078b6f01e6e343b004891201db5

Bytes: 103548.

Artifact state: PROTECTED_IN_PLACE.

## Provenance note

The generated summary.json contains simulationops=0.2.5 because the V0.2 harness inherited a stale metadata literal from the V0.1 harness. The actual governing global protocol had already been updated to SimulationOps 0.2.6 before V0.2 authorization. The original summary is retained unchanged as execution evidence; the harness source is corrected to 0.2.6 after closeout without rerunning the build.

Stop boundary honored: no solve, no H3B continuation, no active-device integration.
