# PROJECT_HANDOFF.md

> Canonical operational handoff file for the design side and execution host H01.

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=3
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=REF-CUI-PASSIVE-REFERENCE
CURRENT_TASK_ID=REF-CUI-R0B-BUILD-ONLY-H01
TASK_OWNER=H01
TASK_STATUS=READY_FOR_HOST
SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
L_BAND_SCALING_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO
HARDWARE_PERMISSION=NO
```

## 1. Sync protocol

Execution host shortcut:

```powershell
.\scripts\sync_handoff.ps1
```

Before any work, read:
1. `docs/PROJECT_RULES.md`
2. `docs/DECISIONS.md`
3. `AGENTS.md`
4. this file

Only the side named by `TASK_OWNER` may advance the current task.

## 2. Stable architecture state

MAINLINE:
- CHARTS-inspired planar balanced active element.

FIRST_BACKUP:
- PUMA / unbalanced tightly-coupled element.

REF-CUI:
- REFERENCE_ONLY passive-EM validation structure.
- It does not replace MAINLINE.

CHARTS exact center/feed geometry remains publicly under-specified.
Do not modify CHARTS during the current task.

## 3. REF-CUI source state

The user supplied the publisher PDF to the design side.

Design-side high-resolution review of Figure 7(a)/(b)/(c) plus Table 1 completed the source map.

```text
REF_CUI_PRIMARY_SOURCE=USER_SUPPLIED_PUBLISHER_PDF
MAPPED_SYMBOLS_EXACT=26/26
SOURCE_GEOMETRY_MAPPING=PASS
DETERMINISTIC_CAD_MAPPING_READY=YES
BUILD_ONLY_PERMISSION=YES
SOLVER_PERMISSION=NO
```

Authoritative repository inputs:

- `refs/cui2023/PROVENANCE.md`
- `refs/cui2023/GEOMETRY_MAP.md`
- `refs/cui2023/parameters.csv`
- `docs/figures/REF_CUI_GEOMETRY_SCHEMATIC.svg`
- `docs/NEXT_ACTION_REF_CUI_R0B_BUILD_ONLY_20260923.md`

H01 does not need publisher-web access and must not retry Cloudflare/Wiley for this task.

## 4. HOST TASK

### Task ID

**REF-CUI-R0B-BUILD-ONLY-H01**

Execute exactly:

`docs/NEXT_ACTION_REF_CUI_R0B_BUILD_ONLY_20260923.md`

### Objective

Create and run a deterministic CST 2022 **BUILD-ONLY** reference model of Cui 2023 from the frozen project geometry map.

No EM solver result is authorized.

### Required outputs

Create at minimum:

- `source/cst/REF_CUI_R0B_BUILD_ONLY_V01.mcr`
- `source/cst/REF_CUI_R0B_BUILD_ONLY_V01.bas`
- `scripts/audit_ref_cui_r0b_macro.py`
- `em/cst/REF_CUI_069_152/README.md`
- `em/cst/REF_CUI_069_152/RUNBOOK_BUILD_ONLY.md`
- `evidence/ref_cui_r0b_h01_<YYYYMMDD_HHMM>/...`

### Mandatory constraints

- all 26 source-mapped dimensions must remain parameterized,
- Rogers 4350B, er=3.48, thickness=0.76 mm,
- main ground = 260 mm square,
- radiator height = 80 mm,
- square loop = 115 mm outer side, 5.9 mm trace width,
- crossed dipole + four open slots,
- two orthogonal vertical balun boards and metal patterns,
- no port objects,
- no solver,
- no monitor,
- no optimization,
- no QPL9547/LNA,
- no GNSS scaling,
- no CHARTS edits.

If a remaining CAD construction choice is not source-unique, label it
`CAD_CONSTRUCTION_ASSUMPTION` and return HOLD if it materially affects source fidelity.

### Allowed final status

Exactly one:

- `PASS_REF_CUI_R0B_BUILD_ONLY`
- `HOLD_REF_CUI_R0B_CAD_AMBIGUITY`
- `HOLD_REF_CUI_R0B_CST_RUNTIME_SYNTAX`
- `HOLD_REF_CUI_R0B_VISUAL_MISMATCH`
- `FAIL_REF_CUI_R0B_REPLAY`

Commit/push, update HOST RETURN, then stop.

## 5. HOST RETURN

Previous H01 source-access HOLD remains preserved at:
- `evidence/ref_cui_r0a_h01_20260923_1229/`

It is superseded only as an access blocker; the historical evidence remains valid.

Current task return:

```text
TASK_STATUS=NOT_RUN_YET
HOST=H01
HOST_START_COMMIT=
HOST_END_COMMIT=
FINAL_STATUS=
EVIDENCE_PATH=
CST_PROJECT_PATH_OR_HASH=
NOTES=
```

## 6. Stop rule

There is no pre-authorized solver task.

After H01 returns, DESIGN must compare the CST build screenshots/model inventory against the user-supplied primary PDF and decide whether REF-CUI can proceed to a passive solver gate.
