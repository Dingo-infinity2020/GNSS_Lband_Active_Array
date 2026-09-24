# NW Workspace Cleanup Record — 2026-09-24

SimulationOps workspace lifecycle: 0.2.4

Task node:
- R1A1 BUILD-ONLY PASS
- operational baton returned to DESIGN

Host:
- NW / DESKTOP-GBTI6Q4

## Inventory

| Workspace | Files | Bytes | Recovery evidence |
|---|---:|---:|---|
| `D:\GNSS_Lband_Active_Array\_r0_1a_h01_work` | 99 | 1,090,506 | `evidence/r0_1a_h01_20260922_2052/` |
| `D:\GNSS_Lband_Active_Array\_r0_1a2_h01_work` | 98 | 1,083,777 | `evidence/r0_1a2_h01_20260922_2123/` |
| `D:\GNSS_Lband_Active_Array\_r0_1a3_h01_work` | 98 | 1,158,651 | `evidence/r0_1a3_h01_20260922_2158/` |
| `D:\GNSS_Lband_Active_Array\_ref_cui_r0b_work` | 99 | 2,247,044 | `evidence/ref_cui_r0b_h01_20260923_1341/` |
| `D:\GNSS_Lband_Active_Array\_r1a1_scaled_aperture_work_recovery` | 98 | 1,166,773 | `evidence/r1a1_recovery_dc_nw_20260924_1113/` |

`_r1a1_scaled_aperture_work` was not present.

## Recovery proof

All listed workspaces are build-only execution copies.

For each:
- source macro/script is in trusted remote Git,
- compact execution evidence is in trusted remote Git,
- CST build path/hash is recorded in the corresponding return report/evidence,
- no solver result or unique physics output exists only inside the work directory,
- no active process references the directories at inventory time.

The latest R1A1 build is reproducible from:
- source macro `source/cst/R1A1_CHARTS_SCALED_APERTURE_BUILD_ONLY_V01.mcr`,
- source HEAD recorded in evidence,
- SimulationOps stage contract.

## Lifecycle decision

```text
ARCHIVE_MODE=REFERENCE_ONLY
WORKSPACE_STATE=PURGE_READY
PURGE_ALLOWED=true
CHECKOUT_PURGE=false
BUILD_WORKDIR_PURGE=true
```

The Git checkout itself is retained as `CHECKPOINTED` because R1A2 will continue on NW.

Only the five listed underscore-prefixed build work directories are authorized for deletion.

## Post-cleanup requirement

After deletion:
- verify each path is absent,
- verify project Git checkout remains present and clean after sync,
- record completion below / in a successor commit.


## Cleanup completion

Completed on NW via Desktop Commander after pulling the authorization record.

Purged and verified absent:

- `D:\GNSS_Lband_Active_Array\_r0_1a_h01_work`
- `D:\GNSS_Lband_Active_Array\_r0_1a2_h01_work`
- `D:\GNSS_Lband_Active_Array\_r0_1a3_h01_work`
- `D:\GNSS_Lband_Active_Array\_ref_cui_r0b_work`
- `D:\GNSS_Lband_Active_Array\_r1a1_scaled_aperture_work_recovery`

Post-cleanup checks:

```text
all_target_paths_exist=false
project_checkout_exists=true
project_checkout_clean=true
active_task_process_dependency=none
```

Lifecycle result:

```text
BUILD_WORKDIR_STATE=PURGED
PROJECT_CHECKOUT_STATE=CHECKPOINTED
PURGE_COMPLETED=true
```
