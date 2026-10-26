# M7C storage recovery result — 2026-10-26

Scientific status: **HOLD_M7C_GUARD**. Runner transaction: PASS.

One formal invocation ran on NW from 23:04:46 to 23:14:18 Asia/Shanghai (9 min 32 s); zero retries. The original 2026-10-08 storage-HOLD attempt remains unchanged. This fresh recovery successfully materialized the required broadband results but did not pass the frozen scientific gate.

## Acceptance

| Gate | Result | Frozen requirement |
| --- | --- | --- |
| Data completeness | 96 complex traces, 1001 native points, 1.0–1.8 GHz; run ID 1 | complete selected 12-row/8-source network |
| Native convergence | final DeltaS 0.0154013 / 0.0149349 | ≤0.02 twice consecutively |
| Numerical/response hard checks | 7/7 PASS | all required |
| Symmetry preservation Sdc | **0/10 PASS** | each ≤0.25 × full-E2C delta |
| Differential restoration Sdd | **6/6 PASS**; 0.212–0.471 × M7B | each ≤0.70 × M7B delta |
| Guard | **20.2398 dB FAIL**; S2,5; 1.2088–1.2584 GHz | new window excursion ≤6 dB |
| Secondary worst raw delta | 0.854548 FAIL | ≤0.656703 |

All comparisons use identical native grids. The secondary raw metric does not replace the primary families or guard. Guard failure takes precedence over partial-improvement classification under the unchanged evaluator.

## Interpretation and limits

M7C reduces the M7B differential-loading penalty by about 52.9–78.8% at all six frozen Sdd checks. It does not retain the intended symmetry benefit: PolA Sdc fractions are 0.343–0.646 of full E2C, and PolB fractions are 1.127–1.415, all above the 0.25 limit. The guard fails by a wide margin. The local-return-island topology is not promoted.

The source-side reciprocity maximum is 0.00390091, below its frozen 0.02 limit. Loaded-power upper-bound closure passes. Cross-pol device coupling peaks at -60.55 dB; this does not override the failed own-pol modal/guard gates.

Native output reports two warnings, preserved in the evidence:

1. Some lossy-conductor intersection edges are modeled as infinitely thin PEC wires. This remains a physical-model interpretation limitation and a relevant offline inspection target; causality for the guard feature is not established.
2. YZ matrices cannot be calculated because all S-parameter columns were not requested. The frozen network intentionally excites eight sources and keeps four load-only ports; its required 96 traces are complete. No full 12×12 or YZ completeness claim is made.

Mesh logs additionally preserve missing-size/max-edge warnings and graphical feedback-item messages. The unchanged numerical hard gates pass; these messages are not erased or reinterpreted as proof of model accuracy.

## Provenance and integrity

- qualified production source: `4ab2648015955e1e6c8f10864f063e916f4d64f1`
- authorization checkout: `339a799112be7f3dbe4f20be6df5332337e254b2`
- grant: `GNSS-M7C-STORAGE-RECOVERY-SOLVE-GRANT-20261026-01`
- packet: `GNSS-M7C-STORAGE-RECOVERY-20261026-V01`
- source BUILD SHA256: `ee25237bc5f70e457adadf3745faf3d64f1401bb47717da5322d7347ba50ce98`
- solved `.cst` SHA256: `90af39c8447d7245d6e1eb6f77930e3789b6c11c64ea14a7d314b33b07a0e5fa` (153,988 bytes)
- solved companion: `cc2d4e501afb14f649c3f183b3cccb33302d12489e3f657ad84da8cda980a87e`; 609 files; 12,407,270,374 bytes; `SIMOPS_TREE_ID_V1`
- extracted response CSV SHA256: `711365d2f3336a5afed0cf94e2394f0ae75e0691421c8729af6dda2425a74cae`; 7,883,596 bytes

Solved file hashes agree before/after qualification and with native expected-output evidence. Post-run source, source-companion and reference CSV checks all PASS. Complete results remain protected in the project-owned C: run directory. Final C: free space was 127,344,459,776 bytes. No archive/relocation/cleanup was performed; long-term storage qualification remains a separate task.

## Closeout and next boundary

The one-shot SOLVE grant is CONSUMED and closed. BUILD_AUTHORIZED=false, SOLVE_AUTHORIZED=false, active_grant=null. Global execution identity is not replayable.

Next work is offline review of S2,5 in the guard window, polarization asymmetry and the native thin-PEC-edge approximation. This result authorizes no geometry change, new solve, sweep, LNA integration or automatic next stage.

See `evidence/M7C_STORAGE_RECOVERY_SOLVE_20261026/CLOSEOUT.json`, `SCIENCE_SUMMARY.json`, `MODAL_ANCHOR_SUMMARY.csv` and the untouched native evidence.
