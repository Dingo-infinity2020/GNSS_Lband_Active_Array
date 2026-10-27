# GNSS L-band Active Array

Low-noise, dual-polarized active antenna array development for full L-band GNSS reception.

## Start here

Read these first:

1. `PROJECT_MAINLINE.md` - long-horizon scientific/simulation authority
2. `PROJECT_HANDOFF.md` - current execution baton, permissions, hashes and stop boundary
3. `docs/SIM_EXECUTION.md` - current SimulationOps execution state
4. `execution/stage_contract.json` - machine-readable stage authorization

## Ver1.0 product direction

A reproducible CHARTS/AR0-B dual-polarized active array element: one planar radiator PCB, two orthogonal PCB stalks carrying four near-feed LNAs, a common backplane, and two independently powered RF outputs. Digital RHCP/LHCP synthesis follows X/Y calibration.

94-mm pitch, approximately 70.7-mm radiator span and 57.1-mm height are engineering starting values. Ver1.0 includes assembly/test/calibration evidence and finite-array validation, not a new digital receiver backend. Product direction is decided; RF and hardware qualification remain open.

Read [the project review and Ver1.0 definition](docs/VER1_0_PRODUCT_DIRECTION_AND_PROJECT_REVIEW_20261027.md) and [D0023](docs/DECISIONS.md#d0023--define-ver10-as-a-chartsar0-b-dual-polarized-active-array-element).

## Current scientific phase

The M7C same-geometry direct-sample diagnostic is COMPLETE: `H_NUM_SUPPORTED_M7C_DIRECT_SAMPLE`. Its formerly strongest weak-response peak is not reproduced in the direct-frequency solution. Broadband branch asymmetry and other guard context remain; original science stays `HOLD_M7C_GUARD`. The prior broadband gate records Sdd restoration 6/6, Sdc symmetry 0/10 and a 20.2398-dB guard excursion against the frozen 6-dB limit.

BUILD/SOLVE are closed. See [the diagnostic result](docs/M7C_DIRECT_SAMPLE_DIAGNOSTIC_RESULT_20261027.md), `PROJECT_HANDOFF.md` and `execution/stage_contract.json`. The mainline remains array-aware receiver co-design; final LNA input matching is not frozen.

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

The integrated feed/ground coexistence and full-network feasibility must close before the pitch/material trade and authoritative R1E2 source cloud. The bare periodic result does not qualify the final active assembly; input matching remains open.

## Current execution

`R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7C_DIRECT_SAMPLE_RESULT_REVIEW`

Diagnostic: `H_NUM_SUPPORTED_M7C_DIRECT_SAMPLE`; original science: `HOLD_M7C_GUARD`.

- One direct-sample SOLVE consumed; no geometry BUILD and zero automatic retries.
- Qualified 96 complex responses x15 direct frequencies; all 11 checks PASS.
- Original runner HOLD and zero-solver recovery histories retained; complete C: output PROTECTED.
- No live grant. Next physical boundary is offline return-path hypothesis review only.

## Core documents

- [Ver1.0 product direction and project review](docs/VER1_0_PRODUCT_DIRECTION_AND_PROJECT_REVIEW_20261027.md)
- `PROJECT_MAINLINE.md`
- `PROJECT_HANDOFF.md`
- `docs/PROJECT_RULES.md`
- `docs/REQUIREMENTS_v0.1.md`
- `docs/R1E0_PERIODIC_UNIT_CELL_PLAN.md`
- `docs/R1E1A2_MECHANICAL_SUPPORT_EM_PLAN.md`
- `docs/R1E1A2_ASSEMBLY_INTERFACE_PLAN.md`
- `docs/R1E0C_FIRST_SCAN_QUALIFICATION_PLAN.md`
- `docs/R1E1_PITCH_MATERIAL_TRADE_PLAN.md`
- `docs/R1E1A0_PITCH_PARAMETERIZATION_CONTRACT.md`
- `docs/SIM_EXECUTION.md`
