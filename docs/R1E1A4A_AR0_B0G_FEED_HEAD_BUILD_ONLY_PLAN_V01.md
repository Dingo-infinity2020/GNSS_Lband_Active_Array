# AR0-B0G Feed-Head Build-Only Plan V0.1

Status: FROZEN PLAN — BUILD NOT AUTHORIZED

Authority:
docs/R1E1A4A_AR0_B0_STALK_TOP_TWIN_MSL_ARCHITECTURE_FREEZE_V01.md

## Purpose

Materialize the new B0 upper feed architecture without committing to active-device RF behavior.

This stage replaces the invalid H3B-C0 antenna/T01 interface. It does not recover or modify the old B artifact.

## Geometry to build

Use the qualified radiator source and add:
- Pol-A fork feed head along NE-SW;
- Pol-B fork feed head as exact +90-degree counterpart;
- two terminal signal tongues per polarization;
- two 1.90-mm nominal MSL strips per polarization;
- no backing ground in first 3.0 mm below the radiator feed plane;
- backside ground rails below 3.0 mm;
- 2 x 2 mm nonconductive QPL9547 package envelopes at u=+-3 mm, v=7 mm;
- nonconductive via-reserve predicates fully contained in stalk FR4.

The feed-head body extends to v=12 mm.
Lower mechanical support may be represented only by a clearly labelled temporary continuation and is not part of the architecture PASS.

## Explicitly absent

- no T01-A geometry;
- no GCPW side-ground pads at the radiator;
- no radiator-PCB backing ground;
- no H3A large top notch;
- no H3A top mechanical land pattern;
- no real QPL9547 pads/device;
- no bias network;
- no matching network;
- no port;
- no load;
- no solver.

## Build audit

Required deterministic checks:
1. parent radiator hash/shape identity;
2. radiator copper unchanged;
3. terminal centers exactly inherited;
4. four and only four terminal-to-signal contacts;
5. zero ground-to-radiator contact;
6. exact 3.0-mm ground setback;
7. four MSL traces, all 1.90 mm nominal width;
8. exact rotational equivalence of Pol-A/Pol-B feed heads;
9. both orthogonal feed heads collision-free over v=0..12 mm;
10. all LNA envelopes and via reserves lie inside positive FR4 volume;
11. CST intersection check returns;
12. fresh reopen;
13. zero RF ports;
14. zero solver result tree.

## Human review

Required views:
- radiator copper only;
- stalk FR4 only;
- signal tongues/traces only;
- backside ground only;
- LNA/via keepout overlays;
- full dual-pol assembly.

Special review questions:
- does any ground metal visually sit behind radiator copper?
- are both feed terminals visibly isolated from stalk ground?
- do the two polarization feed heads physically cross?
- does the 3-mm unbacked tongue look short enough to remain a local launch rather than a long antenna wire?
- is there enough real FR4 around the future LNA/via region?

Stop after review.
No passive solve is implied.
