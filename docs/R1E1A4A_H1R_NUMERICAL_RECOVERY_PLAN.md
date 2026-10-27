# R1E1A4A-H1R Numerical Recovery Plan

Status: DESIGN ONLY — NO SOLVE AUTHORIZATION

Trigger:
`HOLD_R1E1A4A_H1A_BROADSIDE_NUMERICAL_MAXPASSES`

## Recovery objective

Qualify the already-built H1A 2.0-mm offset-ground geometry without changing any physical variable or any Gate-R threshold.

The H1A solve reached MaxPasses=12 with final Delta-S = 0.0213176, narrowly above the frozen 0.02 criterion. After pass 8 the sequence decreased monotonically through 0.04773, 0.04332, 0.03563, 0.02884, 0.02132. This supports a limited numerical-ceiling recovery rather than a geometry change.

## Frozen recovery

Only permitted solver change:
- `MaxPasses: 12 -> 16`.

Unchanged:
- H1A solved-source geometry and source hash;
- broadside theta=0, phi=45;
- HF Frequency Domain / tetrahedral / second order;
- curvature order 3;
- General purpose method;
- HighFrequencyTet / ExpertSystem adaptation;
- MinPasses=3;
- MaxDeltaS=0.02;
- NumberOfDeltaSChecks=2;
- frequency range 1.0–1.8 GHz;
- all ports, materials and boundaries;
- all mixed-mode formulas;
- Gate R V0.1 including R-NF0 <=0.40 dB.

## Recovery acceptance

Numerical PASS requires:
- desired-accuracy termination rather than MaxPasses;
- final two adaptive Delta-S values <=0.02;
- broadband convergence;
- all four two-port S traces present;
- no solver errors.

Only after numerical PASS may the existing mixed-mode and QPL9547 R-NF0 calculations be treated as authoritative.

Any numerical HOLD stops. No MaxPasses >16 escalation is pre-authorized.

## Scientific consequence

If H1R numerically PASSes and R-NF0 still fails only at the low-band edge, the next step is not another numerical recovery. The H1A geometry is then classified physically and the project decides between:
- H1B manufacturable feed/daughterboard modeling if H1A Gate R passes;
- H1C or another frozen local-ground/feed geometry if Gate R fails.

No C60P45/C60P135 scan is run until broadside H1A is numerically and scientifically qualified.

## Stop boundary

DESIGN ONLY. Await fresh explicit solve authorization.
