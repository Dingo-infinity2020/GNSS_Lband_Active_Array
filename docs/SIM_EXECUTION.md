# SIM_EXECUTION

## Current stage

R1A5R_SECOND_ORDER_SYMMETRY_CONVERGENCE

SimulationOps version: 0.2.4

BUILD_AUTHORIZED: copy/config only
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: false

## Attempt history

R1A5 first-order:
- solver completed
- HOLD only on polarization symmetry
- max S11/S22 dB difference = 1.504024537
- reciprocity PASS
- source/geometry/ports PASS

## R1A5R numerical delta

Only change:
- tetra first-order -> second-order
- curvature order 3
- general-purpose tetra method

Unchanged:
- source CST hash
- geometry
- ports
- HF Frequency Domain
- 1.0–1.8 GHz
- open boundaries
- 50 mm background
- adaptation OFF

## Paths

Input:
D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

Work:
D:\GNSS_Lband_Active_Array\_r1a5r_second_order_work

Evidence:
evidence/r1a5r_dc_nw_20260924_second01/

## Stop

Exactly one second-order solve.
No automatic adaptation follow-up.
No geometry edit.
