# R1 CHARTS-Inspired GNSS Derivative — Design Plan

Status: **DESIGN-SIDE PLANNING / NO SOLVER**

## Mission

Create the first project-owned L-band derivative of the accepted CHARTS-inspired visible topology for:

- 1.15–1.65 GHz continuous coverage,
- two independent linear polarizations,
- feed-point active frontend compatibility,
- later digital RHCP/LHCP synthesis,
- later array periodic/finite validation,
- low-cost manufacturability.

## R1A — Geometry scaling baseline

Start from the accepted V0.3 CHARTS visible topology.

Initial electromagnetic scale:
- source nominal center ~400 MHz,
- project nominal center ~1.40 GHz,
- first-pass geometric scale factor = 400/1400 = 0.285714.

Thus the source 300–500 MHz reference maps approximately to:

- 1.05–1.75 GHz.

This intentionally contains the required 1.15–1.65 GHz band with margin.

R1A must not optimize dimensions yet.

It asks only:

> Is the directly scaled visible topology a geometrically plausible L-band starting point?

## R1B — Project-owned balanced feed

Because the CHARTS source does not expose the exact center feed, R1 explicitly owns this geometry.

First passive-feed model:
- one ideal balanced/differential terminal pair per linear polarization,
- X and Y geometrically related by exact 90-degree rotation,
- no passive 90-degree hybrid,
- no LNA in the first passive geometry gate.

Critical requirement:
- define one polarization feed geometry,
- generate the second only through exact 90-degree rotation,
- automated symmetry audit required.

## R1C — Material trade study

Material is a design variable, not a guessed CHARTS fact.

Candidate classes:
- low-cost FR-4 baseline,
- low-loss hydrocarbon/ceramic PCB baseline (e.g. Rogers 4350B-class),
- minimal-dielectric / supported copper option if mechanically practical.

Evaluation later includes:
- radiation efficiency,
- pre-LNA loss contribution,
- cost,
- fabrication tolerance.

No material winner is frozen in R1A.

## R1D — Passive isolated-element solver

Only after build-only geometry and feed symmetry pass.

Targets:
- differential impedance across 1.15–1.65 GHz,
- X/Y equality,
- isolation,
- broadside pattern,
- sensitivity to scale factor / slot dimensions.

No active-array claim yet.

## R1E — Periodic array

Mandatory before active electronics are frozen:
- pitch exploration ~88–100 mm,
- active differential impedance versus scan,
- embedded pattern,
- scan to at least 60 degrees from zenith,
- extended 60–75 degree region if feasible.

## Active electronics remain later

QPL9547 stays a reference candidate.

No LNA is integrated until:
- passive geometry,
- X/Y symmetry,
- array active-impedance locus,
are understood well enough to define the LNA source environment.
