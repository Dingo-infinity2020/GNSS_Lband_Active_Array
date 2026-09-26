# R0.1A Design Review — Scientific Topology Superseded

Status: **HOLD_R0_TOPOLOGY_SCIENTIFIC_MISMATCH**

The H01 execution result in `evidence/r0_1a_h01_20260922_2052/` remains valid as an execution/replay result:

- CST 2022.5 accepted the macro body,
- save/close/fresh-reopen worked,
- 9/9 intended V0.1 objects persisted,
- 0 ports,
- no solver run.

However, after review against CHARTS Fig. 2(a), the V0.1 scientific topology is rejected.

## What V0.1 got wrong

V0.1 modeled:
- four electrically/geometrically separate petal solids,
- four separate passive-ring bars,
- a continuous diagonal gap network,
- a 40 mm central square opening.

Fig. 2(a) instead provides strong visual evidence for:
- one continuous square PCB/aperture silhouette,
- four outer elongated slots,
- four inner elongated slots,
- slot segments are interrupted and do not join into one continuous cut network,
- the central electronics region is not a large through-board square hole.

Therefore the old 9-solid topology changes the current path and mechanical topology and cannot be used for EM validation.

## Consequence

The prior final status is narrowed to:

`PASS_R0_1A_EXECUTION_REPLAY_ONLY`

and is **not** a CHARTS topology PASS.

The scientific gate is now:

`HOLD_R0_TOPOLOGY_SCIENTIFIC_MISMATCH`

until V0.2 continuous-slotted-plate build-only is visually validated.

No solver is authorized.
