# R4-A0-E3D Next Simulation Question and Minimum-Network Freeze V0.1

Status: OFFLINE DECISION FROZEN — NO SOLVE AUTHORIZATION
Date: 2026-10-01

## First-principles question

The next solver invocation should answer only:

Does simultaneous installation of the complete frozen Pol-A and Pol-B landing-zone hardware materially perturb the already-qualified isolated passive source-side behavior?

This is the remaining geometry/coexistence uncertainty after:
- E2C R7 BUILD_ONLY PASS
- human geometry review PASS
- E3A electrical-closure PASS
- E3B port-authority PASS
- E3C branch-local ground-topology PASS

It is not yet a product input-match, noise-match, or assembled active-stability solve.## Minimum sufficient network

Raw R7 build interface = 24 ports.

For the coexistence question, reduce the solve copy to 12 ports:
per branch retain
- E_UP as source
- P_IN as source
- P_OUT as passive 50-ohm load-only

Per branch remove ports
- E_DN
- B_VDD
- B_VBIAS

Physical pads and geometry remain unchanged/open.

Four branches therefore give:
- 12 response ports
- 8 excited source ports
- 4 P_OUT load-only ports
- 96 required complex response traces

No load-only P_OUT port may be excited.## Why not full 24x24 now

A full raw 24x24 extraction would spend solver time on output/bias nodes that are not required to decide the coexistence question.

It would also tempt interpretation of E_DN/B_VDD/B_VBIAS behavior before the circuit-domain C_OUT/L1/decoupling/R4 models have formal authority.

The 12-port sentinel still observes:
- own-pol E_UP/P_IN perturbation
- branch imbalance
- differential/common conversion
- cross-pol P_IN/P_OUT-load coupling
- new narrow resonance/coupling mechanisms

Therefore it is the minimum network that preserves the decision-relevant physics.

## Why not active co-sim first

D0 shows that the formal active model set is not yet complete:
- dense raw QPL9547 S2P is not present on NW/repo
- passive broadband component models are not present

Running active co-sim first would mix a geometry/coexistence question with provisional circuit models and weaken attribution.## Frozen comparison authority

Compare the combined E2C sentinel against the already-qualified isolated Pol-A and Pol-B passive baselines on the same frequency grid.

Primary review metrics:
- own-pol max complex S-block perturbation
- differential/common conversion degradation
- branch return-magnitude imbalance
- narrow unintended-coupling excursions
- cross-pol device-side coupling

Existing review thresholds from the frozen E2C sentinel contract remain unchanged.

No geometry tuning is allowed from a mere REVIEW result. REVIEW first requires offline mechanism attribution.

## Decision

PASS_E3D_NEXT_SIMULATION_IS_E2C_12PORT_COEXISTENCE_SENTINEL

No new BUILD_ONLY is required before this solve.
No full 24x24 extraction is justified before this sentinel.
No active co-sim should precede it.

This document does not authorize SOLVE.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false

After a future sentinel PASS:
1. restore/qualify device/passive component models;
2. establish full passive-network authority required for C1 active feedback/stability;
3. then active feasibility/co-simulation.