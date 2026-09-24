[Reading 64 lines from start (total: 64 lines, 0 remaining)]

[Reading 60 lines from start (total: 60 lines, 0 remaining)]

# GNSS L-band Active Array

Low-noise, dual-polarized **active antenna array** development for full L-band GNSS reception.

## Start here

The project has two root-level authorities:

1. **`PROJECT_MAINLINE.md`** — highest-level scientific/simulation roadmap; prevents architecture and simulation drift.
2. **`PROJECT_HANDOFF.md`** — canonical current execution baton, permissions, artifact hashes and stop boundary.

Every new agent/session must read both before changing scientific artifacts.

## Current scientific phase

**R1A5FQ — final clean-feed isolated-equivalence design before periodic-array work.**

The isolated-element passive radiator has already reached a numerically converged diagnostic baseline.

The mainline is now:

**clean feed -> periodic unit cell -> pitch/material array trade -> active-impedance/embedded-pattern atlas -> finite passive array -> LNA/antenna co-design -> active periodic/finite array.**

Do **not** redirect the project into prolonged isolated-element S11 optimization.

## Target system envelope

- RF coverage: **1.15–1.65 GHz**
- Two independent linear-polarization outputs per element
- Digital RHCP/LHCP synthesis; no analog 90-degree hybrid in generation 1
- Core scan region: **0–60 deg from zenith**
- Extended scan investigation: **60–75 deg**
- Initial pitch search: **88–100 mm**, with **94 mm** as the first periodic baseline
- Low-cost PCB/SMT construction
- Feed-point low-noise frontend
- Minimal pre-LNA passive loss
- QPL9547 is a reference LNA candidate, not a frozen final choice

## Key system rule

The isolated-element return loss is not the design objective.

Before the LNA input network is frozen, the project must establish the array's scan-dependent **active differential impedance** and embedded-element behavior.

Preliminary LNA circuit/model validation may proceed in parallel with periodic-array work, but true active-antenna co-design begins only after the array source-impedance locus is available.

## Current execution

Read `PROJECT_HANDOFF.md`.

Current work is the single authorized R1A5FQ clean-feed isolated-equivalence solve. On PASS, isolated-element qualification closes and the next primary physics gate is R1E0 94-mm periodic unit cell.

## Core documents

- `PROJECT_MAINLINE.md` — long-horizon scientific/simulation authority
- `PROJECT_HANDOFF.md` — current execution authority
- `docs/PROJECT_RULES.md` — anti-divergence/change discipline
- `docs/REQUIREMENTS_v0.1.md` — system requirements
- `docs/R1_CHARTS_GNSS_DERIVATIVE_PLAN.md` — R1 design origin/history
- `docs/SIM_EXECUTION.md` — current SimulationOps execution state

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]