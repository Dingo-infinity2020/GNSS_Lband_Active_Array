# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=19
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1A5M2-ADAPTIVE-CONVERGENCE-RECOVERY
CURRENT_TASK_ID=R1A5M2-DESIGN-MAXPASS-EXTENSION
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

## R1A5M result

Final status:
`HOLD_R1A5M_ADAPTIVE_NOT_CONVERGED`

Formal source:
`1563c64bc55b9c72e23b61d7be110d334a34cf71`

R1A5M CST:
`D:\GNSS_Lband_Active_Array\_r1a5m_adaptive_work\R1A5M_ADAPTIVE_SECOND_ORDER_V01.cst`

SHA256:
`67b44e77aa88709287caf194c8e89cc2535951e1fab66b7c679df9e398a62c9b`

Solver/runtime:
- exit 0
- runtime 81.54 s
- S-parameter results complete
- geometry/ports/provenance PASS
- Pol-A/B max asymmetry 0.179711978 dB
- reciprocity PASS

## Native adaptation sequence

Configured:
- MinPasses 3
- MaxPasses 6
- MaxDeltaS 0.02
- NumberOfDeltaSChecks 2

Observed:
- pass 2: 0.0673917
- pass 3: 0.0497934
- pass 4: 0.0274924
- pass 5: 0.0203932
- pass 6: 0.0173369

CST termination:
`Mesh adaptation terminated because the maximum number of passes is reached.`

Interpretation:
- monotonic convergence trend;
- pass 6 is below threshold;
- pass 5 is slightly above;
- required two consecutive below-threshold checks were not achieved before MaxPasses=6.

## Recovery direction

R1A5M2 is DESIGN only.

Allowed scientific change:
increase MaxPasses from 6 to 8.

Everything else must remain identical:
- physical model
- materials
- ports
- second-order basis
- curvature order 3
- General purpose tetra method
- ExpertSystem adaptive strategy
- MaxDeltaS 0.02
- NumberOfDeltaSChecks 2
- 1.0–1.8 GHz
- boundary/background

R1A5M2 must use fresh work/evidence and a new explicit solver authorization.

No solver is currently authorized.
