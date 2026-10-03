# AR0-B1R-R3-D2-M1 Dual-Polarization One-Shot Solve Freeze V0.2

Status: SOLVE AUTHORIZED
SimulationOps: 0.2.8

## Sources

Pol-A fixture SHA256:
33294aa6200264135582ec0c0742a1b4e6ca7b2148e1adece2f64388d81d3dd6

Pol-B fixture SHA256:
11b3576ff5efb4326a761554fb94d8588d22c54691d713f8181c359415bdb70e

Both:
- exactly 10 solids;
- exactly 3 ports;
- fresh-reopen qualified;
- empty result tree before solve.

## Interpretation boundary

The A/B comparison is NOT a pure one-parameter bridge-height experiment.

Each fixture retains its own physically required complementary half-lap lower-stalk slot plus its supported common-ground merge.

Therefore the comparison measures the total RF consequence of the manufacturable A-vs-B lower-stalk mechanical asymmetry:
- complementary slot orientation;
- common-ground merge location;
- associated return-current geometry.

If the total difference is material, a later mechanism probe may isolate merge height from slot topology.
No such probe is authorized here.

## Solver

Same for A and B:
- HF Frequency Domain;
- 1.0..1.8 GHz;
- tetrahedral second order;
- MinPasses 3;
- MaxPasses 12;
- MaxDeltaS 0.02;
- two consecutive convergence checks;
- open boundaries;
- 30-mm background spacing.

Execution host:
NW.

Formal budgets:
- Pol-A: exactly one run_solver()
- Pol-B: exactly one run_solver()
- no retry
- no sweep

A failure in one branch does not consume the other branch's independent launch budget.

## Metrics

Per branch, decision band 1.15..1.65 GHz:
- S11
- S21 / S31
- amplitude imbalance
- phase error from 180 deg
- common-mode ratio
- power closure
- mismatch-normalized excess loss
- equivalent 100-ohm-reference Zin

Numerical qualification:
final two Delta-S <= 0.02.

A/B comparison:
- B-A S11 dB
- B-A Zin real / imag
- B-A amplitude imbalance
- B-A phase error
- B-A CMR
- B-A normalized excess loss
- values at L5/L2/L1
- max absolute difference over decision band.

No impedance optimization is authorized after solve.
