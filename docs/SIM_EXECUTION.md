# SIM_EXECUTION

## Current stage

R1A4Q_TOY_PORT_TOPOLOGY_SOLVE

SimulationOps version: 0.2.4

BUILD_AUTHORIZED: toy models only
SOLVE_AUTHORIZED: toy models only
PRODUCTION_MODEL_SOLVE_AUTHORIZED: false

## Host/toolchain

Host: NW
CST: 2022.5
Runtime: CST bundled Python 3.6 / cst.interface
Solver: HF Frequency Domain
Mesh order: first
Adaptive mesh: off
Frequency: 0.5–2.0 GHz

## Test objects

Fresh isolated work:
D:\GNSS_Lband_Active_Array\_r1a4q_crossed_port_test

A:
CROSS.cst

B:
LIFTED_REFERENCE.cst

Neither model contains the GNSS radiator.

## Production protection

R1A4 GNSS CST remains:
D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

It must not be opened for solver execution in R1A4Q.

## Stop boundary

Return A/B S-parameter diagnostics and classify the crossed topology.

No R1A5 antenna solve is authorized.
