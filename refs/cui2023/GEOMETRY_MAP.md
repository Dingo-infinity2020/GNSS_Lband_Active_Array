# Cui 2023 — Source-to-Geometry Map (REF-CUI-R0A)

Status: **PASS_REF_CUI_SOURCE_GEOMETRY_FROZEN_DESIGN_SIDE**

Primary source:
- Yuehui Cui et al., IET Microwaves, Antennas & Propagation 17(5), 361–368 (2023)
- DOI 10.1049/mia2.12343
- User-supplied publisher PDF reviewed design-side at native/high-resolution rendering.
- Figure 7(a), Figure 7(b), Figure 7(c), and Table 1 are the authoritative mapping source.

No publisher PDF or raw figure is committed to this repository.

## 1. Material / architecture facts

Paper-explicit:

- two +/-45-degree polarized dipoles,
- surrounding square loop,
- diamond-like regions removed from each dipole arm to form open slots,
- two orthogonal broadband baluns,
- radiator, loop and baluns printed on single-layer Rogers 4350B,
- relative permittivity 3.48,
- substrate thickness 0.76 mm,
- radiator assembly placed above a main ground plane,
- Port 1 = +45-degree polarization,
- Port 2 = -45-degree polarization.

## 2. Figure 7(a) / global dimensions

| Symbol | Value | Exact figure mapping | Confidence | Deterministic CAD |
|---|---:|---|---|---|
| Lg | 260 mm | side length of the square main ground plane / reflector | HIGH | YES |
| H | 80 mm | vertical separation from radiator plane to main ground plane | HIGH | YES |

## 3. Figure 7(b) — planar radiator / loop top view

Coordinate convention for later CAD:
- radiator centered at x=y=0,
- Figure 7(b) viewed from +z,
- dimensions are applied with fourfold symmetry unless explicitly polarization-specific.

| Symbol | Value | Exact dimension-arrow meaning in Fig. 7(b) | Confidence | Deterministic CAD |
|---|---:|---|---|---|
| Lr | 115 mm | outside-to-outside side length of the surrounding square loop | HIGH | YES |
| Wr | 5.9 mm | in-plane conductor trace width of the surrounding square loop | HIGH | YES |
| Ld | 97 mm | side/span of the square envelope occupied by the crossed dipole radiator inside the loop | HIGH | YES |
| Ws | 2.2 mm | width of the U/open-slot cut etched in each dipole-arm region | HIGH | YES |
| Ls | 26.6 mm | length of the straight outer/horizontal leg of the open slot, as dimensioned in the upper-left quadrant | HIGH | YES |
| Wg1 | 1.7 mm | narrow inter-arm gap width at the central crossing/origin | HIGH | YES |
| Wg2 | 3.9 mm | inter-arm gap width at the outer end of the tapered centerline gap, near the dipole-envelope side | HIGH | YES |
| Wp | 8.4 mm | horizontal residual arm/patch distance between the open end of the slot and the adjacent outer-side inter-arm boundary, as drawn in upper-right quadrant | HIGH | YES |
| Lp1 | 36.3 mm | distance normal to the centerline from the center/inter-arm line to the outer horizontal leg of the open slot, shown in lower-left quadrant | HIGH | YES |
| Lp2 | 8.2 mm | short centerline-direction distance from the outer-side arm/slot boundary to the start of the diagonal inner cutout/taper, shown at left-center | HIGH | YES |
| Lp3 | 36.8 mm | length of the diagonal inner cutout/taper edge separating the central triangular copper region from the outer arm region, shown in lower-left quadrant | HIGH | YES |

### Topology interpretation

Figure 7(b) is not treated as four independent rectangular patches.

It contains:
- four tapered dipole-arm sectors arranged with fourfold symmetry,
- narrow central crossed gaps,
- a larger inter-arm gap toward the outer arm ends,
- one U/open-slot feature per arm sector,
- one continuous surrounding square loop that is electromagnetically coupled to, but not electrically attached to, the dipoles.

The square-loop lower resonance and open-slot upper resonance are paper-explicit physical mechanisms.

## 4. Figure 7(c) — broadband baluns

Figure 7(c) shows the broadband baluns for:
- Port 1 (+45-degree polarization),
- Port 2 (-45-degree polarization).

The Lb family defines longitudinal/vertical dimensions.
The Wb family defines transverse widths/offsets.

### Longitudinal dimensions

| Symbol | Value | Exact dimension-arrow meaning in Fig. 7(c) | Confidence | Deterministic CAD |
|---|---:|---|---|---|
| Lb1 | 21 mm | lower vertical feed-section length from the port reference plane to the first width/section transition | HIGH | YES |
| Lb2 | 10 mm | vertical length of the intermediate feed section between the lower and upper feed sections | HIGH | YES |
| Lb3 | 20.5 mm | upper right vertical feed-section length from the Lb2 transition to the top horizontal bend | HIGH | YES |
| Lb4 | 24.5 mm | downward length of the left open-ended stub from the top horizontal branch | HIGH | YES |
| Lb5 | 73 mm | overall main balun-board height from the port plane to the top shoulder of the main substrate | HIGH | YES |

### Transverse dimensions

| Symbol | Value | Exact dimension-arrow meaning in Fig. 7(c) | Confidence | Deterministic CAD |
|---|---:|---|---|---|
| Wb1 | 1.5 mm | width of the lower vertical feed strip adjacent to Port 2 | HIGH | YES |
| Wb2 | 0.65 mm | width of the intermediate narrow feed strip | HIGH | YES |
| Wb3 | 0.95 mm | width of the upper vertical feed strip | HIGH | YES |
| Wb4 | 13 mm | total transverse span of the upper U-shaped matching branch between its two vertical legs | HIGH | YES |
| Wb5 | 28.5 mm | lateral offset from the balun-board left edge to the central feed/slotline region, as arrowed in Port-2 view | HIGH | YES |
| Wb6 | 3.6 mm | width of the central longitudinal white slot/channel in the balun at the mid-board region | HIGH | YES |
| Wb7 | 4.8 mm | width of the right top terminal/tab adjacent to the central slot/channel | HIGH | YES |
| Wb8 | 3.6 mm | width of the left top terminal/tab adjacent to the central slot/channel | HIGH | YES |

## 5. Table-1 completeness check

All 26 Table-1 symbols are now source-mapped:

```text
Lg H
Lr Wr
Ld Ws
Ls Wg1
Wg2 Wp
Lp1 Lp2
Lp3
Lb1 Lb2 Lb3 Lb4 Lb5
Wb1 Wb2 Wb3 Wb4 Wb5 Wb6 Wb7 Wb8
```

Count:

`MAPPED_SYMBOLS_EXACT=26/26`

## 6. Physics anchors for later solver validation

Paper-explicit targets:

- square loop produces lower resonance near 0.7 GHz,
- each two neighboring square-loop sides form a folded-dipole path of length 2*Lr = 230 mm,
- open slots produce upper resonance near 1.5 GHz,
- broadband baluns improve impedance matching,
- reported impedance band: 0.69–1.52 GHz for return loss >15 dB,
- reported isolation: >35 dB.

These are **future solver-validation targets**, not build-only acceptance metrics.

## 7. Current gate

```text
SOURCE_GEOMETRY_MAPPING=PASS
MAPPED_SYMBOLS_EXACT=26/26
DETERMINISTIC_CAD_MAPPING_READY=YES
BUILD_ONLY_PERMISSION=YES
SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
```

The next permitted action is a deterministic REF-CUI CST **BUILD-ONLY** model.
