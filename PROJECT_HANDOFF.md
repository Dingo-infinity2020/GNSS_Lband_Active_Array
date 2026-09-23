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
CURRENT_TASK_ID=R0.1B2-CENTER-FEED-SOURCE-RECOVERY-H01
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

**R0.1B2-CENTER-FEED-SOURCE-RECOVERY-H01**

## Context

The prior R0.1B task correctly returned `HOLD_R0_PRIMARY_SOURCE_UNAVAILABLE` because the host's DOI/metadata path did not expose the paper.

Design-side review has now verified the official IEICE full-text PDF and recorded it in:

- `docs/R0_1B_SOURCE_RECOVERY_20260922.md`
- `refs/charts2025/PROVENANCE.md`

The official PDF may be downloaded locally for inspection but must not be committed.

## Objective

Repeat only the previously blocked high-resolution Fig. 1(a) / Fig. 2(a) center-feed provenance audit.

Read and follow exactly:

`docs/NEXT_ACTION_R0_1B2_CENTER_FEED_SOURCE_RECOVERY_20260922.md`

## Key source

Direct official IEICE PDF:

https://www.ieice.org/publications/proceedings/bin/pdf_link.php?fname=1571143655.pdf&iconf=ISAP&lang=E&number=1571143655&vol=98&year=2025

## Required return fields

- `FIG40_SEMANTICS=RESOLVED:<meaning>|PARTIAL|UNRESOLVED`
- `DIFFERENTIAL_TERMINALS_GEOMETRY=RESOLVED|PARTIAL|UNRESOLVED`
- `CENTRAL_REMOVED_REGION=RESOLVED|PARTIAL|UNRESOLVED`
- `SOLVER_READY=YES|NO`

Final status exactly one of:

- `PASS_R0_CENTER_FEED_PRIMARY_SOURCE_AUDIT_COMPLETE`
- `HOLD_R0_CENTER_FEED_SOURCE_AMBIGUOUS`
- `HOLD_R0_PRIMARY_SOURCE_ACCESS_FAILED`

## Strict prohibitions

- NO CST.
- NO solver.
- NO geometry edit.
- NO L-band scaling.
- NO LNA/shield/Bias-Tee work.
- NO copyrighted PDF or raw source-figure commit.

After push, stop. No successor task is pre-authorized.

---

# HOST RETURN

Previous execution evidence remains preserved in:

- `evidence/r0_1a_h01_20260922_2052/`
- `evidence/r0_1a2_h01_20260922_2123/`
- `evidence/r0_1a3_h01_20260922_2158/`
- `evidence/r0_1b_h01_20260922_2253/` (source-unavailable HOLD; preserved as historical evidence)

Current task return:

```text
TASK_STATUS=HOST_HOLD
HOST=H01
HOST_START_COMMIT=cb7e650
HOST_END_COMMIT=4085e68650192371d04fdfa3c41fa47e0142eeff
FINAL_STATUS=HOLD_R0_PRIMARY_SOURCE_ACCESS_FAILED
EVIDENCE_PATH=evidence/r0_1b2_h01_20260923_1211/
NOTES=Attempted to download the recovered official IEICE PDF but the publisher is behind an AWS WAF "Human Verification" CAPTCHA: landing and direct-PDF URLs returned HTTP 405 with a 2144-byte WAF challenge page (curl/webfetch) and HTTP 403 (Invoke-WebRequest). No PDF bytes obtained; H01 did not bypass the CAPTCHA. Therefore no Fig.1(a)/Fig.2(a) center-feed audit was possible. Decision fields: FIG40_SEMANTICS=UNRESOLVED, DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED, CENTRAL_REMOVED_REGION=PARTIAL, SOLVER_READY=NO. Updated refs/charts2025/CENTER_FEED_EXTRACTION.md with an R0.1B2 access section (prior history preserved; no value upgraded). No CST/solver; no copyrighted PDF/crop stored or committed (challenge page kept in local temp only). See source_access_log.txt and figure_measurements.md. Suggested unblock: provide the PDF to H01 as a git-ignored local file, or perform the figure audit design-side and issue a consolidation task.
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
