# R1E0B Broadside Periodic Active-Impedance Smoke Contract

Status: DESIGN FROZEN — SOLVER NOT AUTHORIZED

## Mainline role

R1E0B is the first actual solve of the infinite periodic array environment.

It follows:
- R1A5F clean non-crossing feed PASS;
- R1A5FQ isolated equivalence PASS;
- R1E0A 94-mm periodic metadata qualification PASS by read-only recovery.

The objective is not isolated return-loss optimization.

The objective is to prove that the discrete-port-driven 94-mm periodic unit cell solves stably and yields a finite broadside active impedance.

## Immutable source

Qualified R1E0A periodic-config CST:

D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

Required SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

This source already contains:
- one Pol-A differential discrete port;
- X/Y unit-cell boundaries;
- Z expanded-open boundaries;
- 94x94 mm fitted unit cell;
- theta=0 deg;
- phi=45 deg;
- outward scan direction.

## Important configuration rule

The R1E0B solver configuration MUST NOT set Boundary values.

Reason:
the isolated-element R1A5M2 solver macro uses open boundaries on all six sides and would destroy the periodic unit-cell configuration if reused directly.

R1E0B therefore reuses only the converged numerical formulation:
- HF Frequency Domain
- tetrahedral second order
- curvature order 3
- General purpose method
- HighFrequencyTet adaptive mesh
- ExpertSystem
- MinPasses 3
- MaxPasses 8
- MaxDeltaS 0.02
- NumberOfDeltaSChecks 2
- LinearGrowthLimitation 40
- 1.0–1.8 GHz

No boundary, geometry, material, or port command is allowed in the solver config.

## Excitation interpretation

The retained 100-ohm differential discrete port represents one identically driven feed per periodic cell.

At broadside, theta=0.

The periodic one-port S11 is interpreted as the broadside active reflection coefficient of the infinite phased array.

Using Z0=100 ohm:

Z_active = Z0 * (1 + S11) / (1 - S11)

Broadside Z_active is NOT required to equal isolated Zin.

Mutual coupling is physical and a difference from the isolated clean-feed curve is expected.

## Required pre-solver audit

Before solver start:
- source hash matches;
- geometry inventory equals R1A5F Pol-A;
- port count = 1;
- X/Y boundaries = unit cell;
- Z boundaries = expanded open;
- x/y cell span = 94 mm;
- theta=0 deg;
- phi=45 deg;
- direction=outward;
- scan-valid flag is nonzero/true;
- no pre-existing solver output in the fresh copy before the formal solve.

## Required outputs

- complex S11 over 1.0–1.8 GHz;
- derived complex Z_active using 100-ohm reference;
- anchor-frequency samples;
- native adaptation Delta-S sequence;
- native termination reason;
- broadband sweep convergence evidence;
- solver warning/error extraction;
- contextual comparison with clean isolated Pol-A S11/Zin.

Contextual isolated comparison:
evidence/r1a5fq_dc_nw_20260924_equiv01/A/s11_and_zin.csv

The isolated comparison is diagnostic only and has no PASS threshold.

## PASS gate

PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE requires:
- immutable source/provenance gates pass;
- pre-solver periodic metadata gates pass;
- solver completes;
- S11 exists and is non-empty;
- all S11 values are finite;
- all derived Z_active values are finite;
- native adaptive solution has two final consecutive Delta-S values <=0.02;
- CST terminates adaptation by desired accuracy rather than max-pass limit;
- broadband sweep convergence is satisfied;
- no solver error lines are present.

Report but do not fail solely because:
- broadside active impedance differs from isolated impedance;
- return loss is weaker/stronger than isolated;
- a physical broadside array resonance shifts.

## Diagnostic anomaly reporting

Report:
- maximum |S11|;
- minimum/maximum Re(Z_active);
- maximum |Z_active|;
- max complex difference vs isolated clean Pol-A over 1.15–1.65 GHz.

Do not reinterpret these as optimization targets in R1E0B.

## Resource boundary

R1E0B is intended as a lightweight NW smoke solve.

If the periodic problem becomes unexpectedly heavy or unstable:
- classify HOLD;
- do not automatically migrate to CST251;
- return to DESIGN for explicit routing.

## Stop boundary

After one broadside periodic smoke:
- return to DESIGN;
- no theta sweep automatically;
- no pitch/material sweep;
- no LNA;
- no geometry optimization;
- no CST251 staging.

On PASS, the next design stage is R1E0C first scan qualification.
