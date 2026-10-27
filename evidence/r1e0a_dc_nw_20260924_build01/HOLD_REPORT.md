# R1E0A Formal Build-Only Attempt — HOLD Report

**FORMAL_STATUS = HOLD_R1E0A_PERIODIC_CONFIG_AUDIT**

Source HEAD:
814fbffb850d7cc35541ce61213c97c436bd6a2c

Formal invocation:
1

Exit code:
0

Runtime:
48.46 s

Solver:
NOT RUN

Artifact:
D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

## Checks that passed

- source hash match
- byte-identical pre-config copy
- geometry unchanged at build
- geometry unchanged after fresh reopen
- retained discrete port count = 1
- Xmin/Xmax = unit cell
- Ymin/Ymax = unit cell
- Zmin/Zmax = expanded open
- structure query succeeded
- structure x span = 94 mm
- structure y span = 94 mm
- scan query returned without API error
- theta = 0 deg
- phi = 45 deg
- direction = outward
- unit-cell angle = 90 deg
- no solver output exists

## Sole failed harness check

The original harness expected:
SCAN_VALID == "true"

CST 2022.5 fresh-reopen output returned:
SCAN_VALID=-1

The build and reopen status are identical:
- SCAN_QUERY_ERR=0
- SCAN_VALID=-1
- SCAN_THETA_DEG=0
- SCAN_PHI_DEG=45
- SCAN_DIRECTION=1

In VBA/COM Boolean convention, -1 represents True.

Therefore the observed HOLD is classified as:
**AUDIT_BOOLEAN_ENCODING_MISMATCH**

It is not a geometry, boundary, port, build, or solver failure.

## Recovery

Do not rerun CST.

Open a separate read-only qualification ticket that:
- preserves this original HOLD evidence;
- fixes future harness Boolean parsing to accept True/1/-1;
- re-evaluates the already generated build/reopen evidence;
- verifies the existing CST artifact hash;
- does not modify the CST artifact;
- does not start a solver.
