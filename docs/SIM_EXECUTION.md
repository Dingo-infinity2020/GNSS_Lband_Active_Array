# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1A5FQ_CLEAN_FEED_EQUIVALENCE_SOLVE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true
PRODUCTION_SOLVE_AUTHORIZED: false

## Inputs

A:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst

SHA256:
74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce

B:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLB_SINGLE_PORT_V01.cst

SHA256:
11ca4ae06baa1d3f18376789c90717f28aee2b02480d7eba88d2f5155d51a1bf

Baseline:
evidence/r1a5m2_dc_nw_20260924_recovery01/sparameters_and_zin.csv

## Solver

HF Frequency Domain
tetrahedral second order
curvature order 3
General purpose
HighFrequencyTet / ExpertSystem adaptive
MinPasses 3
MaxPasses 8
MaxDeltaS 0.02
Delta-S checks 2
1.0–1.8 GHz
open boundaries + 50 mm background

## Paths

Work:
D:\GNSS_Lband_Active_Array\_r1a5fq_equivalence_work

Evidence:
evidence/r1a5fq_dc_nw_20260924_equiv01/

## Stop

One formal A+B sequential equivalence invocation only.
No geometry/material/port changes.
No optimization.
No periodic solver in this stage.
