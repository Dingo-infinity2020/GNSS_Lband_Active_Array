# SIM_EXECUTION

## Protocol
Minimum compatible SimulationOps protocol: 0.2.5

## Current stage
R1E1A4A_H3A_ORTHOGONAL_STALK_ASSEMBLY_BUILD_ONLY

BUILD_AUTHORIZED: true — ONE H3A BUILD-ONLY INVOCATION
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false
CST251_AUTHORIZED: false

## Frozen source
Parent:
D:\GNSS_Lband_Active_Array\_r1e1a1_six_pitch_fr4_work\R1E1A1_P094_PITCH_BUILD_ONLY_V01.cst

SHA256:
fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e

Freeze:
docs/R1E1A4A_H3A_ORTHOGONAL_STALK_ARCHITECTURE_FREEZE_V01.md

Manifest:
execution/h3a_architecture_manifest_v01.json

## Build-only scope
- cut four radiator FR4 mortises inside the existing X/Y copper-free corridors;
- cut four backplane mortises;
- create X/Y 1.0-mm FR4 stalks with top U-notch electronics cavity and half-depth cross interlock;
- add two top and two bottom tenons per stalk;
- add explicit mechanical solder/land envelopes;
- add four radiator-backside dummy LNA envelopes;
- add first-pass corner local-ground patches and a 16-mm shield envelope with +/-X,+/-Y service egress;
- add four post-LNA route envelopes and representative stalk GCPW-class copper rails;
- add separate RF transition pad/ground/solder envelopes;
- add lower service-access envelopes only; no connector part frozen.

## Mandatory qualification
After save and fresh reopen:
1. verify shape/component inventory and frozen parameters;
2. verify port count = 0 and solver-generated results = 0;
3. execute CST built-in command `CDCheckModelIntersections`;
4. run deterministic positive-volume overlap audit against the frozen geometry/allowlist;
5. unresolved or unclassified interference => `HOLD_H3A_GEOMETRY_INTERFERENCE`.

## Stop boundary
Stop after qualified build-only for human 3D review.
No solve and no H3B/H3C continuation.
