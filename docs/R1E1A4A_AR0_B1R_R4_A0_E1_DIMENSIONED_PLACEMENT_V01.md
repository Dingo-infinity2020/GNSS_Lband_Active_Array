# R4-A0-E1 One-LNA Landing-Zone Dimensioned Placement Contract V0.1

Status: FROZEN FOR FIRST BUILD-ONLY
Remote execution: NOT YET AUTHORIZED

## 1. Coupon role

A0-E1 is an electrical landing-zone coupon, not the final twin-LNA stalk.

It answers:
- can a QPL9547 package landing, paddle-ground via cluster, DC-block launches and bias feed be represented cleanly on the 1.00-mm FR4 technology?
- are the device-lead reference planes deterministic and non-pathological?
- is local passive coupling / ground behavior reasonable before radiator integration?

It deliberately omits the full radiator and remote lower stalk.

## 2. Local coordinates

Use branch-local coordinates:
- q: transverse to branch RF direction
- v: downstream away from radiator
- n: board normal

FR4:
- q = -2.0 .. +2.0 mm
- v = 3.0 .. 13.0 mm
- n = -1.0 .. 0.0 mm

Top copper nominal:
- n = 0.0 .. +0.035 mm

Backside local ground:
- q = -2.0 .. +2.0 mm
- v = 3.0 .. 13.0 mm
- n = -1.035 .. -1.0 mm

This 4-mm width intentionally matches one accepted B0 fork prong:
local u=+1..+5 or -5..-1, width 4 mm.

## 3. Package placement

QPL9547 package-center seed:
- q_pkg = +0.25 mm
- v_pkg = 7.000 mm

Package rotation:
- x_pkg -> +v
- y_pkg -> +q

Reason for q_pkg=+0.25:
the RF-IN/RF-OUT row lies at y_pkg=-0.25 mm;
this keeps the RF pin-center line at q=0, aligned with the existing branch signal centerline.

Body envelope:
- q = -0.75 .. +1.25 mm
- v = 6.00 .. 8.00 mm
- height = Rev-D 0.85 mm nominal above land plane for visual/interference envelope only

RF lead centers:
- pin 2 RF-IN:  q=0, v=6.085 mm
- pin 7 RF-OUT/VDD: q=0, v=7.915 mm

Pin-1 Vbias lead center:
- q=-0.50 mm, v=6.085 mm

## 4. Rev-D package lands after rotation

Side-land dimensions on PCB:
- along v = 0.430 mm
- along q = 0.250 mm

Central paddle copper:
- along v = 0.800 mm
- along q = 1.600 mm

Paddle center:
- q=+0.25, v=7.000 mm

Paddle extent:
- q=-0.55 .. +1.05
- v=6.60 .. 7.40 mm

## 5. Paddle vias

Three-via G0 seed, through 1.00-mm FR4.

After package rotation:
- all at v=7.000 mm
- q=-0.25, +0.25, +0.75 mm

This is the package-frame y=-0.50,0,+0.50 seed mapped into stalk q.

Finished hole = 0.25 mm.
Barrel OD seed = 0.35 mm.

All three lie inside the 1.60-mm paddle-long dimension with >=0.125-mm barrel-to-paddle-edge margin.

## 6. G0 0402 land primitive

For first E1 geometry use one deterministic generic RF 0402 land primitive:

- each pad = 0.50 mm along component axis x 0.60 mm transverse
- pad-to-pad copper gap = 0.40 mm
- pad-center spacing = 0.90 mm
- body envelope = 1.00 x 0.50 mm nominal

This is a geometry seed, not final assembler DFM.

The Murata 1005M/0402 S-parameter measurement environment uses the same general dimensional scale and the selected capacitor itself is 1.0 x 0.5 mm.

## 7. Input DC-block placement

C_IN axis along v.

Pad centers:
- upstream pad:   q=0, v=4.650 mm
- downstream pad: q=0, v=5.550 mm

Pad spans:
- upstream v=4.40..4.90
- downstream v=5.30..5.80

Physical gap:
- v=4.90..5.30 mm

Downstream pad to RF-IN land:
- short copper taper/bridge v=5.80..5.870 mm
- q-width transitions 0.60 -> 0.25 mm

Upstream MSL:
- branch center q=0
- nominal 1.90-mm width before taper
- taper from 1.90 mm to 0.60 mm over v=3.40..4.40 mm

## 8. Output DC-block placement

C_OUT axis along v.

Pad centers:
- device-side pad: q=0, v=8.450 mm
- downstream pad:  q=0, v=9.350 mm

Package RF-OUT land to first pad:
- short taper/bridge v=8.130..8.200 mm
- q-width 0.25 -> 0.60 mm

Output component gap:
- v=8.70..9.10 mm

Post-cap trace:
- begins at v=9.60 mm
- taper to 1.90-mm branch line over v=9.60..10.60 mm
- then continues to E1 downstream boundary

## 9. Bias choke placement

G0 L1 = 18 nH.

Place L1 in a side lane so the RF output path stays straight.

Axis along v.
Centerline:
- q=+1.45 mm

Pad centers:
- RF/P_OUT-side pad: q=+1.45, v=8.45 mm
- VDD-side pad:      q=+1.45, v=9.35 mm

The P_OUT node fans from pin-7 land to:
- C_OUT device-side pad on q=0
- L1 RF-side pad at q=+1.45

The branch/fan copper is part of EM geometry.

## 10. RF decoupler placement

C_RF = G0 100 pF shunt decoupler.

Axis along v.
q=+1.45 mm.

Pad centers:
- VDD pad:    v=10.25 mm
- ground pad: v=11.15 mm

Ground-side pad gets its own dedicated through-via:
- q=+1.45 mm
- v=11.15 mm
- same 0.25-mm finished-hole family

The VDD conductor joins:
L1 VDD-side pad
-> B_VDD node
-> C_RF VDD pad.

## 11. Bulk decoupler

The 1-uF bulk capacitor remains in the circuit topology but is not forced into the compact E1 RF landing zone.

A physical bulk-cap reserve/feed stub may be represented near v=12..13 mm.

Its exact production placement is deferred to A0-E2 because its GHz parasitics are not the primary E1 question.

## 12. Vbias / shutdown / NC

Pin-1 Vbias land is retained physically.

A passive EM node B_VBIAS terminates at the pin-1 copper network.

Circuit layer:
B_VDD -> R4 3.32 kOhm -> B_VBIAS.

Pin-6 shutdown:
direct short to local top-ground feature / dedicated via for FDD baseline.

Pins 3/4/5/8:
grounded in G0, matching the EVB choice.

## 13. Component envelopes

Build-only visual envelopes:
- QPL9547 body
- C_IN
- C_OUT
- L1
- C_RF

shall be non-RF solids or metadata-only envelopes and must not accidentally become conductive solver geometry.

## 14. Integration warning

The 4-mm prong is narrow.

A0-E1 is deliberately checking whether:
- the 1.90-mm microstrip taper,
- package,
- bias side lane,
- and dedicated ground returns

can coexist without unacceptable clearance.

If the build-only geometry cannot meet frozen clearance predicates, the correct response is to widen/rework the active-region stalk geometry.

Do not shrink component lands below vendor/seed geometry merely to preserve the old prong.
