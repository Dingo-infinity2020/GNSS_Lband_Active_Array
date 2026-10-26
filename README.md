# GNSS L-band Active Array

Low-noise, dual-polarized active antenna array development for full L-band GNSS reception.

## Start here

Read these first:

1. `PROJECT_MAINLINE.md` - long-horizon scientific/simulation authority
2. `PROJECT_HANDOFF.md` - current execution baton, permissions, hashes and stop boundary
3. `docs/SIM_EXECUTION.md` - current SimulationOps execution state
4. `execution/stage_contract.json` - machine-readable stage authorization

## Current scientific phase

M7C local-return-island diagnostic is closed STORAGE HOLD with no science classification. One same-geometry storage-recovery SOLVE is explicitly authorized; BUILD remains closed.

Read `docs/M7C_STORAGE_RECOVERY_PREPARATION_V01.md`, `PROJECT_HANDOFF.md` and `execution/stage_contract.json` for the current boundary.

The mainline remains support/hub-inclusive array physics, scan-dependent active impedance, finite-array validation and receiver co-design. The LNA input match is not frozen.

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

`R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7C_STORAGE_RECOVERY_SOLVE_V01`

`SOLVE_AUTHORIZED_M7C_RECOVERY_ONE_SHOT_PENDING_PACKET_VALIDATION`

- Output: new C: NTFS project run directory; existing D: baselines preserved.
- Storage: output 32 GiB + TEMP 8 GiB, summed when sharing a filesystem.
- Geometry, 12-port/8-source semantics, solver fidelity and M7C modal gates unchanged.
- One fresh SOLVE grant is live. Packet generation/validation precedes exactly one run; automatic retries=0.

## Core documents

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
