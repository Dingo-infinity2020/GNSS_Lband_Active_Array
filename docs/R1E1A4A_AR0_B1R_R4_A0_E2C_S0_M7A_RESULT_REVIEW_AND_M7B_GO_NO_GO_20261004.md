# M7A Result Review and M7B Go/No-Go — 2026-10-04

## Status

**GO_M7B_BUILD_ONLY_AWAIT_AUTH**

This is an offline scientific/mechanism review only. It does not grant BUILD or SOLVE permission.

## Inputs

- frozen M7 candidate plan: `docs/R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7_CORRECTIVE_CANDIDATE_FREEZE_V01.md`
- M7A diagnostic solve freeze: `docs/R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_DIAGNOSTIC_SOLVE_FREEZE_V01.md`
- M7A canonical result classification in `execution/stage_contract.json`: `REJECT_M7A_INNER_EDGE_LEVER`
- M7B frozen manifest: `execution/R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_CIN_PAD_CLEARANCE_MANIFEST_V01.json`
- M7 candidate static audit: `PASS_M7_CORRECTIVE_CANDIDATE_STATIC_FREEZE`

No Desktop Commander, CST execution, new result extraction, or solver rerun was used for this review.

## What M7A actually established

The M7A classifier was frozen before the solve. `REJECT_M7A_INNER_EDGE_LEVER` is only reached when:

1. numerical hard gates pass;
2. the narrow-resonance guard passes;
3. the primary corrective gate fails;
4. none of the primary reductions reaches even 10%; and
5. the secondary own-pol source-side complex-deviation improvement also fails.

Therefore M7A is not a marginal miss and not a numerical HOLD. It falsifies the **upstream center-facing backside-ground edge** as a useful corrective lever at the tested frozen geometry.

The exact underlying metric values remain in the formal host-side qualification/result packet and are not invented here. This review deliberately uses only the committed classifier semantics and immutable project evidence.

## Mechanism synthesis: M6 + M7A

M6 established:

- pre-CIN signal-only perturbation: weak;
- ground/backside/via-only perturbation: intermediate;
- ground-only frequency dependence is not a scaled copy of the full severe E2C response.

That already favored a composite signal/return-path interaction over a single isolated conductor defect.

M7A then removed one specific ground hypothesis: the center-facing upstream backside-ground edge does not materially suppress the severe mode. Because the M7A geometry left signal copper, CIN pad, package ground, spokes, vias, and outer ground perimeter unchanged, its rejection does **not** falsify terminal-local signal/ground capacitance.

The useful updated picture is therefore:

`composite signal/return-path interaction remains plausible`

but

`upstream inner-edge overlap is not the controlling corrective lever`.

## Why M7B remains scientifically justified

M7B changes a different local observable: it opens a guarded backside-ground projection window directly under each frozen `CIN_UP_PAD` while retaining upstream MSL ground, package ground, spokes, vias, signal copper, and overall ground perimeter.

This directly tests whether **local CIN signal-to-return shunt capacitance** is a necessary resonant element in the 1.2–1.4 GHz composite mode.

M7B is therefore not a retry of M7A and not an arbitrary ground-shape optimization. It is the second and final pre-registered mechanism test.

## Frozen M7B BUILD-only contract

Parent:
`cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c`

Only these four solids may be modified:

- `E2C_A_P_BackGround:LOCAL_BACK_GROUND`
- `E2C_A_N_BackGround:LOCAL_BACK_GROUND`
- `E2C_B_P_BackGround:LOCAL_BACK_GROUND`
- `E2C_B_N_BackGround:LOCAL_BACK_GROUND`

Required BUILD invariants:

- four guarded CIN-projection clearance tools only;
- all four tools consumed;
- final solid count = 177;
- raw port count = 24;
- radiator unchanged;
- all signal copper unchanged;
- package lands/local top ground/vias/bias-output copper unchanged;
- no solver command;
- fresh reopen;
- CST geometry/intersection gate;
- human 3D geometry review;
- stop before SOLVE.

## Authorization boundary

Current live permissions:

- BUILD_AUTHORIZED = false
- SOLVE_AUTHORIZED = false
- CST251_AUTHORIZED = false
- optimization/sweep = false
- silent retry = false

If the user later authorizes M7B BUILD, consume exactly one BUILD-only transaction and stop after automated geometry qualification plus human review. Only after a successful reviewed build should a separate M7B diagnostic SOLVE contract be frozen and a separate SOLVE authorization requested.
