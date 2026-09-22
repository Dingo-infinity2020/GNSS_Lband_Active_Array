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
CURRENT_TASK_ID=R0.1A2-SLOTTED-PLATE-BUILD-ONLY-H01
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

Verified execution/toolchain state from prior task:

```text
PREVIOUS_EXECUTION_STATUS=PASS_R0_1A_EXECUTION_REPLAY_ONLY
PREVIOUS_EVIDENCE=evidence/r0_1a_h01_20260922_2052/
PREVIOUS_FINAL_SOLIDS=9
PREVIOUS_PORTS=0
PREVIOUS_SOLVER_RUN=NO
```

Important design review:

- The V0.1 four-separate-petal + four-separate-ring topology is scientifically superseded.
- CHARTS Fig.2(a) shows one continuous square board/aperture with eight disconnected elongated slots.
- The slot network is not continuous.
- The central electronics region is not a large through-board square hole.
- The prior 9-solid build remains useful only as a CST execution/replay validation.

Current reconstruction hypothesis (Candidate C):

- board/aperture span = 247.5 mm (figure-derived hypothesis),
- outer-slot frame characteristic span = 227.5 mm (figure-derived hypothesis),
- retained central solid/electronics region = 40 mm (figure-derived hypothesis),
- 4 outer slots + 4 inner slots,
- slot width and bridge lengths remain topology-only assumptions,
- plate height = 200 mm (paper explicit).

Current permissions:

- V0.2 slotted topology build-only: YES
- materialized dielectric/copper model: HOLD
- solver: NO
- optimization: NO
- L-band scaling: NO
- LNA integration: NO

---

# HOST TASK

## Task ID

**R0.1A2-SLOTTED-PLATE-BUILD-ONLY-H01**

## Objective

Execute the corrected V0.2 CST **BUILD-ONLY** topology and fresh-reopen audit.

This task answers only:

> Does the Fig.2-consistent continuous slotted-plate topology build reproducibly in CST 2022, remain one connected antenna solid after eight disconnected slot cuts, and visually correct the V0.1 topology error?

It does not authorize any EM performance conclusion.

## Required preflight

From repository root:

```bash
python scripts/r0_manifest_gate.py --stage topology
python scripts/audit_r0_slotted_plate_v02.py
```

Expected:

```text
PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY
PASS_R0_V02_STATIC_AUDIT
EXPECTED_FINAL_SOLIDS=2
EXPECTED_SLOT_SUBTRACTIONS=8
EXPECTED_PORTS=0
CENTER_THROUGH_HOLE=NO
SOLVER_RUN=NO
```

If either gate does not PASS, return HOST_HOLD and do not execute CST.

## CST BUILD-ONLY

Use a fresh MWS project.

Run:

`source/cst/R0_CHARTS_SLOTTED_PLATE_BUILD_ONLY_V02.mcr`

Follow:

`em/cst/R0_CHARTS_300_500/RUNBOOK_SLOTTED_PLATE_V02.md`

Do not run the superseded V0.1 macro.

## Expected final inventory

```text
2 solids total:
  ReferenceGround:GROUND_REFERENCE
  Radiator:ANTENNA_PLATE

0 ports
0 lumped elements
0 solver results
```

The eight `SlotTools:CUT_*` objects should be consumed by boolean subtraction.

## Mandatory visual review

Compare top view against CHARTS Fig.2(a). Record PASS/HOLD for each:

1. one continuous square antenna/PCB silhouette,
2. four outer slots near the perimeter,
3. outer slots stop before corners,
4. four inner slots form a cross / "田"-like partition,
5. inner slots stop before center,
6. inner slots stop before outer slots,
7. all eight slot apertures are mutually disconnected,
8. central region remains solid (no large square through-hole),
9. the plate remains one connected CST solid,
10. topology is materially closer to Fig.2 than V0.1.

Side/oblique:
- antenna plate plane is 200 mm above ground.

Do not tune dimensions for aesthetics. If the placeholder proportions still look materially wrong, return visual mismatch with screenshots.

## Save / close / reopen

Save, close CST, fresh reopen, and recheck:
- 2 solids,
- 0 ports,
- no solver results.

## Required evidence

Create:

`evidence/r0_1a2_h01_<YYYYMMDD_HHMM>/`

At minimum:
- `RETURN_REPORT.md`
- `preflight.txt`
- `object_inventory.txt`
- `reopen_inventory.txt`
- top view
- oblique/side view
- fresh-reopen screenshot
- CST project path + SHA-256 if not committed

Final status must be exactly one of:

- `PASS_R0_V02_SLOTTED_TOPOLOGY_BUILD_ONLY`
- `HOLD_R0_V02_VISUAL_MISMATCH`
- `HOLD_R0_V02_CST_RUNTIME_SYNTAX`
- `FAIL_R0_V02_REPLAY`

## Strict prohibitions

Do not:
- run solver,
- add ports/monitors,
- add dielectric/material stack,
- add LNA/shield/Bias-Tee,
- perform L-band scaling,
- optimize slot dimensions,
- resurrect V0.1 petal/ring topology,
- change the scientific mapping without recording HOLD.

If a CST syntax-only patch is needed, make the minimum patch, preserve all numeric geometry, record exact changes, and return `HOLD_R0_V02_CST_RUNTIME_SYNTAX` for design review.

---

# HOST RETURN

Previous H01 return is preserved in:
`evidence/r0_1a_h01_20260922_2052/`

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
