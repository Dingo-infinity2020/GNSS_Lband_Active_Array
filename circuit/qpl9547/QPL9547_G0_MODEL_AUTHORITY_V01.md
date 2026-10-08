# QPL9547 G0 Active-Device Model Authority V0.1

Status: TRACEABLE REFERENCE DEVICE AUTHORITY — NOT FINAL DEVICE SELECTION
Project: GNSS_Lband_Active_Array
SimulationOps minimum: 0.2.8

## 1. Role

QPL9547 is the project's G0 reference LNA for active-interface and receiver co-simulation.

It is NOT frozen as the final production device.

Architecture-B baseline remains:
- two QPL9547-class single-ended LNAs per balanced polarization;
- four first-stage LNAs per dual-polarization element;
- no passive pre-LNA balun or combiner;
- post-LNA combining/differential handling remains downstream.

## 2. Datasheet authority

Primary device reference:
Qorvo QPL9547 Data Sheet Rev. D, 2023-10-11.

Verified device-level facts:
- operational range: 0.1–6 GHz;
- G0 bias point for project reference: VDD = 5 V, IDD = 65 mA typical;
- package: 8-pin 2 x 2 mm DFN;
- S/noise parameter reference impedance: 50 ohm;
- datasheet S/noise parameter reference plane: device leads;
- pin 2: RF IN, internally matched to 50 ohm, DC block required;
- pin 7: RF OUT and VDD, internally matched to 50 ohm, DC block required;
- pin 1: Vbias / current-setting control;
- pin 6: shutdown control;
- pins 3/4/5/8: NC internally; may float or be grounded subject to final layout policy;
- backside paddle: RF/DC ground.

Package facts used as initial geometry authority:
- body = 2.00 +/- 0.05 mm square;
- exposed DAP nominal = 0.80 x 1.60 mm;
- terminal pitch = 0.50 mm BSC;
- datasheet recommends package-paddle vias;
- recommended via drilling reference: 0.35 mm drill bit, 0.25 mm final plated-through diameter;
- datasheet requires at least 1-oz copper on top and bottom for its recommended PCB layout.

The recommended land-pattern drawing is visible in Rev-D page 8, but exact pad/mask dimensions shall be machine-transcribed / CAD-audited before BUILD authority. Do not hand-tune a footprint from screenshots.

## 3. Existing project S-parameter authority

Existing provenance:
`circuit/qpl9547/QPL9547_SPARAM_SOURCE_NOTE.md`

Reference external file:
`QPL9547_DEEMBEDDED_TRL_SN1_5V_65MA.S2P`

Frozen metadata:
- external-file SHA256:
  `fad334a226acb9fbe1e4bd769f474afa14e2c23c18f31f4750c091f3d5d0424f`
- measurement header date: 2024-10-04;
- bias: 5 V / 65 mA;
- Touchstone reference impedance: 50 ohm;
- source context: Qorvo Tech Forum attachment;
- project uses the file only as a traceable G0 reference, not as immutable final-production device data.

Existing in-band derived data:
`circuit/qpl9547/QPL9547_SPARAM_REFERENCE_1P15_1P65.csv`

Existing stability summary:
`circuit/qpl9547/analysis/QPL9547_SPARAM_STABILITY_SUMMARY.json`

Current project-derived bounds over 1.15–1.65 GHz:
- K_min = 1.2480;
- mu_min = 1.3687;
- mu_prime_min = 1.3873;
- max |Delta| = 0.4437.

Therefore the standalone device 2-port is unconditionally stable in the project science band for this reference measurement.

This does NOT prove assembled active-antenna stability.

The extended S2P source notes that the TRL kit was designed mainly for approximately 600 MHz and above. Data below that region are sentinel-quality only and shall not be used to prove low-frequency stability margin.

## 4. Noise-parameter authority

Existing project-owned Rev-D anchors:
`circuit/qpl9547/QPL9547_NOISE_REFERENCE_1P1_1P7.csv`

They include:
- NFmin;
- GammaOpt magnitude/phase;
- Rn;
- deterministic GammaOpt -> Zopt conversion.

Important:
- the noise-anchor table and the forum S2P reference are separate provenance streams;
- they may be combined for G0 engineering co-simulation only after frequency interpolation is explicit;
- do not claim that the external forum S2P itself contains the project's frozen Rev-D noise anchors unless the raw file is re-audited and proves that statement.

