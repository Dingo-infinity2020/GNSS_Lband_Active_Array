# GNSS L-band Active Array

Low-noise, dual-polarized active antenna array development for full L-band GNSS reception.

## Start here

Read these first:

1. `PROJECT_MAINLINE.md` - long-horizon scientific/simulation authority
2. `PROJECT_HANDOFF.md` - current execution baton, permissions, hashes and stop boundary
3. `docs/SIM_EXECUTION.md` - current SimulationOps execution state
4. `execution/stage_contract.json` - machine-readable stage authorization

## Current scientific phase

**R1E1A1 - authorized six-pitch FR4 source-set BUILD-ONLY on NW.**

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

R1E0C periodic scan qualification:

`PASS_R1E0C_SCAN_QUALIFICATION`

The 94-mm baseline numerically passed broadside, 30/45/60-deg principal-plane checks and the 60-deg orthogonal-plane sentinel under the frozen severe-mismatch gates.

However, the two 60-deg planes differ by up to about 209 ohm in active impedance across the science band.

Therefore the pitch/material trade is now the current mainline, and the final LNA input match is still not frozen.

## Current execution

R1E0C scan qualification is closed PASS.

R1E1A0 parameterization mechanism is now closed PASS after:
- initial formal HOLD on historical `StoreParameter` semantics;
- R1 pitch-ready canonical-source recovery PASS;
- R2 88/100-mm endpoint proof PASS with no protected-parameter warnings.

Canonical status:
`PASS_R1E1A0_PITCH_PARAMETERIZATION_MECHANISM`.

Current work:
**R1E1A1 authorized six-pitch FR4 source-set BUILD-ONLY**.

Pitch set:
88 / 90 / 92 / 94 / 96 / 100 mm

Current permissions:
- BUILD_AUTHORIZED=YES_R1E1A1_SIX_PITCH_SOURCE_SET_ONLY
- SOLVER_PERMISSION=NO

Read `PROJECT_HANDOFF.md` for the exact baton.

## Core documents

- `PROJECT_MAINLINE.md`
- `PROJECT_HANDOFF.md`
- `docs/PROJECT_RULES.md`
- `docs/REQUIREMENTS_v0.1.md`
- `docs/R1E0_PERIODIC_UNIT_CELL_PLAN.md`
- `docs/R1E0C_FIRST_SCAN_QUALIFICATION_PLAN.md`
- `docs/R1E1_PITCH_MATERIAL_TRADE_PLAN.md`
- `docs/R1E1A0_PITCH_PARAMETERIZATION_CONTRACT.md`
- `docs/SIM_EXECUTION.md`
