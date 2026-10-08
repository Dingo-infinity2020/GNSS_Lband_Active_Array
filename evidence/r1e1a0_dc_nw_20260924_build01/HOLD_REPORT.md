# R1E1A0 Pitch Parameterization Endpoint Proof — HOLD

**FORMAL_STATUS = HOLD_R1E1A0_SOURCE_HISTORY_PARAMETER_DECLARATION**

Source HEAD:
`750a036761c3b10a37830c95415b96c1436f3d29`

Formal invocation count:
1

Exit code:
0

Runtime:
99.32 s

Solver:
NOT RUN

## Endpoint artifacts

- P088 SHA256: `65b649a28e148c8c373f06357caff36a8a4a65b06b898bf8abb96c196a3c688a`
- P100 SHA256: `3746c521ffc628eddd257f96323980ac60b5183a36f536dc77876d99b1e5f779`

Both artifact hashes are unique.

## Checks that passed for both endpoints

- immutable source hash match;
- shape count remains 3;
- non-ground radiator/substrate/feed geometry unchanged;
- ground tile volume matches target pitch;
- structure X/Y span matches target pitch;
- periodic UnitCellDs1/Ds2 match target pitch;
- X/Y boundaries remain unit cell;
- Z boundaries remain expanded open;
- port count remains 1;
- broadside theta=0, phi=45, outward;
- `unit_cell_pitch_nominal` persists as 88 or 100 after build and fresh reopen;
- build/reopen metadata is identical;
- no solver markers;
- no solver-generated result-tree items.

## Sole failed predicate

`no_pitch_history_warning = false` for both endpoints.

CST warning:
`Prevented attempt to change the value for parameter unit_cell_pitch_nominal to 94 inside history rebuild at step 1...`

Root cause:
the canonical source history still contains `StoreParameter "unit_cell_pitch_nominal", 94.0` from the early R1A1/R1A2/R1A3 construction lineage.

The direct Parameter List mutation and `RebuildForParametricChange` work numerically, but the source history is not parameterization-clean under the frozen R1E1A0 contract.

## Classification

This is a source-history/tooling HOLD, not a geometry or physics failure.

Do not relax the frozen no-warning predicate after observing results.

Do not rerun the endpoint proof against the same source.

## Recovery direction

Create a pitch-ready canonical source in which the mutable pitch parameter is declared with `MakeSureParameterExists` rather than forced by history `StoreParameter`.

Then re-freeze and rerun the endpoint proof as a separate recovery ticket.
