# R1E0C-A Formal Scan-State Build-Only — HOLD Report

**FORMAL_STATUS = HOLD_R1E0C_A_HARNESS_MACRO_PATH_FORMAT**

Source HEAD:
`746b34d35e6ae4ee948a6fc510bc6c072584e654`

Formal invocation count:
1

Exit code:
1

Runtime:
24.23 s

Solver:
NOT RUN

## Failure point

The harness constructed the macro filename as a literal string:

`R1E0C_%s_SCANSTATE_BUILD_ONLY_V01.mcr`

instead of formatting the current state into the filename.

The resulting exception was:

`FileNotFoundError: ... R1E0C_%s_SCANSTATE_BUILD_ONLY_V01.mcr`

## State before failure

- work/evidence directories were fresh at invocation start;
- only the C30P45 source copy had been created/opened;
- no scan metadata macro was applied;
- the C30P45 CST SHA256 remained identical to the qualified R1E0A source;
- no solver was started;
- no modeler process remained after exit.

Partial C30P45 SHA256:
`48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223`

Therefore this is classified as a pre-build harness HOLD, not a CST, geometry, boundary, or physics failure.

## Recovery design

The harness path expression is corrected to format `% state`.

A new preflight also verifies that all four generated macro files exist before creating any recovery work/evidence directory.

Recovery must use fresh paths and a separately frozen recovery ticket.

The original failed work/evidence are not reused.

No solver is authorized.
