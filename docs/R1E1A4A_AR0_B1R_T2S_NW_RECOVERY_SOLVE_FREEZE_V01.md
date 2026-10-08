# AR0-B1R-T2S-NW Recovery Solve Freeze V0.1

Status: SOLVE AUTHORIZED
SimulationOps: 0.2.8

## Purpose

Recover the T2S transition EM qualification on NW/Windows CST after the CST251/Linux launch failed before Solver_HF_Tet started because Linux headless CST replayed incompatible legacy project history.

This is not a geometry recovery.
This is not a port recovery.
This is an execution-host recovery only.

## Source identity

Configured T2S fixture:
R1E1A4A_AR0_B1R_T2S_CONFIGURED_V01.cst

SHA256:
ab8a61cc781880ba938b729f44862d1d79f36dbb959288fc57ede5e61b4d2858

This configured artifact already passed on NW:
- source T2F hash check;
- fresh reopen;
- port count = 3;
- solver tree empty;
- configured hash stable.

Geometry, ports and solver configuration are immutable.

## Execution

Host:
NW / Windows CST 2022

Method:
CST Python API
open_project -> one modeler.run_solver() -> save -> close.

Exactly one formal NW solver invocation is authorized.
No automatic retry.

The earlier CST251 formal launch remains recorded separately and is not erased.

## Presolve gate

Before run_solver:
- configured source SHA exact;
- fresh work path absent;
- evidence path absent;
- copied solve artifact SHA exact;
- port count exactly 3;
- S-parameter/adaptive result tree empty.

If any gate fails: HOLD without solver launch.

## Solver formulation

Unchanged from T2S freeze:
- 1.0 to 1.8 GHz;
- HF Frequency Domain;
- tetrahedral second order;
- MinPasses 3;
- MaxPasses 12;
- MaxDeltaS 0.02;
- two consecutive checks;
- open boundaries;
- 30-mm background spacing.

## Qualification

After the one formal run:
- require all 9 Sij terms;
- extract adaptive Delta-S;
- numerical PASS requires final two Delta-S <= 0.02;
- evaluate 1.15-1.65 GHz;
- report GNSS L5/L2/L1 points;
- compute S11, branch amplitude/phase balance, common-mode proxy, power closure and mismatch-normalized loss.

Scientific verdict is separate:
PREFERRED / ACCEPTABLE / NEEDS_OPTIMIZATION / STRONG_CONCERN.

A NEEDS_OPTIMIZATION result is still a successful characterization if the solve is numerically qualified and physically consistent.

## Stop boundary

After one NW solve and read-only extraction:
- close SOLVE authority;
- preserve solved artifact on NW;
- push compact evidence;
- no parameter sweep;
- no automatic rerun.
