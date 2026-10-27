# H3A Orthogonal PCB Stalk Assembly V0.1 — BUILD-ONLY Qualification

Canonical status: `PASS_R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY`.

One formal build-only invocation was consumed on NW. No solver was invoked.

Fresh-reopen qualification:
- 126 positive-volume solids with exact component-family counts;
- zero RF ports;
- 94-mm unit cell and broadside metadata preserved;
- no residual `H3A_Tools` cutting solids;
- no solver markers/result-tree items;
- parent evidence unchanged;
- artifact hash unchanged by fresh-reopen qualification.

## Geometry-interference gate

SimulationOps 0.2.5 requirements were applied.

During build, CST electromagnetic auto-intersection checking was enabled with `Solid.SetAutoIntersectionCheckElMag "True"`.

After fresh reopen, the CST built-in full-model intersection command `CDCheckModelIntersections` was actually executed and returned control successfully. CST 2022.5's scripting interface does not expose the interactive intersection list as a structured return value, so this command-execution evidence is paired with deterministic frozen-geometry clearance predicates.

All audited positive clearances passed. Minimum reported margins include:
- tenon-to-mortise side clearance: 0.125 mm;
- interlock side clearance: 0.125 mm;
- route start beyond LNA package corner: 0.2358 mm;
- route-to-shield-egress clearance: 0.2516 mm;
- mechanical-to-RF top-feature gap: 0.400 mm;
- shield-to-stalk cavity side clearance: 0.500 mm;
- mortise-to-existing copper-corridor side clearance: 0.6607 mm.

No unexpected positive-volume interference was identified by the scripted qualification predicates, and the CST built-in command completed without aborting the qualification session. Human 3D review is still required before any RF solve, consistent with the stop boundary.

## Artifact

`D:\GNSS_Lband_Active_Array\_r1e1a4a_h3a_build_work\R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY_V01.cst`

SHA256:
`3d15d5bf36c0d6f60a4d46d48fa5197818559890e27e0950556a0f14e2309043`

Bytes: `100309`

Artifact state: PROTECTED_IN_PLACE.

No H3A solve, active transistor integration, H3B continuation or H1R recovery was performed.
