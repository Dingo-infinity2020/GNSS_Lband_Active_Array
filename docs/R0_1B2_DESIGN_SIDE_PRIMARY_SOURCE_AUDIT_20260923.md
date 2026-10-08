# R0.1B2 Design-Side Primary-Source Audit — 2026-09-23

Status: **PRIMARY SOURCE ACCESSED; CENTER/FEED STILL UNDERDETERMINED**

## Source

Official IEICE proceedings PDF:

- Albert Wai Kit Lau et al.
- "Active Planar Antenna Design for CHARTS Array"
- ISAP 2025
- DOI: 10.34385/proc.98.1571143655
- Official PDF: https://www.ieice.org/publications/proceedings/bin/pdf_link.php?fname=1571143655.pdf&iconf=ISAP&lang=E&number=1571143655&vol=98&year=2025

H01 was blocked by publisher AWS WAF automation checks. The design side was able to access the official PDF through a separate compliant web path. H01's access HOLD remains valid host evidence; it is not treated as an error.

No copyrighted PDF or source figure is committed to this repository.

## Primary-source text confirmed

The paper explicitly states:

- the antenna is a PCB-based square "4-petal" design with a passive ring,
- field intensity is low near the center,
- a small central area can be removed to accommodate feed points/electronics,
- the antenna output is balanced/differential,
- the differential output directly feeds a pair of LNAs,
- the active implementation incorporates a small ground plane beneath the feed points,
- LNA circuits are mounted at the feed region,
- a clip-on metallic shield suppresses positive feedback/self-resonance,
- height over the main reference ground is 200 mm.

## Fig.1(a) review

The official rendering confirms visible labels:

- 227.5 mm,
- 247.5 mm,
- 40 mm.

The 40 mm dimension is clearly associated with the center region of the simulation model.

However, the publicly available figure still does not expose enough detail to determine uniquely whether 40 mm is:

- a copper-clearance / removed-area span,
- a feed-terminal separation,
- a local-ground/electronics footprint dimension,
- or another center-region construction dimension.

Therefore the project does **not** promote 40 mm to an exact feed-gap or cutout dimension.

## Fig.2(a) review

The fabricated active antenna confirms:

- center electronics physically occupy the feed region,
- the center is not represented by a simple large empty square aperture,
- the EMI shield was removed for the photograph,
- hidden copper/terminal details under the electronics are not observable well enough to reconstruct the differential feed exactly.

The photo supports the visible V0.3 large-scale topology but not a unique center-feed CAD model.

## Decision fields

```text
PRIMARY_SOURCE_ACCESS=YES_DESIGN_SIDE
FIG40_SEMANTICS=PARTIAL:CENTER_REGION_DIMENSION_EXACT_FEATURE_UNRESOLVED
DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED
CENTRAL_REMOVED_REGION=PARTIAL
LOCAL_FEED_GROUND=EXISTS_DIMENSIONS_UNRESOLVED
SOLVER_READY_EXACT_CHARTS=NO
```

## Interpretation

The blocker is now **source under-specification**, not source access.

Further retries against the same two-page ISAP paper are unlikely to resolve:
- exact terminal pads,
- differential gap,
- center copper removal,
- local-ground dimensions,
- PCB material stack.

## Recommended project action

Do not invent a falsely precise CHARTS feed.

Use the fully specified, open-access Cui 2023 square-loop dual-polarized antenna as the exact passive-EM reference for:

- CST geometry workflow,
- substrate/material handling,
- differential/dual-port setup,
- square-loop resonance reproduction,
- S-parameter / pattern post-processing.

CHARTS remains the **MAINLINE topology / active-integration inspiration**.

Cui remains **REFERENCE_ONLY** and does not replace the CHARTS-inspired mainline.

After REF-CUI validates the solver workflow, return to the CHARTS-inspired GNSS design with a **project-owned, explicitly documented feed architecture** rather than claiming an unpublished exact CHARTS feed.
