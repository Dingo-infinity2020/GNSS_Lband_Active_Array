# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=17
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A5M-DESIGN-MESH-CONVERGENCE-CONTRACT
TASK_OWNER=DESIGN
TASK_STATUS=READY_FOR_DESIGN
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=NO
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
CST251_PERMISSION=NO
```

## Closed stages

- R1A1: PASS_R1A1_SCALED_APERTURE_BUILD_ONLY
- R1A2: PASS_R1A2_FEED_REFERENCE_BUILD_ONLY
- R1A3: PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
- R1A3 human review: PASS
- R1A4: PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY
- R1A4Q: PASS_R1A4Q_NO_HARD_SHORT_WITH_PARASITIC_COUPLING
- R1A5: HOLD_R1A5_DIAGNOSTIC_INTEGRITY
- R1A5R: PASS_R1A5R_SYMMETRY_CONVERGED

## R1A5 / R1A5R result

R1A5 first-order tetra:
- max Pol-A/B dB asymmetry = 1.504024537 dB
- best S11 = -18.593128 dB @ 1.3976 GHz
- best S22 = -17.137847 dB @ 1.3936 GHz
- formal result = HOLD on the pre-frozen <=1.0 dB symmetry gate

R1A5R second-order tetra:
- max Pol-A/B dB asymmetry = 0.558463159 dB
- best S11 = -19.145166 dB @ 1.7520 GHz
- best S22 = -19.703624 dB @ 1.7520 GHz
- reciprocity PASS
- all result/provenance gates PASS

Conclusion:
the first-order polarization asymmetry was primarily numerical/discretization-related.

## Important absolute-convergence limitation

The first- and second-order absolute S-parameter curves are not sufficiently similar to claim mesh/order convergence.

Observed sampled -10 dB bands:

First-order:
- Pol-A 1.2144–1.6176 GHz
- Pol-B 1.2248–1.5904 GHz

Second-order:
- Pol-A 1.1816 GHz through the 1.8 GHz sweep limit
- Pol-B 1.1776 GHz through the 1.8 GHz sweep limit

Maximum first-vs-second dB differences:
- S11 ~12.25 dB
- S22 ~13.15 dB
- S21 ~16.31 dB

Therefore second-order is the preferred diagnostic baseline for symmetry, but absolute antenna performance is still provisional.

## Current next task

R1A5M is DESIGN only.

Goal:
define a controlled mesh-convergence study around the second-order HF Frequency Domain model without changing physical geometry, ports, materials, boundary family, or frequency band.

The R1A5M contract must define:
- refinement variable(s);
- number of allowed refinement levels/passes;
- convergence metrics for S11/S22 and resonance locations;
- mesh/resource limits on NW;
- when to escalate to CST251 if needed;
- exact PASS/HOLD criteria;
- artifact lifecycle.

No solve is currently authorized.

## Protected/checkpointed artifacts

R1A4 source:
`D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst`

R1A5 first-order result:
`D:\GNSS_Lband_Active_Array\_r1a5_diagnostic_smoke_work\R1A5_DIAGNOSTIC_SMOKE_V01.cst`

R1A5R second-order result:
`D:\GNSS_Lband_Active_Array\_r1a5r_second_order_work\R1A5R_SECOND_ORDER_V01.cst`

Do not purge these before the R1A5M contract decides which are required for convergence comparison.
