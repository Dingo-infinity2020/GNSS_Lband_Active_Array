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

### R1A4 — isolated-element smoke solve

**Not currently authorized.**

If later explicitly authorized:
- NW may run a narrow, lightweight smoke solve for API/port sanity,
- no optimization,
- no broad parameter sweep,
- results are qualification only, not production science.

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
