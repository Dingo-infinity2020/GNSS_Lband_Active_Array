# SIM_EXECUTION

## Protocol
Minimum compatible SimulationOps protocol: 0.2.5

## Current stage
R1E1A4A_H3A_ARCHITECTURE_FROZEN_AWAIT_BUILD_AUTH

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
MATERIAL_AB_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Frozen candidate
`H3A_ORTHOGONAL_STALK_ASSEMBLY_V01`

Freeze document:
`docs/R1E1A4A_H3A_ORTHOGONAL_STALK_ARCHITECTURE_FREEZE_V01.md`

Machine-readable manifest:
`execution/h3a_architecture_manifest_v01.json`

Key frozen decisions:
- X/Y-oriented 1.0-mm FR4 vertical stalks;
- two top and two bottom tenons per stalk;
- half-depth cross-slot interlock;
- central 17 x 17 x 7-mm electronics cavity;
- radiator-backside first-stage LNA topology;
- NE/SW post-LNA branches -> X-stalk;
- NW/SE post-LNA branches -> Y-stalk;
- mechanical insertion and RF transition are separate features;
- bottom RF-ground bond remains configurable.

Mandatory build gate:
Fresh reopen -> CST Geometry Intersection Check -> zero unresolved intersections.

## Stop boundary
Await new explicit H3A BUILD authorization.
No build, solve or active-device execution is currently allowed.
