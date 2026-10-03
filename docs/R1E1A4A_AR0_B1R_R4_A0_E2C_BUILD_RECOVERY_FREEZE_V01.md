# R4-A0-E2C Build Recovery Freeze V0.1

Status: NO_GEOMETRY_REDESIGN RECOVERY READY — NEW BUILD AUTHORIZATION REQUIRED  
Date: 2026-09-30  
SimulationOps: 0.2.15 @ 7dfbeb7a44a82501a7a20bbe62230aa047e80af6

## Formal attempt

Runner packet: `GNSS-E2C-DUALPOL-BUILD-20260930-01`

Core result: `HOLD_ENTRYPOINT`

The generic runner conservatively recorded BUILD authorization consumed because the project entrypoint process launched.

Observed exception:

`TypeError: main() takes 6 positional arguments but 7 were given`

The failure occurred before `main()` entered. Therefore:
- no CST build session entered project logic;
- 16-via kernel reference did not start;
- production combined macro did not start;
- no canonical E2C .cst artifact was generated;
- solver invocation count remains zero.

## Root cause

The review-copy feature changed the CLI call to seven arguments but the build function definition retained the previous six-argument signature.

This is a project-runner bootstrap defect only.

## Recovery class

`NO_GEOMETRY_REDESIGN`

Unchanged:
- canonical parent SHA;
- E2C macro;
- 177-solid inventory;
- 16-via geometry;
- 24 raw ports;
- 29 pairwise intersection contract;
- scientific gates;
- no-solver boundary.

Changed tooling only:
1. `main()` now accepts `review_copy`;
2. static AST audit checks definition/call argument parity;
3. complete review-copy behavior remains part of the same build transaction.

Corrected build runner blob:
`76b3e403a830d9736fc019303dc7f0b0e8b3ee0f`

Entrypoint static-audit blob:
`e2e761d54d263e52d7a7c90a910d9e5863d8251f`

## Recovery preflight

Before a recovery BUILD_ONLY transaction:
- AST entrypoint audit must PASS;
- bridge + CST-Python `--help` check must PASS;
- generic packet validate + dry-run must PASS;
- use a fresh packet_id and fresh target root;
- automatic retry = 0.

## Authorization

The first generic-runner packet consumed its BUILD authorization under runner v0.1 semantics.

BUILD_AUTHORIZED = false  
SOLVE_AUTHORIZED = false

Next:
`R1E1A4A_AR0_B1R_R4_A0_E2C_BUILD_RECOVERY_AWAIT_AUTH`
