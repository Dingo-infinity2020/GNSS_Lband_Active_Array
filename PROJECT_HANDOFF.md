# PROJECT_HANDOFF.md

> **Canonical operational handoff file**
>
> This is the single fixed document used for task exchange between ChatGPT/project design work and the registered execution host(s).
>
> Scientific rules live in `docs/PROJECT_RULES.md`; host capability records live in `docs/HOST_ENVIRONMENT.md`.  
> This file is only the **current baton**: what to sync, what to do now, what must not be done, and what the host returned.

---

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=1
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R0-CHARTS-RECON-PASSIVE
CURRENT_TASK_ID=REF-CUI-R0A-SOURCE-GEOMETRY-FREEZE-H01
TASK_OWNER=H01
TASK_STATUS=READY_FOR_HOST
SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
L_BAND_SCALING_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO
HARDWARE_PERMISSION=NO
```

The execution host must not infer any permission not explicitly listed here or in `AGENTS.md`.

---

## 1. SYNC PROTOCOL

For every new work cycle, both sides use the same sequence.

On the registered Windows host, the safe shortcut is:

```powershell
.\\scripts\\sync_handoff.ps1
```

It only synchronizes the repository and prints the current handoff header; it does not execute CST or change scientific artifacts.

### ChatGPT / design side

1. Fetch the current canonical branch.
2. Read, in order:
   - `docs/PROJECT_RULES.md`
   - `docs/DECISIONS.md`
   - `AGENTS.md`
   - **this file**
3. Review the latest host return/evidence.
4. Update the **HOST TASK** section only when issuing the next execution task.
5. Commit and push to the canonical branch.

### Execution host

1. Do not start from a chat transcript or an old copied prompt.
2. Synchronize the canonical branch:
   ```bash
   git fetch origin
   git checkout project/r0-charts-scaffold
   git pull --ff-only origin project/r0-charts-scaffold
   ```
3. Confirm a clean working tree:
   ```bash
   git status --short
   ```
4. Read:
   - `docs/PROJECT_RULES.md`
   - `AGENTS.md`
   - **this file**
5. Execute only the current **HOST TASK**.
6. Save requested evidence in the repository.
7. Replace/update **HOST RETURN** below.
8. Commit and push to the same canonical branch.
9. Stop. Do not invent the next task.

This makes the Git repository the communication channel. No separate prompt synchronization is required.

---

## 2. CONCURRENCY RULE

Only one side owns the baton at a time.

- `TASK_STATUS=READY_FOR_HOST`: host may act; ChatGPT should not concurrently modify execution artifacts.
- `TASK_STATUS=HOST_COMPLETE` or `HOST_HOLD`: host stops; ChatGPT/design side reviews and issues the successor task.
- `TASK_STATUS=READY_FOR_DESIGN`: design side owns the baton.

If both sides accidentally have unpushed changes, stop and resolve before scientific work continues.

---

## 3. CURRENT BASELINE

Canonical branch:

`project/r0-charts-scaffold`

Host:
- H01 / DESKTOP-GBTI6Q4
- CST 2022.5
- Miniconda Python
- see `docs/HOST_ENVIRONMENT.md`

CHARTS state:

```text
V03_VISIBLE_TOPOLOGY=DESIGN_ACCEPTED
V03_EVIDENCE=evidence/r0_1a3_h01_20260922_2158/
PRIMARY_SOURCE_ACCESS_H01=BLOCKED_BY_WAF
PRIMARY_SOURCE_ACCESS_DESIGN_SIDE=YES
FIG40_SEMANTICS=PARTIAL:CENTER_REGION_DIMENSION_EXACT_FEATURE_UNRESOLVED
DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED
CENTRAL_REMOVED_REGION=PARTIAL
LOCAL_FEED_GROUND=EXISTS_DIMENSIONS_UNRESOLVED
SOLVER_READY_EXACT_CHARTS=NO
```

Design-side official-PDF audit:

- `docs/R0_1B2_DESIGN_SIDE_PRIMARY_SOURCE_AUDIT_20260923.md`
- `refs/charts2025/CENTER_FEED_EXTRACTION.md`

Conclusion:
- CHARTS source access is no longer the blocker.
- Public CHARTS center/feed geometry is under-specified.
- Do not invent an exact feed.
- CHARTS-inspired active planar element remains MAINLINE.

Decision D0006 authorizes a **REFERENCE_ONLY** solver-validation path using Cui 2023, which publishes a complete geometry table and material stack.

Current REF-CUI source facts are recorded in:
- `refs/cui2023/PROVENANCE.md`

Current permissions:

- REF-CUI source/geometry provenance work: YES
- CST: NO
- solver: NO
- optimization: NO
- GNSS L-band scaling: NO
- LNA integration: NO

---

# HOST TASK

## Task ID

**R0.1B2-CENTER-FEED-SOURCE-RECOVERY-H01**

## Context

The prior R0.1B task correctly returned `HOLD_R0_PRIMARY_SOURCE_UNAVAILABLE` because the host's DOI/metadata path did not expose the paper.

Design-side review has now verified the official IEICE full-text PDF and recorded it in:

- `docs/R0_1B_SOURCE_RECOVERY_20260922.md`
- `refs/charts2025/PROVENANCE.md`

Th# HOST TASK

## Task ID

**REF-CUI-R0A-SOURCE-GEOMETRY-FREEZE-H01**

## Objective

Freeze the exact source-to-geometry mapping for the fully specified Cui 2023 reference antenna.

This is a **source/provenance task only**.

Read and follow exactly:

`docs/NEXT_ACTION_REF_CUI_R0A_SOURCE_GEOMETRY_FREEZE_20260923.md`

Primary open-access source:

https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/mia2.12343

The complete published numeric table is already transcribed into:

`refs/cui2023/PROVENANCE.md`

Your job is to map every symbol to the correct physical feature/panel without guessing.

## Required output

At minimum:

- `refs/cui2023/GEOMETRY_MAP.md`
- `refs/cui2023/parameters.csv`
- `docs/figures/REF_CUI_GEOMETRY_SCHEMATIC.svg`
- `evidence/ref_cui_r0a_h01_<YYYYMMDD_HHMM>/RETURN_REPORT.md`
- source access / parameter mapping evidence

Do not commit publisher PDF or raw figures.

## Final status

Exactly one:

- `PASS_REF_CUI_SOURCE_GEOMETRY_FROZEN`
- `HOLD_REF_CUI_FIGURE_ACCESS_FAILED`
- `HOLD_REF_CUI_PARAMETER_MAPPING_AMBIGUOUS`

## Strict prohibitions

- NO CST.
- NO solver.
- NO optimization.
- NO CHARTS geometry edits.
- NO GNSS L-band scaling.
- NO QPL9547/LNA work.
- NO architecture promotion.

After push, stop. No successor task is pre-authorized.

---

# HOST RETURN

Previous H01 CHARTS source-access HOLD remains preserved at:
- `evidence/r0_1b2_h01_20260923_1211/`

Design-side source recovery/audit is recorded separately and does not rewrite that evidence.

Current task return:

```text
TASK_STATUS=NOT_RUN_YET
HOST=H01
HOST_START_COMMIT=
HOST_END_COMMIT=
FINAL_STATUS=
EVIDENCE_PATH=
NOTES=
```

The host updates this section, commits/pushes, then stops.

---

## 4. NEXT-TASK RULE

There is deliberately no pre-authorized next task.

After the host returns, ChatGPT/design review will decide among:

- accept R0.1A PASS and proceed,
- request Candidate-B visual comparison,
- patch CST runtime syntax,
- revise reconstruction assumptions,
- keep R0 on HOLD.

This prevents the execution host from drifting into solver/material/L-band work without review.
