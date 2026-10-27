# R1A3 Materialized Aperture / Copper Topology Design

Status: **DESIGN BASELINE — NO BUILD/SOLVER AUTHORIZATION YET**

R1A3 converts the R1A1/R1A2 topology proxies into a physically meaningful PCB-style structure while preserving the source-limited/project-owned distinction.

## 1. Key separation: mechanical topology vs RF copper topology

This distinction is mandatory.

### Mechanical PCB topology

The substrate remains one mechanically connected square board.

Use the accepted **12 disconnected through-slots**:

- 8 outer slot segments,
- 4 inner radial slot segments.

These openings pass through substrate and top copper.

The disconnected-slot pattern preserves mechanical bridges at:
- four corners,
- four side midpoints,
- the inner-to-outer bridge region.

### RF copper topology

The RF conductor is not required to remain electrically connected across those mechanical bridges.

Project-owned copper-only isolation gaps complete the electrical topology:

1. a **continuous square ring isolation gap** along the R1A1 outer-slot frame;
2. a **continuous four-arm center cross isolation gap** from the origin to the inner edge of the ring isolation gap.

This yields the intended RF concept:

- one outer passive copper ring,
- four central petal conductor regions,
- mechanically one board,
- electrically separated petal/ring regions.

This is a PROJECT_DESIGN interpretation, not an unpublished CHARTS fact.

## 2. Geometry

Reuse exactly:

- R1A1 board span = 70.714285714 mm
- outer slot-frame center span = 65.0 mm
- outer slot width = 1.428571429 mm
- R1A1 12 mechanical slot positions
- height above main ground = 57.142857143 mm
- ground/unit-cell reference = 94 mm
- R1A2 center gap width at origin = 1.20 mm
- center-gap outer width = 2.571428571 mm

Derived copper-only square-ring gap:
- centerline half-span = 32.5 mm
- gap width = 1.428571429 mm
- inner edge radius = 31.785714286 mm

Center cross copper gap:
- one master arm authored from r=0 to r=31.785714286 mm,
- taper 1.20 -> 2.571428571 mm over r=0..8.571428571 mm,
- constant 2.571428571 mm thereafter,
- other three arms only by 90-degree rotations.

## 3. Initial manufacturing material baseline

Primary low-cost build candidate:

### FR4_COST_BASELINE

Project-design nominal values for first materialized geometry:
- substrate: generic FR-4 nominal
- epsilon_r = 4.2
- tan_delta = 0.018
- substrate thickness = 1.00 mm
- copper thickness = 0.035 mm

These are **not** claimed as CHARTS source values and are not final production laminate properties.

Why this is the first candidate:
- low cost,
- readily available,
- easy routing/slot fabrication,
- compatible with a small central active PCB/hub.

Because antenna loss occurs before the LNA, FR-4 is not presumed electrically optimal. It must later be compared against a low-loss laminate.

## 4. Low-loss comparison candidate

### RO4350B_REFERENCE

Planned comparison only:
- epsilon_r ~3.48
- tan_delta ~0.0037
- nominal thickness ~0.76 mm class
- 35 um copper geometry baseline

This is a sensitivity/reference branch, not the current manufacturing winner.

## 5. R1A3 BUILD-ONLY objective

When authorized, NW shall build:

- 94 mm main ground reference,
- 70.714 mm square FR4 substrate at z = 57.143 mm,
- 12 disconnected through-slots in the substrate,
- 35 um top conductor,
- continuous copper-only square ring isolation gap,
- continuous exact-rotation four-arm center isolation gap,
- no ports,
- no LNA,
- no solver.

Expected visual/electrical topology:
- substrate remains one connected shape,
- outer copper ring is isolated from central petal copper,
- four petal copper regions are mutually isolated by the cross gap,
- center-gap geometry obeys the R1A2 exact-rotation construction rule.

## 6. Later solver comparison

Not authorized yet.

A later solver gate should compare at minimum:
- FR4_COST_BASELINE,
- RO4350B_REFERENCE,

using identical geometry and port definition.

Metrics:
- differential impedance,
- radiation efficiency,
- realized gain,
- X/Y symmetry,
- isolation,
- material-loss contribution.

The material winner is chosen only after these metrics and manufacturing cost are compared.

## 7. Stop boundary

R1A3 is currently DESIGN only.

No CST build or solver is authorized by this document alone.
