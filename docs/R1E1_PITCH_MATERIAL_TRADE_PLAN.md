# R1E1 Periodic Pitch / Material Trade Plan

Status: DESIGN BASELINE — NO BUILD OR SOLVER AUTHORIZATION

## Scientific purpose

R1E0C established that the 94-mm periodic baseline is numerically viable through the 0-60 deg core scan under the frozen severe-mismatch gates, but also showed large scan-angle and scan-plane motion of the active source impedance.

R1E1 therefore asks:
- how much of that impedance motion is controlled by lattice pitch;
- which pitch candidates remain robust through the required 0-60 deg scan region;
- whether a lower-loss substrate materially improves efficiency/gain without introducing unacceptable active-impedance behavior;
- which compact pitch/material baseline should be carried into the full R1E2 active-impedance atlas.

R1E1 does not optimize isolated-element S11.

## Pitch candidates

Primary:
- 88 mm
- 90 mm
- 92 mm
- 94 mm

Upper-bound / failure references:
- 96 mm
- 100 mm

94 mm remains a reference, not a winner.

## Analytic grating-lobe context

For a square lattice scanned in a principal lattice plane, a useful first-order no-grating-lobe condition is:

`d/lambda <= 1/(1 + sin(theta_max))`

At 1.65 GHz:
- theta=60 deg gives approximately d <= 97.4 mm;
- theta=75 deg gives approximately d <= 92.4 mm.

Therefore:
- 100 mm is deliberately beyond the approximate 60-deg upper-band geometric limit;
- 96 mm is near the 60-deg required-band edge;
- 88/90/92 mm are naturally interesting if later 65-75 deg extension matters;
- this analytic condition is context, not a substitute for active-impedance/embedded-pattern simulation.

## Existing model fact that controls pitch

The qualified R1E0 periodic model uses:
`Boundary.UnitCellFitToBoundingBox = True`.

The periodic X/Y bounding box is set by:
`UnitCellGround:UNITCELL_GROUND_REFERENCE`.

Its X/Y extent is driven by:
`unit_cell_pitch_nominal -> ground_reference_span`.

The radiator/substrate footprint is smaller than the minimum 88-mm candidate.

Therefore the intended R1E1 pitch operation is:
- change the periodic ground-tile/cell footprint;
- keep radiator, substrate, slots, feed and vertical geometry unchanged.

Do not implement pitch by scaling the radiator.

## R1E1A0 — parameter-list-safe pitch mutation proof

DESIGN / BUILD-ONLY gate.

Purpose:
prove that CST 2022.5 can change the existing `unit_cell_pitch_nominal` parameter and rebuild the dependent ground tile without inserting a parameter-changing history step.

Reason:
R1E0C preserved warnings caused by changing existing scan parameters through model history. R1E1 must instead use the Parameter List plus CST parametric rebuild path.

Required proof:
- start from a clean hash-locked periodic source;
- use a Parameter-List-safe mutation method;
- change only `unit_cell_pitch_nominal`;
- call CST `RebuildForParametricChange` after the Parameter List update;
- verify `ground_reference_span` follows the new pitch;
- verify ground tile X/Y span equals target pitch;
- verify radiator/substrate/feed geometry is unchanged;
- verify periodic `UnitCellDs1/Ds2` equals target pitch;
- fresh reopen and repeat checks;
- no solver.

First validation endpoints:
- 88 mm
- 100 mm.

Endpoint proof is sufficient to validate the mutation mechanism before generating all candidate models.

## R1E1A1 — six-pitch FR4 build-only source set — CLOSED PASS

Canonical status:
`PASS_R1E1A1_SIX_PITCH_FR4_SOURCE_SET_BUILD_ONLY`

The six support-free sources remain immutable bare-array references.

Generated FR4 periodic sources:
88, 90, 92, 94, 96, 100 mm.

Each source retains:
- same radiator geometry;
- same FR4 1.00-mm baseline;
- same copper/PEC representation;
- same clean Pol-A differential feed;
- same vertical height;
- same periodic/open boundary types;
- only the periodic ground-tile/cell pitch changes.

All six passed unique-hash and fresh-reopen qualification.

## R1E1A2 — mechanical support / standoff EM baseline

DESIGN gate before production pitch screening.

Purpose:
- define how the 70.714-mm radiator PCB is held approximately 57.143 mm above the ground/backplane;
- prevent a later support/frame addition from invalidating pitch comparisons;
- prefer symmetric minimal-volume structures and actual material data.

