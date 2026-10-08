# R4-A0-E1 Paddle-Via / Fabrication Seed V0.1

Status: G0 EM/FABRICATION SEED — NOT HARDWARE-RELEASE DFM

## Purpose

Give A0-E1 a manufacturable, deterministic local RF-ground seed without pretending a PCB vendor has already approved it.

## Substrate

Retain current Architecture-B stalk baseline:
- FR4
- thickness = 1.00 mm

Copper:
- 1 oz minimum top/bottom per QPL9547 Rev-D recommendation
- EM seed copper thickness = 0.035 mm

## QPL9547 paddle via G0

Count:
- 3 vias per LNA backside paddle

Why 3:
- historical Qorvo Rev-C recommended pattern explicitly showed 3 paddle vias;
- Rev-D still mandates vias but does not specify a count;
- three vias fit the 0.80 x 1.60 paddle while providing parallel RF ground paths.

Finished hole:
- 0.25 mm

Pre-plate drill:
- 0.35 mm reference

CST barrel seed:
- inner diameter = 0.25 mm
- outer barrel diameter = 0.35 mm
- copper barrel spans the full 1.00-mm FR4 thickness

Via-center seed in package coordinates:
- x_pkg = 0
- y_pkg = -0.50, 0, +0.50 mm

This is intentionally more conservative than placing the outer vias near the paddle ends.

Clearance to the 1.60-mm paddle long edge using 0.35-mm barrel OD:
0.80 - 0.50 - 0.175 = 0.125 mm.

After 90-degree package rotation, the three-via row lies mainly across stalk-local u.

## Copper connection

Top:
- vias connect directly into the exposed-paddle copper land.

Bottom:
- vias connect directly into the branch-local bottom RF ground.

No thermal relief.
No necked remote connection is allowed between paddle vias and the local branch ground.

## Decoupling ground vias

For G0:
- each shunt RF decoupling capacitor gets its own short ground via
- do not make two RF decouplers share a single via
- use the same 0.25-mm finished-hole family unless DFM later requires another drill class

The 1-uF bulk capacitor may share the DC ground region but should not force the RF 100-pF return to route through its via.

## Manufacturing interpretation

The A0-E1 model is allowed to use these via dimensions because they come directly from Qorvo's recommended drill/final-hole guidance.

Still NOT frozen:
- annular-ring minimum of the eventual fabricator
- via fill / resin plug / copper cap
- top-side solder-wicking mitigation
- stencil reduction over the paddle
- solder-mask tenting

Hardware release must revisit these.

## DFM predicate for E1 build

The EM seed shall verify:
- all three via barrels stay inside the intended local ground/paddle region
- no positive-volume collision with signal lands
- no via barrel enters a component keepout
- minimum copper web between signal-land edge and via-barrel outer wall >= 0.20 mm unless explicitly waived
- via-to-board-edge / via-to-slot distances >= 0.25 mm in the coupon
