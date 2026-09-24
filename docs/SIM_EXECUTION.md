# SIM_EXECUTION

## Current stage

R1A5M_ADAPTIVE_ABSOLUTE_MESH_CONVERGENCE

SimulationOps version: 0.2.4

BUILD_AUTHORIZED: copy/config only
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: false

## Host/toolchain

Host: NW
CST: 2022.5
Runtime: CST bundled Python 3.6 / cst.interface
Solver: HF Frequency Domain

## Immutable source

D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

## Fixed numerical formulation

- tetrahedral second order
- curvature order 3
- General purpose
- 1.0–1.8 GHz
- open boundaries
- 50 mm background

## Adaptive mesh

- HighFrequencyTet
- ExpertSystem
- MinPasses 3
- MaxPasses 6
- MaxDeltaS 0.02
- Delta-S checks 2
- LinearGrowthLimitation 40
- MeshAdaptionTet true

## Baseline

R1A5R second-order non-adaptive:
evidence/r1a5r_dc_nw_20260924_second01/sparameters_and_zin.csv

## Convergence gate

Science band:
1.15–1.65 GHz

Require:
- max complex delta S11 vs R1A5R <= 0.05
- max complex delta S22 vs R1A5R <= 0.05
- final Pol-A/B dB asymmetry <= 1.0 dB
- reciprocity error <= 1e-3
- complete finite S curves

## Paths

Work:
D:\GNSS_Lband_Active_Array\_r1a5m_adaptive_work

Evidence:
evidence/r1a5m_dc_nw_20260924_adapt01/

## Stop

One formal adaptive solve only.
No material A/B.
No optimization.
No CST251.
