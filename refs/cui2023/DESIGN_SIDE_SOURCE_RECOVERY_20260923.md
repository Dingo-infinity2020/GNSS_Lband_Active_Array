# REF-CUI Design-Side Source Recovery — 2026-09-23

Status: **PARTIAL_MAPPING / NO_CAD_AUTHORIZATION**

## Context

H01 returned `HOLD_REF_CUI_FIGURE_ACCESS_FAILED` because Wiley/IET pages are
blocked on the execution host by Cloudflare/WAF. That HOLD remains valid.

The design side can access the Wiley full-text HTML, the Figure 7(a) indexed
image, and an independent ResearchGate transcription of the publisher full text.

## Source-confirmed facts

From Cui et al. 2023:

- two +/-45-degree polarized dipoles are surrounded by a square loop;
- diamond-like material is removed from the center part of each dipole arm to
  create open slots;
- the two polarizations are fed by orthogonal broadband baluns;
- dipoles, loop and baluns are printed on single-layer Rogers 4350B;
- er = 3.48;
- substrate thickness = 0.76 mm;
- the assembly is placed above a main ground plane for unidirectional radiation;
- reported impedance band is 0.69-1.52 GHz for RL > 15 dB;
- measured isolation is reported >35 dB.

## Exact mappings recovered

### Lg = 260 mm

Mapped to the side length of the main square ground plane / reflector for the
single element.

Evidence:
- Figure 7(a) visibly places `Lg` along the ground-plane edge.
- In Figure 16, `Lg` and `Wg` are again used as reflector dimensions for the
  four-element array, reinforcing the symbol family.

Confidence: **HIGH**

### H = 80 mm

Mapped to the vertical radiator-to-main-ground separation.

Evidence:
- Figure 7(a) visibly labels `H` as the vertical spacing.
- Table 1 gives 80 mm.

Confidence: **HIGH**

### Lr = 115 mm

Mapped to one side length of the surrounding square loop.

Evidence:
- Section 3.2 explicitly states that every two neighboring sides of the square
  loop form a folded-dipole path of length `2 x Lr = 2 x 115 mm`.

Confidence: **HIGH**

## Partial family mappings

The following are useful but are not yet exact enough for deterministic CAD:

- `Wr`: square-loop conductor-width interpretation is likely, but Figure 7(b)
  label endpoints have not been independently recovered.
- `Ld`: dipole/radiator characteristic length family.
- `Ws, Ls`: open-slot dimension family.
- `Wg1, Wg2, Wp, Lp1, Lp2, Lp3`: radiator/feed-center geometry family.
- `Lb1..Lb5, Wb1..Wb8`: broadband-balun dimensions. Family assignment is
  strong because Figure 7(c) explicitly details the broadband baluns, but exact
  segment-by-segment mapping is still unavailable.

## 2014 precursor cross-check

The 2023 paper explicitly starts from Cui et al. 2014,
"A Broadband Dual-Polarized Planar Antenna for 2G/3G/LTE Base Stations."

Publicly indexed Figure 1 of that precursor confirms the inherited architecture:

- two crossed bow-tie dipoles,
- front/back metal regions,
- microstrip stubs,
- metal/connecting holes,
- coaxial feeds,
- reflector below.

This helps interpret the architecture but is **not** used to assign 2023 Table-1
symbols unless an exact label correspondence is demonstrated.

## Current gate

```text
MAPPED_SYMBOLS_EXACT=3/26
DETERMINISTIC_FULL_CAD_READY=NO
SOLVER_READY=NO
```

Do not make H01 retry Cloudflare.

Next useful evidence would be one of:
- Figure 7(b) at sufficient resolution,
- Figure 7(c) at sufficient resolution,
- the open-access PDF supplied locally by a human/user,
- an author/official figure export.

Until then, keep REF-CUI in source-mapping HOLD rather than filling the remaining
23 mappings from naming conventions.
