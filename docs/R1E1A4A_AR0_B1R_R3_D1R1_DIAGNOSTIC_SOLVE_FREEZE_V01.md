# AR0-B1R-R3-D1R1 Corrected Diagnostic Solves Freeze V0.1

Status: SOLVE AUTHORIZED
SimulationOps: 0.2.8

## Geometry authority

Canonical corrected dual-pol T1R1:
SHA256 fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e

All four backside grounds have zero positive-volume overlap with their own FR4 prongs.

D1R1-A source:
SHA256 5aa3dd603607a70f7ac190c746e25af550f6cfcb81a9b1bb45846d9c776b6bcd
2-port 100-ohm differential-to-differential control.

D1R1-B source:
SHA256 93d97b06bc2a739f84f88454a7efa76b27731e7bbdb2714214118a3ec0bafb35
3-port 100-ohm differential input + two 50-ohm grounded outputs + downstream diagnostic common-ground bridge.

No geometry or port changes are allowed during solve.

## Solver

Same solver configuration as T2S:
- HF Frequency Domain
- 1.0 to 1.8 GHz
- tetrahedral, second order
- MinPasses 3
- MaxPasses 12
- MaxDeltaS 0.02
- 2 consecutive checks
- open boundaries
- 30 mm background spacing.

Execution host:
NW / Windows CST 2022.

Authorized launches:
- D1R1-A: exactly 1 formal run_solver()
- D1R1-B: exactly 1 formal run_solver()

No retry.
No sweep.

The branches are independent:
a HOLD in one branch does not consume or cancel the other branch's separate one-shot authorization.

## D1R1-A metrics

Over 1.15-1.65 GHz and at L5/L2/L1:
- S11 / S22
- S21 / S12
- reciprocity
- power closure |S11|^2+|S21|^2
- mismatch-normalized transition loss
- equivalent 100-ohm-reference input impedance.

Numerical qualification requires final two Delta-S <=0.02.

## D1R1-B metrics

Same mixed-output metrics as T2S-R2:
- S11
- S21 / S31
- amplitude imbalance
- phase error from 180 deg
- common-mode ratio
- power closure
- mismatch-normalized transition loss
- equivalent 100-ohm-reference input impedance.

Numerical qualification requires final two Delta-S <=0.02.

## Scientific comparison

Compare against prior flawed-geometry R2 only as historical diagnostic evidence.

Questions:
1. Does corrected copper placement remove most of the severe input reactance?
2. Is the corrected transition well-behaved in pure differential mode?
3. Does common-ground closure materially improve or worsen matching?
4. Is branch symmetry preserved?

No optimization is authorized after these solves.
