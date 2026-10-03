# R4-A0-E1 One-LNA Passive EM Port Contract V0.1

Status: PORT TOPOLOGY FROZEN; EXACT GLOBAL XYZ PENDING FINAL E1 PLACEMENT DRAWING

## Goal

Export a passive EM landing-zone network into which the G0 circuit components and QPL9547 2-port can be inserted without inventing a product S11 fixture.

## Port count

Five single-ended RF/circuit nodes referenced to the same finite local branch ground.

### E_UP

Upstream side of input DC-block gap.

Represents:
antenna / upstream feed node before C_IN.

### P_IN

Downstream side of C_IN through the short trace to QPL9547 pin-2 land.

Reference plane:
QPL9547 RF-IN device lead.

### P_OUT

QPL9547 pin-7 RF-OUT/VDD land.

Reference plane:
QPL9547 RF-OUT device lead.

This node fans to:
- C_OUT upstream pad
- L1 RF-side pad

### E_DN

Downstream side of output DC-block gap.

Represents post-LNA downstream RF route/load.

### B_VDD

Supply/decoupling node on the VDD side of L1.

Contains:
- L1 supply-side pad
- RF decoupling pad
- bulk-decoupling pad
- VDD feed stub

## Circuit connections

- C_IN between E_UP and P_IN
- QPL9547 S2P between P_IN and P_OUT
- C_OUT between P_OUT and E_DN
- L1 between P_OUT and B_VDD
- C_RF from B_VDD to ground
- C_BULK from B_VDD to ground

Vbias resistor / pin-1 layout is physically present but does not become a fake active RF port in the 2-port QPL9547 model.

## Port implementation

A0-E1 build shall use conductor-interface discrete/lumped reference segments that:
- terminate on the intended node copper
- terminate on the branch-local RF ground
- do not pass through finite-thickness copper
- do not cross a component body or gap
- have deterministic endpoint coordinates recorded in evidence

No 100-ohm differential port exists in A0-E1.

## Reference impedance

The exported passive EM S-matrix uses 50-ohm single-ended normalization for all five nodes.

This does not force the physical nodes to be matched to 50 ohms.

## E1 acceptance quantities

Landing-zone EM should report:
- upstream launch insertion loss E_UP <-> P_IN with C_IN replaced by its circuit model
- output launch insertion loss P_OUT <-> E_DN with C_OUT circuit model
- passive cross-coupling P_IN <-> P_OUT with active device absent
- coupling from P_OUT into B_VDD
- ground/via current distribution
- resonances across 1.0-1.8 GHz

The exact acceptance thresholds are frozen in the prebuild review, not guessed here.
