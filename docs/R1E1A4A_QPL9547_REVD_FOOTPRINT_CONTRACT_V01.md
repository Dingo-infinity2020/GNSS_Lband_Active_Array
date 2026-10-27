# QPL9547 Rev-D Footprint Contract V0.1

Status: FROZEN FOR A0-E1 GEOMETRY SEED
Execution authority: NONE

## Sources

Primary:
- QPL9547 Rev-D datasheet, 2023-10-11, package and recommended PCB layout page.
- Device S/noise reference plane remains the device leads.

Secondary cross-check only:
- historical Qorvo Rev-C land/via pattern;
- historical KiCad Qorvo DFN footprint.

Primary Rev-D geometry always wins when dimensions differ.

## Package geometry

All dimensions mm.

Body:
- 2.00 x 2.00 nominal
- tolerance +/-0.05

Package height:
- 0.85 +/-0.10

Exposed backside paddle:
- 0.80 +/-0.05 x 1.60 +/-0.05

Terminal pitch:
- 0.50 BSC

Package terminal metal:
- terminal length = 0.30 +/-0.05
- terminal width = 0.25 +/-0.05

## Rev-D recommended PCB METAL land pattern

Coordinate frame:
- package center = (x_pkg,y_pkg)=(0,0)
- side terminals are on x_pkg = +/- side
- pin rows use y_pkg = +/-0.75 and +/-0.25

Frozen metal:
- 8 side lands
- side-land size = 0.430 x 0.250
- side-land center x = +/-0.915
- side-land row centers y = -0.75,-0.25,+0.25,+0.75
- center exposed-paddle copper = 0.800 x 1.600

Pin numbering:
- left side: pins 1,2,3,4 from one end to the other
- right side: pins 8,7,6,5 in the corresponding opposing rows
- RF IN = pin 2
- RF OUT/VDD = pin 7

The x=+/-0.915 interpretation is cross-checked against the historic Qorvo/KiCad footprint, which used about +/-0.89 before Rev-D enlarged/repositioned the recommended lands.

## Rev-D recommended PCB SOLDER MASK pattern

- 8 side openings
- side-opening size = 0.530 x 0.350
- same side-opening center coordinates as the corresponding copper lands
- center paddle mask opening = 0.900 x 1.700

Copper thickness:
- Rev-D requires minimum 1 oz top and bottom copper for the recommended PCB implementation.

## Package orientation on the Architecture-B stalk

Use one physical package rotation for both twin branches.

Map package axes into stalk-local coordinates:
- x_pkg -> +v
- y_pkg -> +u

Therefore:
- pin 2 RF-IN lies upstream (-v) of package center
- pin 7 RF-OUT/VDD lies downstream (+v)

RF pin row offset:
- pin 2 and pin 7 both lie at y_pkg=-0.25 in the frozen pin-number convention.

To keep the existing branch RF centerline u_branch straight through pin 2 and pin 7:
- package-center u_seed = u_branch + 0.25 mm
  for the chosen y_pkg=-0.25 convention.

This means the two physical package bodies are not mirror images about the stalk center even though their RF branch centerlines remain at u=+/-3 mm.

This asymmetry is real and shall be modeled.

Historical package-center v seed:
- v_pkg = 7.0 mm

With side-land center x_pkg=+/-0.915:
- RF-IN land center v ~= 6.085 mm
- RF-OUT/VDD land center v ~= 7.915 mm

The v=7 mm package-center value remains a placement seed until E1 prebuild interference review.

## Via requirement

Rev-D:
- vias are REQUIRED under backside paddle
- drill bit = 0.35 mm recommended
- final plated-through diameter = 0.25 mm recommended

Rev-D does not freeze a via count/coordinate pattern.

Historic Rev-C Qorvo layout explicitly used 3 plated-through paddle vias.

Therefore A0-E1 G0 via-count seed:
- 3 paddle vias

Their exact coordinates are frozen separately in the via/fabrication contract.

## Modeling rule

The active transistor/package dielectric is not solved as an active CST object.

A0-E1 shall model:
- PCB copper lands
- solder-mask opening only if mask is explicitly enabled in material contract
- exposed-paddle copper landing
- plated through-via barrels
- finite local ground
- physical passive coupling between input/output/bias land regions

Device S2P reference planes are at RF-IN and RF-OUT device-lead planes.

## HOLD / limits

Not final hardware-release authority:
- solder paste stencil segmentation
- via fill/cap/tent process
- fabrication-specific solder-mask registration
- assembly courtyard
- production PCBA process

Those require final fabricator/assembler DFM.
