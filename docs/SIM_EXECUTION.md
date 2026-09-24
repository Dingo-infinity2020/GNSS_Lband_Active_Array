# SIM_EXECUTION

## Global protocol

SimulationOps version: 0.2.4

## Current stage

R1A5_DIAGNOSTIC_SMOKE_SOLVE

BUILD_AUTHORIZED: copy/config only
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: false

## Toolchain

Host: NW
Simulator: CST Studio Suite 2022.5
Runtime: CST bundled Python 3.6 / cst.interface
Solver: HF Frequency Domain
Mesh: tetrahedral first order
Adaptation: false

## Immutable source

D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

## Solver freeze

Frequency:
1.0–1.8 GHz

Boundary:
open on all six faces

Background:
50 mm all six directions

Ports:
unchanged R1A4 two-port differential representation

Far-field monitors:
none

Optimization:
none

## Artifact paths

Work:
D:\GNSS_Lband_Active_Array\_r1a5_diagnostic_smoke_work

Evidence:
evidence/r1a5_dc_nw_20260924_smoke01/

## Interpretation caveat

R1A4Q crossed-port parasitic coupling is about -69 to -55 dB over 0.5–2.0 GHz.

Any smoke S21 near/below roughly -50 dB is port-model-limited and must not be claimed as physical polarization isolation.

## Stop boundary

One formal smoke invocation only.
No silent retry.
No production solve.
No automatic optimization.
