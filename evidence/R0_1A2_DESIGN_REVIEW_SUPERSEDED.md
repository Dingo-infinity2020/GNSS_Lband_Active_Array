# R0.1A2 Design Review — V0.2 Scientific Topology Superseded

Status: **HOLD_R0_V02_SCIENTIFIC_TOPOLOGY_MISMATCH**

The H01 V0.2 execution in `evidence/r0_1a2_h01_20260922_2123/` remains a valid runtime/replay result:

- CST 2022.5 build succeeded,
- save/close/fresh-reopen succeeded,
- final inventory was 2 solids,
- 0 ports,
- no solver run.

However, direct design-side review of CHARTS Fig. 2(a) shows that V0.2 still under-resolved the slot topology.

## V0.2 error

V0.2 modeled:
- 4 outer slots, one continuous slot per board side,
- 4 inner radial slots,
- 8 total slot subtractions.

The fabricated board in Fig. 2(a) visibly shows:
- **2 separate outer-slot segments per board side**,
- therefore **8 outer slot segments total**,
- plus **4 inner radial slots**,
- therefore **12 disconnected slot segments total**.

Each board side retains a conductor bridge near its midpoint. Four corner regions also remain connected.

## Consequence

V0.2 status is narrowed to:

`PASS_R0_V02_EXECUTION_REPLAY_ONLY`

It is not accepted as the final CHARTS topology reconstruction.

The scientific gate remains HOLD until V0.3 12-slot topology is built and visually reviewed.

No solver is authorized.
