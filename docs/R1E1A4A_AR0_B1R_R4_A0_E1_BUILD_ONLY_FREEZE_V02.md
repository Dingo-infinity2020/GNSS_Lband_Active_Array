# R4-A0-E1 One-LNA Landing-Zone Build-Only Freeze V0.2

Status: SOURCE / CONTRACT FROZEN — BUILD NOT AUTHORIZED
SimulationOps: 0.2.8

## Purpose

First remote/CST action on the new active-interface mainline.

Build only a single QPL9547 landing-zone coupon.

No radiator.
No second LNA.
No full lower stalk.
No remote ground merge.
No solver.

## Frozen build source

CST macro:
source/cst/R1E1A4A_AR0_B1R_R4_A0_E1_ONE_LNA_LANDING_ZONE_BUILD_ONLY_V02.mcr

Primary contracts:
- QPL9547 Rev-D footprint V0.1
- E1 via/fabrication seed V0.1
- E1 grounded-pin spoke V0.1
- E1 dimensioned placement V0.1
- E1 material contract V0.1
- E1 interference predicates V0.1
- E1 port contract V0.2
- E1 prebuild manifest V0.1

Static arithmetic evidence:
evidence/r4_a0_e1_static_prebuild_20260927/R4_A0_E1_STATIC_ARITHMETIC_AUDIT.json

## Target artifact

R1E1A4A_AR0_B1R_R4_A0_E1_ONE_LNA_LANDING_ZONE_BUILD_ONLY_V02.cst

Target host when authorized:
NW.

## Required geometry

Coupon:
- 4.0 x 10.0 x 1.0 mm FR4
- full finite backside local ground

QPL9547 region:
- 8 Rev-D side lands
- one Rev-D exposed-paddle land
- 5 grounded-pin spokes
- 3 plated paddle vias

Passive pads:
- C_IN two pads
- C_OUT two pads
- L1 two pads
- C_RF two pads
- dedicated C_RF ground via

Routing:
- upstream 1.90-mm branch with taper
- C_IN-to-pin2 taper
- pin7-to-C_OUT taper
- P_OUT-to-L1 fan
- VDD trace
- downstream C_OUT-to-1.90-mm taper and line

No physical R4 in E1.
B_VBIAS is exported at pin 1 and R4 is circuit-domain.

## Ports

Exactly 6:
1 E_UP
2 P_IN
3 P_OUT
4 E_DN
5 B_VDD
6 B_VBIAS

All:
- single-ended
- 50-ohm normalized
- signal endpoint z=0
- ground endpoint z=-1.0
- through FR4 only

No differential port.

## Build-only acceptance

Mandatory:
- macro executes in a fresh MWS;
- expected materials exist;
- deterministic solid inventory;
- exactly 6 ports;
- no result tree;
- no solver/monitor/optimizer;
- fresh save + close + reopen;
- artifact hash stable after fresh reopen;
- every node port endpoint matches contract;
- all via coordinates/radii match contract;
- all component-pad rectangles match contract;
- no signal-ground short;
- no copper embedded in FR4 except plated-via barrels;
- all intentional via/paddle/ground contacts present;
- all five grounded side lands connect to exposed paddle;
- no grounded spoke connects pin1, pin2 or pin7;
- minimum unrelated-copper clearance >=0.20 mm;
- downstream RF trace vs right-side decoupling lane must be rechecked explicitly because nominal static margin reaches exactly 0.20 mm.

Interference qualification:
use pairwise or non-destructive methods that do not consume shared solids.
Do not infer PASS from visual inspection alone.

## Human review

Required views:
1. top full coupon
2. QPL9547 land / paddle / 3-via closeup
3. input DC-block launch
4. RFOUT/COUT/L1 fan region
5. C_RF + dedicated via
6. bottom local-ground view
7. cross-section through paddle vias
8. port markers/reference segments

Review question:
does the real 4-mm active-region width remain credible?

If not:
HOLD and widen/rework the active-region stalk.
Do not shrink vendor/package lands to preserve the old fork width.

## Stop

BUILD ONLY.

Even after build PASS:
SOLVE_AUTHORIZED remains false.

A separate E1 solver freeze/authorization is required.


## V0.2 plated-via correction

V0.1 source macro is PRE-EXECUTION SUPERSEDED and MUST NOT be run.

Reason:
V0.1 created annular via copper through the FR4 volume without first materializing the drilled hole.

V0.2 hard rule:
for each of the 3 paddle vias and the dedicated C_RF ground via:
1. create a 0.35-mm-diameter through-hole tool;
2. subtract the tool from FR4;
3. create annular copper barrel with outer diameter 0.35 mm and inner/final-hole diameter 0.25 mm;
4. barrel spans top and bottom copper surfaces.

Build audit must prove:
- four drill tools are consumed;
- four annular copper via barrels remain;
- no via copper has positive-volume overlap with FR4 after drilling;
- top/bottom intentional metal contacts remain.
