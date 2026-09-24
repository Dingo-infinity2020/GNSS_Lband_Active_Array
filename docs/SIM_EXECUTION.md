# SIM_EXECUTION

## Global protocol

SimulationOps version: 0.2.4

## Current state

Current stage:
DESIGN_R1A5_SMOKE_SOLVE_CONTRACT

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_MODEL_SOLVE_AUTHORIZED: false

Last completed qualification:
R1A4Q crossed-discrete-port solver-safety test

Final R1A4Q status:
PASS_R1A4Q_NO_HARD_SHORT_WITH_PARASITIC_COUPLING

## Hash-locked R1A4 candidate

D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

## R1A4Q constraint

Tested solver:
CST 2022.5 HF Frequency Domain

Mesh:
tetrahedral first order

Crossed-port artificial S21:
approximately -69 to -55 dB over 0.5–2.0 GHz.

At 1.4 GHz:
- crossed = -59.40 dB
- lifted reference = -78.09 dB
- crossing penalty = +18.69 dB

No direct short was observed.

This does not qualify transient/hexahedral use.

## R1A5 design boundary

R1A5 may only be authorized later as:
- HF Frequency Domain;
- tetrahedral mesh;
- diagnostic smoke;
- no optimization;
- no production-isolation claim.

No current solver invocation is permitted.
