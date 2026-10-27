# M7C direct-sample stage evidence

Diagnostic: H_NUM_SUPPORTED_M7C_DIRECT_SAMPLE. Original science: HOLD_M7C_GUARD.

One formal solver invocation, no geometry build, zero automatic retries. The original `result_packet.json` remains HOLD_ENTRYPOINT. Its exception and solver invocation are preserved. No solver or CST application was launched for either read-only recovery.

- `AUTHORIZATION_STAGE_CONTRACT.json`, `task_packet.json`, original runner/forensics records: immutable one-shot authority and failure history.
- `FORMAL_EXCEPTION.txt`, `SOLVER_INVOCATION.json`, `PRESOLVE_SUMMARY.json`: solver completed; initial get_data unpacking failure; geometry/material/port persistence checks.
- `qualification_recovery_v01/`: separate-x/y extraction; conservative native-log-format HOLD retained.
- `qualification_recovery_v02/`: CPU-only verification of the direct solver's `Sample N of 16` records and all eight excitations. Original criteria unchanged; all 11 checks pass.
- `FINAL_INTEGRITY.json`: canonical complete-project identity, native snapshot hashes, protected old-source checks and final process/free-space snapshot.
- `V02_PROTECTED_RECEIPT.json`: qualified derived files retained on NW with matching hashes and zero new solver calls.
- `offline_analysis/`: independent result replay, exact complex comparison CSV, selected-point modal context and scientific SVG.
- `CLOSEOUT.json` / `SHA256SUMS`: final provenance and evidence identity.

Reproduce V02 from the retained V01 snapshot and a byte-identical copy of the protected old M7C broadband CSV:

```sh
python3 scripts/recover_m7c_direct_sample_log_semantics_v02.py \
  --source evidence/M7C_DIRECT_SAMPLE_RESULT_20261027_V01/qualification_recovery_v01 \
  --old-csv /absolute/private/path/to/old_M7C.csv \
  --output /absolute/private/path/to/new-cpu-recovery
```

The old CSV must have SHA256 `711365d2f3336a5afed0cf94e2394f0ae75e0691421c8729af6dda2425a74cae`. V02 never starts CST. The standalone V01 reader accepts only the locked new solved SHA and can be replayed with CST's bundled Python and a fresh evidence directory; it never calls a solver. Do not replay the original formal packet or entrypoint.

Native solver log byte authority is the base64-preserved output, rather than a Windows-rendered text copy with translated line endings. Original raw native files and all large CST payload remain in the protected NW project run directory listed in FINAL_INTEGRITY.
