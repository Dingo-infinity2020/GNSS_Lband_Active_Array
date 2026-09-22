# CHARTS Figure Extraction — R0.0

Status: **SOURCE EXTRACTION COMPLETE; SEMANTIC MAPPING PARTIALLY UNRESOLVED**

Primary source:
- Lau et al., "Active Planar Antenna Design for CHARTS Array", ISAP 2025
- Figure 1(a), Figure 2
- DOI 10.34385/proc.98.1571143655

## Directly visible geometry labels in Fig. 1(a)

The published figure contains three readable red dimension labels:

- **227.5 mm**
- **247.5 mm**
- **40 mm**

These values are promoted from UNKNOWN to `FIGURE_DERIVED_UNVERIFIED` as *visible labels*.

Important: the low-resolution proceeding figure does not make the semantic mapping of the two larger values sufficiently unambiguous for this project to claim:
- which one is the petal-envelope dimension,
- which one is the passive-ring dimension,
- whether they represent side length, projected length, or another referenced span.

The 40 mm label is visibly located at the central feed/electronics region and is treated as the leading candidate for the central removed/feed-region span, but remains figure-derived rather than paper-explicit.

## Paper-explicit topology constraints

The text establishes:

- square PCB layout,
- "4-petal" square antenna,
- passive ring around the antenna,
- small low-field central region may be removed for feed/electronics,
- differential balanced feed,
- 200 mm height over a ground plane.

These constraints are sufficient to define the **topological family**, but not one exact CAD geometry.

## Physical-consistency cross-check from Cui 2023

CHARTS explicitly cites Cui et al. 2023 for square-loop loading.

Cui shows that:
- a symmetric loop surrounding orthogonal dipoles creates a lower resonance,
- for the square-loop implementation, two adjacent loop sides behave approximately as a half-wave current path at the lower resonance,
- square-loop dimensions therefore provide a useful physical sanity check for any CHARTS reconstruction.

This reference is used only as a physics consistency check.
Cui dimensions are not substituted into CHARTS.

## Reconstruction candidates

Two semantic mappings are retained until a higher-resolution or additional source resolves the ambiguity.

### Candidate A
- active petal-envelope characteristic dimension: 227.5 mm
- passive-ring characteristic dimension: 247.5 mm
- central removed/feed region: 40 mm

Rationale:
- consistent with the verbal statement that the passive ring surrounds the active antenna,
- larger ring dimension outside smaller active envelope is physically plausible.

### Candidate B
- active petal-envelope characteristic dimension: 247.5 mm
- passive-ring characteristic dimension: 227.5 mm
- central removed/feed region: 40 mm

Rationale:
- retained solely because the low-resolution figure does not allow a defensible semantic assignment.

Candidate B must not be silently deleted merely because Candidate A appears more physically intuitive.

## Still unknown

The source still does not uniquely specify:
- exact polygon/curve of each petal,
- diagonal/inter-petal slit width,
- passive-ring trace width,
- exact PCB edge relative to radiator,
- ground-plane lateral size,
- substrate material and thickness,
- copper thickness.

## R0 consequence

R0 shall not claim an exact reconstruction.

The next allowed artifact is a **parameterized topology generator** that can represent both Candidate A and Candidate B and keeps the remaining unknowns explicit.

No CST solver is authorized.
