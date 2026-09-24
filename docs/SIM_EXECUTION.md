# SIM_EXECUTION

## Current state

SimulationOps version: 0.2.4

Current stage:
DESIGN_R1A5M_MESH_CONVERGENCE_CONTRACT

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Last completed solve

R1A5R second-order HF Frequency Domain

Final status:
PASS_R1A5R_SYMMETRY_CONVERGED

Source HEAD:
73391ffa61cb1fb7f3b8cc5cb785b9c1a3d0ecc6

R1A5R CST:
D:\GNSS_Lband_Active_Array\_r1a5r_second_order_work\R1A5R_SECOND_ORDER_V01.cst

SHA256:
f2254cffe07312270d115e95f5526d5841411a865571dfc22c8a3321a98e24e0

## Numerical findings

First-order max Pol-A/B asymmetry:
1.504024537 dB

Second-order max Pol-A/B asymmetry:
0.558463159 dB

Symmetry convergence:
PASS

Absolute S-parameter convergence:
NOT YET PROVEN

Reason:
first- versus second-order S curves differ materially, especially above 1.5 GHz.

## R1A5M boundary

R1A5M is design-only.

No solver invocation is permitted until a mesh-convergence contract is frozen and explicitly authorized.

Material A/B and production science remain blocked on R1A5M.
