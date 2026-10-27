# R1A1 NW Build-Only Recovery — CST Bundled Python

Status: **RECOVERY_BUILD_AUTHORIZED**

Previous formal invocation:
- evidence: `evidence/r1a1_dc_nw_20260924_1111/`
- status: `HOLD_ENVIRONMENT`
- cause: Miniconda Python 3.13.9 is outside CST 2022 cst-package supported Python range.

Read-only diagnosis confirmed:

```text
D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python\python.exe
Python 3.6.0
import cst, cst.interface -> CST_IMPORT_OK
```

## Recovery changes

Only execution tooling changes:

1. invoke the harness with CST bundled Python 3.6;
2. remove `from __future__ import annotations` from the harness for Python-3.6 compatibility.

No geometry, parameter, macro, stage metric, or scientific gate changes.

## Authorization

```text
BUILD_AUTHORIZED=YES
SOLVE_AUTHORIZED=NO
SILENT_RETRY=NO
RECOVERY_TASK_ID=R1A1-RECOVERY-CSTPY-BUILD-ONLY-DC-NW
```

This is a successor invocation after an explicit environment HOLD, not a silent retry.

## Stop boundary

Fresh-reopen build audit only.

No ports, substrate, feed, solver, optimization, LNA, or CST251 staging.
