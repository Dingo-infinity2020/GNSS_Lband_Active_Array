# GNSS L-band Active Array

Low-noise, dual-polarized active antenna array development for full L-band GNSS reception.

## Start here

Read these first:

1. `PROJECT_MAINLINE.md` - long-horizon scientific/simulation authority
2. `PROJECT_HANDOFF.md` - current execution baton, permissions, hashes and stop boundary
3. `docs/SIM_EXECUTION.md` - current SimulationOps execution state
4. `execution/stage_contract.json` - machine-readable stage authorization

## Current scientific phase

**R1E0C-B - C30P45 PASS; C45P45 next scan-solve design.**

The isolated-element passive phase is closed.

The project mainline is:

**clean feed -> periodic unit cell -> scan qualification -> pitch/material array trade -> active-impedance atlas -> finite passive array -> LNA/antenna co-design -> active periodic/finite array**

Do not redirect the project into prolonged isolated-element S11 optimization.

## Target system envelope

- RF coverage: **1.15-1.65 GHz**
- Two independent linear-polarization outputs per element
- Digital RHCP/LHCP synthesis
- Core scan region: **0-60 deg from zenith**
- Extended scan investigation: **60-75 deg**
- Initial pitch search: **88-100 mm**
- First periodic baseline pitch: **94 mm**
- Low-cost PCB/SMT construction
- Feed-point low-noise frontend
- Minimal pre-LNA passive loss
- QPL9547 is a reference LNA candidate, not a frozen final choice

## Key system rule

The isolated-element return loss is not the design objective.

Before the LNA input network is frozen, the project must establish the array's scan-dependent active differential impedance and embedded-element behavior.

Preliminary LNA model/circuit research may proceed in parallel, but true active-antenna input matching is blocked until the array source-impedance locus is available.

## Latest closed physics gate

R1E0B broadside periodic smoke:

`PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE`

At 94-mm pitch and broadside, the periodic array materially shifts the source impedance away from the isolated-element intuition.

Science-band broadside range:
- Re(Z_active): about 85-264 ohm
- Im(Z_active): about -84 to +142 ohm
- |Z_active|: about 105-267 ohm

This is why the LNA match is not frozen yet.

## Current execution

R1E0C-A is closed PASS. C30P45 scan solve is also PASS and protected. Current work is **C45P45 DESIGN ONLY**; all remaining scan solvers are unauthorized.

Prepared scan states:
- theta=30, phi=45
- theta=45, phi=45
- theta=60, phi=45
- theta=60, phi=135

Current permissions:
- BUILD_AUTHORIZED=NO
- SOLVER_PERMISSION=NO

Read `PROJECT_HANDOFF.md` for the exact baton.

## Core documents

- `PROJECT_MAINLINE.md`
- `PROJECT_HANDOFF.md`
- `docs/PROJECT_RULES.md`
- `docs/REQUIREMENTS_v0.1.md`
- `docs/R1E0_PERIODIC_UNIT_CELL_PLAN.md`
- `docs/R1E0C_FIRST_SCAN_QUALIFICATION_PLAN.md`
- `docs/SIM_EXECUTION.md`
