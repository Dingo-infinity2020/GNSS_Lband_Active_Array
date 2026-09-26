# REF-CUI-R0B Construction Assumptions

Task: `REF-CUI-R0B-BUILD-ONLY-H01`
Status: build succeeded; the following are project CAD choices, not paper dimensions.

## Source-locked (PAPER_EXPLICIT) — used exactly, never tuned

All 26 Table-1 symbols (Lg, H, Lr, Wr, Ld, Ws, Ls, Wg1, Wg2, Wp, Lp1, Lp2, Lp3,
Lb1..Lb5, Wb1..Wb8) are macro parameters with the frozen values. Material
Rogers 4350B: er = 3.48, substrate thickness 0.76 mm.

## CAD construction assumptions (not source-explicit)

| Parameter | Value | Reason |
|---|---:|---|
| `copper_t` | 0.035 mm | copper proxy thickness (Table 1 omits copper thickness) |
| `ground_t` | 0.5 mm | solid-metal thickness for the reflector proxy |
| `rad_margin` | 5.0 mm | radiator dielectric lateral margin beyond the loop (not published) |
| `rad_sub_side` | Lr+2*rad_margin = 125 mm | resulting board side |
| `balun_w` | 30.0 mm | balun board lateral width (not published) |
| `balun_off` | 1.0 mm | lateral offset of each balun plane to avoid an accidental short between the two orthogonal baluns |
| `eps` | 0.01 mm | infinitesimal through-cut overlap only |

## Shape-level assumptions (material — flagged for design visual review)

1. **Open-slot shape.** The source describes a U/open slot with a straight leg
   (Ls), position (Lp1), end clearance (Wp) and a diagonal inner cutout
   (Lp2, Lp3). This build represents each arm's open slot as an **L-bend proxy**
   (two rectangular legs, `SLOTn_A`/`SLOTn_B`) plus a diagonal taper triangle
   (`TAPERn`). The exact slot bend vertices are not uniquely defined by the
   provided mapping.
2. **Arm cross gap.** A four-trapezoid tapered cross gap (Wg1 at the centre to
   Wg2 at the envelope edge) separates the four dipole-arm sectors.
3. **Balun metal pattern.** Represented as a **schematic strip proxy** built from
   the Wb1..Wb8 / Lb1..Lb5 arrows (feed stack F1→F2→F3, left stub Lb4, upper U
   branch Wb4, top tabs Wb7/Wb8). This is not claimed to be the exact published
   balun polygon.
4. **Balun orientation.** The two baluns lie in the two diagonal vertical planes
   (matching the ±45° arms), offset by `balun_off` so they do not touch.
5. **Board/ground copper thickness** is a proxy (see table); zero-thickness
   sheets were not used so that boolean cuts remain robust.
6. **Board margin** beyond the loop is not source-explicit (see table).

## Consequence

The build is deterministic and reproducible from the macro, and all source
dimensions are exact. The arm/slot/balun *shape* proxies above are the only
non-source-explicit construction choices and are flagged for design-side visual
comparison against the primary PDF (per the handoff stop rule).
