# AR0-B1R-R4-A0-E1 Landing-Zone Design Seed V0.1

Status: DESIGN SEED — NO BUILD / NO SOLVE AUTHORIZATION
Parent authority:
- docs/R1E1A4A_AR0_B1R_R4_A0_ACTIVE_INTERFACE_PRE_SIM_FREEZE_V01.md
- circuit/qpl9547/QPL9547_G0_MODEL_AUTHORITY_V01.md

## 1. Local coordinates

Retain Architecture-B stalk-local coordinates:
- u: branch-separation direction;
- v: distance away from radiator / down the stalk;
- existing branch centerlines: u = +/-3.0 mm;
- terminal/feed head: v = 0;
- existing T1R1 full-ground acquisition begins near v = 4.5 mm.

The historical B0 LNA-envelope center at v ~ 7 mm is retained as the first placement seed only.

It is not yet product geometry.

## 2. QPL9547 orientation seed

For each branch, orient the package RF axis along local v:

radiator
-> RF IN pin 2
-> active device
-> RF OUT/VDD pin 7
-> downstream route.

Therefore:
- RF-IN faces upstream toward decreasing v;
- RF-OUT/VDD faces downstream toward increasing v.

Both twin LNAs use the same physical package rotation so that pin 2 faces the radiator for both branches.

Do NOT mirror the silicon/package pinout to create artificial geometric symmetry.

Consequence:
the Vbias / NC side-pad arrangement is not an exact mirror between +u and -u branches.
This asymmetry is accepted as a real package-layout effect and must be captured by the landing-zone EM model.

## 3. Signal-continuity seed

Per branch the first product-representative chain is:

terminal/tongue
-> continuous pre-LNA trace
-> input DC-block pads + circuit element
-> QPL9547 RF-IN device-lead plane
-> QPL9547 S2P
-> QPL9547 RF-OUT/VDD device-lead plane
-> output DC-block pads + circuit element
-> post-LNA trace / load plane.

The only intentional pre-LNA signal interruption is the physical series DC-block component.

An open-ended MSL stub is not a product-representative branch.

## 4. Input/output DC-block seed

QPL9547 Rev-D / EVB reference uses 100-pF input and output DC-block capacitors.

For 100 pF ideal capacitance:
- |Xc| at 1.15 GHz ~= 1.384 ohm;
- |Xc| at L5 ~= 1.353 ohm;
- |Xc| at L2 ~= 1.296 ohm;
- |Xc| at L1 ~= 1.010 ohm;
- |Xc| at 1.65 GHz ~= 0.965 ohm.

Therefore 100 pF is a sensible G0 topology seed in the science band, but:
- its package ESL/ESR/SRF cannot be ignored for wideband stability;
- no generic ideal 100-pF part may be promoted to final BOM authority.

A0-C0 may use ideal 100 pF.
A0-E1 shall include the physical 0402 pads.
A0-C1 shall use a vendor broadband model before final qualification.

## 5. VDD choke seed

EVB reference:
Coilcraft 0402CS-18NXGRW, 18 nH.

Ideal-reactance scale:
- X_L at 1.15 GHz ~= 130 ohm;
- X_L at L5 ~= 133 ohm;
- X_L at L2 ~= 139 ohm;
- X_L at L1 ~= 178 ohm;
- X_L at 1.65 GHz ~= 187 ohm.

Current Coilcraft data for the 18-nH part:
- SRF typical ~= 3.1 GHz;
- Q typical ~= 57 at 900 MHz;
- Q typical ~= 62 at 1.7 GHz;
- DCR max ~= 0.23 ohm;
- Irms ~= 420 mA.

Interpretation:
18 nH is a credible G0 bias-choke seed for 1.15–1.65 GHz,
but its 3.1-GHz self resonance lies inside the wider 0.1–6-GHz device range.

Therefore the actual Coilcraft/vendor model, not an ideal inductor, is mandatory for the assembled wideband stability model.

## 6. Package-ground seed

Hard:
each QPL9547 backside paddle gets local vias into a branch-local RF ground region.

Datasheet reference:
- 0.35-mm drill;
- 0.25-mm finished plated-through diameter.

Do not freeze via pad diameter or via count until the selected fabricator's annular-ring rules are applied.

The first landing-zone model shall not use the old "ground continues down the stalk and only closes near the half-lap" topology as its baseline.

## 7. Mechanical conflict discovered before simulation

The existing orthogonal half-lap mechanics create a real conflict with local common-ground closure.

