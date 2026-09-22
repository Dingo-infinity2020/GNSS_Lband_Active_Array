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
CURRENT_TASK_ID=R0.1A-TOPOLOGY-BUILD-ONLY-H01
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

Verified before this handoff:

```text
PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY
PASS_R0_TOPOLOGY_MACRO_STATIC_AUDIT
EXPECTED_SOLIDS=9
EXPECTED_PORTS=0
SOLVER_RUN=NO
```

Current scientific state:

- CHARTS figure-derived labels retained: 227.5 mm, 247.5 mm, 40 mm.
- Candidate A currently maps:
  - petal span = 227.5 mm
  - passive ring span = 247.5 mm
  - center opening = 40 mm
- Candidate B remains available by setting `candidate_swap=1`.
- R0 topology build is allowed.
- R0 materialized build remains HOLD.
- No solver is authorized.

---

# HOST TASK

## Task ID

**R0.1A-TOPOLOGY-BUILD-ONLY-H01**

## Objective

Execute the first CST 2022 **BUILD-ONLY** runtime validation of the repository-controlled CHARTS topology macro and perform a fresh-reopen audit.

This task answers only:

> Does the committed topology macro build reproducibly in CST 2022 and produce the intended nine-object Candidate-A geometry without ports or solver activity?

It does **not** answer whether the antenna has correct S11, gain, beamwidth, or material properties.

## Required preflight

From repository root, use the verified Miniconda Python or activated conda environment:

```bash
python scripts/r0_manifest_gate.py --stage topology
python scripts/audit_r0_topology_macro.py
```

Both must PASS.

If either does not PASS:
- set `TASK_STATUS=HOST_HOLD`,
- record the exact output,
- do not open/run the CST macro.

## CST BUILD-ONLY execution

Use a fresh CST Microwave Studio project.

Run:

`source/cst/R0_CHARTS_TOPOLOGY_BUILD_ONLY_V01.mcr`

Follow:

`em/cst/R0_CHARTS_300_500/RUNBOOK_TOPOLOGY_BUILD_ONLY.md`

### Expected inventory

```text
9 solids total:
  1 x GROUND_REFERENCE
  4 x PETAL_*
  4 x RING_*

0 ports
0 lumped elements
0 solver results
```

### Visual checks — Candidate A only

Verify and record:

1. fourfold rotational symmetry,
2. central square opening present,
3. four petal gaps remain electrically open,
4. passive ring surrounds the petals without electrical contact,
5. radiator/ring plane is 200 mm above the reference ground,
6. no obvious malformed/self-crossing extruded polygon,
7. model tree names match the runbook.

Do **not** alter geometry to make it look closer to the paper.

## Save / close / reopen audit

If build succeeds:

1. save the CST project under a clearly R0/build-only name,
2. close CST,
3. reopen CST fresh,
4. reopen the saved project,
5. verify the same 9 solids remain,
6. verify 0 ports,
7. verify there is no solver-result tree created by this task.

## Required evidence

Create a new directory:

`evidence/r0_1a_h01_<YYYYMMDD_HHMM>/`

Store at minimum:

- `RETURN_REPORT.md`
- `preflight.txt`
- `object_inventory.txt`
- `reopen_inventory.txt`
- at least one top-view screenshot
- at least one oblique/side-view screenshot showing ground separation
- screenshot after fresh reopen
- CST project file may be included if practical; if too large, record its local path and SHA-256 instead

`RETURN_REPORT.md` must state one final status exactly:

- `PASS_R0_TOPOLOGY_BUILD_ONLY`
- `HOLD_R0_TOPOLOGY_VISUAL_MISMATCH`
- `HOLD_R0_CST_RUNTIME_SYNTAX`
- `FAIL_R0_TOPOLOGY_REPLAY`

## Strict prohibitions

For this task, do not:

- run any solver,
- create ports,
- create monitors,
- add substrate/dielectric,
- add QPL9547/LNA,
- add Bias-Tee,
- scale to L band,
- optimize any parameter,
- repair scientific geometry silently,
- switch to Candidate B unless a future handoff explicitly requests it.

If the macro requires a syntax-only patch to run in CST 2022:
- make the smallest possible syntax patch,
- do not change numeric geometry,
- record exact old/new lines and reason,
- rerun static audit,
- commit separately,
- return `HOLD_R0_CST_RUNTIME_SYNTAX` unless the handoff is explicitly reissued after review.

---

# HOST RETURN

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

The host updates this section after execution and then stops.

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
