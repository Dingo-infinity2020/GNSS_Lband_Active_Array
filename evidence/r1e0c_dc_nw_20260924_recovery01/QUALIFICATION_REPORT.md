# R1E0C-A Read-Only Scan-State Qualification

**STATUS = PASS_R1E0C_SCANSTATE_BUILD_ONLY_READONLY_QUALIFICATION**

Canonical stage conclusion:
`PASS_R1E0C_SCANSTATE_BUILD_ONLY`

Qualification source HEAD:
`b286a717b798c91caf26eda156347f70f50a604b`

CST rebuild:
NO

Solver run:
NO

## Qualified artifacts

- C30P45: `e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2`
- C45P45: `ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed`
- C60P45: `94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01`
- C60P135: `c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1`

All four hashes are unique.

## Verified per state

- artifact SHA256 matches frozen value;
- build geometry equals qualified R1E0A geometry;
- fresh-reopen geometry equals qualified R1E0A geometry;
- port count = 1;
- X/Y = unit cell;
- Z = expanded open;
- 94 x 94 mm cell;
- scan query valid;
- intended theta/phi persisted;
- outward direction;
- build and reopen metadata identical;
- `Model\Parameters.json` theta/phi values match intended state;
- no solver execution markers in message log;
- zero S-Parameter / Adaptive-Meshing / Power-Excitation result-tree items.

## Historical HOLDs retained

1. `HOLD_R1E0C_A_HARNESS_MACRO_PATH_FORMAT`
   - pre-build harness path-format bug;
   - no scan metadata applied;
   - no solver run.

2. `HOLD_R1E0C_A_RECOVERY_NO_SOLVER_PREDICATE`
   - four CSTs were actually built correctly;
   - harness incorrectly interpreted `Result\output.txt` existence as solver execution.

Neither HOLD is a physics or geometry failure.

## Parameter-history warning

CST message logs contain warnings that earlier history steps attempted to restore broadside scan parameters during history rebuild.

The warning is preserved. It is accepted for this gate because:
- persisted project parameter values match the target scan states;
- Boundary scan metadata matches the target scan states after fresh reopen;
- build/reopen evidence is identical;
- no solver results exist.

Future parameterized builders should avoid changing existing project parameters from inside a history rebuild step.

## Conclusion

R1E0C-A successfully produced four immutable periodic scan-state CST inputs for separate future scan solves.

Next stage:
R1E0C-B scan solve DESIGN ONLY.
