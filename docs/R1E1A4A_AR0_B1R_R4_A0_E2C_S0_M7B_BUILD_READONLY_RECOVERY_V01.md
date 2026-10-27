# M7B BUILD read-only qualification recovery V0.1

## Canonical status

**PASS_M7B_BUILD_READONLY_QUALIFICATION_RECOVERY_AWAIT_HUMAN_REVIEW**

Exactly one formal M7B BUILD_ONLY transaction was executed. The SimulationOps runner returned `HOLD_ENTRYPOINT` with exit 4 and conservatively consumed the BUILD grant. No solver authorization was present and solver invocation count is zero.

## Why the runner held

The build artifact itself satisfied every automated invariant except the M7B volume-loss expectation. The first M7B-specific runner calculated expected removal using the **clearance tool depth**:

`1.10 x 1.00 x 0.07 = 0.077 mm^3`.

That is the wrong physical thickness for the object being subtracted.

The frozen E2A, E2B and E2C build sources define each backside `LOCAL_BACK_GROUND` as copper extruded to **0.035 mm** thickness. The M7B cutter is intentionally 0.07 mm deep so that it fully penetrates that ground; cutter depth is not removed-material thickness.

Therefore the correct expected removal is:

`1.10 x 1.00 x 0.035 = 0.0385 mm^3`.

Observed losses were:
- E2C_A_N: 0.03849999999999998 mm^3
- E2C_A_P: 0.03849999999999998 mm^3
- E2C_B_N: 0.03850000000000020 mm^3
- E2C_B_P: 0.03849999999999998 mm^3

These are equal to the corrected physical expectation within floating-point roundoff and are four-branch symmetric.

## Other build evidence

PASS:
- parent gate;
- exactly 177 solids;
- exactly 24 ports;
- every expected solid queryable;
- all 173 unmodified solids preserved;
- no unexpected changed entities;
- port byte semantics unchanged;
- history persistent;
- fresh-reopen artifact hash stable;
- no solver-result files after build.

Artifact SHA256:
`5498e9c447fdd4eeb969c02701d27886e839144ebe9941c4e7f56bc7419c69ea`

## Recovery decision

This is a **read-only qualification recovery**. It does not rerun or modify the formal BUILD and does not refund the consumed BUILD grant.

Do not rerun M7B BUILD.

Current permissions:
- BUILD_AUTHORIZED = false
- SOLVE_AUTHORIZED = false

## Human review checklist

Inspect the protected M7B artifact in CST and confirm:

1. exactly four guarded windows exist, one under each corresponding `CIN_UP_PAD` projection;
2. each window is 1.10 x 1.00 mm with the frozen 0.25-mm guard around the 0.60 x 0.50 mm CIN pad projection;
3. upstream MSL ground and the overall ground perimeter remain unchanged outside those four windows;
4. all signal copper, radiator, package lands, local-ground-top copper, vias and bias/output copper are visually unchanged;
5. no window reaches paddle-via or CRF-via regions and no unintended galvanic break appears;
6. the four branches remain mirror/rotation symmetric.

A human PASS authorizes neither SOLVE nor another BUILD. After PASS, freeze the diagnostic SOLVE contract offline and stop at a separate SOLVE authorization boundary.
