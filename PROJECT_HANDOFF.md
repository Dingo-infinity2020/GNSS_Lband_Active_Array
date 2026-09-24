# PROJECT_HANDOFF.md

## MACHINE-READABLE HEADER

```text
HANDOFF_VERSION=28
CANONICAL_BRANCH=project/r0-charts-scaffold
MAINLINE_AUTHORITY=PROJECT_MAINLINE.md
CURRENT_GATE=R1E0A-PERIODIC-CONFIG-RECOVERY
CURRENT_TASK_ID=R1E0A-R1-READONLY-AUDIT-RECOVERY
TASK_OWNER=DC_NW
TASK_STATUS=READY_FOR_READONLY_QUALIFICATION
SIMULATIONOPS_PROTOCOL=0.2.4
BUILD_AUTHORIZED=NO
SOLVER_PERMISSION=NO
PRODUCTION_SOLVER_PERMISSION=NO
OPTIMIZATION_PERMISSION=NO
MATERIAL_AB_PERMISSION=NO
LNA_INTEGRATION_PERMISSION=NO
CST251_PERMISSION=NO
```

## Long-horizon authority

Read `PROJECT_MAINLINE.md` first.

R1E0 remains the first primary array-physics gate.

## R1E0A formal invocation

Source HEAD:
`814fbffb850d7cc35541ce61213c97c436bd6a2c`

Formal status:
`HOLD_R1E0A_PERIODIC_CONFIG_AUDIT`

Formal invocation count:
1

Exit:
0

Runtime:
48.46 s

Solver:
NOT RUN

Artifact:
`D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst`

SHA256:
`48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223`

## HOLD classification

The only failed check was the harness representation of the unit-cell scan-valid Boolean.

Fresh reopen returned:
- SCAN_QUERY_ERR=0
- SCAN_VALID=-1
- theta=0
- phi=45
- direction=1 / outward

CST/VBA COM Boolean convention uses nonzero, including -1, for True.

All physical/configuration checks passed:
- geometry unchanged
- port count=1
- x/y boundaries=unit cell
- z boundaries=expanded open
- 94x94 mm structure/cell metadata
- no solver output

Classification:
`AUDIT_BOOLEAN_ENCODING_MISMATCH`

## R1E0A-R1 recovery

Recovery is read-only.

Qualifier:
`scripts/qualify_r1e0a_existing_evidence.py`

Allowed actions:
- read the existing build/reopen evidence;
- re-hash the existing CST artifact;
- interpret True/1/-1 as Boolean true;
- produce a separate requalification summary.

Forbidden:
- reopen/modify CST for recovery;
- rerun build;
- start solver;
- change boundary metadata.

Future build harness parser has been corrected, but the formal CST invocation will not be repeated.

## Stop boundary

After read-only qualification:
- if PASS, close R1E0A and open R1E0B broadside periodic smoke DESIGN;
- if HOLD, return to DESIGN.

No solver is currently authorized.
