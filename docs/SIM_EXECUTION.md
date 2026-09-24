# SIM_EXECUTION

## Global protocol

- SimulationOps version: 0.2.4
- Build/control host: NW
- Simulator: CST Studio Suite 2022.5
- Runtime: CST bundled Python 3.6 / cst.interface
- Production solve host: CST251-C only after a future explicit production authorization

## Current state

Model identity:
CHARTS_GNSS_R1A4_DIFFERENTIAL_PORT_V01

Current stage:
DESIGN_R1A5_SMOKE_SOLVE_CONTRACT

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false

Last completed stage:
BUILD_ONLY_R1A4

Last status:
PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY

## Hash-locked R1A4 candidate source

D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

Ports:
- Pol-A NE->SW
- Pol-B NW->SE
- 100 ohm differential reference
- fresh-reopen count = 2

Geometry identity to R1A3:
PASS

## R1A5 boundary

R1A5 smoke solve is not authorized yet.

Before any solver invocation, freeze:
- solver/boundary/mesh/frequency contract;
- exact diagnostic outputs;
- smoke PASS/HOLD logic;
- one-shot invocation;
- no optimization;
- no broad sweep.

No solver may start from the current state.