From the accepted B1M/M0 geometry:
- Pol-A has intact central FR4 immediately below the feed/LNA region and can support an early ground merge;
- Pol-B's complementary half-lap slot removes central FR4 over a long interval beginning near v ~= 12 mm and extending to about v ~= 34.6 mm.

That is why M0/M1 forced the Pol-B ground merge far down the stalk.

For a real active device this is no longer acceptable as an unquestioned baseline.

QPL9547 paddle grounding is local; therefore the mechanical interlock must adapt to the active RF-ground requirement if needed, not vice versa.

## 8. Ground-topology candidates for A0-E1/A0-E2

Do not sweep matching dimensions yet.

Study only a small ground-topology set:

### G-L0 — branch-local ground baseline

Each LNA paddle:
-> local via cluster
-> its own branch ground rail.

No forced remote common merge is used to define the device ground quality.

This is the minimum physically valid LNA landing-zone model.

### G-L1 — short local/common connection

Provide a short, manufacturable common RF-ground connection close to the two LNA cells.

Possible implementation families:
- preserve / create a local FR4 bridge window in the half-lap mechanics;
- use an intentional short grounded interconnect/jumper/edge-plated feature;
- use a local grounded metal/shield feature only if it is modeled as an RF object.

The exact family is NOT selected yet.

### G-R — remote lower-stalk merge sentinel

Retain the M0/M1 remote merge only as a sentinel / comparison case.

It is not the baseline.

The first mechanism question is:
does a physically short local ground remove the pathological long-return behavior while retaining the mechanical B architecture?

## 9. Half-lap policy

The half-lap interlock is no longer an untouchable RF-independent Class-A detail.

Frozen:
- orthogonal two-stalk architecture;
- radiator-to-stalk and stalk-to-reflector mechanical support concept.

Released if required by active-ground evidence:
- exact slot extent / split height / local bridge window near the active electronics.

A small local mechanical revision is preferred over forcing the first-stage LNA to use a demonstrably poor remote RF return.

## 10. Landing-zone footprint seed

Rev-D package facts:
- package body: 2.00 x 2.00 mm nominal;
- exposed paddle: 0.80 x 1.60 mm nominal;
- terminal pitch: 0.50 mm BSC;
- terminal nominal geometry shown in Rev-D page 8;
- recommended PCB metal/solder-mask pattern shall be transcribed from the Rev-D drawing before BUILD.

A0-E1 shall use the Qorvo recommended land pattern as G0 unless a manufacturing audit requires a documented modification.

Do not scale the footprint to fit the stalk.

The stalk/local electronics geometry must fit the real package footprint.

## 11. First A0-E1 model extent

One-LNA landing-zone coupon, before radiator integration:

include:
- 1.00-mm FR4 stalk section;
- Qorvo G0 RF-IN/RF-OUT/Vbias/NC/backside-paddle land pattern;
- paddle via cluster;
- input/output 0402 capacitor pads;
- VDD-choke pads;
- local 100-pF / 1-uF decoupling pad region;
- dedicated decoupling ground-via locations;
- short upstream/downstream MSL;
- local branch ground;
- nearby keepout representation of the second LNA cell.

Do NOT include:
- active transistor inside CST;
- full radiator;
- full lower stalk;
- remote M0/M1 bridge;
- final shield;
- array periodic boundary.

Purpose:
validate the landing-zone EM / ground / port definition cheaply before integration.

## 12. A0-E1 reference planes

For the one-LNA coupon:
- E_UP: upstream line reference;
- P_IN: QPL9547 RF-IN device-lead plane;
- P_OUT: QPL9547 RF-OUT device-lead plane;
- E_DN: downstream line reference.

All are single-ended to the finite local RF ground.

Component gaps may introduce additional lumped/circuit reference pairs as needed.
Their port count must be frozen before BUILD.

For the later twin-LNA integrated model:
P1A_IN / P1A_OUT / P1B_IN / P1B_OUT remain the authoritative device-lead planes.

## 13. Before BUILD still required

1. exact machine transcription of Rev-D land/mask pattern;
2. choose a manufacturable paddle-via count/pad size for the actual PCB vendor;
3. draw G-L0 and at least one G-L1 mechanical concept;
4. choose initial 0402 DC-block candidate with broadband model;
5. freeze the exact E1 port set if component gaps are represented as circuit ports;
6. define copper conductivity/solder assumptions;
7. freeze clearance/interference predicates.

Until these are complete:
BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false.
