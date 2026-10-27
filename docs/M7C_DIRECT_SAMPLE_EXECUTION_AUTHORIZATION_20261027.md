# M7C direct-sample diagnostic execution authorization — 2026-10-27

Status: ONE_SHOT_SOLVE_GRANTED_AFTER_HOST_QUALIFICATION.

The user explicitly confirmed the direct-sample plan and delegated BUILD/SOLVE decisions until this stage is complete. Exact scope is recorded in `M7C_DIRECT_SAMPLE_STAGE_PLAN_20261027.md`. Codex selects no geometry BUILD and exactly one new same-geometry diagnostic SOLVE; this is a concrete invocation under that explicit authority, not inferred from a previous consumed grant.

- stage: `R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7C_DIRECT_SAMPLE_DIAGNOSTIC_V01`
- grant: `GNSS-M7C-DIRECT-SAMPLE-SOLVE-GRANT-20261027-01`
- packet: `GNSS-M7C-DIRECT-SAMPLE-20261027-V01`
- qualified source commit: `d8fdb3f17a8084c910be41701f6c01e9f91181f4`
- entrypoint: `scripts/run_m7c_direct_sample_solve_v01.py`
- entrypoint SHA256: `8905fa6bd7d13a01eeda1ce6c814af59b8642d48dd0ea6022f1c48eb5e3927e6`
- qualification: `evidence/M7C_DIRECT_SAMPLE_PREPARATION_20261027_V01/nw_qualification/RECEIPT.json`, PASS; control Python and CST Python, 7 tests each; six qualification commands; 32 host/source/storage checks.
- granted_at: `2026-10-27T02:17:39Z`; expires_at: `2026-10-27T08:17:39Z`.

Scientific freeze is unchanged: reviewed M7C BUILD source, frozen 12-port/8-source/4-load network, fifteen diagnostic frequencies plus the 1.8-GHz mesh-adaptation point, `Discrete samples only`; no geometry/material/port/linear-precision change. The old M7C science remains HOLD_M7C_GUARD regardless of this diagnostic's outcome.

BUILD_AUTHORIZED=false; SOLVE_AUTHORIZED=true only for this matching live grant. Fresh project-owned C: NTFS output; output/TEMP same-volume reservation remains 40 GiB. Native contract-check, validate and dry-run must pass before the sole run_solver call. Zero automatic retries; no extra frequencies or source choices.

The entrypoint closes its owned project/environment in finally blocks. Phase budgets are conservative elapsed audits (presolve 600 s, solver 7200 s, qualification 900 s), with generic runner 9000-s outer fail-safe for an unreturned call. There is no claim of an independent asynchronous solver-kill watchdog. Stable execution is awaited without recurring native log/process polling.

At any terminal runner outcome: close the live grant, reconcile actual solver invocation count, preserve the result and global one-shot identity, and record the diagnostic outcome. If the solver completed but post-processing failed, only zero-solver read-only extraction recovery is within scope; do not rerun the solver. No automatic geometry/topology/optimization/LNA/CST251/cleanup/relocation follows.


## Consumption closeout

The one formal invocation ended 2026-10-27T02:35:09Z. Solver completed once (614.187 s); the transaction is HOLD_ENTRYPOINT because post-solve extraction raised ValueError while unpacking a get_data() representation. Grant is CONSUMED and live BUILD/SOLVE are false, active_grant=null. Solved SHA256 c21fa9f047d83f4f3776d5e6ef5718e8924aaf8e54f0ad8cbb7cb6a7c6681851 is locked. Only zero-solver read-only qualification recovery remains.
