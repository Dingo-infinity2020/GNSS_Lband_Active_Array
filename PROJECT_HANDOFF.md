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
CURRENT_TASK_ID=R0.1B-CENTER-FEED-PROVENANCE-H01
TASK_OWNER=H01
TASK_STATUS=HOST_HOLD
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

Host registration already completed by H01:

- Host: `DESKTOP-GBTI6Q4`
- CST: CST Studio Suite 2022.5
- Python: Miniconda CPython 3.13.9
- Detailed paths/toolchain: `docs/HOST_ENVIRONMENT.md`

Verified execution/toolchain state from prior tasks:

```text
V01_STATUS=PASS_EXECUTION_REPLAY_ONLY / SCIENTIFICALLY_SUPERSEDED
V01_EVIDENCE=evidence/r0_1a_h01_20260922_2052/
V02_STATUS=PASS_EXECUTION_REPLAY_ONLY / SCIENTIFICALLY_SUPERSEDED
V02_EVIDENCE=evidence/r0_1a2_h01_20260922_2123/
V03_STATUS=PASS_R0_V03_12SLOT_TOPOLOGY_BUILD_ONLY / DESIGN_ACCEPTED
V03_EVIDENCE=evidence/r0_1a3_h01_20260922_2158/
V03_REVIEW=docs/R0_1A3_DESIGN_REVIEW_20260922.md
SOLVER_RUN=NO
```

Latest design-side review of CHARTS Fig.2(a):

- V0.2 still under-resolved the outer slot topology.
- The fabricated board has **8 outer slot segments**: 2 per board side.
- It also has **4 inner radial slots**.
- Total disconnected slot count is therefore **12**.
- Each side retains a midpoint conductor bridge.
- Corner conductor bridges remain.
- No large center through-hole is introduced in V0.3.
- The Fig.1 40 mm label is retained but its exact semantics are unresolved.

Current V0.3 photo-constrained topology values:

- board span = 247.5 mm
- opposing outer-slot centerline span = 227.5 mm
- outer slot width = 5 mm
- each outer slot segment = 94.125 mm
- midpoint conductor bridge = 18 mm
- inner slot width = 9 mm
- inner slot length = 73 mm
- visible center clear span = 60 mm
- height over ground = 200 mm

Source/provenance:
- `refs/charts2025/PHOTO_GEOMETRY_ESTIMATE.md`
- `refs/charts2025/FIGURE_EXTRACTION.md`
- `docs/R0_RECONSTRUCTION_ASSUMPTIONS.md`

---

# HOST TASK

## Task ID

**R0.1B-CENTER-FEED-PROVENANCE-H01**

## Objective

Perform a source/figure extraction focused only on the **central feed/electronics region** of the CHARTS antenna.

The current visible 12-slot V0.3 topology is accepted and frozen for this step. Do not change it.

This task answers:

> What central metal removal, balanced feed-terminal geometry, and Fig.1 `40 mm` semantics are actually supported by the primary source, and what remains unresolved?

## Authoritative instruction

Read and follow:

`docs/NEXT_ACTION_R0_1B_CENTER_FEED_PROVENANCE_20260922.md`

Also read:

- `docs/R0_1A3_DESIGN_REVIEW_20260922.md`
- `refs/charts2025/PROVENANCE.md`
- `refs/charts2025/FIGURE_EXTRACTION.md`
- `refs/charts2025/PHOTO_GEOMETRY_ESTIMATE.md`
- `docs/R0_RECONSTRUCTION_ASSUMPTIONS.md`

## Required outputs

Create:

- `refs/charts2025/CENTER_FEED_EXTRACTION.md`
- optionally `docs/figures/R0_CENTER_FEED_INTERPRETATION.svg`
- `evidence/r0_1b_h01_<YYYYMMDD_HHMM>/RETURN_REPORT.md`
- source-audit / measurement log and hashes for project-owned outputs

The report must explicitly return:

- `FIG40_SEMANTICS=...`
- `DIFFERENTIAL_TERMINALS_GEOMETRY=RESOLVED|PARTIAL|UNRESOLVED`
- `CENTRAL_REMOVED_REGION=RESOLVED|PARTIAL|UNRESOLVED`
- `SOLVER_READY=YES|NO`

Final status exactly one of:

- `PASS_R0_CENTER_FEED_EXTRACTION_COMPLETE`
- `HOLD_R0_CENTER_FEED_SOURCE_AMBIGUOUS`
- `HOLD_R0_PRIMARY_SOURCE_UNAVAILABLE`

A PASS means the extraction task is complete; it does not imply that the geometry is fully resolved.

## Strict prohibitions

Do not:

- run CST,
- run any solver,
- edit V0.3 geometry,
- add ports/materials/LNA/shield/Bias-Tee,
- tune dimensions,
- scale to L band,
- silently reinterpret the `40 mm` label,
- commit the copyrighted source PDF or raw source figures.

After push, stop. No successor task is pre-authorized.

---

# HOST RETURN

Previous execution evidence remains preserved in:

- `evidence/r0_1a_h01_20260922_2052/`
- `evidence/r0_1a2_h01_20260922_2123/`
- `evidence/r0_1a3_h01_20260922_2158/`

Current task return:

```text
TASK_STATUS=HOST_HOLD
HOST=H01
HOST_START_COMMIT=e1bb1a3
HOST_END_COMMIT=7687778a51ceb333de33905f55ffc55eacc991b0
FINAL_STATUS=HOLD_R0_PRIMARY_SOURCE_UNAVAILABLE
EVIDENCE_PATH=evidence/r0_1b_h01_20260922_2253/
NOTES=Primary source figures unavailable to H01: repo stores no copyrighted figures; no local copy found; DOI resolves to bibliographic metadata only (no full text); Crossref/DataCite APIs returned 404. Required new Fig.1(a)/Fig.2(a) center-feed audit could therefore not be performed. Delivered a provenance-only consolidation from repository records: refs/charts2025/CENTER_FEED_EXTRACTION.md (required table + 40mm candidates A/B/C/D, no winner) and docs/figures/R0_CENTER_FEED_INTERPRETATION.svg (project-owned redraw, no source imagery). Decision fields: FIG40_SEMANTICS=UNRESOLVED, DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED, CENTRAL_REMOVED_REGION=PARTIAL, SOLVER_READY=NO. No CST/solver run; V0.3 geometry untouched; no copyrighted material downloaded or committed. See source_audit_log.txt.
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
