# AR0-B1R-R3-D1R1 Polarization-Aware Ground Placement Recovery Freeze V0.2

Status: BUILD AUTHORIZED; CONDITIONAL SOLVE AUTHORIZED
SimulationOps: 0.2.8

## Proven geometry facts

Original T1 boolean audits:
- Pol-A P/N backside grounds: full-volume overlap with own FR4 prongs.
- Pol-B P/N backside grounds: zero volumetric overlap with own FR4 prongs.

Therefore the original error is polarization-dependent and comes from local-coordinate handedness.

Frozen extrusion signs:
- Pol-A corrected ground height = -0.035 mm.
- Pol-B ground height = +0.035 mm.

Both polarizations must independently prove:
- ground volume = 1.134 mm^3 per branch;
- own-prong volumetric intersection = 0.

The failed D1 attempt that used -0.035 mm for both polarizations is preserved as HOLD evidence and is not reused.

## Products

D1R1 build produces fresh artifacts:
1. dual-pol T1R1 corrected canonical artifact;
2. D1R1-A 2-port differential control;
3. D1R1-B 3-port downstream common-ground control.

D1R1-A/B use corrected Pol-A grounds and otherwise the exact same D0 diagnostic definitions.

## Conditional solves

The user's existing authorization covers this explicit recovery.
If and only if the full D1R1 build PASSes:
- solve D1R1-A once on NW;
- solve D1R1-B once on NW;
- same frozen 1.0-1.8 GHz HF Frequency Domain adaptive configuration;
- no retry;
- no parameter sweep.

Any branch HOLD stops that branch.
