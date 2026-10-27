# R1A4 Differential Port BUILD-ONLY Runbook

## Immutable source

Use only:
D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst

Required SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

Never overwrite this source.

## Execution

Host: NW
CST: 2022.5
Interpreter: CST bundled Python 3.6
Mode: BUILD_ONLY

1. Static audit must PASS.
2. Fresh R1A4 work/evidence directories must not exist.
3. Copy immutable R1A3 CST to R1A4 work.
4. Verify copied file hash equals R1A3 source hash before adding ports.
5. Add exactly two ideal differential discrete ports.
6. Save and close.
7. Fresh reopen.
8. Audit Solver.GetNumberOfPorts() = 2.
9. Verify shape inventory is identical to R1A3.
10. Export top/perspective screenshots and hashes.

## Stop

No Solver.Start.
No FDSolver.Start.
No frequency range setup.
No CST251 staging.
No optimization.

PASS only means the port representation survives build/fresh reopen.
