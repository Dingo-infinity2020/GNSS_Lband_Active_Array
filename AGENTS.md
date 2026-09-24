[Reading 190 lines from start (total: 190 lines, 0 remaining)]

[Reading 185 lines from start (total: 185 lines, 0 remaining)]

[Reading 180 lines from start (total: 180 lines, 0 remaining)]

[Reading 176 lines from start (total: 176 lines, 0 remaining)]

[Reading 170 lines from start (total: 170 lines, 0 remaining)]

[Reading 161 lines from start (total: 161 lines, 0 remaining)]

[Reading 157 lines from start (total: 157 lines, 0 remaining)]

[Reading 152 lines from start (total: 152 lines, 0 remaining)]

[Reading 149 lines from start (total: 149 lines, 0 remaining)]

[Reading 144 lines from start (total: 144 lines, 0 remaining)]

[Reading 141 lines from start (total: 141 lines, 0 remaining)]

[Reading 139 lines from start (total: 139 lines, 0 remaining)]

[Reading 138 lines from start (total: 138 lines, 0 remaining)]

[Reading 131 lines from start (total: 131 lines, 0 remaining)]

[Reading 127 lines from start (total: 127 lines, 0 remaining)]

[Reading 124 lines from start (total: 124 lines, 0 remaining)]

[Reading 120 lines from start (total: 120 lines, 0 remaining)]

# Agent Instructions

This repository is a staged scientific hardware project.

## Mandatory reading order

Before changing any scientific or engineering artifact, read:

1. `PROJECT_MAINLINE.md` — highest-level scientific/simulation roadmap
2. `docs/PROJECT_RULES.md`
3. `docs/DECISIONS.md`
4. `docs/REQUIREMENTS_v0.1.md`
5. `PROJECT_HANDOFF.md` — canonical current execution baton
6. the document for the current gate
7. relevant parameter/provenance manifests

`PROJECT_MAINLINE.md` is the long-horizon authority for the project sequence. In particular, it locks the array-first transition: clean feed -> periodic unit cell -> active-impedance atlas -> finite-array validation -> LNA/antenna co-design. Do not silently redirect the project into prolonged isolated-element optimization.

`docs/PROJECT_RULES.md` is the anti-divergence charter. Its rules apply unless an explicit human-approved architecture decision supersedes them.

`PROJECT_HANDOFF.md` is the only operational task-exchange document between design review and execution hosts. It controls the current permissions but must remain consistent with `PROJECT_MAINLINE.md`. Do not execute a task copied from an old chat or local note if it conflicts with either authority.

## Current gate

Current task: **R1E0A-PERIODIC-CONFIG-BUILD-ONLY-NW**

Authoritative current execution state is defined by:
- `PROJECT_MAINLINE.md`
- `PROJECT_HANDOFF.md`
- `docs/SIM_EXECUTION.md`
- `execution/stage_contract.json`

Current permissions:
- copy the protected clean Pol-A R1A5F CST into fresh R1E0A work: YES
- apply the frozen unit-cell/broadside boundary metadata: YES
- save, close, fresh reopen and audit periodic metadata: YES
- run any CST solver: NO
- create Floquet ports: NO
- modify geometry/materials/feed port: NO
- scan sweep / pitch-material trade / LNA integration / CST251: NO

This is the first array-physics configuration gate.
Stop after periodic metadata persistence qualification.

## Architecture control

Current MAINLINE:
- CHARTS-inspired planar balanced element with feed-point differential active frontend;
- transition to periodic/unit-cell active-impedance physics immediately after the clean-feed gate;
- LNA input matching remains unfrozen until the scan-dependent array source-impedance locus is established.

Current FIRST_BACKUP:
- PUMA / unbalanced tightly-coupled element with LNA behind the ground plane.

All other architectures are REFERENCE_ONLY unless promoted through the replacement test defined in `docs/PROJECT_RULES.md`.

New literature or component ideas must first go to `docs/IDEA_BACKLOG.md`.
Do not silently redirect the project toward a newly discovered architecture.

## Hard rules for R0

- Do not run a CST solver unless the task explicitly authorizes it.
- Build-only means geometry construction and validation only.
- Do not add QPL9547, active PCB, shield, Bias-Tee, array periodic boundaries, or L-band optimization during R0.
- Do not claim an exact CHARTS replica.
- Never convert a visually inferred dimension into a paper-explicit dimension.
- Every geometry parameter must exist in the parameter manifest with one provenance class:
  - PAPER_EXPLICIT
  - FIGURE_DERIVED_UNVERIFIED
  - ASSUMPTION
  - MEASURED
  - OPTIMIZED (not allowed in initial R0 build)
- If a required dimension is unknown, keep it visibly unknown until a documented reconstruction assumption is approved.
- Preserve source/reference metadata; do not copy entire copyrighted papers into the repository.
- Do not edit multiple scientific layers at once (for example geometry + LNA + conclusions) unless the gate explicitly requires a co-design step.

## Change discipline

Any electromagnetic geometry change must report:
- parameter,
- old value,
- new value,
- provenance,
- reason,
- expected physical effect.

Any design-decision reversal must update `docs/DECISIONS.md`.

Any new candidate architecture/component must update `docs/IDEA_BACKLOG.md` before entering the mainline.

## Expected engineering style

- parameterized scripts/macros over opaque manual edits,
- deterministic builds,
- small commits,
- one scientific question per gate,
- build reports before solver reports,
- explicit PASS/HOLD/FAIL status,
- no silent auto-tuning to match a paper plot,
- preserve failed evidence rather than rewriting history,
- stop optimization when a gate's acceptance criteria are met.

## Primary tools

- CST: antenna/full-wave geometry and later periodic/finite-array EM
- ADS: later LNA/noise/stability and EM-circuit co-design
- HFSS: optional independent cross-check
- Python: post-processing and parameter bookkeeping

## Execution hosts

Registered hosts and their verified toolchains are tracked in `docs/HOST_ENVIRONMENT.md`.
Registration records capability only; it does not grant any gate permission.

## Stop rules

Stop and document instead of guessing when:
- a source ambiguity materially changes geometry,
- a new idea would require changing architecture mid-gate,
- a solver result cannot be traced to a parameter manifest,
- an optimization objective has not been frozen,
- a proposed added feature has no quantified problem it solves.

A HOLD is an acceptable scientific outcome.

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]