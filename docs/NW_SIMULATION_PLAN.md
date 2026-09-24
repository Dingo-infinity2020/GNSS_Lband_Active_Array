[Reading 107 lines from start (total: 107 lines, 0 remaining)]

# NW Simulation / Execution Plan

SimulationOps protocol: **0.2.4**

This file records project-local routing only. Global host facts remain in `SimulationOps/infrastructure/HOSTS.md`.

## Role of NW

`NW = NAOC-Win = DESKTOP-GBTI6Q4`

Use NW for:
- repository sync and staging,
- CST 2022 build-only,
- fresh reopen / object inventory / hash audit,
- screenshots and lightweight qualification,
- project scripts and geometry audits,
- optional small smoke solves only after a future explicit `SOLVE_AUTHORIZED=true`.

Do not default large production scans to NW.

## Completed

### R1A1 scaled aperture BUILD-ONLY

Status:
`PASS_R1A1_SCALED_APERTURE_BUILD_ONLY`

Evidence:
`evidence/r1a1_recovery_dc_nw_20260924_1113/`

No solver.

## Planned NW stages

### R1A2 — symmetric center-feed BUILD-ONLY

Prerequisite:
- R1A2 center-feed geometry freeze,
- exact one-master + 90-degree-copy construction,
- static rotational-symmetry audit.

NW actions:
- build in fresh MWS,
- 0 ports,
- 0 solver,
- fresh reopen,
- geometry symmetry metrics,
- screenshots/hash.

### R1A3 — materialized passive element BUILD-ONLY

Prerequisite:
- substrate/material choice explicitly frozen,
- copper stack frozen,
- center-feed copper topology frozen.

NW actions:
- full geometry/material build,
- no production solver,
- port geometry may still remain absent unless separately authorized.

### R1A4 — differential-port BUILD-ONLY

Status:
`PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY`

Completed on NW:
- immutable copy of human-reviewed R1A3 CST;
- 2 ideal balanced differential ports;
- Pol-A NE->SW;
- Pol-B NW->SE;
- 100 ohm differential normalization;
- fresh reopen port count = 2;
- geometry inventory unchanged;
- no solver.

### R1A5 — isolated-element smoke solve

**Not currently authorized.**

If later explicitly authorized:
- NW may run one lightweight smoke solve on the hash-locked R1A4 CST;
- no optimization;
- no broad parameter sweep;
- diagnostic/qualification outputs only;
- production science remains a later separately authorized stage.

### R1B — periodic-array build

NW:
- periodic unit-cell geometry build,
- Floquet/scan setup audit,
- hash-lock and fresh reopen.

### R1B production scan / broad solve

Default route:
- immutable staging from NW,
- production solve on `CST251-C`,
- one-shot solve,
- read-only qualification.

## Solve-host boundary

Current:
`SOLVE_AUTHORIZED=false`

No model is staged to CST251-C yet.

Future production tasks likely to use CST251-C:
- broad frequency sweep,
- many scan angles,
- periodic active-impedance map,
- finite-array/high-memory validation.

## Workspace hygiene

At every PASS/HOLD:
- clean Git checkout or checkpoint it,
- record source/head/artifact hashes,
- classify build work directories,
- retain only what the next stage requires,
- mark reproducible temporary CST workspaces PURGE_READY before deletion.

[executed on device: DESKTOP-GBTI6Q4 (fb6fe085-c539-483b-9729-1bab7aadce3f)]