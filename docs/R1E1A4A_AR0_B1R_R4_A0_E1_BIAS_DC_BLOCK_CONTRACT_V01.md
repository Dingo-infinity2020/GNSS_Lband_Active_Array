# R4-A0-E1 QPL9547 Bias / DC-Block Circuit Contract V0.1

Status: G0 CIRCUIT TOPOLOGY FROZEN

## QPL9547 operating reference

- VDD = 5 V
- IDD = 65 mA typical
- FDD baseline: always-on LNA

## RF input

Source/antenna-side node
-> C_IN
-> QPL9547 pin 2 RF-IN

G0 C_IN:
- 100 pF
- 0402
- C0G/NP0
- 50 V class

Selected G0 component family:
Murata GRM1555C1H101JA01#

Why:
- 0402 / 1005M
- 100 pF +/-5%
- C0G
- 50 V
- vendor provides SPICE and S-parameter product data

A0-C0 may use an ideal 100-pF capacitor.
A0-C1 shall use the Murata broadband model.

## RF output / VDD node

QPL9547 pin 7 RF-OUT/VDD is one RF/DC node.

Two branches leave pin 7:

RF:
pin 7
-> C_OUT 100 pF
-> downstream RF node/load

Bias:
pin 7
-> L1 18 nH
-> VDD_DECOUPLED node

G0 C_OUT:
same Murata 100-pF family as C_IN.

G0 L1:
Coilcraft 0402CS-18NXGRW
- 18 nH
- 2%
- SRF typ 3.1 GHz
- DCR max 0.23 ohm
- Irms 420 mA

Wideband stability MUST use a vendor/Modelithics/SPICE/S-parameter model, not ideal L.

## VDD decoupling

Qorvo EVB topology retained:
VDD_DECOUPLED
-> 100 pF RF decoupling to local ground
-> 1.0 uF bulk/local decoupling to local ground

For G0:
- 100-pF RF decoupler uses the Murata C0G family
- 1-uF part remains topology-only until a low-ESL 0402 vendor model is selected

Each RF 100-pF shunt capacitor gets its own short ground via.

## Vbias

Qorvo EVB:
VDD_DECOUPLED
-> R4 = 3.32 kOhm
-> pin 1 Vbias

For small-signal QPL9547 S2P co-simulation:
- 5 V / 65 mA bias behavior is already embedded in the measured device two-port
- pin-1 is not an independent S2P circuit port

Therefore A0-E1 physically reserves/models the pin-1 land and nearby R4 routing/pads,
but A0-C1 does not create a fictitious third active-device RF port.

## Shutdown pin

FDD baseline:
- pin 6 is tied to local ground with a short connection

This matches Qorvo's allowed FDD configuration.

No TDD control network is included in A0-E1 baseline.

## NC pins

Qorvo permits pins 3,4,5,8 to float or be grounded.
The QPL9547 EVB schematic grounds 3,4,5,8.

G0 A0-E1 baseline:
- pins 3,4,5,8 PCB lands are tied to local RF ground

This is a layout/ground choice, not an active-device port.

## EM / circuit ownership

EM:
- all PCB lands
- all traces
- via barrels
- component pads
- local ground

Circuit:
- C_IN
- QPL9547 2-port
- C_OUT
- L1
- RF decoupling C
- bulk C
- source/load

The physical component gaps remain open in the pure EM geometry and are connected in circuit co-simulation.
