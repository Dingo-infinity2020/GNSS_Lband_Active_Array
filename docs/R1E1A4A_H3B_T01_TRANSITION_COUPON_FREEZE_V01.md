# H3B-T01 Post-LNA Orthogonal PCB Transition Coupon Freeze V0.1

Status: FROZEN FOR ONE BUILD-ONLY INVOCATION — NO SOLVE

Purpose: isolate and qualify the physical 90-degree PCB-to-PCB transition that transfers one already-amplified single-ended LNA output from the horizontal radiator-side PCB to a vertical stalk PCB.

This is a technology coupon. It intentionally excludes the antenna radiator, first-stage LNA input, balun/combiner, filter, final connector and array environment.

## Coordinate system

- horizontal PCB: XY plane, substrate z = 0 ... +1.0 mm;
- vertical PCB: XZ plane, substrate y = -0.5 ... +0.5 mm and z = -18 ... 0 mm;
- the vertical PCB top edge contacts the horizontal PCB underside at z=0;
- RF transition is centered at x=0, on the +Y face of the vertical PCB.

Horizontal board: x = -5 ... +5 mm, y = -4 ... +16 mm.
Vertical board: x = -5 ... +5 mm, z = -18 ... 0 mm.

## Substrate and copper baseline

- substrate: FR4 cost-baseline, er=4.3, tanD=0.02 for later passive qualification;
- thickness: 1.00 mm;
- copper thickness: 0.035 mm;
- BUILD-ONLY uses PEC geometry proxies; passive solve must replace/freeze conductor loss models explicitly.

## Controlled-line baseline

Both horizontal and vertical sections use the same first-pass grounded coplanar-waveguide class geometry:
- signal width Wsig = 1.80 mm;
- signal-to-ground gap G = 0.30 mm;
- same-side ground-rail width = 2.20 mm;
- opposite-side local ground-plane half-width = 4.0 mm;
- nominal line length from transition region to each reference plane exceeds 10 mm.

Ground-via baseline:
- plated-via outer diameter = 0.40 mm;
- finished inner hole diameter = 0.30 mm;
- via barrel thickness proxy = 0.05 mm;
- via-fence X positions = +/-2.30 mm;
- four via stations per side on each board;
- horizontal stations y = 3, 6, 9, 12 mm;
- vertical stations z = -3, -6, -9, -12 mm.

These are module-local Class-B variables. They may be optimized after the first passive solve; they do not reopen antenna geometry.

## Reference planes

- RP1: horizontal line, y = +12.0 mm;
- RP2: vertical line, z = -12.0 mm.

BUILD-ONLY creates no RF port. RP1/RP2 are stored parameters only. The passive-solve stage will create ports/reference planes after human geometry review.

## 90-degree transition

Baseline transition-pad geometry:
- signal pad width = 2.20 mm;
- signal-to-ground transition gap = 0.25 mm;
- ground pad width = 2.40 mm;
- horizontal pad length = 1.0 mm, y = 0.5 ... 1.5 mm;
- vertical pad length = 1.165 mm, z = -1.20 ... -0.035 mm;
- vertical-board plated/castellated top-edge caps explicitly modeled;
- signal and both grounds use separate solder-fillet envelopes.

Solder-fillet envelope:
- y = 0.535 ... 1.00 mm;
- z = -0.45 ... -0.035 mm;
- separate signal/GND solids;
- no signal-ground overlap permitted.

## Grounded-CPW local backing

- horizontal opposite-face local ground plane: x = +/-4.0 mm, y = 1.5 ... 14.5 mm, on z = 1.0 ... 1.035 mm;
- vertical opposite-face local ground plane: x = +/-4.0 mm, z = -14.5 ... -1.2 mm, on y = -0.535 ... -0.5 mm;
- via fences tie same-side ground rails to these local planes.

Backing planes stop before the transition pad region so the first build does not hide the 90-degree discontinuity inside an oversized local ground block.

## Build-only acceptance

- fresh blank CST MWS; no inherited antenna geometry;
- exact frozen board/line/pad/via dimensions;
- via holes consumed; no H3B_Tools residual shapes;
- zero RF ports;
- no solver result tree / no solver run;
- CST EM auto-intersection checking during build;
- CST CDCheckModelIntersections after fresh reopen;
- all critical positive-clearance predicates pass;
- every intentional touching interface is face contact only; no unexplained positive-volume overlap.

## Stop boundary

Stop after human 3D/manufacturing review.
No passive solve, no optimization sweep, no integration into H3A, and no active-device model in this authorization.
