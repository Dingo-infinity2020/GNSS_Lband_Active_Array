# CHARTS Fig. 2(a) Photo Geometry Estimate — R0.1A3

Status: **FIGURE-DERIVED / UNVERIFIED / FOR TOPOLOGY BUILD ONLY**

Source:
- Lau et al., ISAP 2025, Fig. 2(a), fabricated CHARTS active planar antenna.
- The project does not store the copyrighted source photograph.
- Measurements below were made from a perspective-rectified copy for design review.

## Method

The four visible PCB corners were used to approximately rectify the board to a square.
The known/figure-labeled board-scale hypothesis was then used as the metric reference:

- board span: 247.5 mm,
- outer slot-frame characteristic span: 227.5 mm.

Because the source photograph has perspective, glare, electronics occlusion, and limited resolution,
all measurements below remain `FIGURE_DERIVED_UNVERIFIED`.

They are intended to improve topology fidelity before any solver work.

## Strong topology observations

The fabricated board contains **12 disconnected elongated slots**:

### Outer family
- 8 slots total,
- 2 horizontal/vertical segments per board side,
- a conductor bridge remains at each side midpoint,
- conductor remains at all four corners,
- outer slots do not connect to the inner radial slots.

### Inner family
- 4 radial slots total,
- one along each +/-X and +/-Y direction,
- slots stop before the central electronics/feed region,
- slots stop before the outer-slot family.

## Metric estimates from the photograph

### Board / outer slot frame

The pair of Fig. 1 labels 247.5 mm and 227.5 mm is strongly consistent with:

- square board span ≈ 247.5 mm,
- opposing outer-slot centerline span ≈ 227.5 mm,
- resulting slot-centerline inset ≈ (247.5 - 227.5)/2 = **10.0 mm per side**.

This mapping is substantially better supported by Fig. 2 than the earlier V0.1 petal/ring interpretation.

### Outer slots

Approximate photograph-derived values:

- outer slot width: **~5 mm** (uncertainty roughly +/-1 mm),
- each outer slot segment length: **~94 mm** (roughly +/-3 mm),
- conductor bridge at each side midpoint: **~18 mm** (roughly +/-3 mm),
- board-edge-to-segment-end margin along each side near corners: **~20–21 mm**.

Consistency check:

`2 * 94.25 + 18 + 2 * 20.5 ≈ 247.5 mm`.

This matches the visual segmentation of each side into:
corner bridge / slot / mid-side bridge / slot / corner bridge.

### Inner radial slots

Approximate visible values:

- inner slot width: **~9 mm** (roughly +/-1 mm),
- inner slot visible length: **~73 mm** (roughly +/-4 mm),
- visible central slot-to-slot clear span: **~60 mm** (roughly +/-5 mm),
- solid bridge between an inner-slot outer end and the nearest outer-slot aperture: **~8 mm**.

A convenient symmetric topology hypothesis is therefore:

- inner slot starts at radius ≈ 30 mm,
- inner slot ends at radius ≈ 103 mm,
- inner slot length ≈ 73 mm.

For an outer slot centered at radius 113.75 mm with ~5 mm width,
the remaining solid bridge is approximately:

`113.75 - 2.5 - 103 ≈ 8.25 mm`.

## The 40 mm Fig. 1 label

**Do not currently map the 40 mm label to the visible center-clear span.**

The photograph shows a visible center clear region closer to ~60 mm, while electronics and a local ground/feed region obscure the exact center geometry.

Therefore:

- `fig_label_40 = 40 mm` remains a real visible Fig. 1 label,
- its exact geometric meaning is now **SEMANTICS_UNRESOLVED**,
- V0.3 topology must not create a 40 mm through-hole,
- V0.3 must not force the inner-slot endpoint spacing to 40 mm.

The 40 mm feature will be resolved later from a better source or detailed active-feed geometry.

## V0.3 topology hypothesis

Use for BUILD-ONLY:

- board span = 247.5 mm,
- outer slot centerline frame span = 227.5 mm,
- outer slot width = 5 mm,
- outer slot segment length = 94.25 mm,
- mid-side conductor bridge = 18 mm,
- inner slot width = 9 mm,
- inner slot length = 73 mm,
- inner center clear span = 60 mm,
- no central through-hole,
- 12 mutually disconnected slots total.

No EM performance claim is permitted from these figure-derived values.
