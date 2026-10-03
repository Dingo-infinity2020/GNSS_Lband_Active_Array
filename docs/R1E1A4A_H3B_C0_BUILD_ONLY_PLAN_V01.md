# H3B-C0 Complete Passive Unit Build-Only Plan V0.1

Status: FROZEN PLAN — BUILD NOT AUTHORIZED

Authority: docs/R1E1A4A_H3B_COMPLETE_PASSIVE_ROUTE_FREEZE_V01.md

## Formal products

Build two fresh P094 models from the same immutable H3A V0.2 authority:

A. H3A_MECH_ONLY_PHYSICALIZED_BUILD_ONLY_V01.cst
B. H3B_COMPLETE_PASSIVE_V1_BUILD_ONLY_V01.cst

A is the later I01 A/B reference.
B differs from A only by four frozen T01-A local integration slices.

## Builder behavior

The builder shall:
1. verify parent hash;
2. reconstruct/clone the accepted H3A V0.2 geometry deterministically;
3. strip visual-surrogate solids from formal EM geometry while preserving keepout coordinates in evidence;
4. strip H3A schematic RF placeholder components;
5. convert real physical conductor/solder families to the frozen finite-conductivity models;
6. write A and fresh-reopen/audit it;
7. derive B from the same pre-T01 authority;
8. insert four local T01-A integration slices from the replacement-map transforms;
9. write B and fresh-reopen/audit it;
10. stop.

No port/load/solver command may appear in the C0 builder.

## Static evidence

Required:
- source/parent hashes;
- generated macro/source hash;
- component-family inventory;
- material-family inventory;
- visual-surrogate absence;
- RF-placeholder absence;
- T01 branch-center / face / transform manifest;
- 3-mm integration-plane coordinates;
- critical mechanical clearances;
- intersection allowlist and unexplained-overlap count;
- fresh-reopen hash;
- zero-port / zero-lumped / zero-result proof.

## Human 3D review order

1. substrate + stalk only;
2. bridge/mortise/tenon/interlock;
3. hub ground / shield / mechanical lands;
4. each T01 branch independently;
5. all four T01 branches together;
6. keepout overlays from LNA/route/service predicates, displayed by review tooling only.

Review specifically:
- transition is on the correct stalk face for all four quadrants;
- local horizontal slice points toward the associated accepted route corridor;
- no signal/ground short;
- no T01 metal cuts through mortise/tenon;
- no duplicate FR4 board;
- no T01 metal violates LNA/route/service keepout predicates.

Stop after C0 review. I01 solve needs separate authorization.
