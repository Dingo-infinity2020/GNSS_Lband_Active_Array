# R4-A0-E1 QPL9547 Grounded-Pin Spoke Contract V0.1

Status: FROZEN FOR A0-E1 BUILD-ONLY

## Purpose

Complete the physical local-ground definition for the QPL9547 package.

The QPL9547 active S2P remains only a two-port between pin 2 RF-IN and pin 7 RF-OUT/VDD.
Nevertheless the physical PCB lands of grounded pins must not be left as artificial floating parasitic islands.

G0 FDD grounded pins:
- pin 3
- pin 4
- pin 5
- pin 6 shutdown
- pin 8

Pin 1 Vbias, pin 2 RF-IN and pin 7 RF-OUT/VDD remain separate nodes.

## Package / paddle coordinates

Stalk-local one-LNA coupon coordinates:
- package center q=+0.25 mm, v=7.00 mm
- paddle q=-0.55..+1.05 mm
- paddle v=6.60..7.40 mm

Upstream side-land span:
- v=5.870..6.300 mm

Downstream side-land span:
- v=7.700..8.130 mm

Row centers after package rotation:
- q=-0.50, 0.00, +0.50, +1.00 mm

Upstream:
- pin1 q=-0.50
- pin2 q=0.00
- pin3 q=+0.50
- pin4 q=+1.00

Downstream:
- pin8 q=-0.50
- pin7 q=0.00
- pin6 q=+0.50
- pin5 q=+1.00

## Ground-spoke geometry

Use top-copper spokes:
- width in q = 0.20 mm
- copper thickness = 0.035 mm

Upstream spokes:
- pin3 center q=+0.50
- pin4 center q=+1.00
- v=6.300..6.600 mm

Downstream spokes:
- pin8 center q=-0.50
- pin6 center q=+0.50
- pin5 center q=+1.00
- v=7.400..7.700 mm

Each spoke is an intentional metal connection:
side ground land -> central exposed-paddle land.

The exposed-paddle land then connects through the three frozen paddle vias to the full backside branch-local ground.

No extra ground via is required for these five side lands in the G0 coupon.

## Contact proof

For q=+/-0.50 spokes:
- spoke q interval = center +/-0.10 mm
- overlap with corresponding 0.25-mm side land is >=0.20 mm
- overlap with paddle q range is >=0.15 mm.

For q=+1.00 spokes:
- spoke q=0.90..1.10 mm
- paddle ends at q=1.05 mm
- intentional spoke/paddle transverse overlap = 0.15 mm.

Thus all five grounded lands have positive-area top-copper continuity to the exposed paddle.

## Isolation proof

No spoke is created at:
- q=-0.50 upstream pin1 Vbias except downstream pin8 on the opposite side of the package;
- q=0 upstream pin2 RF-IN;
- q=0 downstream pin7 RF-OUT/VDD.

The upstream and downstream spoke v-ranges are separated by the paddle body and do not bridge RF-IN to RF-OUT.

## B_VBIAS scope correction

A0-E1 exports B_VBIAS directly on the pin-1 PCB land.

R4 = 3.32 kOhm is connected in the circuit domain from B_VDD to B_VBIAS.

A0-E1 does NOT yet include physical R4 pads/routing.

Reason:
the E1 question is the RF landing-zone / package-ground / bias-feed parasitic environment.
The high-resistance Vbias routing may be added in A0-E2 when the complete active-region PCB layout is established.

This supersedes any earlier wording that implied R4 pads must already exist in E1.

## Build audit

Required:
- exactly five grounded-pin spoke solids or five deterministic regions merged into the ground-node copper;
- each spoke face-connects its intended side land;
- each spoke face-connects the exposed paddle;
- no spoke overlaps pin1, pin2 or pin7 copper;
- all grounded side lands share the paddle/via/backside-ground node after fresh reopen.
