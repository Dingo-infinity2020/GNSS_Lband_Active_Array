# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=13
CANONICAL_BRANCH=project/r0-charts-scaffold
CURRENT_GATE=R1A4Q-CROSSED-DISCRETE-PORT-QUALIFICATION
CURRENT_TASK_ID=R1A4Q-ATTEMPT3-LIFTED-REFERENCE-SOLVE-NW
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_FRESH_ATTEMPT3
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=YES_TOY_ONLY
SOLVER_PERMISSION=YES_TOY_ONLY
PRODUCTION_MODEL_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
CST251_PERMISSION=NO
```

## Attempt history

Attempt 1:
- HOLD before solver;
- unsupported Python modeler.evaluate() call;
- solver_run=NO.

Attempt 2:
- CROSS toy solver completed;
- LIFTED_REFERENCE solver not started;
- post-process failed after CROSS because CST S11 rows include reference impedance as a third item;
- existing CROSS results recovered read-only;
- CROSS S21 at 1.4 GHz = -59.402 dB;
- no strong direct short signature observed.

Attempt-2 evidence:
`evidence/r1a4q_dc_nw_20260924_attempt2/`

## Attempt 3

Purpose:
complete the originally frozen A/B test by solving **LIFTED_REFERENCE only**.

No CROSS rerun is authorized.

Correction:
- result parser now reads row[0] as frequency and row[1] as complex S value;
- self-term reference-impedance field is ignored for magnitude extraction;
- new `--only lifted` mode guarantees the CROSS model is not rebuilt/re-solved.

Fresh work:
`D:\GNSS_Lband_Active_Array\_r1a4q_lifted_reference_attempt3`

Fresh evidence:
`evidence/r1a4q_dc_nw_20260924_attempt3/`

Frozen solver:
- HF Frequency Domain;
- 0.5–2.0 GHz;
- tetrahedral first order;
- adaptation off;
- NW only.

Hard stop:
- LIFTED_REFERENCE toy only;
- no GNSS model solver;
- no R1A5 antenna solve;
- no CST251;
- no optimization.
