# H3B-T01 Orthogonal PCB Transition Coupon V0.1 — BUILD-ONLY Qualification

Canonical status: PASS_R1E1A4A_H3B_T01_TRANSITION_COUPON_BUILD_ONLY.

One formal standalone build-only invocation was consumed on NW. No solver was invoked.

Artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h3b_t01_build_work\R1E1A4A_H3B_T01_ORTHOGONAL_TRANSITION_BUILD_ONLY_V01.cst

SHA256:
f321b678d390470a2420df40fd6d0cf6553cc041f9219bfcd011c7e41fbadf3d

Bytes: 49937.

Fresh-reopen qualification:
- shape count = 38;
- exact component counts: 2 boards, 6 G-S-G line conductors, 2 local backing grounds, 6 transition pads, 3 edge caps, 3 solder envelopes, 16 plated via barrels;
- all shape volumes positive;
- all via-hole tools consumed;
- RF port count = 0;
- RP1 = horizontal y=+12 mm and RP2 = vertical z=-12 mm retained as parameters;
- no solver markers or solver-result tree items;
- artifact hash unchanged by fresh-reopen qualification.

Intersection gate:
- CST electromagnetic auto-intersection checking enabled during build;
- CST built-in CDCheckModelIntersections executed after fresh reopen and returned control;
- line signal/ground gap = 0.30 mm;
- transition pad signal/ground gap = 0.25 mm;
- pad outer edge to PCB edge = 1.25 mm;
- via barrel to either ground-rail edge = 0.90 mm;
- via to PCB edge = 2.50 mm;
- local backing-ground to PCB edge = 1.00 mm;
- horizontal and vertical board substrates have zero positive-volume overlap and meet by intended face contact only.

This is a geometry/assembly coupon only. PEC conductors are build proxies; conductor/solder loss models and RF ports are deferred to the separately authorized passive-solve stage.

Stop boundary honored: no passive solve, no optimization sweep, no H3B-I01 integration and no active-device model.
