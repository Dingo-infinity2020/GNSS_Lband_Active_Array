# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=14
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1-CHARTS-GNSS-DERIVATIVE
CURRENT_TASK_ID=R1A5-DESIGN-SMOKE-SOLVE-CONTRACT
TASK_OWNER=DESIGN
TASK_STATUS=READY_FOR_DESIGN
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=NO
PRODUCTION_MODEL_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
CST251_PERMISSION=NO
```

## Closed stages

- R1A1: PASS_R1A1_SCALED_APERTURE_BUILD_ONLY
- R1A2: PASS_R1A2_FEED_REFERENCE_BUILD_ONLY
- R1A3: PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
- R1A3 human review: PASS
- R1A4: PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY
- R1A4Q: PASS_R1A4Q_NO_HARD_SHORT_WITH_PARASITIC_COUPLING

## R1A4Q finding

User concern:
crossed diagonal CST discrete edge ports might short at the center.

CST 2022.5 local documentation confirms that discrete edge ports contain perfect-conducting wire sections plus a central lumped/source element.

Isolated A/B toy-model qualification was therefore performed on NW.

CROSS versus non-intersecting LIFTED_REFERENCE:
- at 0.5 GHz: -69.09 vs -86.21 dB S21
- at 1.0 GHz: -62.75 vs -80.53 dB
- at 1.4 GHz: -59.40 vs -78.09 dB
- at 2.0 GHz: -55.43 vs -76.76 dB

Conclusion:
- no direct galvanic short observed;
- crossing adds approximately 17.1–21.3 dB artificial inter-port coupling;
- tested only for HF Frequency Domain / tetrahedral mesh;
- transient/hexahedral behavior remains unqualified.

Evidence:
`evidence/r1a4q_dc_nw_20260924_attempt3/`

## R1A4 port-model status

R1A4 GNSS CST:
`D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst`

SHA256:
`4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364`

Conditional use:
- MAY be used as input to an R1A5 lightweight smoke only after a new explicit authorization;
- solver must be HF Frequency Domain with tetrahedral mesh;
- results are diagnostic only;
- crossed-port isolation floor must not be interpreted as physical antenna isolation.

Not approved for:
- final production feed modeling;
- transient/hexahedral solver;
- high-dynamic-range polarization-isolation claims.

## Current next task

R1A5 is DESIGN only.

Freeze before any solve:
- HF Frequency Domain / tetrahedral solver;
- open boundary policy;
- 1.0–1.8 GHz diagnostic window unless design review changes it;
- mesh policy;
- two-port excitation policy;
- output set;
- explicit interpretation limits caused by crossed-port parasitic coupling;
- PASS/HOLD criteria.

A later production-quality feed model should investigate non-intersecting alternatives such as a physically realized transition, discrete face formulation, or appropriate multipin/circuit-domain differential treatment.

No antenna solver is currently authorized.
