# R4-A0-E1 Formal Build HOLD Handoff — 2026-09-28

Status: `HOLD_R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_ONLY`

The one authorized formal A0-E1 build-only invocation was consumed on NW. No retry and no solver invocation occurred.

## What passed

- frozen V02 macro executed and produced the expected 36-solid inventory;
- component counts and materials match the frozen contract;
- four drilled/plated via objects remain and drill-tool solids are consumed;
- result tree is empty;
- artifact SHA256 is stable across fresh reopen.

Protected artifact:
`D:\GNSS_R4A0E1_20260928_ARTIFACTS\R1E1A4A_AR0_B1R_R4_A0_E1_ONE_LNA_LANDING_ZONE_BUILD_ONLY_V02.cst`

SHA256:
`f5ee6fceab2c26db5d4d63365e37abec65b87698633c577e1ca87613b86a9745`

## What held

1. Frozen contract requires six discrete ports; fresh-reopen audit reports `PORT_COUNT=0`.
2. All ten destructive-on-copy `Solid.Intersect` checks returned the same CST automation error `-2147418113`. Their reported intersection volume is zero, but this is not accepted as zero-overlap proof because the Boolean command itself errored.

This is currently classified as an unresolved BUILD/audit HOLD, not a physics failure.

## Stop boundary

- BUILD authorization is consumed and closed.
- SOLVE remains unauthorized.
- Do not rebuild or retry.
- Preserve the NW artifact/evidence in place.
- Next work is design/read-only recovery planning for port creation/persistence and a non-ambiguous intersection qualification method.
- A new formal build requires a separately frozen recovery contract and explicit authorization.
