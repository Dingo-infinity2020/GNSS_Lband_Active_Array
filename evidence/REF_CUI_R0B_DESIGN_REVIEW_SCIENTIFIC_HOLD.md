# REF-CUI R0B Design Review — Execution PASS, Scientific Geometry HOLD

Status: **HOLD_REF_CUI_R0B_SCIENTIFIC_GEOMETRY_MISMATCH**

Host evidence:
- `evidence/ref_cui_r0b_h01_20260923_1341/`
- host final status was `PASS_REF_CUI_R0B_BUILD_ONLY`

That host status remains valid for:
- CST 2022.5 macro execution,
- save/close/fresh-reopen replay,
- parameter retention,
- no-port/no-solver discipline.

It is **not** accepted as a faithful Cui 2023 geometry reproduction after design-side visual comparison with the user-supplied publisher PDF.

## Primary-source comparison

Cui 2023 Figure 7(b) shows:
- four equivalent tapered dipole-arm sectors,
- exact 90-degree rotational relationship between neighboring arms,
- a central symmetric diamond/cross feed gap,
- one open-slot feature per arm,
- every open-slot feature rotates with its arm,
- a symmetric surrounding square loop.

The paper text explicitly states that the final antenna consists of two +/-45-degree dipoles surrounded by a square loop, with diamond-like material removed from the center part of each arm to form open slots.

## Problems in V01 build

### 1. Arm construction is proxy-first rather than symmetry-first

V01 creates one square `ARMS` plate and subtracts four independently defined tapered cross-gap cutters.

This can look nominally symmetric but it does not guarantee that each physical dipole arm is one canonical source-faithful polygon related to the others by exact 90-degree rotation.

### 2. Open-slot construction is not source-faithful

The build report itself labels the slots as:

`L-bend open-slot proxy`

The source Figure 7(b) shows an arm-specific open-slot geometry embedded in each tapered arm sector.

The V01 model builds four slot pairs independently in global x/y coordinates rather than constructing one source-faithful slot and rotating it with a master arm.

### 3. Taper/cutout geometry is independently authored

`TAPER1..TAPER4` are four separately authored triangles.

This is not acceptable for a geometry whose scientific requirement is exact fourfold rotational symmetry.

### 4. Visual mismatch is visible in the host top-view screenshot

The host top-view shows:
- rectangular/proxy slot features,
- non-source-like local cutout shapes,
- a radiator silhouette that does not visually match Figure 7(b) closely enough for solver validation.

### 5. Balun remains schematic

The host explicitly labels the balun metal as a schematic strip proxy.

Therefore even if the radiator were corrected, V01 is not solver-ready as an exact literature reproduction.

## Revised status

```text
CST_EXECUTION_REPLAY=PASS
SOURCE_PARAMETER_RETENTION=PASS
SCIENTIFIC_GEOMETRY_FIDELITY=HOLD
FOURFOLD_ARM_SYMMETRY_METHOD=REJECTED
OPEN_SLOT_SHAPE=REJECTED_PROXY
BALUN_POLYGON=REJECTED_PROXY_FOR_SOLVER
SOLVER_READY=NO
```

## If REF-CUI is ever rebuilt

The only acceptable reconstruction method is:

1. construct **one canonical dipole-arm sector** from Figure 7(b);
2. include its exact open-slot/cutout topology in that same canonical arm;
3. create the other three arms only by exact rotations of 90, 180, and 270 degrees;
4. perform an automated rotational Hausdorff/area/bbox symmetry audit;
5. construct the two baluns from Figure 7(c) with a similar source-locked local-coordinate method.

No independently authored Arm2/Arm3/Arm4 geometry.

## Project consequence

REF-CUI remains REFERENCE_ONLY and is stopped before solver.

The project returns operational focus to the CHARTS-inspired MAINLINE.
