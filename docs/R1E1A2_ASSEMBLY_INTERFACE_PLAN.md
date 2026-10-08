# R1E1A2 Assembly Interface Plan

Status: DESIGN ONLY — NO BUILD OR SOLVER AUTHORIZATION

## Scope

The mechanical support cannot be qualified independently of the joints that attach it to the radiator PCB and to the ground/backplane. R1E1A2 therefore treats the following as one assembly:

`radiator PCB -> upper joint -> support body -> lower joint -> ground/backplane`

The assembly must control both EM perturbation and the geometric state of the antenna.

Primary mechanical/RF variables:
- support material and cross-section;
- support position and symmetry;
- upper attachment to radiator PCB;
- lower attachment to ground/backplane;
- any holes, pads, screws, clips or bonded areas;
- bond-line material and thickness;
- stand-off height, tilt, warp and lateral registration.

## Preferred baseline concept — A1 bonded dielectric/foam posts

First candidate for evaluation:
- four symmetric minimal-section low-density RF-foam or low-permittivity dielectric posts;
- no metal hardware above the ground plane;
- no through-holes in the radiator PCB for the first candidate;
- small, repeatable adhesive pads at the PCB/support interface;
- small adhesive pads or dielectric sockets at the support/ground interface.

Reason:
- preserves the existing radiator copper/substrate geometry;
- avoids conductive vertical parasitic structures;
- avoids drilling the qualified R1A3/R1E1 radiator geometry;
- gives a clean EM reference for deciding whether a serviceable fastener architecture is worth the added complexity.

Adhesive is not assumed transparent. Exact adhesive chemistry, epsilon_r, loss tangent and bond-line thickness must be frozen from a datasheet or measurement before a production solve.

## Serviceable alternative — A2 dielectric standoff + dielectric fastener

Second candidate only if removability/rework is important:
- PEEK/other qualified low-loss dielectric standoff;
- dielectric screw or captive feature at the radiator side;
- any radiator-PCB mounting hole becomes explicit antenna geometry and must be modelled;
- metal hardware, if used to retain the lower end, should remain at or below the conducting ground/backplane surface and must not project upward as a free conductor.

This architecture is mechanically attractive but electromagnetically more invasive than the bonded baseline because it may require holes, local pads and larger dielectric volume.

Nylon may be useful for prototypes but should not be frozen merely for convenience; moisture uptake and dielectric-property stability must be considered before release.

## Explicitly non-preferred first-pass joints

### Soldered metal legs / soldered metal standoffs
Not a default support method. A soldered conductor extending from the radiator PCB toward the ground plane is an RF structure, not a neutral mechanical connection. Use only if the connection is intentionally part of the RF/ground architecture and is fully modelled.

### Exposed aluminium/brass screws or tubes above the ground plane
High-risk. Their electrical length, grounding state and symmetry must be treated as antenna parameters.

### Edge clips / peripheral frame
Not assumed benign because the periodic fringing fields extend around the board edge and toward the unit-cell boundary. Use only after explicit EM qualification.

### Large-area adhesive or full-area foam block
Mechanically simple, but it increases dielectric volume in the near field. Prefer small symmetric bonded regions first; a full block is a separate candidate, not the default meaning of 'foam support'.

## Geometric tolerance is part of the RF design

The support assembly defines the radiator-to-ground spacing. Therefore R1E1A2 must later freeze and audit:
- nominal support height;
- board-to-ground parallelism / tilt;
- board warp or sag;
- X/Y lateral registration;
- rotational registration;
- compression or creep of foam/adhesive.

The existing approximately 57.143-mm height is an EM baseline, not yet a manufacturing tolerance specification.

A later tolerance study may perturb height/tilt after the nominal support is selected. Do not silently absorb assembly tolerance into the nominal geometry.

## Decision sequence

1. Freeze two mechanically credible assembly candidates: bonded low-density support baseline and one serviceable dielectric-fastener alternative.
2. Freeze actual support and adhesive material properties plus bond-line geometry.
3. Build-only P094 variants after separate authorization.
4. Run a small support/joint sensitivity gate only after separate solver authorization.
5. If one assembly is EM-benign and mechanically credible, freeze it before propagating support geometry to the six pitch candidates.

## Current stop

DESIGN ONLY.
No CST build.
No solver.
No fastener/material winner is frozen yet.
