# R1A5R Symmetry Convergence Check

Status: FROZEN FOR NW NUMERICAL REFINEMENT

## Trigger

R1A5 first-order tetrahedral smoke completed successfully but returned:
HOLD_R1A5_DIAGNOSTIC_INTEGRITY

Only failed metric:
max |S11_dB - S22_dB| = 1.504024537 dB
against a frozen <=1.0 dB integrity threshold.

The difference peaks near the deep 1.4 GHz resonance.
Best-match frequencies differ by only ~4 MHz.

## Purpose

Determine whether the R1A5 polarization asymmetry is a first-order tetrahedral discretization effect before considering any physical geometry or port change.

## Immutable source

Use the original R1A4 CST, not the configured R1A5 result:

D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

## Unchanged controls

- geometry: unchanged
- ports: unchanged
- port reference: 100 ohm
- frequency: 1.0–1.8 GHz
- boundaries: open all six faces
- background space: 50 mm all directions
- solver family: HF Frequency Domain
- mesh adaptation: OFF
- no far-field monitors
- no optimization
- no material changes

## Single numerical change

Refinement settings are taken from CST 2022.5 installed Compare Solvers macro:

- MeshSettings.SetMeshType "Tet"
- MeshSettings.Set "CurvatureOrder", "3"
- FDSolver.OrderTet "Second"
- FDSolver.SetMethod "Tetrahedral", "General purpose"

## Required outputs

Same S-parameter/impedance outputs as R1A5.

Additionally compare against R1A5 first-order:
- max S11/S22 dB asymmetry
- best-match depth/frequency
- resonance frequency separation
- anchor-frequency differences

## Classification

PASS_R1A5R_SYMMETRY_CONVERGED if:
- all normal provenance/result gates pass;
- max |S11_dB-S22_dB| <= 1.0 dB.

HOLD_R1A5R_IMPROVED_NOT_CONVERGED if:
- asymmetry improves materially but remains >1.0 dB.

HOLD_R1A5R_NOT_NUMERICALLY_CONVERGING if:
- asymmetry does not improve meaningfully or worsens.

No geometry edit is authorized by this task.

## Stop boundary

Return to DESIGN after exactly one second-order solve.
No adaptation follow-up is automatic.
No CST251.
