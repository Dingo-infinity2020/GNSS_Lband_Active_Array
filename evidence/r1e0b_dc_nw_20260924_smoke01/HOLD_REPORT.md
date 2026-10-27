# R1E0B Formal Broadside Periodic Smoke — HOLD Report

**FORMAL_STATUS = HOLD_R1E0B_RESULT_PATH_QUALIFICATION**

Source HEAD:
10b50b0102cd50a4f21ed2d5ee07da80e9c01a63

Formal invocation count:
1

Exit code:
1

Runtime:
99.99 s

## Solver state

The CST solver itself completed.

Native periodic adaptation:
- pass 2: 0.0453805
- pass 3: 0.0552784
- pass 4: 0.0530417
- pass 5: 0.0204615
- pass 6: 0.0179226
- pass 7: 0.0185901

Pass 6 and 7 are both below 0.02.

CST termination:
`Mesh adaptation terminated because the desired accuracy limit is reached.`

Broadband sweep:
`All broadband sweep convergence criteria have been satisfied after calculating 7 frequency samples.`

The solver recognized the periodic scan state:
`Theta: 0, Phi: 45`

## Pre-solver periodic integrity

PASS:
- geometry unchanged
- port count = 1
- X/Y = unit cell
- Z = expanded open
- UnitCellDs1 = 94 mm
- UnitCellDs2 = 94 mm
- theta = 0 deg
- phi = 45 deg
- direction = outward
- scan valid raw = -1 / True

## Formal failure point

The post-solve harness expected isolated-model result path:

`1D Results\S-Parameters\S1,1`

The periodic solved result tree instead contains:

`1D Results\S-Parameters\S1(1),1(1)`

Therefore the harness raised:

`RuntimeError: missing S1,1`

This is a qualification-path mismatch, not a solver or physics failure.

## Solved artifact

D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work\R1E0B_POLA_PERIODIC_BROADSIDE_SMOKE_V01.cst

SHA256:
339021e580efa6aae6dfcfa229e4194b4dcf0bbef854398d44a0efed65aac7ad

Bytes:
43620

## Additional CST warning

Postprocessing reports:

`No calculation of YZ Matrices possible! Not all S-parameters were calculated.`

The periodic result tree nevertheless contains the driven-port self-reflection:
`S1(1),1(1)`

The warning is retained for scientific interpretation and is not silently discarded.

## Recovery

Do not rerun the solver.

Open a separate read-only result recovery that:
- reads the already solved CST;
- uses the actual periodic S11 path;
- extracts S11 and Z_active;
- re-parses native convergence;
- preserves the warning;
- verifies the existing solved artifact hash;
- does not modify the CST;
- does not start a solver.
