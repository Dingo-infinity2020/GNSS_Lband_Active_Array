# R1E0C-A-R1 Recovery Build-Only — HOLD Report

**FORMAL_STATUS = HOLD_R1E0C_A_RECOVERY_NO_SOLVER_PREDICATE**

Recovery source HEAD:
`cde5f8827d82473750c1a6e92510ac617d3835ab`

Recovery invocation count:
1

Exit code:
0

Runtime:
197.31 s

Solver:
NOT RUN

## Four built artifacts

- C30P45: `e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2`
- C45P45: `ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed`
- C60P45: `94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01`
- C60P135: `c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1`

All four hashes are unique.

## Checks that passed for every state

- pre-copy source hash match;
- geometry unchanged at build;
- geometry unchanged after fresh reopen;
- port count = 1;
- X/Y boundaries = unit cell;
- Z boundaries = expanded open;
- 94 x 94 mm cell metadata;
- scan query succeeds;
- scan-valid raw = -1 / True;
- intended theta/phi match;
- outward direction;
- build/reopen status identical;
- scan parameter table values persist correctly.

## Sole harness failure

The original recovery harness classified the mere existence of `Result\output.txt` as evidence that a solver ran.

CST created `output.txt` only as a message log. The files contain parameter-history warnings, not solver execution.

Read-only result-tree inspection found zero:
- S-Parameter result items;
- Adaptive Meshing result items;
- Power/Excitation result items.

No output log contains mesh/adaptive/excitation/broadband solver markers.

Therefore the HOLD is classified as:
`NO_SOLVER_PREDICATE_FILE_EXISTENCE_MISMATCH`

## Parameter-history warning

CST warns that an earlier history step attempted to restore the original scan parameters during history rebuild.

Fresh-reopen Boundary metadata and `Model\Parameters.json` nevertheless agree exactly for all four target scan states.

The warning is preserved and must be reported, but it is not evidence of solver execution.

## Recovery

Do not rebuild the CSTs.

Open a read-only qualification ticket that verifies artifact hashes, geometry/status evidence, persisted parameter values, message-log solver markers, and result-tree absence of solver results.

The future build harness has been corrected to detect actual solver execution markers rather than `output.txt` existence.
