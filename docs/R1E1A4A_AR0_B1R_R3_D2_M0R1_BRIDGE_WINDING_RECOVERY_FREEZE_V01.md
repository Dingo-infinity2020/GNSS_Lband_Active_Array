# AR0-B1R-R3-D2-M0R1 Bridge-Winding Recovery Freeze V0.1

Status: BUILD AUTHORIZED; SOLVE FORBIDDEN
SimulationOps: 0.2.8

## Root cause of M0 HOLD

M0 formal build created the intended lower rails correctly:
- all four lower rails had zero overlap with own FR4;
- all four lower rails had zero overlap with the opposite stalk.

However both 0.049-mm^3 common-ground bridges were fully embedded in their own FR4.

Pairwise destructive audit:
- A bridge own-FR4 intersection = 0.049 mm^3;
- B bridge own-FR4 intersection = 0.049 mm^3;
- both bridge/opposite-stalk intersections = 0.

The physical bridge location and dimensions were correct.
The defect was polygon winding:
the bridge rectangle used the opposite point orientation from the validated lower-rail polygons, reversing the CST extrusion normal.

## M0R1 correction

Fresh-build from canonical T1R1 parent.

All M0 dimensions remain frozen:
- lower rail taper v=12..13 mm, 3.60 -> 3.20 mm;
- lower rails v=13..40 mm, width 3.20 mm;
- A bridge u=-1.4..+1.4 mm, v=33.80..34.30 mm;
- B bridge u=-1.4..+1.4 mm, v=34.85..35.35 mm.

Only bridge polygon winding changes.

Validated winding convention:
upper-left -> upper-right -> lower-right -> lower-left
in local u-z coordinates, matching the existing rail polygon orientation.

No other geometry change is authorized.

## Audit correction

M0R1 must not use a shared destructive Boolean target for multiple pairs.

Each overlap pair is checked on its own temporary copy:
- 6 new-copper vs own-FR4 pairs;
- 6 new-copper vs opposite-stalk pairs.

Required:
12/12 zero positive-volume overlap.

## Products

1. full dual-pol canonical M0R1 artifact;
2. Pol-A 3-port RF fixture with the same inherited corrected 100/50/50-ohm ports.

## Stop

Build-only.
No solve.
No parameter sweep.
