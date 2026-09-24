# SIM_EXECUTION

## Current stage

R1A5M2_MAXPASS8_ADAPTIVE_RECOVERY

SimulationOps version: 0.2.4

BUILD_AUTHORIZED: copy/config only
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: false

## Immutable source

D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

## Recovery delta

Only:
MaxPasses 6 -> 8

Unchanged:
- second-order tetrahedral
- curvature order 3
- General purpose
- HighFrequencyTet
- ExpertSystem
- MinPasses 3
- MaxDeltaS 0.02
- Delta-S checks 2
- LinearGrowthLimitation 40
- 1.0–1.8 GHz
- boundaries/background/ports/materials/geometry

## Incremental baseline

evidence/r1a5m_dc_nw_20260924_adapt01/sparameters_and_zin.csv

## Native PASS

- last two Delta-S <= 0.02
- no max-pass termination
- broadband sweep convergence
- no solver errors

## External PASS

Science band 1.15–1.65 GHz:
- max complex delta S11 <= 0.03
- max complex delta S22 <= 0.03
- Pol-A/B asymmetry <= 1.0 dB
- reciprocity <= 1e-3

## Paths

Work:
D:\GNSS_Lband_Active_Array\_r1a5m2_maxpass8_work

Evidence:
evidence/r1a5m2_dc_nw_20260924_recovery01/

## Stop

One recovery solve only.
No further automatic extension.