Candidate order:
- low-density RF foam support first;
- small-section dielectric posts second;
- FR4 ribs as a manufacturability reference;
- aluminium/metal posts only as an explicitly modelled high-risk reference.

No material is assumed electromagnetically transparent.
See `docs/R1E1A2_MECHANICAL_SUPPORT_EM_PLAN.md`.

## R1E1A3 — P094 support-sensitivity qualification

Only after separate BUILD and SOLVER authorizations.

Minimum comparison:
- support-free P094 reference;
- preferred low-density support candidate;
- only the most useful alternative/worst-case candidate if needed.

Minimum scan set:
- broadside;
- theta=60, phi=45 deg;
- theta=60, phi=135 deg.

Acceptance/transparency thresholds must be frozen before results are viewed.
If support perturbation is benign, freeze the support and derive support-inclusive six-pitch sources. If it is material, support geometry becomes a co-design variable and R1E1B remains blocked.

## R1E1B — FR4 pitch screen

Purpose:
screen pitch before paying for material/far-field expansion.

Minimal scan states per pitch:
- broadside;
- theta=60, phi=45 deg principal-plane core limit;
- theta=60, phi=135 deg orthogonal-plane sentinel.

This is 6 pitches x 3 scan states = 18 one-shot periodic solves.

Use the same converged HF frequency-domain formulation as R1E0C unless a separately frozen numerical reason requires change.

Required first-pass metrics:
- complex active S11;
- Z_active;
- frozen severe-mismatch alerts;
- principal/orthogonal 60-deg plane divergence;
- convergence behavior;
- grating/periodic anomaly indicators available from the solver/result set.

Decision method:
- no scalar S11 ranking;
- eliminate candidates with numerical failure or severe required-band scan anomaly;
- carry a small Pareto subset based on scan robustness and impedance-locus compactness;
- preserve at least one low-pitch and one higher-pitch comparison if scientifically useful.

## R1E1C — pitch shortlist qualification

For the surviving pitch subset, restore intermediate scan information:
- theta=0, 30, 45, 60 deg at phi=45;
- theta=60 deg at phi=135.

Confirm that the reduced R1E1B screen did not hide a mid-angle anomaly.

Freeze a pitch shortlist before material A/B.

## R1E1D — material A/B on pitch shortlist

Materials:
- FR4 cost baseline;
- RO4350B-class low-loss reference.

Material properties must be frozen from an explicit datasheet/reference before solver authorization.

Comparison philosophy:
- hold pitch, radiator, feed, copper geometry, substrate thickness and solver settings fixed;
- change dielectric material properties only;
- do not declare a winner from S11 alone.

Add outputs needed to evaluate material loss:
- radiation efficiency;
- total efficiency;
- realized gain;
- active impedance;
- representative embedded/far-field patterns.

Representative monitor frequencies should include low/mid/high GNSS/L-band anchors and must be frozen before results are seen.

## R1E1E — array baseline freeze

Close R1E1 with:
- selected pitch/material baseline or a documented unresolved Pareto pair;
- evidence for rejected candidates;
- exact source hashes;
- explicit reason for the baseline choice;
- no final LNA input match yet.

## LNA relationship

Preliminary LNA model/circuit research may proceed in parallel now.

Allowed:
- QPL9547 model validation;
- S/noise parameter checks;
- bias/stability work;
- source-impedance/noise sensitivity sweeps.

Still blocked:
- final antenna/LNA matching-network freeze;
- final receiver NF claim based on one scan state.

True antenna/LNA co-design remains after R1E2 provides the authoritative scan-dependent source-impedance cloud.

## Resource routing

R1E1A0/A1 build-only:
NW.

R1E1A2 support design/build-only and the later lightweight P094 support-sensitivity gate:
NW unless the frozen model becomes materially heavier.

R1E1B reduced periodic screen:
NW is acceptable if per-case runtime remains comparable to R1E0C; each case remains separately authorized/recorded.

If monitor expansion or material/far-field cases become materially heavier:
return to DESIGN and decide NW versus CST251 explicitly.

## Current stop boundary

R1E1 is DESIGN ONLY.

R1E1A1 is closed PASS.
R1E1A2 is DESIGN ONLY.
No mechanical-support build is authorized.
No R1E1 solver is authorized.
No material A/B solver is authorized.
No LNA integration is authorized.
