# CHARTS Figure Extraction — R0.0

Status: **TOPOLOGY REVISED AFTER FIG. 2 REVIEW**

Primary source:
- Lau et al., "Active Planar Antenna Design for CHARTS Array", ISAP 2025
- Fig. 1(a) simulation model
- Fig. 2(a) fabricated active antenna
- DOI 10.34385/proc.98.1571143655

## Figure-derived labels

Fig. 1(a) visibly includes:
- 227.5 mm
- 247.5 mm
- 40 mm

All remain `FIGURE_DERIVED_UNVERIFIED`.

The previous V0.1 mapping of 227.5/247.5 mm to separate petal/ring solids and 40 mm to a through-board center opening is rejected.

## Strong topology evidence from Fig. 2(a)

The fabricated antenna shows a continuous square PCB/aperture with **eight elongated, disconnected slots**:

- four outer slots near the perimeter,
- four inner slots arranged as the arms of a cross/"田"-like partition,
- inner slots stop before the central electronics region,
- inner slots also stop before the outer slot family,
- outer slots stop before the corners,
- the slot network is therefore **not continuous**,
- the PCB remains mechanically one piece,
- there is no large central square through-hole.

This photographic topology evidence overrides the earlier abstract four-separate-petal reconstruction.

## Candidate C — preferred topology hypothesis

For the next build-only reconstruction:

- `board_span = 247.5 mm`
- `outer_slot_frame_span = 227.5 mm`
- `center_solid_span = 40 mm`

Interpretation:
- 247.5 mm is treated as the square board/aperture outer span,
- 227.5 mm is treated as the characteristic span of the outer slot frame,
- 40 mm is treated as the retained central electronics/feed region, **not a through-hole**.

Why this is plausible:
- the paper explicitly says square PCB layout,
- 247.5 - 227.5 = 20 mm gives about 10 mm per-side outer margin,
- this matches the fabricated photograph qualitatively.

This mapping is still figure-derived and reversible; it is not promoted to `PAPER_EXPLICIT`.

## Still unknown

The short proceeding does not uniquely specify:
- slot width,
- exact inner-slot length,
- exact outer-slot length,
- exact corner bridge length,
- exact bridge between inner slots and outer slots,
- conductor stack/material,
- substrate material/thickness,
- copper thickness,
- detailed center copper/feed pattern.

These remain explicit topology placeholders or materialized-build HOLD items.

## R0 consequence

The next allowed model is V0.2:

**one continuous slotted plate + reference ground**

No ports, no dielectric, no LNA, no solver.
