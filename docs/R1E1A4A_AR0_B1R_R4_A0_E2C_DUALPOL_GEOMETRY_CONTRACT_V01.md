# R4-A0-E2C Dual-Polarization Coexistence Geometry Contract V0.1

Status: GEOMETRY CONTRACT FROZEN — NO BUILD AUTHORIZATION  
Date: 2026-09-29

## 1. Scientific purpose

E2C is a coexistence test, not a new RF design.

Question:

**Can the already-qualified E2A and E2B landing-zone geometries exist simultaneously in the final dual-pol mechanical assembly without introducing hidden geometry/contact/interference changes?**

No RF retuning is allowed inside E2C.

## 2. Canonical parent

E2C must be generated directly from the same pre-E2 canonical parent used by E2A/E2B:

SHA256:
`fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e`

Do not merge the solved/built E2A and E2B .cst containers.

Reason:
independent construction from one canonical parent preserves exact provenance of all four prongs, drill operations and component geometry.

## 3. Frozen source lineage

Pol-A geometry authority:
- build source blob `9931736f1129624d94aee1c9e983a1eaabca5f24`
- inventory blob `e10886a4c01d9aafd55a16d8126418b7e22025fd`

Pol-B geometry authority:
- build source blob `e8cbb334173b093165c4ef05bb9d374d39ff74b4`
- inventory blob `30cde1d4b5b155c360cf5654789eb6e942dd6d6d`

The E2C source must reuse their already-qualified local geometry exactly.

## 4. Combined geometry composition

Starting parent solids: 45.

Delete the same 12 superseded pre-E2 objects:
- four B0 MSL objects;
- four B0 LNA-envelope objects;
- four T1R1 ground-taper objects.

Preserved parent solids after deletion: 33.

Add:

### Pol-A
- two E2A active v=0..3 mm stubs;
- exact E2A P landing-zone cell: 35 solids;
- exact E2A N landing-zone cell: 35 solids.

Total Pol-A additions: 72 solids.

### Pol-B
- two E2B active v=0..3 mm stubs;
- exact E2B P landing-zone cell: 35 solids;
- exact E2B N landing-zone cell: 35 solids.

Total Pol-B additions: 72 solids.

Expected final shape count:

`45 - 12 + 72 + 72 = 177 solids`

No E2A inactive-B stub and no E2B inactive-A stub is retained.

## 5. Mechanical invariants

Pol-A:
- geometry identical to E2A;
- no retune.

Pol-B:
- geometry identical to E2B;
- retain the frozen N-backside-ground half-lap notch:
  - downstream v=12..13 mm;
  - inner edge u=-1.125 mm instead of -1.0 mm;
  - removed copper footprint = 0.125 mm^2.

The notch is not released as an optimization variable.

## 6. Drill/via authority

Four physical branch prongs:
- A_P
- A_N
- B_P
- B_N

Each receives four qualified holes:
- three paddle vias;
- one C_RF ground via.

Total:
- 16 temporary drill tools, all consumed;
- 16 plated vias.

A CST-native drill-kernel reference must independently establish the Boolean volume change for all four prongs before formal production History.

Analytic cylinder volume is diagnostic only.

## 7. Raw port contract

Each branch retains six raw audit/reference planes:

`E_UP, P_IN, P_OUT, E_DN, B_VDD, B_VBIAS`

Four branches -> 24 raw ports.

Frozen numbering:

### Pol-A P branch
1 E_UP  
2 P_IN  
3 P_OUT  
4 E_DN  
5 B_VDD  
6 B_VBIAS

### Pol-A N branch
7 E_UP  
8 P_IN  
9 P_OUT  
10 E_DN  
11 B_VDD  
12 B_VBIAS

### Pol-B P branch
13 E_UP  
14 P_IN  
15 P_OUT  
16 E_DN  
17 B_VDD  
18 B_VBIAS

### Pol-B N branch
19 E_UP  
20 P_IN  
21 P_OUT  
22 E_DN  
23 B_VDD  
24 B_VBIAS

All raw ports:
- single-ended;
- 50 ohm;
- reference to the branch-local ground;
- exact local coordinates inherited from E2A/E2B.

Device planes:
`2,3,8,9,14,15,20,21`

## 8. Build qualification

Hard gates:

1. canonical parent SHA exact;
2. exact 177-solid name/component inventory;
3. all 12 superseded parent objects absent;
4. all preserved parent geometry unchanged except the four prong drill volume changes;
5. four prong drill losses match independent CST-kernel references;
6. 16 plated vias exact;
7. exact 24 ports and coordinates;
8. persistent History;
9. empty result tree;
10. fresh-reopen hash stability;
11. built-in whole-model intersection command returns normally.

## 9. Cross-pol coexistence interference authority

The central E2C question cannot be qualified only by the old 14 isolated-pol pair checks.

Required additional audit:

1. classify every E2A_* and E2B_* conductor/via solid;
2. obtain a geometric bounding envelope for every new A/B solid;
3. broad-phase every A-solid vs B-solid pair;
4. for every overlapping/touching candidate envelope, execute a qualified non-destructive intersection API or destructive `Solid.Intersect` on a complete disposable project copy;
5. require zero unclassified positive-volume A/B conductor intersection.

Any A/B galvanic contact not explicitly frozen as intentional => HOLD.

Via barrels may intersect only their own qualified branch/prong geometry.

The RF tongue/solder contacts already present in the canonical radiator-feed structure remain separately classified known seams; E2C may not create a new landing-zone-to-landing-zone contact.

## 10. Human review

After automated build PASS, human 3D review must inspect:
- all four QPL9547 landing zones present simultaneously;
- same package rotation within every branch;
- 16 vias pass through intended FR4;
- Pol-B half-lap notch remains correct;
- no A/B local-ground contact;
- no A/B package-land contact;
- no hidden shared copper bridge;
- all 24 raw ports at intended planes.

## 11. Stop boundary

This contract does not authorize build.

After source/inventory/runner preparation:
`E2C_BUILD_AWAIT_AUTH`

BUILD_AUTHORIZED = false  
SOLVE_AUTHORIZED = false
