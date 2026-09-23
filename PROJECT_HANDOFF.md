# PROJECT_HANDOFF.md

> Canonical operational handoff file for the design side and execution host H01.

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=2
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R0-CHARTS-RECON-PASSIVE
CURRENT_TASK_ID=REF-CUI-R0A-DESIGN-SOURCE-MAPPING
TASK_OWNER=DESIGN
TASK_STATUS=READY_FOR_DESIGN
SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
L_BAND_SCALING_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO
HARDWARE_PERMISSION=NO
```

## 1. Sync protocol

Execution host sync shortcut:

```powershell
.\scripts\sync_handoff.ps1
```

Before any work, read:
1. `docs/PROJECT_RULES.md`
2. `docs/DECISIONS.md`
3. `AGENTS.md`
4. this file

Only the side named by `TASK_OWNER` may advance the current task.

- `READY_FOR_HOST`: H01 may execute the HOST TASK, commit/push, update HOST RETURN, then stop.
- `HOST_COMPLETE` / `HOST_HOLD`: design side reviews.
- `READY_FOR_DESIGN`: H01 must not start a new scientific task.

## 2. Stable project state

MAINLINE:
- CHARTS-inspired planar balanced active element.

FIRST_BACKUP:
- PUMA / unbalanced tightly-coupled element.

CHARTS state:

```text
V03_VISIBLE_TOPOLOGY=DESIGN_ACCEPTED
V03_EVIDENCE=evidence/r0_1a3_h01_20260922_2158/
CHARTS_EXACT_CENTER_FEED=UNDER_SPECIFIED_PUBLICLY
FIG40_SEMANTICS=PARTIAL
SOLVER_READY_EXACT_CHARTS=NO
```

Relevant design-side audit:
- `docs/R0_1B2_DESIGN_SIDE_PRIMARY_SOURCE_AUDIT_20260923.md`
- `refs/charts2025/CENTER_FEED_EXTRACTION.md`

Decision D0006:
- do not invent unpublished CHARTS center/feed geometry;
- keep CHARTS as MAINLINE inspiration;
- use REF-CUI as REFERENCE_ONLY passive-EM workflow validation if deterministic geometry can be frozen.

## 3. REF-CUI current state

H01 source task:

```text
H01_STATUS=HOLD_REF_CUI_FIGURE_ACCESS_FAILED
H01_EVIDENCE=evidence/ref_cui_r0a_h01_20260923_1229/
H01_MAPPED_SYMBOLS=0/26
CAUSE=publisher Cloudflare/WAF access block
```

Design-side source recovery:

```text
WILEY_FULL_TEXT_ACCESS=YES
FIGURE_7A_INDEXED_IMAGE_ACCESS=YES
MAPPED_SYMBOLS_EXACT=3/26
Lg=260 mm -> square main ground-plane side length
H=80 mm -> radiator-to-main-ground height
Lr=115 mm -> square-loop side length
FIGURE_7B_EXACT_LABEL_ENDPOINTS=NOT_YET_RECOVERED
FIGURE_7C_EXACT_BALUN_SEGMENT_MAPPING=NOT_YET_RECOVERED
DETERMINISTIC_FULL_CAD_READY=NO
SOLVER_READY=NO
```

Source/provenance:
- `refs/cui2023/PROVENANCE.md`
- `refs/cui2023/GEOMETRY_MAP.md`
- `refs/cui2023/parameters.csv`

The design side is currently attempting to resolve Figure 7(b)/(c) mappings.
H01 must not retry Wiley/Cloudflare unless a later handoff explicitly requests it.

## 4. HOST TASK

**NONE.**

Current owner is DESIGN. H01 should only sync/read and wait.

## 5. HOST RETURN

Most recent H01 return:

```text
TASK_STATUS=HOST_HOLD
HOST=H01
FINAL_STATUS=HOLD_REF_CUI_FIGURE_ACCESS_FAILED
EVIDENCE_PATH=evidence/ref_cui_r0a_h01_20260923_1229/
NOTES=Publisher figures blocked by Cloudflare; no bypass attempted; no CST/solver.
```

## 6. Current design-side stop condition

Do not authorize a deterministic REF-CUI CST build until either:

1. Figure 7(b)/(c) exact parameter endpoints are recovered sufficiently for CAD, or
2. a documented decision replaces REF-CUI with a reference whose exact geometry is genuinely accessible.

No solver, L-band scaling, LNA work, or CHARTS geometry edit is authorized by this handoff.
