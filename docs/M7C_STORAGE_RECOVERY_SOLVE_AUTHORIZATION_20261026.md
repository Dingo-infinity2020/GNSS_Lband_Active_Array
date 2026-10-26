# M7C storage recovery SOLVE authorization — 2026-10-26

Status: SOLVE_AUTHORIZED_M7C_RECOVERY_ONE_SHOT_PENDING_PACKET_VALIDATION

The human user explicitly wrote **授权求解** in the current conversation after reviewing the completed recovery preparation package. This grants exactly one NW-local same-geometry M7C infrastructure-recovery diagnostic SOLVE, with zero automatic retries. Build, optimization, material A/B, LNA integration, CST251 execution and automatic next-stage authority remain closed.

- grant id: `GNSS-M7C-STORAGE-RECOVERY-SOLVE-GRANT-20261026-01`
- packet id: `GNSS-M7C-STORAGE-RECOVERY-20261026-V01`
- stage: `R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7C_STORAGE_RECOVERY_SOLVE_V01`
- qualified source: `4ab2648015955e1e6c8f10864f063e916f4d64f1`
- entrypoint SHA256: `85e02268de7e13bbc3e26fad9d3b98522536a1850d32f4bcd34eee79b555e605`
- manifest SHA256: `7fde455373c882724c7098f79c779fd58179ce4dff70a7d151a66e9acc4d79ac`
- granted at: `2026-10-26T14:56:44Z`
- expiry: `2026-10-26T20:56:44Z`
- reviewed `.cst`: `ee25237bc5f70e457adadf3745faf3d64f1401bb47717da5322d7347ba50ce98`
- output: `C:\GNSS_Lband_Active_Array\runs\formal\solver_runs\M7C_STORAGE_RECOVERY_20261026_V01`

The recovery manifest, geometry, ports, solver configuration, evaluator and frozen Sdc/Sdd/guard criteria are unchanged. Qualified source and later authorization checkout HEAD are separate identities; the packet binds both the qualified source and exact authorization contract/checkout bytes.

Before launch: native contract-check, packet generation from this live grant, native validate and `run --dry-run` must PASS. Dry-run is not the formal invocation. The formal `run` occurs once only under the global execution lock. A terminal outcome closes this grant whether consumed or unconsumed; no packet replay or replacement grant is implied.

Use direct SSH as explicitly authorized by the user. Follow `M7C_STORAGE_RECOVERY_PREPARATION_V01.md` for storage reservations and acceptance. Stop after qualification/modal classification and preserve all failure evidence.
