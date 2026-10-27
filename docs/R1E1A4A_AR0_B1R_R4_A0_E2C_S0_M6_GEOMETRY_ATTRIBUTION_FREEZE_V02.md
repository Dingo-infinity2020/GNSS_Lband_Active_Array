# R4-A0-E2C-S0 M6 Geometry Attribution Freeze V0.2

Status: PASS_M6_V02_EXACT_ENTITY_ATTRIBUTION_READY

M6 V0.1 is superseded because its primitive parser omitted CST Extrude copper and produced a false zero-entity PASS.

V0.2 follows a literature-style structure-evolution/current-path methodology.

## Diagnostic architecture

Use Pol-A/E2A as the observer network. Do not create Pol-B ports.

### M6-D1-SIG

Add only the exact Pol-B PRE-CIN signal-extension entities listed in the V0.2 evidence.

Question: does opposite-pol signal metal alone drive the observer toward the full-E2C mixed-mode degradation?

### M6-D2-GND

Add only the exact Pol-B local-ground/backside/via entities listed in the V0.2 evidence.

Question: does opposite-pol return/ground metal alone drive branch imbalance and common-mode conversion?

### Interaction decision

Full E2C is already the combined SIG+GND(+device) endpoint.

If D1 and D2 are both weak but full E2C is severe, the primary mechanism is a signal-ground interaction/composite eigenchannel and the next design action should target that interaction, not either metal class independently.

If future diagnostic solves are authorized, include surface-current monitors at L2, approximately 1.3384 GHz, and L1 so that the S-parameter attribution is backed by current-path evidence.

No geometry optimization is authorized in M6.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
