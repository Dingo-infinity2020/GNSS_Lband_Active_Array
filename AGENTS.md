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

1. `docs/PROJECT_RULES.md`
2. `docs/DECISIONS.md`
3. `docs/REQUIREMENTS_v0.1.md`
4. `PROJECT_HANDOFF.md` — canonical current execution baton
5. the document for the current gate
6. relevant parameter/provenance manifests

`docs/PROJECT_RULES.md` is the anti-divergence charter. Its rules apply unless an explicit human-approved architecture decision supersedes them.

`PROJECT_HANDOFF.md` is the only operational task-exchange document between design review and execution hosts. Do not execute a task copied from an old chat or local note if it conflicts with the current handoff.

## Current gate

Current task: **R1A5F-DESIGN-SPLIT-SINGLE-PORT-FEED**

Authoritative current execution state is defined by:
- `PROJECT_HANDOFF.md`
- `docs/SIM_EXECUTION.md`
- `execution/stage_contract.json`

Current permissions:
- inspect R1A5M2 converged evidence: YES
- design/document split single-port production-passive feed models: YES
- run any new CST build or solver: NO
- modify geometry/materials: NO
- optimization/material A-B/production solve/CST251: NO

R1A5M2 has closed PASS with native adaptive convergence.
The crossed two-port model remains diagnostic-only for isolation.
R1A5F is design-only until a new explicit build authorization is committed.

## Architecture control

Current MAINLINE:
- CHARTS-inspired planar balanced element with feed-point differential active frontend.

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