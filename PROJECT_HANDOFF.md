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
CURRENT_TASK_ID=R0.1A3-12SLOT-BUILD-ONLY-H01
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
- `docs/R0_RECONSTRUCT# HOST TASK

## Task ID

**R0.1A3-12SLOT-BUILD-ONLY-H01**

## Objective

Execute the V0.3 photo-constrained **12-slot** CST BUILD-ONLY topology and perform a save/close/fresh-reopen audit.

This task answers only:

> Does the corrected one-piece, 12-disconnected-slot topology build reproducibly and preserve the intended geometry in CST 2022?

It does not authorize any EM performance conclusion.

## Required preflight

From repository root:

```bash
python scripts/r0_manifest_gate.py --stage topology
python scripts/audit_r0_12slot_v03.py
```

Expected:

```text
PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY
PASS_R0_V03_STATIC_AUDIT
EXPECTED_FINAL_SOLIDS=2
EXPECTED_OUTER_SLOT_SEGMENTS=8
EXPECTED_INNER_SLOT_SEGMENTS=4
EXPECTED_SLOT_SUBTRACTIONS=12
EXPECTED_PORTS=0
CENTER_THROUGH_HOLE=NO
FIG40_SEMANTICS=UNRESOLVED
SOLVER_RUN=NO
```

If either gate fails, return HOST_HOLD and do not execute CST.

## CST BUILD-ONLY

Use a fresh MWS project.

Run:

`source/cst/R0_CHARTS_12SLOT_BUILD_ONLY_V03.mcr`

Follow:

`em/cst/R0_CHARTS_300_500/RUNBOOK_12SLOT_V03.md`

Do not run V0.1 or V0.2.

## Expected final inventory

```text
2 solids:
  ReferenceGround:GROUND_REFERENCE
  Radiator:ANTENNA_PLATE

12 consumed slot cutters
0 ports
0 lumped elements
0 solver results
```

## Mandatory visual/build review

Verify:

1. antenna plate remains one connected solid,
2. 8 outer slots total,
3. exactly 2 outer slots per side,
4. midpoint conductor bridge present on all 4 sides,
5. conductor remains at all 4 corners,
6. 4 inner radial slots,
7. inner slots stop before center,
8. inner slots stop before outer slots,
9. all 12 slots are mutually disconnected,
10. no large central through-hole,
11. antenna plane is 200 mm above ground,
12. CST top view matches `docs/figures/R0_V03_12SLOT_TOPOLOGY_SCHEMATIC.svg`.

Do not tune any dimension.

## Save / close / reopen

Save project, close CST, reopen fresh and recheck:
- 2 final solids,
- 0 ports,
- no solver results.

## Required evidence

Create:

`evidence/r0_1a3_h01_<YYYYMMDD_HHMM>/`

Include at minimum:

- `RETURN_REPORT.md`
- `preflight.txt`
- `object_inventory.txt`
- `reopen_inventory.txt`
- top-view screenshot
- side/oblique screenshot
- fresh-reopen screenshot
- CST project local path + SHA-256 if not committed

Final status exactly one of:

- `PASS_R0_V03_12SLOT_TOPOLOGY_BUILD_ONLY`
- `HOLD_R0_V03_VISUAL_MISMATCH`
- `HOLD_R0_V03_CST_RUNTIME_SYNTAX`
- `FAIL_R0_V03_REPLAY`

## Strict prohibitions

Do not:
- run solver,
- add ports/monitors,
- add substrate/material stack,
- add QPL9547/LNA,
- add shield or Bias-Tee,
- scale to L band,
- optimize any dimension,
- reinterpret the 40 mm Fig.1 label,
- revive V0.1/V0.2 geometry.

If a syntax-only CST patch is required, make the smallest possible syntax patch without numerical geometry changes, document exact lines, and return HOLD for design review.

---

# HOST RETURN

Previous execution evidence remains preserved in:
- `evidence/r0_1a_h01_20260922_2052/`
- `evidence/r0_1a2_h01_20260922_2123/`

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