The old `illustrative_2xzopt` columns remain diagnostic only.
They are not a differential antenna target.

## 5. EVB circuit reference

QPL9547EVB-01 is a reference topology, not a PCB geometry template for the 1.00-mm FR4 stalk.

Rev-D EVB facts:
- C1 input DC block = 100 pF in the reference schematic;
- C2 output DC block = 100 pF in the reference schematic;
- L1 = 18 nH, Coilcraft 0402CS-18NXGRW, in the output/VDD bias feed;
- R4 = 3.32 kOhm nominal current-setting reference;
- C3/C5/C6/C7 = 100 pF class RF decoupling/reference parts in the EVB BOM;
- C4 = 1.0 uF bulk/local decoupling;
- EVB components are 0402.

These are starting reference values only.
They are NOT yet frozen production values for the stalk implementation.

The EVB uses a multilayer Rogers/FR4/Rogers stack and its 50-ohm line dimensions must NOT be copied into the project's 1.00-mm FR4 stalk.

## 6. Grounding authority

Hard baseline rules for the next active model:
- backside paddle must have a short local RF/DC ground path;
- package grounding shall use local plated vias under / immediately adjacent to the paddle region;
- remote lower-stalk common-ground closure alone is NOT an acceptable first-stage-LNA ground baseline;
- each local decoupling capacitor shall have its own short ground via/return in the reference layout;
- shield/ground/output-return topology is part of stability, not a mechanical afterthought.

Exact via count, pad diameter, anti-pad, local-island outline and shield contact geometry remain released until footprint/landing-zone design is frozen.

## 7. DC / bias authority

Hard:
- input DC block is mandatory;
- output DC block is mandatory;
- RF OUT is also the VDD supply pin;
- Vbias/current-setting and VDD injection must be represented in the circuit model;
- a DC path shall never be inferred through the antenna terminal.

G0 reference circuit starts from the EVB topology.

For the first project implementation:
- physical pads/traces/vias belong to EM geometry;
- ideal/component electrical behavior belongs to the circuit model unless a measured component S-parameter model is explicitly imported;
- final capacitor/inductor vendor models are deferred until topology validation.

## 8. Stability frequency policy

Science-performance decision band:
1.15–1.65 GHz.

Initial full-wave active-interface band:
1.0–1.8 GHz.

Circuit/device stability sweep:
use the full reliable device-model span available from the reference model.
For the current TRL-derived external S2P:
- >=0.6 GHz may be used as the main wideband stability reference;
- 0.1–0.6 GHz is sentinel-only because of the source calibration caveat.

Before hardware release, obtain / verify a production-authority model across the intended out-of-band stability range.

## 9. Source references

- Qorvo QPL9547 product page:
  https://store.qorvo.com/products/detail/qpl9547-qorvo/675339/
- Qorvo QPL9547EVB-01 product page:
  https://store.qorvo.com/products/detail/qpl9547evb01-qorvo/678748/
- Qorvo Rev-D data-sheet copy used for visual/layout audit:
  https://cdn.icstop.com/upload/pdfs/63/a4/63a4fc143fac7feb70038b6a282aaae1.pdf
- Qorvo forum S2P provenance:
  https://forum.qorvo.com/t/qpl9547-25-mhz-operation/22732
- Qorvo grounding / decoupling guidance:
  https://forum.qorvo.com/t/qpl9547-for-uhf/24872
- Qorvo input DC-block clarification:
  https://forum.qorvo.com/t/qpl9547-voltage-bias-issue/24390
- Qorvo shield/ground stability case:
  https://forum.qorvo.com/t/qpl9547-oscillating-depending-on-shield-grounding/25241

## 10. Open items before active BUILD

HOLD / not yet frozen:
- exact machine-transcribed PCB land pattern and solder-mask geometry;
- exact number/placement of paddle vias on the project's 1.00-mm FR4;
- exact local-ground-island topology shared by the twin LNAs;
- selected real DC-block capacitor and its broadband model;
- selected VDD choke / damping / decoupling network for 1.15–1.65 GHz plus out-of-band stability;
- selected shield geometry;
- final LNA placement along the stalk;
- final production device choice.

No BUILD or SOLVE authorization is implied by this model authority.
