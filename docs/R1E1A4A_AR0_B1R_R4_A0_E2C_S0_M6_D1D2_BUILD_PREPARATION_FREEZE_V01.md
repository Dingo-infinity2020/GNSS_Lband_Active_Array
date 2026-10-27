# R4-A0-E2C-S0 M6 D1/D2 BUILD Preparation Freeze V0.1

Status: PREPARED_OFFLINE_AWAIT_BUILD_AUTH

Parent authority is the protected E2A Pol-A BUILD_ONLY baseline:
- 107 solids
- 12 audit/reference ports
- empty result tree
- SHA256 78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804

## D1 — SIG attribution

Add exactly six Pol-B pre-CIN signal solids:
- P/N UPSTREAM_MSL
- P/N UPSTREAM_TAPER
- P/N CIN_UP_PAD

Expected final shape count: 113.

No parent solid may be modified.
No Pol-B port is added.
No monitor or solver configuration is added.

Prediction: if pre-CIN signal metal is dominant, Pol-A own-pol complex delta and E_UP differential/common degradation should move strongly toward the full-E2C severe state.

## D2 — GND attribution

Add exactly 34 Pol-B ground/via solids:
- 2 local backside grounds
- 10 grounded package lands
- 14 local-ground-top paddle/spoke/pad solids
- 8 plated vias

Only B0_Stalk:B_P_PRONG and B0_Stalk:B_N_PRONG may be modified, and only by the eight declared via-hole subtract operations.

Expected final shape count: 141.

No Pol-B port is added.
No monitor or solver configuration is added.

Prediction: if the return structure is dominant, Pol-A branch imbalance and E_UP differential/common degradation should move strongly toward full E2C while D1 remains comparatively weak.

## Future solve evidence, if separately authorized

The build artifact remains a 12-port geometry/audit model. A future solve-copy must preserve the E2A observer semantics and add no Pol-B excitation ports.

Surface-current evidence must be captured at:
- L2 1.2276 GHz
- mixed-mode region 1.3384 GHz
- L1 1.57542 GHz

The first attribution comparison is D1 vs D2 vs existing isolated E2A vs existing full E2C.

## Automation boundary

A generic future BUILD runner and runner-task-v0.2 packet generator are prepared, but the packet generator fails closed without a live BUILD grant bound to the exact stage and runner SHA.

No destructive pairwise-intersection fan-out is part of these diagnostic BUILDs. Fresh-reopen inventory, port invariance and mandatory human geometry review are the build gates.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
